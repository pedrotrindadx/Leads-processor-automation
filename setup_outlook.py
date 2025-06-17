#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup Outlook Method

This module provides a replacement for the setup_outlook method.
"""

import logging

# Configure logging
logger = logging.getLogger("SetupOutlook")

def setup_outlook_method(self, timeout=10, email="pedro@viahouseleiloes.com.br", password="Novaearth2131*"):
    """
    Connect to the Outlook application with timeout.
    
    Args:
        timeout: Maximum time in seconds to wait for connection
        email: Email address to use for login
        password: Password to use for login
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        logger.info(f"Connecting to Outlook (timeout: {timeout}s)...")
        print(f"[STATUS] Tentando conectar ao Outlook (timeout: {timeout}s)...")
        
        # Use the outlook_connector module to connect to Outlook
        from outlook_connector import connect_to_outlook
        print("[INFO] Usando credenciais fornecidas para conectar ao Outlook...")
        success, outlook_app, error_message = connect_to_outlook(email, password)
        
        if success:
            self.outlook = outlook_app
            print("[SUCESSO] Conexão com Outlook estabelecida!")
            logger.info("Successfully connected to Outlook")
            return True
        else:
            print(f"[ERRO] Falha ao conectar ao Outlook: {error_message}")
            logger.error(f"Failed to connect to Outlook: {error_message}")
            return False
        
    except Exception as e:
        logger.error(f"Failed to connect to Outlook: {str(e)}")
        print(f"[ERRO] Falha ao conectar ao Outlook: {str(e)}")
        return False