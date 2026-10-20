# Configuration Files

This folder contains configuration files for Axis Ops Tracker.

## Required Files

### credentials.json (REQUIRED for Google Sheets)

This file contains your Google Service Account credentials for syncing data with Google Sheets.

**Setup:**
1. Follow the instructions in `GOOGLE_SHEETS_SETUP.md`
2. Download the service account JSON key from Google Cloud Console
3. Rename it to `credentials.json`
4. Place it in this folder

**File should look like:**
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

## Security Notes

⚠️ **NEVER commit credentials.json to Git!**

This folder is configured in `.gitignore` to prevent accidental commits.

## File Locations

```
config/
├── credentials.json          ← Your service account key (create this)
├── credentials.example.json  ← Example template
└── README.md                ← This file
```

## Testing

To test if your credentials are working:

```powershell
.\venv\Scripts\python.exe scripts\test_google_sheets.py
```

## Troubleshooting

If you're having issues:

1. **File not found**: Check the file is named exactly `credentials.json`
2. **Permission denied**: Share your Google Sheet with the email in `client_email`
3. **API not enabled**: Enable Google Sheets API and Google Drive API in Cloud Console
4. **Invalid format**: Compare your file with `credentials.example.json`

For detailed help, see `GOOGLE_SHEETS_SETUP.md` in the project root.
