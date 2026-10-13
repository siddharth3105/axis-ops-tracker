/**
 * Google Apps Script for Axis Ops Tracker
 * This script automates Google Sheets and integrates with the Flask API
 * 
 * SETUP INSTRUCTIONS:
 * 1. Open your Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Delete any existing code
 * 4. Paste this entire script
 * 5. Update the CONFIG section with your API URL
 * 6. Save and authorize the script
 * 7. Set up triggers from the Triggers menu (clock icon)
 */

// ============================================================================
// CONFIGURATION
// ============================================================================

const CONFIG = {
  // Your Flask API URL (update after deployment)
  API_URL: 'http://localhost:5000/api',
  
  // Sheet configuration
  EMPLOYEE_SHEET: 'Sheet1',
  
  // Column mappings (zero-indexed)
  COLUMNS: {
    EMPLOYEE_ID: 0,
    NAME: 1,
    EMAIL: 2,
    MOBILE: 3,
    SHIFT: 4,
    WEEKOFF_DAY: 5,
    SUPERVISOR: 6,
    STATUS: 7,
    IS_RESIDENT: 8,
    IS_SUPERVISOR: 9,
    SUPERVISOR_EMAIL: 10,
    WORK_SITE: 11,
    DATE_OF_JOINING: 12,
    TOTAL_DAYS_WORKED: 13,
    TOTAL_PRODUCTION: 14,
    QUALITY: 15,
    TOTAL_VIDEOS: 16,
    PAYMENT_DATES: 17,
    HOURS_PROCESSED: 18,
    LAST_PAYMENT_DATE: 19,
    TOTAL_AMOUNT: 20
  }
};

// ============================================================================
// CUSTOM MENU
// ============================================================================

/**
 * Creates custom menu when spreadsheet opens
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🔄 Axis Ops Tracker')
    .addItem('📊 Sync to Dashboard', 'syncToDashboard')
    .addItem('📥 Import from Dashboard', 'importFromDashboard')
    .addSeparator()
    .addItem('✅ Validate Data', 'validateAllData')
    .addItem('📈 Calculate Metrics', 'calculateMetrics')
    .addSeparator()
    .addItem('🔔 Setup Triggers', 'setupTriggers')
    .addItem('⚙️ Settings', 'showSettings')
    .addToUi();
}

// ============================================================================
// DATA VALIDATION
// ============================================================================

/**
 * Validates email format
 */
function isValidEmail(email) {
  if (!email) return false;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validates mobile number
 */
function isValidMobile(mobile) {
  if (!mobile) return false;
  const mobileRegex = /^[0-9]{10}$/;
  return mobileRegex.test(mobile.toString().replace(/\s/g, ''));
}

/**
 * Validates all data in the sheet
 */
function validateAllData() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.EMPLOYEE_SHEET);
  const data = sheet.getDataRange().getValues();
  const errors = [];
  
  // Start from row 2 (skip header)
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const rowNum = i + 1;
    
    // Check required fields
    if (!row[CONFIG.COLUMNS.EMPLOYEE_ID]) {
      errors.push(`Row ${rowNum}: Missing Employee ID`);
    }
    if (!row[CONFIG.COLUMNS.NAME]) {
      errors.push(`Row ${rowNum}: Missing Name`);
    }
    if (!row[CONFIG.COLUMNS.EMAIL]) {
      errors.push(`Row ${rowNum}: Missing Email`);
    } else if (!isValidEmail(row[CONFIG.COLUMNS.EMAIL])) {
      errors.push(`Row ${rowNum}: Invalid Email format`);
    }
    
    // Validate mobile if present
    if (row[CONFIG.COLUMNS.MOBILE] && !isValidMobile(row[CONFIG.COLUMNS.MOBILE])) {
      errors.push(`Row ${rowNum}: Invalid Mobile number (should be 10 digits)`);
    }
    
    // Validate status
    const validStatuses = ['Active', 'Inactive', ''];
    if (row[CONFIG.COLUMNS.STATUS] && !validStatuses.includes(row[CONFIG.COLUMNS.STATUS])) {
      errors.push(`Row ${rowNum}: Invalid Status (should be Active or Inactive)`);
    }
  }
  
  // Show results
  if (errors.length === 0) {
    SpreadsheetApp.getUi().alert('✅ Validation Complete', 'All data is valid!', SpreadsheetApp.getUi().ButtonSet.OK);
  } else {
    SpreadsheetApp.getUi().alert('⚠️ Validation Errors', errors.join('\n'), SpreadsheetApp.getUi().ButtonSet.OK);
  }
}

// ============================================================================
// DATA CALCULATIONS
// ============================================================================

/**
 * Calculate total days worked based on date of joining
 */
function calculateDaysWorked(dateOfJoining) {
  if (!dateOfJoining) return 0;
  
  const today = new Date();
  const joinDate = new Date(dateOfJoining);
  const diffTime = Math.abs(today - joinDate);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  return diffDays;
}

/**
 * Calculate and update metrics for all employees
 */
