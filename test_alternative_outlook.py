import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Import the OutlookConnector class
from alternative_outlook_connector import OutlookConnector, test_outlook_connection

# Run the test
if __name__ == "__main__":
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
    else:
        print("\nTest FAILED: Could not connect to Outlook.")
    
    print("\n=== Test completed ===")