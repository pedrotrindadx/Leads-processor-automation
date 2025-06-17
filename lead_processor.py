#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lead Processor for Real Estate Leads

This script automates the process of:
1. Extracting lead information from Outlook emails
2. Searching for property details on viahouseleiloes.com.br
3. Sending a personalized WhatsApp message to the lead

Author: AI Assistant
Version: 1.0
Date: 2024-10-24
"""

import re
import time
import logging
import os
import tempfile
import urllib.parse
from typing import Dict, Optional, Tuple

# External dependencies
import win32com.client
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Import the OutlookConnector
from outlook_connector import OutlookConnector

# Import the fixed methods
try:
    from fixed_lead_processor import apply_fixed_methods
except ImportError:
    # Define a dummy function if the import fails
    def apply_fixed_methods(processor):
        return processor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("lead_processor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("LeadProcessor")

class LeadProcessor:
    """
    Main class for processing real estate leads from Outlook emails.
    """
    
    def __init__(self):
        """Initialize the LeadProcessor with necessary components."""
        self.outlook_connector = OutlookConnector()
        self.outlook = None
        self.driver = None
        
    def setup_outlook(self, timeout=15):
        """
        Connect to the Outlook application with timeout.
        
        Args:
            timeout: Maximum time in seconds to wait for connection
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        logger.info(f"Connecting to Outlook (timeout: {timeout}s)...")
        print(f"[INFO] Conectando ao Outlook (timeout: {timeout}s)...")
        
        # Use our new OutlookConnector to connect to Outlook
        result = self.outlook_connector.setup_outlook(timeout=timeout)
        
        if result:
            # For compatibility with existing code, we need to set self.outlook
            # to access the Outlook application object
            try:
                # Get the Outlook application object using PowerShell
                import subprocess
                import tempfile
                
                # PowerShell command to get Outlook application
                ps_command = """
                $outlook = New-Object -ComObject Outlook.Application
                Write-Output "SUCCESS"
                """
                
                # Save the command to a temporary file
                temp_ps_file = os.path.join(tempfile.gettempdir(), 'get_outlook.ps1')
                with open(temp_ps_file, 'w') as f:
                    f.write(ps_command)
                
                # Execute the PowerShell script
                result = subprocess.run(
                    ["powershell", "-ExecutionPolicy", "Bypass", "-File", temp_ps_file],
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                
                # Check if the command was successful
                if "SUCCESS" in result.stdout:
                    # Now we can use win32com to get the Outlook application
                    import win32com.client
                    self.outlook = win32com.client.Dispatch("Outlook.Application")
                    logger.info("Successfully got Outlook application object")
                    return True
                else:
                    logger.warning(f"Failed to get Outlook application object: {result.stderr}")
                    print(f"[AVISO] Falha ao obter objeto do Outlook: {result.stderr}")
                    return False
            except Exception as e:
                logger.error(f"Failed to get Outlook application object: {str(e)}")
                print(f"[ERRO] Falha ao obter objeto do Outlook: {str(e)}")
                return False
        
        return False
        
    def setup_selenium(self, headless=False):
        """
        Set up the Selenium WebDriver for web automation.
        
        Args:
            headless: Whether to run the browser in headless mode
            
        Returns:
            bool: True if setup successful, False otherwise
        """
        try:
            logger.info("Setting up Selenium WebDriver...")
            print("[INFO] Configurando WebDriver do Selenium...")
            
            # Set up Chrome options
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-extensions")
            
            # Set up the Chrome driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set implicit wait time
            self.driver.implicitly_wait(10)
            
            logger.info("Selenium WebDriver setup successful")
            print("[INFO] WebDriver do Selenium configurado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Failed to set up Selenium WebDriver: {str(e)}")
            print(f"[ERRO] Falha ao configurar WebDriver do Selenium: {str(e)}")
            return False
    
    def extract_leads_from_emails(self, days=1, max_emails=10):
        """
        Extract lead information from Outlook emails.
        
        Args:
            days: Number of days to look back for emails
            max_emails: Maximum number of emails to process
            
        Returns:
            list: List of lead dictionaries
        """
        if not self.outlook:
            logger.error("Cannot extract leads: Outlook not connected")
            print("[ERRO] Não é possível extrair leads: Outlook não conectado")
            return []
        
        try:
            logger.info(f"Extracting leads from emails (last {days} days, max {max_emails} emails)...")
            print(f"[INFO] Extraindo leads de emails (últimos {days} dias, máximo {max_emails} emails)...")
            
            # Access the Outlook namespace and inbox folder
            namespace = self.outlook.GetNamespace("MAPI")
            inbox = namespace.GetDefaultFolder(6)  # 6 corresponds to the inbox folder
            
            # Calculate the date threshold
            import datetime
            threshold_date = datetime.datetime.now() - datetime.timedelta(days=days)
            
            # Filter emails by date
            filter_string = f"[ReceivedTime] >= '{threshold_date.strftime('%m/%d/%Y %H:%M %p')}'"
            filtered_emails = inbox.Items.Restrict(filter_string)
            filtered_emails.Sort("[ReceivedTime]", True)  # Sort by received time, descending
            
            # Process emails
            leads = []
            count = 0
            
            for email in filtered_emails:
                if count >= max_emails:
                    break
                
                try:
                    # Check if the email is from a lead source
                    if self._is_lead_email(email):
                        lead_info = self._extract_lead_info(email)
                        if lead_info:
                            leads.append(lead_info)
                            logger.info(f"Extracted lead: {lead_info.get('name', 'Unknown')}")
                            print(f"[INFO] Lead extraído: {lead_info.get('name', 'Desconhecido')}")
                    
                    count += 1
                except Exception as e:
                    logger.warning(f"Failed to process email: {str(e)}")
                    print(f"[AVISO] Falha ao processar email: {str(e)}")
                    continue
            
            logger.info(f"Extracted {len(leads)} leads from {count} emails")
            print(f"[INFO] Extraídos {len(leads)} leads de {count} emails")
            return leads
        except Exception as e:
            logger.error(f"Failed to extract leads from emails: {str(e)}")
            print(f"[ERRO] Falha ao extrair leads de emails: {str(e)}")
            return []
    
    def _is_lead_email(self, email):
        """
        Check if an email is from a lead source.
        
        Args:
            email: Outlook email object
            
        Returns:
            bool: True if the email is from a lead source, False otherwise
        """
        # Define lead source patterns
        lead_sources = [
            "viahouseleiloes.com.br",
            "imovelweb.com.br",
            "vivareal.com.br",
            "zapimoveis.com.br",
            "olx.com.br",
            "mercadolivre.com.br",
            "contato@imobiliaria",
            "lead@",
            "contato@",
            "imoveis@"
        ]
        
        # Check sender email
        sender = email.SenderEmailAddress.lower() if hasattr(email, "SenderEmailAddress") else ""
        
        # Check subject
        subject = email.Subject.lower() if hasattr(email, "Subject") else ""
        
        # Check if any lead source pattern matches
        for source in lead_sources:
            if source in sender or source in subject:
                return True
        
        # Check for common lead keywords in subject
        lead_keywords = [
            "lead",
            "contato",
            "interesse",
            "imóvel",
            "imovel",
            "casa",
            "apartamento",
            "compra",
            "venda",
            "aluguel"
        ]
        
        for keyword in lead_keywords:
            if keyword in subject:
                return True
        
        return False
    
    def _extract_lead_info(self, email):
        """
        Extract lead information from an email.
        
        Args:
            email: Outlook email object
            
        Returns:
            dict: Lead information dictionary
        """
        lead_info = {
            "name": "",
            "email": "",
            "phone": "",
            "property_id": "",
            "property_type": "",
            "property_location": "",
            "message": "",
            "source": "",
            "received_date": ""
        }
        
        try:
            # Extract basic information
            lead_info["received_date"] = email.ReceivedTime.strftime("%Y-%m-%d %H:%M:%S") if hasattr(email, "ReceivedTime") else ""
            lead_info["source"] = email.SenderEmailAddress if hasattr(email, "SenderEmailAddress") else ""
            
            # Extract information from subject
            subject = email.Subject if hasattr(email, "Subject") else ""
            lead_info["property_id"] = self._extract_property_id(subject)
            
            # Extract information from body
            body = email.Body if hasattr(email, "Body") else ""
            if not body and hasattr(email, "HTMLBody"):
                # Convert HTML body to plain text
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(email.HTMLBody, "html.parser")
                body = soup.get_text()
            
            # Extract contact information
            lead_info["name"] = self._extract_name(body, subject)
            lead_info["email"] = self._extract_email(body)
            lead_info["phone"] = self._extract_phone(body)
            lead_info["message"] = self._extract_message(body)
            lead_info["property_type"] = self._extract_property_type(body, subject)
            lead_info["property_location"] = self._extract_location(body, subject)
            
            return lead_info
        except Exception as e:
            logger.warning(f"Failed to extract lead information: {str(e)}")
            print(f"[AVISO] Falha ao extrair informações do lead: {str(e)}")
            return None
    
    def _extract_property_id(self, text):
        """Extract property ID from text"""
        # Common patterns for property IDs
        patterns = [
            r"ID[:\s]*([A-Za-z0-9\-]+)",
            r"Código[:\s]*([A-Za-z0-9\-]+)",
            r"Ref[:\s]*([A-Za-z0-9\-]+)",
            r"Referência[:\s]*([A-Za-z0-9\-]+)",
            r"Imóvel[:\s]*([A-Za-z0-9\-]+)",
            r"Imovel[:\s]*([A-Za-z0-9\-]+)",
            r"Propriedade[:\s]*([A-Za-z0-9\-]+)",
            r"#([A-Za-z0-9\-]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_name(self, body, subject=""):
        """Extract name from email body or subject"""
        # Common patterns for names
        patterns = [
            r"Nome[:\s]*([A-Za-zÀ-ÖØ-öø-ÿ\s]+?)[\r\n]",
            r"Cliente[:\s]*([A-Za-zÀ-ÖØ-öø-ÿ\s]+?)[\r\n]",
            r"De[:\s]*([A-Za-zÀ-ÖØ-öø-ÿ\s]+?)[\r\n]",
            r"From[:\s]*([A-Za-zÀ-ÖØ-öø-ÿ\s]+?)[\r\n]"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Filter out email addresses
                if "@" not in name:
                    return name
        
        # If no name found in body, try to extract from subject
        if "interesse" in subject.lower():
            parts = subject.split(":")
            if len(parts) > 1:
                return parts[1].strip()
        
        return "Cliente"  # Default name if none found
    
    def _extract_email(self, text):
        """Extract email address from text"""
        # Pattern for email addresses
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        
        match = re.search(pattern, text)
        if match:
            return match.group(0)
        
        return ""
    
    def _extract_phone(self, text):
        """Extract phone number from text"""
        # Common patterns for Brazilian phone numbers
        patterns = [
            r"Telefone[:\s]*(\+?55?\s?(?:\d{2})?\s?\d{4,5}[-\s]?\d{4})",
            r"Tel[:\s]*(\+?55?\s?(?:\d{2})?\s?\d{4,5}[-\s]?\d{4})",
            r"Celular[:\s]*(\+?55?\s?(?:\d{2})?\s?\d{4,5}[-\s]?\d{4})",
            r"Whatsapp[:\s]*(\+?55?\s?(?:\d{2})?\s?\d{4,5}[-\s]?\d{4})",
            r"WhatsApp[:\s]*(\+?55?\s?(?:\d{2})?\s?\d{4,5}[-\s]?\d{4})",
            r"Contato[:\s]*(\+?55?\s?(?:\d{2})?\s?\d{4,5}[-\s]?\d{4})",
            # Generic patterns for phone numbers
            r"(\+?55?\s?(?:\d{2})?\s?\d{4,5}[-\s]?\d{4})"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                phone = match.group(1)
                # Clean up the phone number
                phone = re.sub(r"[^\d]", "", phone)
                
                # Format the phone number
                if len(phone) == 11:  # Mobile with DDD
                    return f"({phone[0:2]}) {phone[2:7]}-{phone[7:11]}"
                elif len(phone) == 10:  # Landline with DDD
                    return f"({phone[0:2]}) {phone[2:6]}-{phone[6:10]}"
                elif len(phone) == 9:  # Mobile without DDD
                    return f"{phone[0:5]}-{phone[5:9]}"
                elif len(phone) == 8:  # Landline without DDD
                    return f"{phone[0:4]}-{phone[4:8]}"
                else:
                    return phone
        
        return ""
    
    def _extract_message(self, text):
        """Extract message from text"""
        # Common patterns for messages
        patterns = [
            r"Mensagem[:\s]*([^\r\n]+(?:[\r\n][^\r\n]+)*)",
            r"Comentário[:\s]*([^\r\n]+(?:[\r\n][^\r\n]+)*)",
            r"Comentario[:\s]*([^\r\n]+(?:[\r\n][^\r\n]+)*)",
            r"Observação[:\s]*([^\r\n]+(?:[\r\n][^\r\n]+)*)",
            r"Observacao[:\s]*([^\r\n]+(?:[\r\n][^\r\n]+)*)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # If no specific message pattern found, try to extract a generic message
        lines = text.split("\n")
        message_lines = []
        in_message = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip header lines
            if ":" in line and not in_message:
                continue
            
            # Skip footer lines
            if "atenciosamente" in line.lower() or "cordialmente" in line.lower():
                break
            
            # Consider this part of the message
            in_message = True
            message_lines.append(line)
            
            # Limit message length
            if len(message_lines) >= 5:
                break
        
        if message_lines:
            return " ".join(message_lines)
        
        return ""
    
    def _extract_property_type(self, body, subject=""):
        """Extract property type from text"""
        # Common property types
        property_types = [
            "casa",
            "apartamento",
            "terreno",
            "lote",
            "sítio",
            "sitio",
            "fazenda",
            "chácara",
            "chacara",
            "sala comercial",
            "loja",
            "galpão",
            "galpao",
            "prédio",
            "predio",
            "cobertura",
            "flat",
            "kitnet"
        ]
        
        # Check subject first
        for prop_type in property_types:
            if prop_type in subject.lower():
                return prop_type.capitalize()
        
        # Then check body
        for prop_type in property_types:
            if prop_type in body.lower():
                return prop_type.capitalize()
        
        return "Imóvel"  # Default if no specific type found
    
    def _extract_location(self, body, subject=""):
        """Extract property location from text"""
        # Try to find location patterns
        patterns = [
            r"Localização[:\s]*([^\r\n]+)",
            r"Localizacao[:\s]*([^\r\n]+)",
            r"Endereço[:\s]*([^\r\n]+)",
            r"Endereco[:\s]*([^\r\n]+)",
            r"Bairro[:\s]*([^\r\n]+)",
            r"Cidade[:\s]*([^\r\n]+)",
            r"em ([A-Za-zÀ-ÖØ-öø-ÿ\s]+?)[,\.]"
        ]
        
        # Check body
        for pattern in patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Check subject
        for pattern in patterns:
            match = re.search(pattern, subject, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def search_property_details(self, property_id):
        """
        Search for property details on viahouseleiloes.com.br.
        
        Args:
            property_id: Property ID to search for
            
        Returns:
            dict: Property details dictionary
        """
        if not self.driver:
            logger.error("Cannot search property: Selenium WebDriver not set up")
            print("[ERRO] Não é possível pesquisar imóvel: WebDriver do Selenium não configurado")
            return {}
        
        try:
            logger.info(f"Searching for property details (ID: {property_id})...")
            print(f"[INFO] Pesquisando detalhes do imóvel (ID: {property_id})...")
            
            # Navigate to the website
            self.driver.get("https://www.viahouseleiloes.com.br/")
            
            # Wait for the search box to be available
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "search-input"))
            )
            
            # Enter the property ID
            search_box.clear()
            search_box.send_keys(property_id)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for search results
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "property-card"))
            )
            
            # Take a screenshot of the search results
            screenshot_path = os.path.join(os.getcwd(), f"search_results_{property_id}.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Saved search results screenshot to {screenshot_path}")
            print(f"[INFO] Captura de tela dos resultados salva em {screenshot_path}")
            
            # Click on the first result
            first_result = self.driver.find_element(By.CLASS_NAME, "property-card")
            first_result.click()
            
            # Wait for the property details page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "property-details"))
            )
            
            # Take a screenshot of the property details
            screenshot_path = os.path.join(os.getcwd(), f"property_details_{property_id}.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Saved property details screenshot to {screenshot_path}")
            print(f"[INFO] Captura de tela dos detalhes do imóvel salva em {screenshot_path}")
            
            # Extract property details
            property_details = self._extract_property_details()
            
            logger.info(f"Found property details: {property_details}")
            print(f"[INFO] Detalhes do imóvel encontrados: {property_details}")
            return property_details
        except Exception as e:
            logger.error(f"Failed to search property details: {str(e)}")
            print(f"[ERRO] Falha ao pesquisar detalhes do imóvel: {str(e)}")
            
            # Take a screenshot of the error
            try:
                screenshot_path = os.path.join(os.getcwd(), f"error_screenshot_{property_id}.png")
                self.driver.save_screenshot(screenshot_path)
                logger.info(f"Saved error screenshot to {screenshot_path}")
                print(f"[INFO] Captura de tela do erro salva em {screenshot_path}")
            except:
                pass
            
            return {}
    
    def _extract_property_details(self):
        """
        Extract property details from the current page.
        
        Returns:
            dict: Property details dictionary
        """
        property_details = {
            "title": "",
            "price": "",
            "address": "",
            "area": "",
            "bedrooms": "",
            "bathrooms": "",
            "description": "",
            "features": [],
            "images": []
        }
        
        try:
            # Extract title
            title_element = self.driver.find_element(By.CLASS_NAME, "property-title")
            property_details["title"] = title_element.text.strip()
            
            # Extract price
            price_element = self.driver.find_element(By.CLASS_NAME, "property-price")
            property_details["price"] = price_element.text.strip()
            
            # Extract address
            address_element = self.driver.find_element(By.CLASS_NAME, "property-address")
            property_details["address"] = address_element.text.strip()
            
            # Extract area
            area_element = self.driver.find_element(By.CSS_SELECTOR, ".property-features .area")
            property_details["area"] = area_element.text.strip()
            
            # Extract bedrooms
            bedrooms_element = self.driver.find_element(By.CSS_SELECTOR, ".property-features .bedrooms")
            property_details["bedrooms"] = bedrooms_element.text.strip()
            
            # Extract bathrooms
            bathrooms_element = self.driver.find_element(By.CSS_SELECTOR, ".property-features .bathrooms")
            property_details["bathrooms"] = bathrooms_element.text.strip()
            
            # Extract description
            description_element = self.driver.find_element(By.CLASS_NAME, "property-description")
            property_details["description"] = description_element.text.strip()
            
            # Extract features
            features_elements = self.driver.find_elements(By.CSS_SELECTOR, ".property-features-list li")
            property_details["features"] = [feature.text.strip() for feature in features_elements]
            
            # Extract images
            image_elements = self.driver.find_elements(By.CSS_SELECTOR, ".property-images img")
            property_details["images"] = [image.get_attribute("src") for image in image_elements]
            
            return property_details
        except Exception as e:
            logger.warning(f"Failed to extract some property details: {str(e)}")
            print(f"[AVISO] Falha ao extrair alguns detalhes do imóvel: {str(e)}")
            return property_details
    
    def send_whatsapp_message(self, phone, message):
        """
        Send a WhatsApp message to a lead.
        
        Args:
            phone: Phone number to send the message to
            message: Message to send
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        if not self.driver:
            logger.error("Cannot send WhatsApp message: Selenium WebDriver not set up")
            print("[ERRO] Não é possível enviar mensagem do WhatsApp: WebDriver do Selenium não configurado")
            return False
        
        try:
            logger.info(f"Sending WhatsApp message to {phone}...")
            print(f"[INFO] Enviando mensagem do WhatsApp para {phone}...")
            
            # Clean up the phone number
            clean_phone = re.sub(r"[^\d]", "", phone)
            
            # Make sure the phone number has the country code
            if len(clean_phone) == 11:  # Mobile with DDD
                clean_phone = "55" + clean_phone
            elif len(clean_phone) == 10:  # Landline with DDD
                clean_phone = "55" + clean_phone
            
            # Create the WhatsApp URL
            whatsapp_url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={urllib.parse.quote(message)}"
            
            # Navigate to the WhatsApp URL
            self.driver.get(whatsapp_url)
            
            # Wait for the page to load and the message input to be available
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[@title='Digite uma mensagem']"))
            )
            
            # Take a screenshot before sending
            screenshot_path = os.path.join(os.getcwd(), f"whatsapp_before_send_{clean_phone}.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Saved WhatsApp screenshot to {screenshot_path}")
            print(f"[INFO] Captura de tela do WhatsApp salva em {screenshot_path}")
            
            # Press Enter to send the message
            message_input = self.driver.find_element(By.XPATH, "//div[@title='Digite uma mensagem']")
            message_input.send_keys(Keys.RETURN)
            
            # Wait a bit for the message to be sent
            time.sleep(5)
            
            # Take a screenshot after sending
            screenshot_path = os.path.join(os.getcwd(), f"whatsapp_after_send_{clean_phone}.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Saved WhatsApp screenshot to {screenshot_path}")
            print(f"[INFO] Captura de tela do WhatsApp salva em {screenshot_path}")
            
            logger.info("WhatsApp message sent successfully")
            print("[INFO] Mensagem do WhatsApp enviada com sucesso")
            return True
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {str(e)}")
            print(f"[ERRO] Falha ao enviar mensagem do WhatsApp: {str(e)}")
            
            # Take a screenshot of the error
            try:
                screenshot_path = os.path.join(os.getcwd(), f"whatsapp_error_{clean_phone}.png")
                self.driver.save_screenshot(screenshot_path)
                logger.info(f"Saved WhatsApp error screenshot to {screenshot_path}")
                print(f"[INFO] Captura de tela do erro do WhatsApp salva em {screenshot_path}")
            except:
                pass
            
            return False
    
    def generate_message_template(self, lead_info, property_details):
        """
        Generate a personalized message template for a lead.
        
        Args:
            lead_info: Lead information dictionary
            property_details: Property details dictionary
            
        Returns:
            str: Personalized message template
        """
        # Get the lead's name or use a default
        name = lead_info.get("name", "Cliente")
        
        # Get the property type or use a default
        property_type = lead_info.get("property_type", "imóvel")
        
        # Get the property title or use a default
        property_title = property_details.get("title", f"o {property_type}")
        
        # Get the property price or use a default
        property_price = property_details.get("price", "")
        price_text = f" com valor de {property_price}" if property_price else ""
        
        # Get the property address or use a default
        property_address = property_details.get("address", "")
        address_text = f" localizado em {property_address}" if property_address else ""
        
        # Generate the message
        message = f"""Olá {name}, tudo bem?

