# UlyssesBlock - Sistema de Bloqueio de Domínios

Uma ferramenta Python **open source** para bloquear domínios específicos a nível de sistema no Windows, inspirada na famosa "Regra de Ulisses" - uma estratégia de autocontrole que impede decisões impulsivas removendo a capacidade de escolha.

**Uma alternativa gratuita e de código aberto para aplicativos como Freedom, Cold Turkey, FocusMe e similares.**

## 🎯 O que faz

O UlyssesBlock bloqueia completamente o acesso a websites específicos em todo o sistema Windows, criando regras no Firewall do Windows que impedem qualquer aplicação (navegadores, apps, etc.) de se conectar aos domínios especificados.

### 🆚 Por que usar em vez de apps pagos?

- **🆓 Completamente gratuito** - Sem assinaturas ou limitações
- **🔓 Código aberto** - Você pode ver exatamente o que o código faz
- **🔧 Personalizável** - Modifique conforme suas necessidades
- **🛡️ Privacidade** - Nenhum dado é enviado para servidores externos
- **⚡ Leve** - Não consome recursos do sistema rodando em background

## 🛡️ Como funciona

1. **Resolução de DNS**: O script resolve os domínios especificados para seus endereços IP atuais
2. **Criação de Regras**: Cria regras específicas no Firewall do Windows para bloquear tráfego de saída para esses IPs
3. **Isolamento Seguro**: Todas as regras são criadas em um grupo isolado chamado "UlyssesBlock", sem afetar outras configurações do firewall

## 📋 Pré-requisitos

- **Windows** (qualquer versão moderna)
- **Python 3.6+**
- **Privilégios de Administrador** (necessário para modificar o firewall)
- **PowerShell** (incluído no Windows por padrão)

## 🚀 Como usar

### 1. Configurar os domínios a bloquear

Edite o arquivo `ulysses_blocker.py` e modifique a lista `DOMAINS_TO_BLOCK`:

```python
DOMAINS_TO_BLOCK = [
    "facebook.com",
    "youtube.com", 
    "twitter.com",
    "instagram.com",
    # Adicione seus domínios aqui
]
```

### 2. Executar o bloqueio

1. **Abra o Prompt de Comando como Administrador**:
   - Clique no menu Iniciar
   - Digite "cmd" ou "PowerShell"
   - Clique com o botão direito e selecione **"Executar como administrador"**

2. **Navegue até a pasta do projeto**:
   ```cmd
   cd "C:\caminho\para\UlRule"
   ```

3. **Execute o script**:
   ```cmd
   python ulysses_blocker.py
   ```

### 3. Verificar se funcionou

Execute o script de verificação:
```cmd
python check_ulysses_rules.py
```

Este script mostrará:
- Quantas regras foram criadas
- Quais IPs estão sendo bloqueados
- Teste de conectividade para verificar o bloqueio

## 📁 Arquivos do projeto

- **`ulysses_blocker.py`** - Script principal que cria o bloqueio
- **`check_ulysses_rules.py`** - Script para verificar se o bloqueio está funcionando
- **`README.md`** - Este arquivo de documentação

## ⚠️ Características importantes

### ✅ Segurança
- **Isolado**: Só modifica regras do grupo "UlyssesBlock"
- **Não destrutivo**: Não afeta outras regras de firewall existentes
- **Reversível**: As regras podem ser removidas manualmente pelo Firewall do Windows

### 🔒 Efetividade
- **Sistema-wide**: Bloqueia em todos os aplicativos, não só navegadores
- **Múltiplos IPs**: Resolve e bloqueia todos os IPs dos domínios
- **Subdomínios**: Inclui automaticamente subdomínios `www.`

### ⚡ Limitações
- **IPs dinâmicos**: Sites grandes mudam IPs frequentemente
- **CDNs**: Sites podem usar centenas de servidores diferentes
- **Contornável**: Usuários técnicos podem desabilitar via Firewall do Windows
- **DNS alternativo**: Pode ser contornado com VPNs ou DNS alternativos

## 🔧 Solução de problemas

### "Permission denied" ou "Access denied"
- Certifique-se de executar como Administrador
- Verifique se o antivírus não está bloqueando

### "No domains resolved"
- Verifique sua conexão com a internet
- Confirme que os domínios na lista existem

### Sites ainda funcionam
- Execute `check_ulysses_rules.py` para verificar se as regras foram criadas
- Sites grandes podem usar IPs diferentes - execute o script novamente
- Limpe o cache DNS: `ipconfig /flushdns`
- Desative DNS seguro no navegador

## 🎭 A Regra de Ulisses

> Na Odisseia de Homero, Ulisses pediu para ser amarrado ao mastro do navio para poder ouvir o canto das sereias sem sucumbir à tentação. A "Regra de Ulisses" é uma estratégia de autocontrole onde você remove sua capacidade de fazer escolhas impulsivas no futuro.

Este projeto implementa essa filosofia para o uso de internet, criando uma barreira técnica que requer esforço deliberado para remover, ajudando a quebrar ciclos de uso compulsivo de redes sociais e sites de entretenimento.

## 📜 Licença

Este projeto é de domínio público. Use, modifique e distribua livremente.

---

**⚠️ Aviso**: Este software é fornecido "como está". Use por sua própria conta e risco. Sempre mantenha backups das suas configurações importantes antes de modificar o firewall do sistema.