function calculateMetrics() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.EMPLOYEE_SHEET);
  const data = sheet.getDataRange().getValues();
  
  let updatedCount = 0;
  
  // Start from row 2 (skip header)
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const dateOfJoining = row[CONFIG.COLUMNS.DATE_OF_JOINING];
    
    if (dateOfJoining) {
      const daysWorked = calculateDaysWorked(dateOfJoining);
      
      // Update the cell
      const cellRow = i + 1;
      sheet.getRange(cellRow, CONFIG.COLUMNS.TOTAL_DAYS_WORKED + 1).setValue(daysWorked);
      updatedCount++;
    }
  }
  
  SpreadsheetApp.getUi().alert(
    '✅ Metrics Updated',
    `Updated ${updatedCount} employee records with calculated days worked.`,
    SpreadsheetApp.getUi().ButtonSet.OK
  );
}

// ============================================================================
// API INTEGRATION
// ============================================================================

/**
 * Sync data to Flask Dashboard
 */
function syncToDashboard() {
  const ui = SpreadsheetApp.getUi();
  const response = ui.alert(
    'Sync to Dashboard',
    'This will push all sheet data to the Flask dashboard. Continue?',
    ui.ButtonSet.YES_NO
  );
  
  if (response !== ui.Button.YES) return;
  
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.EMPLOYEE_SHEET);
    const data = sheet.getDataRange().getValues();
    const headers = data[0];
    
    // Convert to JSON
    const employees = [];
    for (let i = 1; i < data.length; i++) {
      const row = data[i];
      if (!row[CONFIG.COLUMNS.EMPLOYEE_ID]) continue;
      
      employees.push({
        employee_id: row[CONFIG.COLUMNS.EMPLOYEE_ID],
        name: row[CONFIG.COLUMNS.NAME],
        email: row[CONFIG.COLUMNS.EMAIL],
        mobile: row[CONFIG.COLUMNS.MOBILE],
        shift: row[CONFIG.COLUMNS.SHIFT],
        weekoff_day: row[CONFIG.COLUMNS.WEEKOFF_DAY],
        supervisor: row[CONFIG.COLUMNS.SUPERVISOR],
        status: row[CONFIG.COLUMNS.STATUS] || 'Active',
        is_resident: row[CONFIG.COLUMNS.IS_RESIDENT],
        is_supervisor: row[CONFIG.COLUMNS.IS_SUPERVISOR],
        supervisor_email: row[CONFIG.COLUMNS.SUPERVISOR_EMAIL],
        work_site: row[CONFIG.COLUMNS.WORK_SITE],
        date_of_joining: row[CONFIG.COLUMNS.DATE_OF_JOINING],
        total_days_worked: row[CONFIG.COLUMNS.TOTAL_DAYS_WORKED],
        total_production_hours: row[CONFIG.COLUMNS.TOTAL_PRODUCTION],
        quality_percentage: row[CONFIG.COLUMNS.QUALITY],
        total_videos: row[CONFIG.COLUMNS.TOTAL_VIDEOS],
        hours_processed: row[CONFIG.COLUMNS.HOURS_PROCESSED],
        last_payment_date: row[CONFIG.COLUMNS.LAST_PAYMENT_DATE],
        total_amount: row[CONFIG.COLUMNS.TOTAL_AMOUNT]
      });
    }
    
    // Note: Actual API call would require proper authentication
    // This is a placeholder for the structure
    Logger.log(`Prepared ${employees.length} employees for sync`);
    
    ui.alert(
      '✅ Sync Prepared',
      `Prepared ${employees.length} employee records.\n\nNote: Configure API_URL in script settings to enable actual sync.`,
      ui.ButtonSet.OK
    );
    
  } catch (error) {
    ui.alert('❌ Sync Error', error.toString(), ui.ButtonSet.OK);
  }
}

/**
 * Import data from Flask Dashboard
 */
function importFromDashboard() {
  const ui = SpreadsheetApp.getUi();
  ui.alert(
    'Import from Dashboard',
    'This feature requires API configuration.\n\nTo enable:\n1. Deploy your Flask app\n2. Update CONFIG.API_URL in the script\n3. Run this function again',
    ui.ButtonSet.OK
  );
}

// ============================================================================
// AUTOMATED TRIGGERS
// ============================================================================

/**
 * Setup automated triggers
 */
function setupTriggers() {
  // Delete existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));
  
  // Create new triggers
  
  // 1. On edit trigger - validate data on cell edit
  ScriptApp.newTrigger('onEditTrigger')
    .forSpreadsheet(SpreadsheetApp.getActive())
    .onEdit()
    .create();
  
  // 2. Daily trigger - calculate metrics daily at 2 AM
  ScriptApp.newTrigger('calculateMetrics')
    .timeBased()
    .atHour(2)
    .everyDays(1)
    .create();
  
  // 3. Hourly trigger - auto-save backup (optional)
  ScriptApp.newTrigger('createBackup')
    .timeBased()
    .everyHours(6)
    .create();
  
  SpreadsheetApp.getUi().alert(
    '✅ Triggers Setup Complete',
    'Automated triggers have been configured:\n\n' +
    '• Data validation on edit\n' +
    '• Daily metrics calculation at 2 AM\n' +
    '• Backup every 6 hours',
    SpreadsheetApp.getUi().ButtonSet.OK
  );
}

