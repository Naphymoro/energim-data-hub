function doGet(e) {
  const action = (e && e.parameter && e.parameter.action) || 'status';
  if (action === 'status') {
    return jsonOutput({status: 'ok', service: 'ENERGIM Apps Script Backend'});
  }
  if (action === 'listRuns') {
    return jsonOutput(listRuns());
  }
  return jsonOutput({error: 'Unknown action'});
}

function doPost(e) {
  const payload = JSON.parse(e.postData.contents || '{}');
  const action = payload.action || 'unknown';

  if (action === 'createRun') {
    return jsonOutput(createRun(payload));
  }

  if (action === 'registerDriveFolder') {
    return jsonOutput(registerDriveFolder(payload));
  }

  return jsonOutput({error: 'Unknown action'});
}

function jsonOutput(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function getSheet(name) {
  const ss = SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('SPREADSHEET_ID'));
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
  }
  return sheet;
}

function createRun(payload) {
  const sheet = getSheet('runs');
  const runId = 'RUN_' + Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyyMMdd_HHmmss');

  sheet.appendRow([
    runId,
    new Date(),
    payload.operator || 'unknown',
    payload.description || '',
    'created'
  ]);

  return {
    run_id: runId,
    status: 'created'
  };
}

function listRuns() {
  const sheet = getSheet('runs');
  return {
    rows: sheet.getDataRange().getValues()
  };
}

function registerDriveFolder(payload) {
  const sheet = getSheet('drive_folders');

  sheet.appendRow([
    payload.folder_id || '',
    payload.folder_name || '',
    payload.institution || '',
    payload.folder_url || '',
    new Date()
  ]);

  return {
    status: 'registered'
  };
}
