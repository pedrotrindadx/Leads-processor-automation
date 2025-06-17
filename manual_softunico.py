#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Manual Softunico Email Processor

This script adds the process_manual_softunico_email method to the LeadProcessor class.
"""

def add_manual_softunico_method(lead_processor):
    """
    Add the process_manual_softunico_email method to the LeadProcessor instance.
    
    Args:
        lead_processor: An instance of the LeadProcessor class
    """
    
    def process_manual_softunico_email(self):
        """Process a manually entered Softunico email."""
        try:
            print("\n" + "=" * 60)
            print(" " * 10 + "ENTRADA MANUAL DE EMAIL SOFTUNICO")
            print("=" * 60)
            
            print("\nInsira os dados do email no formato esperado:")
            print("Exemplo: Você possui um novo lead para o imóvel (CX12345678):")
            print("Nome: João Silva E-mail: joao@example.com Telefone: 11987654321")
            print("Mensagem: Tenho interesse neste imóvel\n")
            
            # Option to use a template
            use_template = input("Deseja usar um template para facilitar? (s/n): ").strip().lower()
            
            if use_template == 's':
                property_code = input("\nCódigo do imóvel (formato CXxxxxxxxxxx): ").strip()
                name = input("Nome do cliente: ").strip()
                email = input("Email do cliente: ").strip()
                phone = input("Telefone do cliente (apenas números): ").strip()
                message = input("Mensagem (opcional): ").strip()
                
                # Create email body from template
                email_body = f"""Você possui um novo lead para o imóvel ({property_code}):
Nome: {name} E-mail: {email} Telefone: {phone}
Mensagem: {message}"""
                
                print("\n[PRÉVIA] Email gerado:")
                print("-" * 60)
                print(email_body)
                print("-" * 60)
                
                confirm = input("\nConfirma estes dados? (s/n): ").strip().lower()
                if confirm != 's':
                    print("[CANCELADO] Operação cancelada pelo usuário.")
                    return False
            else:
                # Manual entry
                print("\n[ENTRADA] Cole o conteúdo completo do email abaixo (termine com Enter em linha vazia):")
                lines = []
                while True:
                    line = input()
                    if not line:
                        break
                    lines.append(line)
                
                email_body = "\n".join(lines)
                
                if not email_body:
                    print("[CANCELADO] Nenhum conteúdo de email fornecido.")
                    return False
            
            # Process the manually entered email
            lead_info = self.extract_lead_info_from_softunico_email(email_body)
            
            if lead_info["property_code"] and lead_info["name"] and lead_info["phone"]:
                # Process the lead
                return self.process_lead(lead_info)
            else:
                print("[ERRO] Não foi possível extrair todas as informações necessárias do email.")
                print("Verifique se o formato está correto e tente novamente.")
                return False
                
        except Exception as e:
            import logging
            logger = logging.getLogger("LeadProcessor")
            logger.error(f"Error processing manual Softunico email: {str(e)}")
            print(f"[ERRO] Erro ao processar email manual da Softunico: {str(e)}")
            return False
    
    # Add the method to the LeadProcessor instance
    lead_processor.process_manual_softunico_email = process_manual_softunico_email.__get__(lead_processor)
    
    return lead_processor