/**
 * On edit trigger - validates data on cell edit
 */
function onEditTrigger(e) {
  const sheet = e.source.getActiveSheet();
  if (sheet.getName() !== CONFIG.EMPLOYEE_SHEET) return;
  
  const range = e.range;
  const row = range.getRow();
  const col = range.getColumn();
  
  // Skip header row
  if (row === 1) return;
  
  // Validate email column
  if (col === CONFIG.COLUMNS.EMAIL + 1) {
    const email = range.getValue();
    if (email && !isValidEmail(email)) {
      range.setBackground('#ffcccc');
      SpreadsheetApp.getUi().alert('Invalid email format!');
    } else {
      range.setBackground(null);
    }
  }
  
  // Validate mobile column
  if (col === CONFIG.COLUMNS.MOBILE + 1) {
    const mobile = range.getValue();
    if (mobile && !isValidMobile(mobile)) {
      range.setBackground('#ffcccc');
      SpreadsheetApp.getUi().alert('Invalid mobile number! Should be 10 digits.');
    } else {
      range.setBackground(null);
    }
  }
  
  // Auto-calculate days worked when date of joining changes
  if (col === CONFIG.COLUMNS.DATE_OF_JOINING + 1) {
    const dateOfJoining = range.getValue();
    if (dateOfJoining) {
      const daysWorked = calculateDaysWorked(dateOfJoining);
      sheet.getRange(row, CONFIG.COLUMNS.TOTAL_DAYS_WORKED + 1).setValue(daysWorked);
    }
  }
}

// ============================================================================
// BACKUP FUNCTIONALITY
// ============================================================================

/**
 * Create backup of current sheet data
 */
function createBackup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(CONFIG.EMPLOYEE_SHEET);
  
  // Create backup sheet name with timestamp
  const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd_HHmmss');
  const backupName = `Backup_${timestamp}`;
  
  // Copy sheet
  const backup = sheet.copyTo(ss);
  backup.setName(backupName);
  
  // Move to end
  ss.moveActiveSheet(ss.getNumSheets());
  
  Logger.log(`Backup created: ${backupName}`);
}

// ============================================================================
// UTILITIES
// ============================================================================

/**
 * Show settings dialog
 */
function showSettings() {
  const html = HtmlService.createHtmlOutput(`
    <style>
      body { font-family: Arial, sans-serif; padding: 20px; }
      h2 { color: #2196F3; }
      .setting { margin: 15px 0; padding: 10px; background: #f5f5f5; border-radius: 5px; }
      .label { font-weight: bold; }
      .value { color: #666; }
    </style>
    <h2>🔧 Axis Ops Tracker Settings</h2>
    <div class="setting">
      <div class="label">API URL:</div>
      <div class="value">${CONFIG.API_URL}</div>
    </div>
    <div class="setting">
      <div class="label">Employee Sheet:</div>
      <div class="value">${CONFIG.EMPLOYEE_SHEET}</div>
    </div>
    <div class="setting">
      <div class="label">Script Version:</div>
      <div class="value">1.0.0</div>
    </div>
    <p><em>To update settings, edit the CONFIG section in the Apps Script editor.</em></p>
  `)
    .setWidth(400)
    .setHeight(300);
  
  SpreadsheetApp.getUi().showModalDialog(html, 'Settings');
}

/**
 * Export data as JSON (for debugging)
 */
function exportAsJSON() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.EMPLOYEE_SHEET);
  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  
  const json = [];
  for (let i = 1; i < data.length; i++) {
    const row = {};
    for (let j = 0; j < headers.length; j++) {
      row[headers[j]] = data[i][j];
    }
    json.push(row);
  }
  
  Logger.log(JSON.stringify(json, null, 2));
  SpreadsheetApp.getUi().alert('JSON exported to logs. View: Extensions > Apps Script > Execution log');
}

// ============================================================================
// FORMATTING
// ============================================================================

/**
 * Format the sheet with colors and styles
 */
function formatSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.EMPLOYEE_SHEET);
  
  // Format header row
  const headerRange = sheet.getRange(1, 1, 1, sheet.getLastColumn());
  headerRange.setBackground('#2196F3');
  headerRange.setFontColor('#FFFFFF');
  headerRange.setFontWeight('bold');
  headerRange.setHorizontalAlignment('center');
  
  // Freeze header row
  sheet.setFrozenRows(1);
  
  // Auto-resize columns
  for (let i = 1; i <= sheet.getLastColumn(); i++) {
    sheet.autoResizeColumn(i);
  }
  
  SpreadsheetApp.getUi().alert('✅ Sheet formatted successfully!');
}
