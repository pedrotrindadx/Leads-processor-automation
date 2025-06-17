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

# Create a logger
logger = logging.getLogger('outlook_test')

# Import the OutlookConnector directly
from outlook_connector import OutlookConnector

# Run the test
if __name__ == "__main__":
    print("Starting Outlook connection test...")
    
    # Test our new connector
    print("\n=== Testing OutlookConnector ===")
    connector = OutlookConnector()
    result = connector.setup_outlook(timeout=30)
    
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