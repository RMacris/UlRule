import subprocess
import sys
import os

def is_admin():
    """Checks if the script is running with administrative privileges on Windows."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except (ImportError, AttributeError):
        return False

def check_ulysses_rules():
    """Lists all firewall rules in the UlyssesBlock group."""
    print("Checking UlyssesBlock firewall rules...")
    print("=" * 60)
    
    # Count total rules
    count_command = ["powershell", "-NoProfile", "-Command", 
                    "Get-NetFirewallRule -Group 'UlyssesBlock' -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count"]
    
    try:
        result = subprocess.run(count_command, capture_output=True, text=True, check=False)
        if result.returncode == 0 and result.stdout.strip():
            rule_count = result.stdout.strip()
            print(f"Total UlyssesBlock rules found: {rule_count}")
        else:
            print("No UlyssesBlock rules found or error occurred.")
            return
    except Exception as e:
        print(f"Error checking rule count: {e}")
        return
    
    print("\nDetailed rule information:")
    print("-" * 60)
    
    # Get detailed rule information
    detail_command = ["powershell", "-NoProfile", "-Command", 
                     "Get-NetFirewallRule -Group 'UlyssesBlock' -ErrorAction SilentlyContinue | Select-Object DisplayName, Enabled, Direction, Action | Format-Table -AutoSize"]
    
    try:
        result = subprocess.run(detail_command, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Error retrieving detailed rule information.")
    except Exception as e:
        print(f"Error retrieving rule details: {e}")
    
    # Check specific IPs being blocked
    print("\nBlocked IP addresses:")
    print("-" * 60)
    
    ip_command = ["powershell", "-NoProfile", "-Command", 
                 "Get-NetFirewallRule -Group 'UlyssesBlock' -ErrorAction SilentlyContinue | Get-NetFirewallAddressFilter | Select-Object -ExpandProperty RemoteAddress | Sort-Object -Unique"]
    
    try:
        result = subprocess.run(ip_command, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            ips = result.stdout.strip().split('\n')
            for i, ip in enumerate(ips, 1):
                if ip.strip():
                    print(f"{i:2}. {ip.strip()}")
        else:
            print("Error retrieving blocked IP addresses.")
    except Exception as e:
        print(f"Error retrieving blocked IPs: {e}")

def test_connectivity():
    """Test connectivity to some blocked domains to verify blocking is working."""
    print("\nTesting connectivity to blocked domains:")
    print("-" * 60)
    
    test_domains = ["youtube.com", "facebook.com", "twitter.com"]
    
    for domain in test_domains:
        print(f"\nTesting {domain}:")
        ping_command = ["ping", domain, "-n", "1", "-w", "2000"]
        
        try:
            result = subprocess.run(ping_command, capture_output=True, text=True, check=False, timeout=5)
            if "tempo limite" in result.stdout.lower() or "request timed out" in result.stdout.lower():
                print(f"  ✅ {domain} - BLOCKED (timeout)")
            elif "destination host unreachable" in result.stdout.lower():
                print(f"  ✅ {domain} - BLOCKED (unreachable)")
            elif "resposta de" in result.stdout.lower():
                print(f"  ⚠️  {domain} - NOT BLOCKED (ping successful)")
            else:
                print(f"  ❓ {domain} - UNCLEAR (unexpected response)")
        except subprocess.TimeoutExpired:
            print(f"  ✅ {domain} - BLOCKED (timeout)")
        except Exception as e:
            print(f"  ❌ {domain} - ERROR: {e}")

def main():
    """Main function."""
    print("UlyssesBlock Firewall Rules Checker")
    print("=" * 40)
    
    if os.name != 'nt':
        print("This script is for Windows only.")
        sys.exit(1)
    
    if not is_admin():
        print("⚠️  Warning: Not running as administrator.")
        print("Some information may not be available.")
        print()
    
    check_ulysses_rules()
    test_connectivity()
    
    print("\n" + "=" * 60)
    print("Check complete!")

if __name__ == "__main__":
    main()
