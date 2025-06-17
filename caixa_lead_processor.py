#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import logging
import datetime
import random
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('CAIXALeadProcessor')

class CAIXALeadProcessor:
    """
    Class for processing CAIXA leads from emails.
    """
    
    def __init__(self, leads_file=None, headless=False):
        """
        Initialize the CAIXALeadProcessor.
        
        Args:
            leads_file: Path to the file containing leads
            headless: Whether to run the browser in headless mode
        """
        self.driver = None
        self.leads_file = leads_file or os.path.join(os.getcwd(), "leads.txt")
    
    def setup_driver(self, headless=False):
        """
        Set up the Selenium WebDriver for web automation.
        
        Args:
            headless: Whether to run the browser in headless mode
            
        Returns:
            bool: True if setup was successful, False otherwise
        """
        try:
            logger.info("Setting up Selenium WebDriver...")
            print("[INFO] Configurando WebDriver do Selenium...")
            
            # Configure Chrome options
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            
            if headless:
                chrome_options.add_argument("--headless=new")  # Use new headless mode
            
            # Add additional options for stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-notifications")
            
            # Set up the WebDriver
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            # Set implicit wait time
            self.driver.implicitly_wait(10)
            
            logger.info("Selenium WebDriver setup successful")
            print("[INFO] WebDriver do Selenium configurado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Failed to set up Selenium WebDriver: {str(e)}")
            print(f"[ERRO] Falha ao configurar WebDriver do Selenium: {str(e)}")
            return False
    
    def extract_leads(self, file_path=None):
        """
        Extract lead information from a text file containing copied email content.
        
        Args:
            file_path: Path to the text file (optional, uses self.leads_file if not provided)
            
        Returns:
            list: List of lead dictionaries
        """
        try:
            file_path = file_path or self.leads_file
            logger.info(f"Extracting leads from file: {file_path}")
            print(f"[INFO] Extraindo leads do arquivo: {file_path}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                print(f"[ERRO] Arquivo não encontrado: {file_path}")
                return []
            
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if the content is empty
            if not content.strip():
                logger.warning("File is empty")
                print("[AVISO] Arquivo está vazio")
                return []
            
            # Split the content by the pattern that indicates the start of a new lead
            # This pattern is "Olá ," which appears at the beginning of each lead
            lead_blocks = re.split(r'(?=Olá\s*,)', content)
            
            # Remove any empty blocks
            lead_blocks = [block for block in lead_blocks if block.strip()]
            
            print(f"[INFO] Encontrados {len(lead_blocks)} blocos de leads no arquivo")
            
            # Process each lead block
            leads = []
            for i, lead_block in enumerate(lead_blocks):
                if not lead_block.strip():
                    continue
                
                print(f"\n[INFO] Processando lead #{i+1}:")
                print("-" * 40)
                print(lead_block[:200] + "..." if len(lead_block) > 200 else lead_block)
                print("-" * 40)
                
                # Extract lead information using regex patterns that match the specified format
                property_id_match = re.search(r'imóvel\s+(CX[0-9A-Z]+):', lead_block, re.IGNORECASE)
                name_match = re.search(r'Nome:\s+([^\r\n]+)', lead_block, re.IGNORECASE)
                email_match = re.search(r'E-mail:\s+([^\r\n]+)', lead_block, re.IGNORECASE)
                phone_match = re.search(r'Telefone:\s+([^\r\n]+)', lead_block, re.IGNORECASE)
                
                # Create lead dictionary
                lead = {}
                
                if property_id_match:
                    lead["property_id"] = property_id_match.group(1)
                    print(f"[INFO] Código do imóvel encontrado: {lead['property_id']}")
                else:
                    print("[AVISO] Código do imóvel não encontrado")
                
                if name_match:
                    # Format name with first letters capitalized
                    raw_name = name_match.group(1).strip()
                    formatted_name = ' '.join(word.capitalize() for word in raw_name.split())
                    lead["name"] = formatted_name
                    print(f"[INFO] Nome encontrado: {lead['name']}")
                else:
                    print("[AVISO] Nome não encontrado")
                
                if email_match:
                    lead["email"] = email_match.group(1).strip()
                    print(f"[INFO] Email encontrado: {lead['email']}")
                else:
                    print("[AVISO] Email não encontrado")
                
                if phone_match:
                    # Clean up the phone number (remove non-digits)
                    phone = re.sub(r'[^\d]', '', phone_match.group(1).strip())
                    lead["phone"] = phone
                    print(f"[INFO] Telefone encontrado: {lead['phone']}")
                else:
                    print("[AVISO] Telefone não encontrado")
                
                # If any information is missing, allow manual input
                if not lead.get("property_id") or not lead.get("name") or not lead.get("phone"):
                    print("\n[AVISO] Algumas informações não foram encontradas automaticamente.")
                    manual_input = input("Deseja inserir as informações manualmente? (s/n): ")
                    
                    if manual_input.lower() == "s":
                        if not lead.get("property_id"):
                            property_id = input("Digite o código do imóvel (ex: CX123456): ")
                            lead["property_id"] = property_id
                        
                        if not lead.get("name"):
                            name = input("Digite o nome do cliente: ")
                            # Format name with first letters capitalized
                            lead["name"] = ' '.join(word.capitalize() for word in name.split())
                        
                        if not lead.get("phone"):
                            phone = input("Digite o telefone do cliente (apenas números): ")
                            lead["phone"] = re.sub(r'[^\d]', '', phone)
                
                # Check if we have the minimum required information
                if lead.get("property_id") and lead.get("name") and lead.get("phone"):
                    leads.append(lead)
                    logger.info(f"Extracted lead: {lead.get('name', 'Unknown')}")
                    print(f"[INFO] Lead extraído com sucesso: {lead.get('name')}")
                else:
                    logger.warning(f"Incomplete lead information in email text")
                    print(f"[AVISO] Informações incompletas no texto do email. Este lead será ignorado.")
            
            logger.info(f"Extracted {len(leads)} leads from file")
            print(f"\n[INFO] Extraídos {len(leads)} leads do arquivo")
            return leads
        except Exception as e:
            logger.error(f"Failed to extract leads from file: {str(e)}")
            print(f"[ERRO] Falha ao extrair leads do arquivo: {str(e)}")
            return []
    
    def search_property_details(self, property_id, timeout=30):
        """
        Search for property details on viahouseleiloes.com.br.
        
        Args:
            property_id: Property ID to search for
            timeout: Maximum time to wait for operations (default: 30 seconds)
            
        Returns:
            dict: Property details dictionary
        """
        property_details = {
            "url": "",
            "city": "",
            "manual_review_needed": False,
            "error_details": ""
        }
        
        try:
            logger.info(f"Searching for property details (ID: {property_id})...")
            print(f"[INFO] Pesquisando detalhes do imóvel (ID: {property_id})...")
            
            # Set timeout for the driver
            self.driver.set_page_load_timeout(timeout)
            
            # Navigate to the website
            self.driver.get("https://viahouseleiloes.com.br/")
            
            # Wait for the page to load with reduced time
            time.sleep(2)
            
            # Wait for the search box to be available
            try:
                search_box = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Digite condomínio, região, bairro ou cidade']"))
                )
            except:
                # Try a different selector
                search_box = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][name='q']"))
                )
            
            # Enter the property ID and search
            search_box.clear()
            search_box.send_keys(property_id)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for the page to load after search (reduced time but more responsive)
            time.sleep(5)
            
            # Get the current URL (after redirection)
            current_url = self.driver.current_url
            property_details["url"] = current_url
            
            print(f"[INFO] URL do imóvel: {current_url}")
            
            # Check if property is no longer for sale
            try:
                not_found_element = self.driver.find_element(By.CSS_SELECTOR, ".container h1")
                if "Imóvel não encontrado" in not_found_element.text:
                    print(f"[AVISO] Imóvel não está mais disponível para venda")
                    property_details["city"] = ""
                    property_details["manual_review_needed"] = True
                    property_details["error_details"] = "property_no_longer_available"
                    property_details["property_not_available"] = True
                    return property_details
            except:
                # Element not found, property is still available
                pass
            
            # Try to extract the city from the page
            try:
                # Wait for the location element to be present
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".info-destaque.localizacao"))
                )
                
                # Get the location element
                location_element = self.driver.find_element(By.CSS_SELECTOR, ".info-destaque.localizacao")
                
                # Try to get the HTML content to parse the city
                location_html = location_element.get_attribute('innerHTML')
                
                # Try to extract city from HTML (format: "(Street) s/n <br> (city)- SP")
                city_match = re.search(r'<br>\s*([^-<]+)-\s*SP', location_html)
                
                if city_match:
                    city = city_match.group(1).strip()
                    property_details["city"] = city
                    print(f"[INFO] Cidade encontrada: {city}")
                else:
                    # Fallback to text extraction
                    location_text = location_element.text.strip()
                    
                    # Try to extract city from text
                    # Look for pattern: something followed by a dash and SP
                    city_text_match = re.search(r'([^-\n]+)-\s*SP', location_text)
                    
                    if city_text_match:
                        city = city_text_match.group(1).strip()
                        property_details["city"] = city
                        print(f"[INFO] Cidade encontrada: {city}")
                    else:
                        # Last resort: just use the whole text and clean it up
                        city_text = location_text.replace("SP", "").replace("-", "").strip()
                        # Remove any street address if present
                        if "," in city_text:
                            city_text = city_text.split(",")[-1].strip()
                        property_details["city"] = city_text
                        print(f"[INFO] Cidade extraída: {city_text}")
            except Exception as e:
                logger.warning(f"Could not extract city automatically: {str(e)}")
                print(f"[AVISO] Não foi possível extrair a cidade automaticamente: {str(e)}")
                
                # Mark for manual review instead of asking for console input
                property_details["city"] = ""
                property_details["manual_review_needed"] = True
                property_details["error_details"] = str(e)
                print(f"[INFO] Cidade será revisada manualmente após o processamento")
            
            return property_details
        except TimeoutException as e:
            logger.error(f"Timeout searching for property details: {str(e)}")
            print(f"[ERRO] Timeout ao pesquisar detalhes do imóvel: {str(e)}")
            property_details["manual_review_needed"] = True
            property_details["error_details"] = f"Timeout: {str(e)}"
            return property_details
        except Exception as e:
            logger.error(f"Failed to search for property details: {str(e)}")
            print(f"[ERRO] Falha ao pesquisar detalhes do imóvel: {str(e)}")
            property_details["manual_review_needed"] = True
            property_details["error_details"] = str(e)
            return property_details
    

    
    def send_whatsapp_message(self, lead):
        """
        Send a WhatsApp message to a lead.
        
        Args:
            lead: Lead dictionary
            
        Returns:
            bool: True if message was sent, False otherwise
        """
        try:
            logger.info(f"Sending WhatsApp message to {lead.get('name')}...")
            print(f"[INFO] Enviando mensagem de WhatsApp para {lead.get('name')}...")
            
            # Format the phone number (add country code)
            phone = lead.get("phone", "")
            if phone:
                # Remove any non-digit characters
                phone = re.sub(r'[^\d]', '', phone)
                
                # Add country code if not already present
                if not phone.startswith("55"):
                    phone = "55" + phone
            
            # Get the greeting based on the current time
            greeting = self._get_greeting()
            
            # Clean up the city text (remove extra spaces and line breaks)
            city = lead.get('city', '')
            if city:
                city = re.sub(r'\s+', ' ', city).strip()
            
            # Format the message with proper line breaks
            message = f"{greeting} {lead.get('name', '')}! tudo bem?\n\nVi que demonstrou interesse nesse imóvel da CAIXA em {city}, nós somos uma imobiliária credenciada pela Caixa e lhe damos assessoria de ponta á ponta no processo de arremate desse imóvel, e de forma completamente gratuita nas modalidades de Venda Online e Compra Direta (somos remunerados pela CAIXA). Você já tem conhecimento de como os arremates funcionam?\n\nSegue o link do imóvel abaixo:\n{lead.get('property_url', '')}"
            
            # URL encode the message
            encoded_message = urllib.parse.quote(message)
            
            # Construct the WhatsApp URL for the app (direct app link)
            whatsapp_api_url = f"whatsapp://send?phone={phone}&text={encoded_message}"
            
            # Primeiro, criar e abrir a página HTML com a mensagem
            try:
                # Salvar a mensagem em um arquivo de texto
                message_file = os.path.join(os.getcwd(), f"mensagem_{lead.get('name', 'desconhecido')}.txt")
                with open(message_file, 'w', encoding='utf-8') as f:
                    f.write(message)
                print(f"\n[INFO] Mensagem salva no arquivo: {message_file}")
                
                # Criar um arquivo HTML para exibir a mensagem com formatação correta
                html_file = os.path.join(os.getcwd(), f"mensagem_{lead.get('name', 'desconhecido')}.html")
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write('<!DOCTYPE html>\n')
                    f.write('<html>\n')
                    f.write('<head>\n')
                    f.write('    <meta charset="UTF-8">\n')
                    f.write('    <title>Mensagem para WhatsApp</title>\n')
                    f.write('    <style>\n')
                    f.write('        body { font-family: Arial, sans-serif; padding: 20px; background-color: #f0f0f0; }\n')
                    f.write('        .container { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }\n')
                    f.write('        h1 { color: #075e54; font-size: 18px; }\n')
                    f.write('        .message { white-space: pre-wrap; background-color: #dcf8c6; padding: 15px; border-radius: 10px; margin: 20px 0; }\n')
                    f.write('        .instructions { background-color: #ffe0b2; padding: 10px; border-radius: 5px; margin-top: 20px; }\n')
                    f.write('        .buttons { display: flex; gap: 10px; margin-top: 15px; }\n')
                    f.write('        button { background-color: #075e54; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; }\n')
                    f.write('        button:hover { background-color: #128c7e; }\n')
                    f.write('        .whatsapp-btn { background-color: #25D366; }\n')
                    f.write('        .whatsapp-btn:hover { background-color: #1da851; }\n')
                    f.write('    </style>\n')
                    f.write('</head>\n')
                    f.write('<body>\n')
                    f.write('    <div class="container">\n')
                    f.write('        <h1>Mensagem para WhatsApp - Copie e Cole no App</h1>\n')
                    # Escapar caracteres HTML e preservar quebras de linha
                    escaped_message = message.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    formatted_message = escaped_message.replace('\n', '<br>')
                    f.write(f'        <div class="message" id="messageText">{formatted_message}</div>\n')
                    f.write('        <div class="buttons">\n')
                    f.write('            <button onclick="copyMessage()">Copiar Mensagem</button>\n')
                    f.write(f'            <button class="whatsapp-btn" onclick="openWhatsApp()">Abrir WhatsApp</button>\n')
                    f.write('        </div>\n')
                    f.write('        <div class="instructions">\n')
                    f.write('            <p><strong>Instruções:</strong></p>\n')
                    f.write('            <ol>\n')
                    f.write('                <li>Clique no botão "Copiar Mensagem" acima</li>\n')
                    f.write('                <li>Clique no botão "Abrir WhatsApp" ou abra o WhatsApp manualmente</li>\n')
                    f.write('                <li>Cole a mensagem no WhatsApp</li>\n')
                    f.write('                <li>Feche esta janela quando terminar</li>\n')
                    f.write('            </ol>\n')
                    f.write('        </div>\n')
                    f.write('    </div>\n')
                    # Armazenar a mensagem original em um elemento oculto para preservar formatação
                    f.write('    <textarea id="originalMessage" style="display:none;">' + message + '</textarea>\n')
                    f.write('    <script>\n')
                    f.write('        function copyMessage() {\n')
                    f.write('            // Usar o texto original do textarea oculto para preservar quebras de linha\n')
                    f.write('            const messageText = document.getElementById("originalMessage").value;\n')
                    f.write('            navigator.clipboard.writeText(messageText)\n')
                    f.write('                .then(() => {\n')
                    f.write('                    // Destacar visualmente que a cópia foi bem-sucedida\n')
                    f.write('                    const button = document.querySelector("button");\n')
                    f.write('                    button.textContent = "✓ Copiado!";\n')
                    f.write('                    button.style.backgroundColor = "#4CAF50";\n')
                    f.write('                    setTimeout(() => {\n')
                    f.write('                        button.textContent = "Copiar Mensagem";\n')
                    f.write('                        button.style.backgroundColor = "#075e54";\n')
                    f.write('                    }, 2000);\n')
                    f.write('                })\n')
                    f.write('                .catch(err => alert("Erro ao copiar: " + err));\n')
                    f.write('        }\n')
                    f.write(f'        function openWhatsApp() {{\n')
                    f.write(f'            window.open("{whatsapp_api_url}", "_blank");\n')
                    f.write('        }\n')
                    f.write('    </script>\n')
                    f.write('</body>\n')
                    f.write('</html>\n')
                
                # Abrir o arquivo HTML no navegador padrão
                import webbrowser
                webbrowser.open(html_file)
                print("[INFO] Mensagem aberta em uma página HTML para fácil cópia")
            except Exception as e:
                print(f"[AVISO] Não foi possível criar a página HTML: {str(e)}")
                # Mostrar mensagem no terminal atual
                print("\n[INFO] Por favor, copie a mensagem manualmente:")
                print("-" * 50)
                print(message)
                print("-" * 50)
            
            # Perguntar ao usuário se deseja abrir o link do WhatsApp no navegador
            open_link = input("\nDeseja abrir o link do WhatsApp no navegador? (s/n): ")
            
            if open_link.lower() == "s":
                # Abrir o link do WhatsApp no navegador
                print("[INFO] Abrindo link para o WhatsApp App...")
                self.driver.get(whatsapp_api_url)
                
                # Verificar se precisamos clicar no botão "Continue to chat"
                try:
                    continue_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, "action-button"))
                    )
                    continue_button.click()
                    print("[INFO] Botão 'Continue to chat' clicado.")
                except:
                    # Elemento não encontrado, pode estar redirecionando para o app
                    print("[INFO] Redirecionando para o WhatsApp App...")
            
            # Wait for the page to load or app to open
            time.sleep(3)
            
            # Take a screenshot
            screenshot_path = os.path.join(os.getcwd(), f"whatsapp_{lead.get('name', 'unknown')}.png")
            self.driver.save_screenshot(screenshot_path)
            
            logger.info(f"WhatsApp link opened for {lead.get('name')}")
            print(f"[INFO] Link do WhatsApp aberto para {lead.get('name')}")
            
            # Ask the user if the message was sent successfully
            print("[INFO] Verifique se o WhatsApp App foi aberto com a mensagem.")
            print("[INFO] Você pode copiar a mensagem da janela de terminal que foi aberta.")
            manual_send = input("A mensagem foi enviada com sucesso? (s/n): ")
            
            if manual_send.lower() == "s":
                logger.info(f"WhatsApp message sent to {lead.get('name')} (confirmed by user)")
                print(f"[INFO] Mensagem de WhatsApp enviada para {lead.get('name')} (confirmado pelo usuário)")
                return True
            else:
                logger.warning(f"WhatsApp message not sent to {lead.get('name')} (confirmed by user)")
                print(f"[AVISO] Mensagem não enviada para {lead.get('name')}")
                return False
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {str(e)}")
            print(f"[ERRO] Falha ao enviar mensagem de WhatsApp: {str(e)}")
            return False
    
    def _get_greeting(self):
        """
        Get a greeting based on the current time.
        
        Returns:
            str: Greeting
        """
        hour = datetime.datetime.now().hour
        
        if hour < 12:
            return "Bom dia"
        elif hour < 18:
            return "Boa tarde"
        else:
            return "Boa noite"
    
    # Alias for backward compatibility
    extract_leads_from_file = extract_leads
    
    def process_leads(self, headless=False):
        """
        Process CAIXA leads from a text file.
        
        Args:
            headless: Whether to run the browser in headless mode
            
        Returns:
            bool: True if processing was successful, False otherwise
        """
        try:
            logger.info("Starting CAIXA lead processing...")
            print("[INFO] Iniciando processamento de leads da CAIXA...")
            
            # Use the file path from the instance
            file_path = self.leads_file
            
            print(f"[INFO] Usando arquivo: {file_path}")
            
            # Check if the file exists and has content
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                print("[AVISO] Arquivo de leads vazio ou não encontrado.")
                print("[INFO] Por favor, adicione os leads ao arquivo leads.txt no formato:")
                print("Olá ,")
                print("Você possui um novo lead para o imóvel CX08787701604879SP:")
                print("Nome: Valmir")
                print("E-mail: valmir100190@gmail.com")
                print("Telefone: 11992963253")
                return False
            
            # Extract leads from the file
            leads = self.extract_leads(file_path)
            
            if not leads:
                print("[AVISO] Nenhum lead encontrado no arquivo.")
                print("[STATUS] Saindo do programa...")
                return False
            
            # Setup Selenium WebDriver
            selenium_success = self.setup_driver(headless=headless)
            if not selenium_success:
                print("[ERRO] Não foi possível configurar o WebDriver do Selenium.")
                return False
            
            # Process each lead
            for i, lead in enumerate(leads):
                print(f"\n[INFO] Processando lead {i+1} de {len(leads)}: {lead.get('name', 'Desconhecido')}")
                
                # Search for property details if we have a property ID
                property_details = {}
                if lead.get("property_id"):
                    property_details = self.search_property_details(lead["property_id"])
                    
                    # Add property details to the lead
                    lead["property_url"] = property_details.get("url", "")
                    lead["city"] = property_details.get("city", "")
                
                # If property details are missing, ask the user if they want to search on Google or provide manually
                if not lead.get("property_url") or not lead.get("city"):
                    print("[AVISO] Não foi possível encontrar detalhes do imóvel automaticamente.")
                    print("Escolha uma opção:")
                    print("1. Pesquisar no Google")
                    print("2. Inserir detalhes manualmente")
                    print("3. Pular este lead")
                    
                    option = input("Digite o número da opção desejada: ")
                    
                    if option == "1":
                        # Search on Google
                        google_details = self.search_property_on_google(lead.get("property_id", ""))
                        
                        if google_details.get("url"):
                            lead["property_url"] = google_details.get("url", "")
                        
                        if google_details.get("city"):
                            lead["city"] = google_details.get("city", "")
                    
                    elif option == "2":
                        # Manual input
                        if not lead.get("property_url"):
                            property_url = input("Digite a URL do imóvel: ")
                            lead["property_url"] = property_url
                        
                        if not lead.get("city"):
                            city = input("Digite a cidade do imóvel: ")
                            lead["city"] = city
                    
                    elif option == "3":
                        # Skip this lead
                        print("[INFO] Pulando este lead...")
                        continue
                    else:
                        print("[ERRO] Opção inválida. Pulando este lead...")
                        continue
                
                # Send WhatsApp message
                if lead.get("phone") and lead.get("property_url") and lead.get("city"):
                    sent = self.send_whatsapp_message(lead)
                    if sent:
                        print("[SUCESSO] Mensagem enviada com sucesso!")
                    else:
                        print("[AVISO] Mensagem não enviada.")
                else:
                    print("[AVISO] Não foi possível enviar a mensagem: informações incompletas.")
                    missing = []
                    if not lead.get("phone"):
                        missing.append("telefone")
                    if not lead.get("property_url"):
                        missing.append("URL do imóvel")
                    if not lead.get("city"):
                        missing.append("cidade")
                    print(f"[DETALHE] Informações faltantes: {', '.join(missing)}")
                
                # Ask if the user wants to continue to the next lead
                if i < len(leads) - 1:
                    continue_processing = input("\nDeseja continuar para o próximo lead? (s/n): ")
                    if continue_processing.lower() != "s":
                        print("[STATUS] Interrompendo processamento de leads...")
                        break
            
            logger.info("CAIXA lead processing completed")
            print("\n[INFO] Processamento de leads da CAIXA concluído")
            return True
        except Exception as e:
            logger.error(f"Failed to process leads: {str(e)}")
            print(f"[ERRO] Falha ao processar leads: {str(e)}")
            return False
        finally:
            # Close the WebDriver
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                    
    def get_greeting(self):
        """
        Get greeting based on time of day.
        
        Returns:
            str: Greeting
        """
        hour = datetime.datetime.now().hour
        
        if hour < 12:
            return "Bom dia"
        elif hour < 18:
            return "Boa tarde"
        else:
            return "Boa noite"
            
    def generate_whatsapp_message(self, lead):
        """
        Generate WhatsApp message for a lead without sending it.
        
        Args:
            lead: Lead dictionary
            
        Returns:
            str: WhatsApp message
        """
        try:
            from app_settings import AppSettings
            settings = AppSettings()
            
            # Check if property is no longer available OR if it's a pending lead that needs manual review
            is_property_unavailable = lead.get("property_not_available") or lead.get("error_details") == "property_no_longer_available"
            is_pending_manual_review = "Pendente" in lead.get("status", "") or lead.get("manual_review_needed", False)
            
            if is_property_unavailable or is_pending_manual_review:
                # Use custom template for properties no longer for sale
                template = settings.get("message_templates.unavailable_lead", 
                    "Bom dia {{name}}! tudo bem?\nVi que demonstrou interesse em um imóvel da CAIXA, porém ele já foi arrematado ou está fora do ar por algum outro motivo!\nNós somos uma imobiliária credenciada pela Caixa e lhe damos assessoria de ponta á ponta no processo de arremate desse imóvel, e de forma completamente gratuita nas modalidades de Venda Online e Compra Direta (somos remunerados pela CAIXA).\nVocê já tem conhecimento de como os arremates funcionam?\nEncontre seu investimento ou imóvel dos sonhos por preços bem abaixo do praticado no mercado aqui no próprio site da CAIXA:\nvenda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis")
                
                return self.process_message_template(template, lead)
            
            # Check if we have all the required information for regular message
            if not lead.get("name") or not lead.get("city") or not lead.get("property_url"):
                missing = []
                if not lead.get("name"):
                    missing.append("nome")
                if not lead.get("city"):
                    missing.append("cidade")
                if not lead.get("property_url"):
                    missing.append("URL do imóvel")
                
                raise ValueError(f"Informações faltantes: {', '.join(missing)}")
            
            # Use custom template for regular leads
            template = settings.get("message_templates.normal_lead",
                "{{greeting}} {{name}}! tudo bem?\n\nVi que demonstrou interesse nesse imóvel da CAIXA em {{city}}, nós somos uma imobiliária credenciada pela Caixa e lhe damos assessoria de ponta á ponta no processo de arremate desse imóvel, e de forma completamente gratuita nas modalidades de Venda Online e Compra Direta (somos remunerados pela CAIXA). Você já tem conhecimento de como os arremates funcionam?\n\nSegue o link do imóvel abaixo:\n{{property_url}}")
            
            return self.process_message_template(template, lead)
            
        except Exception as e:
            logger.error(f"Failed to generate WhatsApp message: {str(e)}")
            raise
    
    def process_message_template(self, template, lead):
        """Process message template with lead data"""
        try:
            # Get greeting based on time of day
            greeting = self.get_greeting()
            
            # Map template variables
            variables = {
                '{{name}}': lead.get('name', 'pessoa'),
                '{{city}}': lead.get('city', ''),
                '{{property_url}}': lead.get('property_url', ''),
                '{{telephone}}': lead.get('phone', ''),
                '{{greeting}}': greeting
            }
            
            # Replace variables in template
            message = template
            for var, value in variables.items():
                message = message.replace(var, str(value))
            
            return message
            
        except Exception as e:
            logger.error(f"Failed to process message template: {str(e)}")
            raise

def main():
    """
    Main function.
    """
    print("\n" + "=" * 50)
    print("PROCESSADOR DE LEADS DA CAIXA")
    print("=" * 50 + "\n")
    
    # Ask if the user wants to run the browser in headless mode
    headless = input("Executar navegador em modo invisível? (s/n, padrão: n): ").lower() == "s"
    
    # Create an instance of the CAIXALeadProcessor
    processor = CAIXALeadProcessor()
    
    # Process leads
    result = processor.process_leads(headless=headless)
    
    print("\n" + "=" * 50)
    print("PROCESSAMENTO CONCLUÍDO")
    print("=" * 50 + "\n")
    
    return result

if __name__ == "__main__":
    main()