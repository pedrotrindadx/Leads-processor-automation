#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from caixa_lead_gui import LeadProcessorGUI

def main():
    """
    Main function to start the GUI application.
    """
    app = QApplication(sys.argv)
    window = LeadProcessorGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()