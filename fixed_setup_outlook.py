import logging

# Create a logger
logger = logging.getLogger('outlook_setup')

def setup_outlook(self, timeout=15):
    """
    Connect to the Outlook application with timeout.
    
    Args:
        timeout: Maximum time in seconds to wait for connection
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    import threading
    import queue
    import time
    
    logger.info(f"Connecting to Outlook (timeout: {timeout}s)...")
    print(f"[INFO] Conectando ao Outlook (timeout: {timeout}s)...")
    
    # Create a queue for thread-safe communication
    result_queue = queue.Queue()
    
    # Define a function to connect to Outlook in a separate thread
    def connect_to_outlook(win32com_client):
        try:
            # Initialize COM in this thread
            import pythoncom
            pythoncom.CoInitialize()
            
            # Try to connect to Outlook
            outlook_app = win32com_client.Dispatch("Outlook.Application")
            # Test the connection
            name = outlook_app.Name
            result_queue.put((True, outlook_app, name))
        except Exception as e:
            result_queue.put((False, None, str(e)))
        finally:
            # Uninitialize COM when done
            try:
                pythoncom.CoUninitialize()
            except:
                pass
    
    # Check if Outlook is running
    try:
        import subprocess
        outlook_process = subprocess.check_output('tasklist /FI "IMAGENAME eq OUTLOOK.EXE"', shell=True)
        if b"OUTLOOK.EXE" in outlook_process:
            logger.info("Outlook is running")
            print("[INFO] Outlook está em execução")
            
            # Try to connect to the running instance
            try:
                # Import win32com.client inside the function to avoid scope issues
                import win32com.client
                import pythoncom
                
                # Initialize COM
                pythoncom.CoInitialize()
                
                # Try to connect directly
                self.outlook = win32com.client.Dispatch("Outlook.Application")
                name = self.outlook.Name
                logger.info(f"Successfully connected to running Outlook ({name})")
                print(f"[SUCESSO] Conexão com Outlook estabelecida! (Aplicativo: {name})")
                
                # Uninitialize COM when done
                try:
                    pythoncom.CoUninitialize()
                except:
                    pass
                    
                return True
            except Exception as e:
                logger.warning(f"Failed to connect to running Outlook: {str(e)}")
                print(f"[AVISO] Falha ao conectar ao Outlook em execução: {str(e)}")
                # Continue with the rest of the connection attempts
        else:
            logger.info("Outlook is not running, attempting to start it")
            print("[INFO] Outlook não está em execução, tentando iniciar...")
            try:
                subprocess.Popen(["start", "outlook"], shell=True)
                time.sleep(5)  # Give Outlook time to start
            except Exception as e:
                logger.warning(f"Failed to start Outlook: {str(e)}")
                print(f"[AVISO] Falha ao iniciar Outlook: {str(e)}")
    except Exception as e:
        logger.warning(f"Failed to check if Outlook is running: {str(e)}")
        print(f"[AVISO] Falha ao verificar se Outlook está em execução: {str(e)}")
    
    # Maximum number of connection attempts
    max_attempts = 3
    attempt_count = 0
    last_error = None
    
    # Try to connect to Outlook with multiple attempts
    while attempt_count < max_attempts:
        attempt_count += 1
        print(f"[INFO] Tentativa {attempt_count} de {max_attempts}...")
        
        try:
            # Import win32com.client inside the function to avoid scope issues
            import win32com.client as win32com_client
            
            # Start the connection in a separate thread
            connection_thread = threading.Thread(target=connect_to_outlook, args=(win32com_client,))
            connection_thread.daemon = True
            connection_thread.start()
            
            # Wait for the thread to complete or timeout
            connection_thread.join(5)  # 5 second timeout for each attempt
            
            if connection_thread.is_alive():
                # Thread is still running after timeout
                print("[AVISO] Tentativa de conexão está demorando muito, abortando...")
                last_error = "Timeout na conexão COM"
                # We can't kill the thread, but we can continue
                time.sleep(1)
                continue
            
            # Get the result from the queue
            if not result_queue.empty():
                success, outlook_obj, result = result_queue.get()
                if success:
                    self.outlook = outlook_obj
                    logger.info(f"Successfully connected to Outlook ({result})")
                    print(f"[SUCESSO] Conexão com Outlook estabelecida! (Aplicativo: {result})")
                    return True
                else:
                    last_error = result
                    logger.warning(f"Connection attempt failed: {last_error}")
                    print(f"[AVISO] Falha na tentativa: {last_error}")
            else:
                last_error = "Não foi possível obter resultado da tentativa de conexão"
                logger.warning(f"Connection attempt failed: {last_error}")
                print(f"[AVISO] Falha na tentativa: {last_error}")
            
        except Exception as e:
            # Store the last error
            last_error = str(e)
            logger.warning(f"Connection attempt failed: {last_error}")
            print(f"[AVISO] Falha na tentativa: {last_error}")
        
        # Wait a bit before retrying
        print(f"[INFO] Aguardando 2 segundos antes da próxima tentativa...")
        time.sleep(2)
    
    # If we get here, the timeout was reached or max attempts were made
    logger.error(f"Outlook connection failed after {attempt_count} attempts. Last error: {last_error}")
    print(f"[ERRO] Falha na conexão com Outlook após {attempt_count} tentativas")
    print(f"[DETALHE] Último erro: {last_error}")
    
    # Try an alternative approach - direct connection to default profile
    print("\n[INFO] Tentando método alternativo de conexão...")
    try:
        # Import inside the function to avoid scope issues
        import win32com.client
        import pythoncom
        import subprocess
        import os
        
        # Make sure COM is initialized
        try:
            pythoncom.CoInitialize()
            print("[INFO] COM inicializado para métodos alternativos")
        except Exception as e:
            print(f"[AVISO] Falha ao inicializar COM: {str(e)}")
        
        # Try to connect using GetObject instead of Dispatch
        print("[TENTATIVA] Conectando usando GetObject...")
        try:
            self.outlook = win32com.client.GetObject(None, "Outlook.Application")
            print("[SUCESSO] Conexão alternativa estabelecida via GetObject!")
            logger.info("Successfully connected to Outlook via GetObject")
            return True
        except Exception as e:
            print(f"[AVISO] GetObject falhou: {str(e)}")
        
        # Try to connect directly to MAPI namespace
        print("[TENTATIVA] Conectando diretamente ao namespace MAPI...")
        try:
            mapi_namespace = win32com.client.Dispatch("MAPI.Session")
            mapi_namespace.Logon("Outlook")
            
            # If we get here, we connected successfully
            print("[SUCESSO] Conexão alternativa estabelecida via MAPI!")
            logger.info("Successfully connected to Outlook via MAPI")
            
            # Now try to get the Outlook application
            self.outlook = win32com.client.Dispatch("Outlook.Application")
            return True
        except Exception as e:
            print(f"[AVISO] MAPI falhou: {str(e)}")
        
        # Try one more approach - creating a new instance
        print("[TENTATIVA] Criando nova instância do Outlook...")
        try:
            self.outlook = win32com.client.DispatchEx("Outlook.Application")
            print("[SUCESSO] Nova instância do Outlook criada!")
            logger.info("Successfully created new Outlook instance")
            return True
        except Exception as e:
            print(f"[AVISO] Criação de nova instância falhou: {str(e)}")
        
        # Try using early binding with explicit CLSID
        print("[TENTATIVA] Conectando usando CLSID explícito...")
        try:
            # Outlook Application CLSID
            OUTLOOK_CLSID = "{0006F03A-0000-0000-C000-000000000046}"
            self.outlook = win32com.client.Dispatch(OUTLOOK_CLSID)
            print("[SUCESSO] Conexão estabelecida via CLSID!")
            logger.info("Successfully connected to Outlook via CLSID")
            return True
        except Exception as e:
            print(f"[AVISO] Conexão via CLSID falhou: {str(e)}")
        
        # Try direct shell command to start Outlook and then connect
        print("[TENTATIVA] Iniciando Outlook via shell...")
        try:
            # Kill any existing Outlook processes first
            subprocess.run(["taskkill", "/f", "/im", "OUTLOOK.EXE"], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL)
            time.sleep(2)
            
            # Start Outlook
            subprocess.Popen(["start", "outlook"], shell=True)
            print("[INFO] Comando para iniciar Outlook enviado")
            print("[INFO] Aguardando 10 segundos para o Outlook iniciar...")
            time.sleep(10)
            
            # Try to connect again
            self.outlook = win32com.client.Dispatch("Outlook.Application")
            print("[SUCESSO] Conexão estabelecida após iniciar Outlook!")
            logger.info("Successfully connected to Outlook after starting it")
            return True
        except Exception as e:
            print(f"[AVISO] Falha ao iniciar Outlook: {str(e)}")
        
        # Try using the default mail client
        print("[TENTATIVA] Conectando ao cliente de email padrão...")
        try:
            # Open the default mail client
            os.system('start outlook:')
            time.sleep(5)
            
            # Try to connect again
            self.outlook = win32com.client.Dispatch("Outlook.Application")
            print("[SUCESSO] Conexão estabelecida via cliente de email padrão!")
            logger.info("Successfully connected to default mail client")
            return True
        except Exception as e:
            print(f"[AVISO] Conexão ao cliente de email padrão falhou: {str(e)}")
        
        # All attempts failed
        logger.error("All alternative connection methods failed")
        print("[ERRO] Todos os métodos alternativos falharam")
        print("[INFO] Recomendação: Tente executar o script como administrador")
        
        # Uninitialize COM
        try:
            pythoncom.CoUninitialize()
        except:
            pass
            
        return False
    except Exception as e:
        logger.error(f"Alternative connection methods failed: {str(e)}")
        print(f"[ERRO] Métodos alternativos falharam: {str(e)}")
        
        # Uninitialize COM
        try:
            import pythoncom
            pythoncom.CoUninitialize()
        except:
            pass
            
        return False
    
    # Provide troubleshooting tips
    print("\n[DICAS DE SOLUÇÃO]:")
    print("1. Verifique se o Outlook está aberto e funcionando corretamente")
    print("2. Reinicie o Outlook e tente novamente")
    print("3. Verifique se há permissões de segurança bloqueando o acesso")
    print("4. Tente executar este script como administrador")
    print("5. Verifique se o Outlook está configurado como cliente de email padrão")
    
    return False