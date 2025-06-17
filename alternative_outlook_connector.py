import logging
import subprocess
import time
import os
import sys

# Create a logger
logger = logging.getLogger('outlook_alternative')

class OutlookConnector:
    """
    A class to connect to Outlook using alternative methods that don't rely on win32com.
    """
    
    def __init__(self):
        self.connected = False
        self.connection_method = None
        self.outlook_path = None
        self.outlook_version = None
    
    def connect(self, timeout=30):
        """
        Connect to Outlook using alternative methods.
        
        Args:
            timeout: Maximum time in seconds to wait for connection
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        logger.info(f"Attempting to connect to Outlook (timeout: {timeout}s)...")
        print(f"[INFO] Tentando conectar ao Outlook (timeout: {timeout}s)...")
        
        # Try different connection methods
        methods = [
            self._connect_via_command_line,
            self._connect_via_powershell,
            self._connect_via_registry,
            self._connect_via_default_mail_client
        ]
        
        for method in methods:
            try:
                if method():
                    return True
            except Exception as e:
                logger.warning(f"Method {method.__name__} failed: {str(e)}")
                print(f"[AVISO] Método {method.__name__} falhou: {str(e)}")
                continue
        
        # If we get here, all methods failed
        logger.error("All connection methods failed")
        print("[ERRO] Todos os métodos de conexão falharam")
        self._show_troubleshooting_tips()
        return False
    
    def _connect_via_command_line(self):
        """Try to connect to Outlook via command line"""
        print("[TENTATIVA] Conectando via linha de comando...")
        
        # Check if Outlook is running
        try:
            outlook_process = subprocess.check_output('tasklist /FI "IMAGENAME eq OUTLOOK.EXE"', shell=True)
            if b"OUTLOOK.EXE" in outlook_process:
                logger.info("Outlook is already running")
                print("[INFO] Outlook já está em execução")
                
                # Get process details to verify it's working
                process_details = subprocess.check_output('wmic process where name="OUTLOOK.EXE" get ExecutablePath', shell=True)
                if b"ExecutablePath" in process_details:
                    path_lines = process_details.decode('utf-8', errors='ignore').strip().split('\n')
                    if len(path_lines) > 1:
                        self.outlook_path = path_lines[1].strip()
                        logger.info(f"Outlook path: {self.outlook_path}")
                        print(f"[INFO] Caminho do Outlook: {self.outlook_path}")
                        
                        # Consider this a successful connection
                        self.connected = True
                        self.connection_method = "command_line_running"
                        return True
            
            # If Outlook is not running or we couldn't get its path, try to start it
            logger.info("Attempting to start Outlook")
            print("[INFO] Tentando iniciar o Outlook...")
            
            # Try to find Outlook in common locations
            outlook_locations = [
                r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE",
                r"C:\Program Files\Microsoft Office\Office16\OUTLOOK.EXE",
                r"C:\Program Files (x86)\Microsoft Office\Office16\OUTLOOK.EXE",
                r"C:\Program Files\Microsoft Office\Office15\OUTLOOK.EXE",
                r"C:\Program Files (x86)\Microsoft Office\Office15\OUTLOOK.EXE",
            ]
            
            for location in outlook_locations:
                if os.path.exists(location):
                    logger.info(f"Found Outlook at {location}")
                    print(f"[INFO] Outlook encontrado em {location}")
                    self.outlook_path = location
                    
                    # Start Outlook
                    subprocess.Popen([location], shell=True)
                    print("[INFO] Outlook iniciado, aguardando inicialização...")
                    time.sleep(10)  # Wait for Outlook to start
                    
                    # Check if it's running
                    outlook_process = subprocess.check_output('tasklist /FI "IMAGENAME eq OUTLOOK.EXE"', shell=True)
                    if b"OUTLOOK.EXE" in outlook_process:
                        logger.info("Successfully started Outlook")
                        print("[SUCESSO] Outlook iniciado com sucesso!")
                        self.connected = True
                        self.connection_method = "command_line_started"
                        return True
            
            # If we couldn't find Outlook in common locations, try the generic command
            subprocess.Popen(["start", "outlook"], shell=True)
            print("[INFO] Tentando iniciar Outlook com comando genérico...")
            time.sleep(10)  # Wait for Outlook to start
            
            # Check if it's running
            outlook_process = subprocess.check_output('tasklist /FI "IMAGENAME eq OUTLOOK.EXE"', shell=True)
            if b"OUTLOOK.EXE" in outlook_process:
                logger.info("Successfully started Outlook with generic command")
                print("[SUCESSO] Outlook iniciado com sucesso usando comando genérico!")
                self.connected = True
                self.connection_method = "command_line_generic"
                return True
                
        except Exception as e:
            logger.error(f"Command line connection failed: {str(e)}")
            print(f"[ERRO] Conexão via linha de comando falhou: {str(e)}")
        
        return False
    
    def _connect_via_powershell(self):
        """Try to connect to Outlook via PowerShell"""
        print("[TENTATIVA] Conectando via PowerShell...")
        
        try:
            # PowerShell command to check Outlook version
            ps_command = """
            $outlook = New-Object -ComObject Outlook.Application
            $version = $outlook.Version
            Write-Output "Outlook Version: $version"
            """
            
            # Save the command to a temporary file
            temp_ps_file = os.path.join(os.environ['TEMP'], 'check_outlook.ps1')
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
            if "Outlook Version" in result.stdout:
                version_line = [line for line in result.stdout.split('\n') if "Outlook Version" in line][0]
                self.outlook_version = version_line.split(': ')[1].strip()
                logger.info(f"Successfully connected to Outlook via PowerShell. Version: {self.outlook_version}")
                print(f"[SUCESSO] Conexão via PowerShell estabelecida! Versão: {self.outlook_version}")
                self.connected = True
                self.connection_method = "powershell"
                return True
            else:
                logger.warning(f"PowerShell connection failed: {result.stderr}")
                print(f"[AVISO] Conexão via PowerShell falhou: {result.stderr}")
        except Exception as e:
            logger.error(f"PowerShell connection failed: {str(e)}")
            print(f"[ERRO] Conexão via PowerShell falhou: {str(e)}")
        
        return False
    
    def _connect_via_registry(self):
        """Try to get Outlook information from the registry"""
        print("[TENTATIVA] Obtendo informações do Outlook via registro do Windows...")
        
        try:
            # Use reg query to find Outlook information
            reg_command = 'reg query "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Office" /s /f "outlook.exe"'
            result = subprocess.run(reg_command, shell=True, capture_output=True, text=True)
            
            if "outlook.exe" in result.stdout.lower():
                # Found Outlook in registry
                logger.info("Found Outlook information in registry")
                print("[INFO] Informações do Outlook encontradas no registro")
                
                # Try to get the path
                path_lines = [line for line in result.stdout.split('\n') if "REG_SZ" in line and "outlook.exe" in line.lower()]
                if path_lines:
                    # Extract path from registry output
                    for line in path_lines:
                        parts = line.split('REG_SZ')
                        if len(parts) > 1:
                            potential_path = parts[1].strip()
                            if os.path.exists(potential_path):
                                self.outlook_path = potential_path
                                logger.info(f"Found Outlook path in registry: {self.outlook_path}")
                                print(f"[INFO] Caminho do Outlook encontrado no registro: {self.outlook_path}")
                                
                                # Try to start Outlook using this path
                                subprocess.Popen([self.outlook_path], shell=True)
                                print("[INFO] Iniciando Outlook usando caminho do registro...")
                                time.sleep(10)  # Wait for Outlook to start
                                
                                # Check if it's running
                                outlook_process = subprocess.check_output('tasklist /FI "IMAGENAME eq OUTLOOK.EXE"', shell=True)
                                if b"OUTLOOK.EXE" in outlook_process:
                                    logger.info("Successfully started Outlook using registry path")
                                    print("[SUCESSO] Outlook iniciado com sucesso usando caminho do registro!")
                                    self.connected = True
                                    self.connection_method = "registry"
                                    return True
                
                # If we couldn't start Outlook with the registry path, at least we know it's installed
                logger.info("Outlook is installed according to registry")
                print("[INFO] Outlook está instalado de acordo com o registro")
                return False
            else:
                logger.warning("Outlook not found in registry")
                print("[AVISO] Outlook não encontrado no registro")
        except Exception as e:
            logger.error(f"Registry connection failed: {str(e)}")
            print(f"[ERRO] Conexão via registro falhou: {str(e)}")
        
        return False
    
    def _connect_via_default_mail_client(self):
        """Try to connect to Outlook as the default mail client"""
        print("[TENTATIVA] Conectando via cliente de email padrão...")
        
        try:
            # Check if Outlook is the default mail client
            reg_command = 'reg query "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\mailto\\UserChoice" /v ProgId'
            result = subprocess.run(reg_command, shell=True, capture_output=True, text=True)
            
            if "outlook" in result.stdout.lower():
                logger.info("Outlook is the default mail client")
                print("[INFO] Outlook é o cliente de email padrão")
                
                # Try to open the default mail client
                os.system('start outlook:')
                print("[INFO] Abrindo cliente de email padrão...")
                time.sleep(5)  # Wait for Outlook to start
                
                # Check if Outlook is running
                outlook_process = subprocess.check_output('tasklist /FI "IMAGENAME eq OUTLOOK.EXE"', shell=True)
                if b"OUTLOOK.EXE" in outlook_process:
                    logger.info("Successfully opened default mail client (Outlook)")
                    print("[SUCESSO] Cliente de email padrão (Outlook) aberto com sucesso!")
                    self.connected = True
                    self.connection_method = "default_mail_client"
                    return True
            else:
                logger.warning("Outlook is not the default mail client")
                print("[AVISO] Outlook não é o cliente de email padrão")
        except Exception as e:
            logger.error(f"Default mail client connection failed: {str(e)}")
            print(f"[ERRO] Conexão via cliente de email padrão falhou: {str(e)}")
        
        return False
    
    def send_email(self, to, subject, body, html=False, attachments=None):
        """
        Send an email using the command line.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            html: Whether the body is HTML
            attachments: List of file paths to attach
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not self.connected:
            logger.error("Cannot send email: Not connected to Outlook")
            print("[ERRO] Não é possível enviar email: Não conectado ao Outlook")
            return False
        
        try:
            # Create a temporary file for the email body
            temp_body_file = os.path.join(os.environ['TEMP'], 'email_body.txt')
            with open(temp_body_file, 'w', encoding='utf-8') as f:
                f.write(body)
            
            # Build the PowerShell command
            ps_command = f"""
            $outlook = New-Object -ComObject Outlook.Application
            $mail = $outlook.CreateItem(0)
            $mail.To = "{to}"
            $mail.Subject = "{subject}"
            """
            
            # Add body
            if html:
                ps_command += f'$mail.HTMLBody = Get-Content -Path "{temp_body_file}" -Raw\n'
            else:
                ps_command += f'$mail.Body = Get-Content -Path "{temp_body_file}" -Raw\n'
            
            # Add attachments
            if attachments:
                for attachment in attachments:
                    ps_command += f'$mail.Attachments.Add("{attachment}")\n'
            
            # Send the email
            ps_command += """
            $mail.Send()
            Write-Output "Email sent successfully"
            """
            
            # Save the command to a temporary file
            temp_ps_file = os.path.join(os.environ['TEMP'], 'send_email.ps1')
            with open(temp_ps_file, 'w') as f:
                f.write(ps_command)
            
            # Execute the PowerShell script
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", temp_ps_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check if the command was successful
            if "Email sent successfully" in result.stdout:
                logger.info("Email sent successfully")
                print("[SUCESSO] Email enviado com sucesso!")
                return True
            else:
                logger.error(f"Failed to send email: {result.stderr}")
                print(f"[ERRO] Falha ao enviar email: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            print(f"[ERRO] Falha ao enviar email: {str(e)}")
            return False
    
    def _show_troubleshooting_tips(self):
        """Show troubleshooting tips for Outlook connection issues"""
        print("\n[DICAS DE SOLUÇÃO]:")
        print("1. Verifique se o Outlook está instalado no sistema")
        print("2. Tente abrir o Outlook manualmente e verificar se funciona")
        print("3. Verifique se o Outlook está configurado como cliente de email padrão")
        print("4. Tente executar este script como administrador")
        print("5. Verifique se há permissões de segurança bloqueando o acesso")
        print("6. Reinicie o computador e tente novamente")
        print("7. Verifique se há atualizações pendentes do Office/Outlook")


# Test function
def test_outlook_connection():
    """Test the OutlookConnector class"""
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    print("Starting alternative Outlook connection test...")
    
    # Create an instance of the OutlookConnector
    connector = OutlookConnector()
    
    # Try to connect
    result = connector.connect(timeout=30)
    
    if result:
        print("\nTest PASSED: Successfully connected to Outlook!")
        print(f"Connection method: {connector.connection_method}")
        if connector.outlook_path:
            print(f"Outlook path: {connector.outlook_path}")
        if connector.outlook_version:
            print(f"Outlook version: {connector.outlook_version}")
        
        # Test sending an email (uncomment to test)
        # test_email = connector.send_email(
        #     to="test@example.com",
        #     subject="Test Email",
        #     body="This is a test email sent from Python.",
        #     html=False
        # )
        # if test_email:
        #     print("Email test PASSED: Successfully sent a test email")
        # else:
        #     print("Email test FAILED: Could not send a test email")
    else:
        print("\nTest FAILED: Could not connect to Outlook.")
    
    print("\n=== Test completed ===")
    return result


# Run the test if this file is executed directly
if __name__ == "__main__":
    test_outlook_connection()