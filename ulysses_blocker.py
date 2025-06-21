import os
import sys
import socket
import subprocess

# --- Configuration ---
# The group name for all firewall rules created by this script.
FIREWALL_GROUP = "UlyssesBlock"

# List of domains to block.
# The script will also try to block the 'www.' subdomain (e.g., 'www.facebook.com').
DOMAINS_TO_BLOCK = [
    "tumblr.com",
    "facebook.com",
    "youtube.com",
    "twitter.com",
    "instagram.com",
    "tiktok.com",
    "netflix.com",
    "twitch.tv",
    "reddit.com",
    "pinterest.com",
    "snapchat.com",
    "x.com"
]
# --- End of Configuration ---

def is_admin():
    """Checks if the script is running with administrative privileges on Windows."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except (ImportError, AttributeError):
        print("Non-Windows system detected. This script is for Windows only.")
        return False

def clear_existing_rules_powershell():
    """Removes ONLY firewall rules previously created by this script using PowerShell."""
    print(f"Checking for existing UlyssesBlock rules to remove...")
    
    # First, check if any rules exist in our specific group
    check_command = f"Get-NetFirewallRule -Group '{FIREWALL_GROUP}' -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count"
    command = ["powershell", "-NoProfile", "-Command", check_command]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode == 0 and result.stdout.strip():
            rule_count = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
            if rule_count > 0:
                print(f"Found {rule_count} existing UlyssesBlock rules. Removing them...")
                # Only remove rules that are specifically in our group
                remove_command = f"Get-NetFirewallRule -Group '{FIREWALL_GROUP}' -ErrorAction SilentlyContinue | Remove-NetFirewallRule -ErrorAction SilentlyContinue"
                subprocess.run(["powershell", "-NoProfile", "-Command", remove_command], 
                             capture_output=True, text=False, check=False)
                print("Cleanup of old UlyssesBlock rules complete.")
            else:
                print("No existing UlyssesBlock rules found.")
        else:
            print("No existing UlyssesBlock rules found.")
    except FileNotFoundError:
        print("Error: 'powershell' command not found. This script requires Windows with PowerShell.")
        sys.exit(1)
    except Exception as e:
        print(f"Warning: Could not check existing rules: {e}")
        print("Continuing with rule creation...")

def resolve_domains(domains):
    """Resolves domains to a unique set of IP addresses (IPv4 and IPv6) for blocking."""
    unique_ips = set()
    print(f"\nResolving {len(domains)} domains to IP addresses...")
    
    for domain in domains:
        # Check both the main domain and www subdomain
        subdomains_to_check = [domain, f"www.{domain}"]
        
        for d in subdomains_to_check:
            try:
                # Resolve both IPv4 and IPv6 addresses
                addr_info = socket.getaddrinfo(d, None)
                for family, socktype, proto, canonname, sockaddr in addr_info:
                    ip = sockaddr[0]
                    
                    # Skip localhost and invalid addresses
                    if ip not in ['127.0.0.1', '::1', '0.0.0.0', '::'] and ip not in unique_ips:
                        print(f"  {d} -> {ip}")
                        unique_ips.add(ip)
                        
            except socket.gaierror as e:
                # Only show warning for the main domain, not www subdomain
                if d == domain:
                    print(f"  ⚠️  Warning: Could not resolve '{d}': {e}")
            except Exception as e:
                if d == domain:
                    print(f"  ❌ Error resolving '{d}': {e}")
    
    # Remove any localhost addresses that might have been included
    unique_ips.discard('127.0.0.1')
    unique_ips.discard('::1')
    unique_ips.discard('0.0.0.0')
    unique_ips.discard('::')
    
    valid_ips = list(unique_ips)
    
    if not valid_ips:
        print("\n⚠️  Warning: Could not resolve any valid IP addresses to block.")
        print("   This might be due to DNS issues or the domains not existing.")
    else:
        print(f"\n📋 Found {len(valid_ips)} unique IP addresses to block.")
    
    return valid_ips

def create_firewall_rules_powershell(ips_to_block):
    """Creates outbound firewall rules to block ONLY the given IP addresses using PowerShell."""
    if not ips_to_block:
        print("No IP addresses to block.")
        return
    
    print(f"\nCreating {len(ips_to_block)} new firewall rules for UlyssesBlock group...")
    successful_rules = 0
    failed_rules = 0
    
    for i, ip in enumerate(ips_to_block, 1):
        # Validate IP address format
        if not ip or ip in ['', '0.0.0.0', '::']:
            print(f"  [{i}/{len(ips_to_block)}] Skipping invalid IP: {ip}")
            failed_rules += 1
            continue
            
        rule_name = f"{FIREWALL_GROUP} - Block {ip}"
        
        # Create rule with very specific parameters to avoid affecting other traffic
        ps_command = (
            f"New-NetFirewallRule "
            f"-DisplayName '{rule_name}' "
            f"-Group '{FIREWALL_GROUP}' "
            f"-Direction Outbound "
            f"-Action Block "
            f"-RemoteAddress '{ip}' "
            f"-Protocol Any "
            f"-Enabled True "
            f"-ErrorAction SilentlyContinue"
        )
        command = ["powershell", "-NoProfile", "-Command", ps_command]
        
        try:
            result = subprocess.run(command, check=False, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  [{i}/{len(ips_to_block)}] ✅ Successfully blocked {ip}")
                successful_rules += 1
            else:
                print(f"  [{i}/{len(ips_to_block)}] ⚠️  Could not create rule for {ip} (may already exist)")
                failed_rules += 1
        except Exception as e:
            print(f"  [{i}/{len(ips_to_block)}] ❌ Error creating rule for {ip}: {e}")
            failed_rules += 1
    
    print(f"\nRule creation summary:")
    print(f"  ✅ Successful: {successful_rules}")
    print(f"  ❌ Failed: {failed_rules}")
    print(f"  📊 Total: {len(ips_to_block)}")

def main():
    """Main function to run the blocking process safely."""
    print("🛡️  UlyssesBlock - Domain Blocking Tool")
    print("=" * 50)
    
    # Safety checks
    if os.name != 'nt':
        print("❌ Error: This script is designed for Windows only.")
        sys.exit(1)
    
    if not is_admin():
        print("❌ Error: This script must be run with administrative privileges.")
        print("   Please right-click your terminal and select 'Run as administrator'.")
        sys.exit(1)
    
    print(f"🎯 Target domains to block: {len(DOMAINS_TO_BLOCK)}")
    for i, domain in enumerate(DOMAINS_TO_BLOCK, 1):
        print(f"   {i}. {domain}")
    
    print(f"\n🔧 Firewall group: {FIREWALL_GROUP}")
    print("⚠️  This script will ONLY modify rules in the UlyssesBlock group.")
    print("   It will NOT affect any other firewall rules on your system.")
    
    # Step 1: Safely remove only our previous rules
    clear_existing_rules_powershell()
    
    # Step 2: Resolve domains to current IP addresses
    ips_to_block = resolve_domains(DOMAINS_TO_BLOCK)
    
    if not ips_to_block:
        print("\n❌ No IP addresses could be resolved. Exiting without making changes.")
        sys.exit(1)
    
    # Step 3: Create new blocking rules
    create_firewall_rules_powershell(ips_to_block)
    
    print("\n" + "=" * 70)
    print("✅ Process complete! UlyssesBlock firewall rules have been updated.")
    print("🔒 The specified domains should now be blocked system-wide.")
    print("💡 Tip: Use 'python check_ulysses_rules.py' to verify the blocking.")
    print("=" * 70)


if __name__ == "__main__":
    main()