Recebi seu interesse no {property_title}{price_text}{address_text}.

Gostaria de saber mais detalhes sobre o que você está procurando? Estou à disposição para ajudar na sua busca pelo imóvel ideal.

Podemos agendar uma visita ou posso enviar mais informações sobre este ou outros imóveis semelhantes.

Aguardo seu retorno!

Atenciosamente,
[Seu Nome]
[Sua Imobiliária]
[Seu Telefone]"""
        
        return message
    
    def process_leads(self, days=1, max_emails=10, headless=False):
        """
        Process leads from emails.
        
        Args:
            days: Number of days to look back for emails
            max_emails: Maximum number of emails to process
            headless: Whether to run the browser in headless mode
            
        Returns:
            bool: True if processing was successful, False otherwise
        """
        try:
            logger.info("Starting lead processing...")
            print("[INFO] Iniciando processamento de leads...")
            
            # Setup Outlook connection with timeout
            connection_success = self.setup_outlook(timeout=15)
            
            if not connection_success:
                print("\n[ERRO] Não foi possível conectar ao Outlook.")
                print("Escolha uma opção:")
                print("1. Tentar conectar novamente")
                print("2. Continuar sem Outlook (usar dados de teste)")
                print("3. Sair do programa")
                
                choice = input("Digite o número da opção desejada: ")
                
                if choice == "1":
                    print("[STATUS] Tentando conectar novamente...")
                    connection_success = self.setup_outlook(timeout=30)
                    if not connection_success:
                        print("[ERRO] Falha na segunda tentativa de conexão.")
                        return False
                elif choice == "2":
                    print("[STATUS] Continuando com dados de teste...")
                    # Use test data instead of extracting from Outlook
                    leads = self._generate_test_leads()
                elif choice == "3":
                    print("[STATUS] Saindo do programa...")
                    return False
                else:
                    print("[ERRO] Opção inválida. Saindo do programa...")
                    return False
            
            # If Outlook connection was successful, extract leads from emails
            if connection_success:
                # If the user wants to use a specific Outlook profile
                use_profile = input("Deseja usar um perfil específico do Outlook? (s/n): ")
                if use_profile.lower() == "s":
                    email = input("Digite o email do perfil: ")
                    password = input("Digite a senha do perfil: ")
                    
                    try:
                        # This is a simplified approach - in a real implementation,
                        # you would need to use a more secure method to handle credentials
                        self.outlook = win32com.client.Dispatch("Outlook.Application")
                        namespace = self.outlook.GetNamespace("MAPI")
                        namespace.Logon(email, password, False, True)
                        print("[SUCESSO] Conectado com credenciais fornecidas!")
                    except Exception as e:
                        print(f"[ERRO] Falha ao conectar com credenciais: {str(e)}")
                        return False
                
                # Extract leads from emails
                leads = self.extract_leads_from_emails(days=days, max_emails=max_emails)
                
                if not leads:
                    print("[AVISO] Nenhum lead encontrado nos emails.")
                    use_test_data = input("Deseja usar dados de teste? (s/n): ")
                    if use_test_data.lower() == "s":
                        leads = self._generate_test_leads()
                    else:
                        print("[STATUS] Saindo do programa...")
                        return False
            
            # Setup Selenium WebDriver
            selenium_success = self.setup_selenium(headless=headless)
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
                
                # Generate a personalized message
                message = self.generate_message_template(lead, property_details)
                
                # Show the message and ask for confirmation
                print("\n[MENSAGEM GERADA]:")
                print(message)
                
                send_message = input("\nDeseja enviar esta mensagem? (s/n): ")
                if send_message.lower() == "s":
                    # Check if we have a phone number
                    if lead.get("phone"):
                        # Send the WhatsApp message
                        sent = self.send_whatsapp_message(lead["phone"], message)
                        if sent:
                            print("[SUCESSO] Mensagem enviada com sucesso!")
                        else:
                            print("[ERRO] Falha ao enviar mensagem.")
                    else:
                        print("[AVISO] Não foi possível enviar a mensagem: número de telefone não encontrado.")
                else:
                    print("[INFO] Mensagem não enviada.")
                
                # Ask if the user wants to continue to the next lead
                if i < len(leads) - 1:
                    continue_processing = input("\nDeseja continuar para o próximo lead? (s/n): ")
                    if continue_processing.lower() != "s":
                        print("[STATUS] Interrompendo processamento de leads...")
                        break
            
            logger.info("Lead processing completed")
            print("\n[INFO] Processamento de leads concluído")
            return True
        except Exception as e:
            logger.error(f"Failed to process leads: {str(e)}")
            print(f"[ERRO] Falha ao processar leads: {str(e)}")
            return False
        finally:
            # Clean up resources
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
    
    def _generate_test_leads(self):
        """
        Generate test leads for testing purposes.
        
        Returns:
            list: List of test lead dictionaries
        """
        test_leads = [
            {
                "name": "João Silva",
                "email": "joao.silva@example.com",
                "phone": "(11) 98765-4321",
                "property_id": "AP123",
                "property_type": "Apartamento",
                "property_location": "São Paulo, SP",
                "message": "Estou interessado neste apartamento. Gostaria de mais informações.",
                "source": "viahouseleiloes.com.br",
                "received_date": "2023-10-24 10:30:00"
            },
            {
                "name": "Maria Oliveira",
                "email": "maria.oliveira@example.com",
                "phone": "(21) 98765-4321",
                "property_id": "CA456",
                "property_type": "Casa",
                "property_location": "Rio de Janeiro, RJ",
                "message": "Olá, gostaria de agendar uma visita a esta casa.",
                "source": "imovelweb.com.br",
                "received_date": "2023-10-23 15:45:00"
            },
            {
                "name": "Pedro Santos",
                "email": "pedro.santos@example.com",
                "phone": "(31) 98765-4321",
                "property_id": "TE789",
                "property_type": "Terreno",
                "property_location": "Belo Horizonte, MG",
                "message": "Tenho interesse neste terreno para construção.",
                "source": "vivareal.com.br",
                "received_date": "2023-10-22 09:15:00"
            }
        ]
        
        logger.info(f"Generated {len(test_leads)} test leads")
        print(f"[INFO] Gerados {len(test_leads)} leads de teste")
        return test_leads


# Apply any fixed methods to the LeadProcessor class
LeadProcessor = apply_fixed_methods(LeadProcessor)


def main():
    """Main function to run the lead processor."""
    print("\n" + "="*50)
    print("PROCESSADOR DE LEADS IMOBILIÁRIOS")
    print("="*50 + "\n")
    
    # Create an instance of the LeadProcessor
    processor = LeadProcessor()
    
    # Ask for user preferences
    days = int(input("Quantos dias de emails deseja processar? (padrão: 1): ") or "1")
    max_emails = int(input("Número máximo de emails a processar? (padrão: 10): ") or "10")
    headless = input("Executar navegador em modo invisível? (s/n, padrão: n): ").lower() == "s"
    
    # Process leads
    processor.process_leads(days=days, max_emails=max_emails, headless=headless)
    
    print("\n" + "="*50)
    print("PROCESSAMENTO CONCLUÍDO")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()