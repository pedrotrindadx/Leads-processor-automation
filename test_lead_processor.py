#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for the Lead Processor script.

This module contains tests for the lead extraction functionality.
"""

import unittest
from lead_processor import LeadProcessor

class TestLeadProcessor(unittest.TestCase):
    """Test cases for the LeadProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a LeadProcessor instance without connecting to Outlook
        self.processor = LeadProcessor.__new__(LeadProcessor)
        # Skip the __init__ method to avoid connecting to Outlook
    
    def test_extract_lead_info_from_email(self):
        """Test the extraction of lead information from an email body."""
        # Sample email body
        email_body = """
        Softunico Olá , Você possui um novo lead para o imóvel CX08787710134227SP:
        Nome: pedro guelere
        E-mail: pguelere2015@gmail.com
        Telefone: 14981057073
        """
        
        # Expected result
        expected_result = {
            "name": "Pedro Guelere",
            "phone": "14981057073",
            "property_code": "CX08787710134227SP"
        }
        
        # Call the method
        result = self.processor.extract_lead_info_from_email(email_body)
        
        # Assert the result
        self.assertEqual(result, expected_result)
    
    def test_extract_lead_info_from_email_with_different_format(self):
        """Test the extraction of lead information from an email with a different format."""
        # Sample email body with a different format
        email_body = """
        Softunico Olá , Você possui um novo lead para o imóvel CX12345678901234SP:
        Nome: MARIA SILVA SANTOS
        E-mail: maria.silva@example.com
        Telefone: 11987654321
        """
        
        # Expected result
        expected_result = {
            "name": "Maria Silva Santos",
            "phone": "11987654321",
            "property_code": "CX12345678901234SP"
        }
        
        # Call the method
        result = self.processor.extract_lead_info_from_email(email_body)
        
        # Assert the result
        self.assertEqual(result, expected_result)
    
    def test_extract_lead_info_from_email_with_missing_data(self):
        """Test the extraction of lead information from an email with missing data."""
        # Sample email body with missing data
        email_body = """
        Softunico Olá , Você possui um novo lead para o imóvel CX12345678901234SP:
        Nome: MARIA SILVA SANTOS
        E-mail: maria.silva@example.com
        """
        
        # Expected result (phone should be empty)
        expected_result = {
            "name": "Maria Silva Santos",
            "phone": "",
            "property_code": "CX12345678901234SP"
        }
        
        # Call the method
        result = self.processor.extract_lead_info_from_email(email_body)
        
        # Assert the result
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()