# CAIXA Lead Processor - Real Estate Lead Automation

A comprehensive Python application for automating real estate lead processing with both GUI and command-line interfaces. This tool processes leads from text files or manual input, searches for property details, and facilitates WhatsApp messaging for lead follow-up.

## 🚀 Features

### Core Functionality
- **Text File Processing**: Reads lead information from leads.txt file
- **Manual Lead Input**: GUI interface for entering leads manually 
- **Bulk Lead Processing**: Process multiple leads from pasted text templates
- **Web Scraping**: Searches for property details on viahouseleiloes.com.br
- **WhatsApp Automation**: Opens WhatsApp Web with pre-filled personalized messages
- **Comprehensive Logging**: Detailed logging for troubleshooting and audit trails

### GUI Application
- **Modern PyQt5 Interface**: User-friendly graphical interface with multiple tabs
- **Manual Input Tab**: Form-based lead entry with validation
- **Bulk Import**: Paste lead templates for automatic extraction
- **Real-time Processing**: Live updates and progress tracking
- **Settings Management**: Configurable application settings and message templates
- **Multi-threading**: Non-blocking UI during processing

### Command Line Tools
- **Flexible Processing**: Multiple processing modes and options
- **Batch Operations**: Process multiple leads efficiently
- **Testing Tools**: Built-in testing and validation utilities

## 📋 Requirements

- **Python 3.7+**
- **Google Chrome** browser
- **Internet connection**
- **Windows OS** (recommended)

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/pedrotrindadx/Leads-processor-automation.git
cd Leads-processor-automation
```

2. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify Chrome WebDriver:**
The application uses webdriver-manager to automatically handle ChromeDriver installation.

## 🎯 Usage

### GUI Application (Recommended)
Launch the graphical interface:
```bash
python caixa_lead_gui.py
```
or
```bash
python run_gui.py
```

### Command Line Interface
For direct processing:
```bash
python caixa_lead_processor.py
```

For testing:
```bash
python test_lead_processor.py
```

## 📁 Project Structure

```
├── caixa_lead_gui.py              # Main GUI application
├── caixa_lead_processor.py        # Core processing engine
├── run_gui.py                     # GUI launcher
├── app_settings.py                # Settings management
├── outlook_connector.py           # Outlook integration
├── alternative_outlook_connector.py # Alternative Outlook connection
├── fixed_lead_processor.py        # Fixed/stable version
├── manual_softunico.py           # Manual processing tools
├── test_*.py                     # Testing utilities
├── build_app.py                  # Application builder
├── requirements.txt              # Python dependencies
├── config/                       # Configuration files
│   ├── settings.json
│   └── window_state.json
└── icons/                        # Application icons
    ├── CAIXA.ico
    ├── CAIXA.png
    └── *.svg
```

## ⚙️ Configuration

### Settings
The application stores settings in `config/settings.json`:
- Lead processing preferences
- WhatsApp message templates
- Window positions and sizes
- Processing options

### Lead Input Methods
1. **Manual Input**: Use the GUI form to enter individual leads
2. **Text File**: Place leads in `leads.txt` file in the application directory
3. **Bulk Import**: Paste formatted lead text in the bulk import section

## 🔧 How It Works

### 1. Lead Processing
- Reads lead data from `leads.txt` file or manual GUI input
- Supports multiple lead formats and templates
- Extracts lead data (name, phone, email, property code)
- Validates lead information before processing

### 2. Property Search
- Automated web scraping of viahouseleiloes.com.br
- Extracts property URLs and location data
- Handles various property code formats
- Fallback mechanisms for missing data

### 3. WhatsApp Integration
- Opens WhatsApp Web with pre-filled messages
- Customizable message templates
- Manual review before sending (intentional safety feature)

## 📝 Lead Input Formats

### Manual Input (GUI)
Use the "➕ Entrada Manual" tab to input leads individually:
- Nome Completo
- E-mail
- Telefone
- Código do Imóvel

### Text File Format (leads.txt)
```
Nome: João Silva Santos
E-mail: joao@email.com
Telefone: 11987654321
Código: CX08444425765084SP
---
Nome: Maria Oliveira
E-mail: maria@email.com
Telefone: 21987654321
Código: CX08444425765085SP
```

### Bulk Import Template
```
Olá ,
Você possui um novo lead para o imóvel CX08444425765084SP:
Nome: João Silva Santos
E-mail: joao@email.com
Telefone: 11987654321
```

## 🎨 Customization

### Message Templates
Edit the message template in the processor:
```python
message = (
    f"Bom dia {name}! Vi que demonstrou interesse nesse imóvel da CAIXA em {city}. "
    f"Somos uma imobiliária credenciada e oferecemos assessoria gratuita. "
    f"Link do imóvel: {property_url}"
)
```

### Processing Options
- Modify search parameters
- Adjust timeout values
- Configure retry mechanisms
- Set custom data extraction rules

## 🛠️ Troubleshooting

### Common Issues
1. **Lead File Issues**: Ensure leads.txt is in the correct format
2. **Chrome Issues**: Update Chrome to the latest version
3. **Permission Errors**: Run as administrator if needed
4. **Network Issues**: Check internet connectivity
5. **GUI Issues**: Ensure PyQt5 is properly installed

### Debugging
- Check log files for detailed error information
- Use test scripts to verify individual components
- Enable verbose logging for detailed diagnostics
- Verify lead data format before processing

## 🔐 Security & Privacy

- No sensitive data is stored in the repository
- All personal messages and lead data are excluded from version control
- Local configuration files contain no sensitive information
- WhatsApp messages require manual review before sending

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues and support:
1. Check the troubleshooting section
2. Review log files for error details
3. Create an issue on GitHub with detailed information
4. Include relevant log snippets (remove sensitive data)

---

**Note**: This application is designed for real estate professionals working with CAIXA properties. It processes leads from text files or manual input rather than email integration. Ensure compliance with all applicable terms of service and regulations when using automated tools.