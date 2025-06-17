# Lead Processor for Real Estate Leads

This Python script automates the process of handling real estate leads from Outlook emails, searching for property details, and sending personalized WhatsApp messages.

## Features

- Extracts lead information (name, phone, property code) from Outlook emails
- Only processes emails that haven't been flagged (to avoid duplicate responses)
- Automatically marks processed emails as flagged after sending a message
- Searches for property details on viahouseleiloes.com.br
- Extracts property URL and city information
- Opens WhatsApp Web and prepares a personalized message for the lead
- Comprehensive logging for troubleshooting

## Requirements

- Python 3.6+
- Microsoft Outlook installed
- Chrome browser installed
- Internet connection

## Installation

1. Clone or download this repository to your local machine.

2. Install the required Python packages:

```bash
pip install selenium webdriver-manager beautifulsoup4 pywin32
```

## Usage

### Basic Usage

Run the script with:

```bash
python lead_processor.py
```

By default, the script will process a test email included in the code. To process your own emails, you have two options:

### Option 1: Process the Latest Email from Outlook

Modify the `main()` function in `lead_processor.py` to use:

```python
# Comment out or remove this line
# processor.process_specific_email(test_email)

# Uncomment this line
processor.process_latest_email()
```

### Option 2: Process a Specific Email Text

You can modify the test email text in the `main()` function:

```python
test_email = """
Softunico Olá , Você possui um novo lead para o imóvel CX08787710134227SP:
Nome: pedro guelere
E-mail: pguelere2015@gmail.com
Telefone: 14981057073
"""
```

Replace this with your own email text and run the script.

## How It Works

1. **Email Processing**: 
   - The script connects to Outlook and searches for unflagged emails from Softunico.
   - It extracts lead information (name, phone, property code) from the email.
   - After processing, it marks the email as flagged to avoid duplicate processing.

2. **Web Automation**: 
   - Using Selenium, the script searches for the property on viahouseleiloes.com.br.
   - It extracts the property URL and city information.
   - If the property details can't be found, it uses example values to continue the process.

3. **WhatsApp Messaging**: 
   - The script opens WhatsApp Web with a pre-filled message for the lead.
   - It provides clear instructions if manual intervention is needed.

## Important Notes

- The script requires manual intervention to send the WhatsApp message. This is intentional to allow you to review the message before sending.
- You need to be logged into WhatsApp Web on your browser for the WhatsApp functionality to work properly.
- The script uses Chrome browser for web automation. Make sure Chrome is installed on your system.

## Customization

You can customize the WhatsApp message template in the `send_whatsapp_message()` method:

```python
message = (
    f"Bom dia {name}! tudo bem? Vi que demonstrou interesse nesse imóvel da CAIXA em {city}, "
    f"nós somos uma imobiliária credenciada pela Caixa e lhe damos assessoria de ponta á ponta "
    f"no processo de arremate desse imóvel, e de forma completamente gratuita nas modalidades de "
    f"Venda Online e Compra Direta (somos remunerados pela CAIXA). Você já tem conhecimento de "
    f"como os arremates funcionam? Segue o link do imóvel abaixo: {property_url}"
)
```

## Troubleshooting

If you encounter any issues:

1. Check the log file `lead_processor.log` for detailed error messages.
2. Make sure Outlook is running and accessible.
3. Ensure you have a stable internet connection.
4. Verify that Chrome is installed and up to date.

## License

This project is licensed under the MIT License - see the LICENSE file for details.