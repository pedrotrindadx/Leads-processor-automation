# CAIXA Lead Processor v1.0

Um processador de leads profissional para imóveis da CAIXA com interface gráfica moderna e funcionalidades avançadas.

## 🌟 Funcionalidades

### 📋 Processamento de Leads
- **Extração automática** de leads de arquivos de texto
- **Busca automática** de informações de imóveis
- **Geração automática** de mensagens personalizadas do WhatsApp
- **Navegação** entre leads com controles intuitivos

### ➕ Entrada Manual de Leads
- **Formulário individual** para entrada de leads
- **Entrada em massa** via template de texto
- **Validação automática** de dados (email, telefone)
- **Backup automático** de leads não processados

### 💬 Integração com WhatsApp
- **Abertura direta** do WhatsApp (app ou web)
- **Mensagens personalizadas** com informações do imóvel
- **Envio sem prompts** para fluxo mais rápido

### 📊 Relatórios e Análises
- **Tabela de leads** processados com filtros
- **Estatísticas detalhadas** de processamento
- **Exportação para Excel** (.xlsx)
- **Histórico** de sessões de processamento

### ⚙️ Configurações Avançadas
- **Persistência de dados** entre sessões
- **Auto-salvamento** configurável
- **Gerenciamento de cache** e limpeza
- **Exportação/importação** de configurações
- **Tema e personalização** da interface

## 🚀 Instalação

### Opção 1: Executável (Recomendado)
1. Baixe o executável `CAIXA_Lead_Processor.exe`
2. Execute o arquivo `install.bat` para instalação completa
3. Use o atalho criado na área de trabalho

### Opção 2: Código Fonte
```bash
# Clone ou baixe os arquivos
git clone [repositório]

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python caixa_lead_gui.py
```

## 💻 Uso

### 1. Configuração Inicial
- **Arquivo de Leads**: Selecione ou deixe o padrão `leads.txt`
- **Modo Headless**: Mantenha marcado para melhor performance
- **WhatsApp**: Configure preferências de envio

### 2. Entrada de Leads

#### Método 1: Arquivo de Texto
- Cole os leads no arquivo `leads.txt` no formato:
```
Olá ,
Você possui um novo lead para o imóvel CX08444425765084SP:
Nome: João Silva Santos
E-mail: joao@email.com
Telefone: 11987654321
```

#### Método 2: Entrada Manual
- Use a aba "➕ Entrada Manual"
- Preencha o formulário individual
- Ou use a entrada em massa com template

### 3. Processamento
- Vá para a aba "▶️ Processamento"
- Clique em "Iniciar Processamento"
- Acompanhe o progresso em tempo real
- Use os controles de navegação entre leads

### 4. Envio via WhatsApp
- Clique em "Enviar WhatsApp" para cada lead
- A aplicação abre automaticamente o WhatsApp
- Confirme o envio e avance para o próximo

### 5. Relatórios
- Veja estatísticas na aba "📊 Relatórios"
- Exporte dados para Excel
- Consulte logs detalhados

## 🛠️ Build do Executável

Para criar o executável standalone:

```bash
python build_app.py
```

Isso criará:
- `dist/CAIXA_Lead_Processor.exe` - Executável principal
- `install.bat` - Script de instalação
- Atalhos para desktop e menu iniciar

---

**CAIXA Lead Processor** - Desenvolvido com ❤️ para otimizar o processamento de leads de imóveis.