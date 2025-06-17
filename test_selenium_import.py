#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script to verify Selenium imports
"""

try:
    print("Importing selenium...")
    from selenium import webdriver
    print("Importing Service...")
    from selenium.webdriver.chrome.service import Service
    print("Importing Options...")
    from selenium.webdriver.chrome.options import Options
    print("Importing By...")
    from selenium.webdriver.common.by import By
    print("Importing Keys...")
    from selenium.webdriver.common.keys import Keys
    print("Importing WebDriverWait...")
    from selenium.webdriver.support.ui import WebDriverWait
    print("Importing expected_conditions...")
    from selenium.webdriver.support import expected_conditions as EC
    print("Importing ChromeDriverManager...")
    from webdriver_manager.chrome import ChromeDriverManager
    
    print("All imports successful!")
    
    # Test creating Options object
    print("Creating Options object...")
    options = Options()
    print("Options object created successfully!")
    
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Error: {e}")