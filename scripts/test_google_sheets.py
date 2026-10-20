"""
Test Google Sheets Connection
Run this to verify your credentials are set up correctly
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.google_sheets import GoogleSheetsSync
from app import create_app


def main():
    print("\n" + "="*60)
    print("GOOGLE SHEETS CONNECTION TEST")
    print("="*60 + "\n")
    
    # Check credentials file
    sync = GoogleSheetsSync()
    cred_path = sync.credentials_path
    
    print(f"📁 Checking credentials file...")
    print(f"   Expected location: {cred_path}")
    
    if os.path.exists(cred_path):
        print(f"   ✅ Found: credentials.json")
    else:
        print(f"   ❌ Not found: credentials.json")
        print(f"\n📝 Setup Instructions:")
        print(f"   1. Download service account key from Google Cloud Console")
        print(f"   2. Rename it to 'credentials.json'")
        print(f"   3. Place it in: {os.path.dirname(cred_path)}")
        print(f"   4. See GOOGLE_SHEETS_SETUP.md for detailed steps")
        return 1
    
    # Test connection
    print(f"\n🔌 Testing connection to Google Sheets...")
    if sync.connect():
        print(f"   ✅ Connected successfully!")
        print(f"   📊 Spreadsheet ID: {sync.SPREADSHEET_ID}")
        
        try:
            # Get spreadsheet info
            print(f"\n📋 Spreadsheet Details:")
            print(f"   Title: {sync.spreadsheet.title}")
            print(f"   URL: {sync.SPREADSHEET_URL}")
            
            # List worksheets
            worksheets = sync.spreadsheet.worksheets()
            print(f"\n📄 Existing Worksheets ({len(worksheets)}):")
            for ws in worksheets:
                print(f"   • {ws.title} ({ws.row_count} rows x {ws.col_count} cols)")
            
            print(f"\n✅ Google Sheets integration is ready!")
            print(f"\n🚀 Next Steps:")
            print(f"   1. Start the server: python run.py")
            print(f"   2. Click 'Sync with Sheets' button in the web interface")
            print(f"   3. Check your Google Sheet for synced data")
            
            return 0
            
        except Exception as e:
            print(f"   ⚠️  Connected but error reading spreadsheet: {str(e)}")
            print(f"\n💡 Possible issues:")
            print(f"   • Spreadsheet might not be shared with service account")
            print(f"   • Check the email in credentials.json → client_email")
            print(f"   • Share the sheet with that email (Editor permission)")
            return 1
    else:
        print(f"   ❌ Connection failed")
        print(f"\n💡 Common issues:")
        print(f"   • Google Sheets API not enabled in Cloud Console")
        print(f"   • Google Drive API not enabled in Cloud Console")
        print(f"   • Invalid credentials.json file")
        print(f"   • Spreadsheet not shared with service account")
        print(f"\n📝 See GOOGLE_SHEETS_SETUP.md for troubleshooting")
        return 1


if __name__ == '__main__':
    sys.exit(main())
