# Fringe API Connectors
This API package GSuite and GCP API connections into classes with simpler executions. 

## Requirements
- Oauth Credentials for GSuite services
- Service Account for GCP services

## Defaults
- scopes:
```python
scopes = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://mail.google.com/'
]
```

## Classes & Functions
### import fringe_connector.api
- `GSuite()` - authenticates using the Oauth credentials .json file
- `GSheets()`- creates service using GSuite class upon instantiation
    - `get()` - gets the values of a specified range
    - `update()` - updates a specified range with the provide set of values
    - `append()` - appends values to the end of a range
    - `getColumnNumber()` - returns numerical column number of letter column
    - `getIndexesFromRange()` - returns numerical indexes of alphanumeric range
    - `create()` - creates a new spreadsheet
- `GMail()` - creates service using GSuite class upon instantiation
    - `fetchEmails()`
    - `sendEmail()`
- `GDrive()`- creates service using GSuite class upon instantiation
    - `moveFile()`
    - `uploadFile()`
- `GSlides()` - creates service using GSuite class upon instantiation
- `BigQuery()` creates service using Service Account .json upon instantiation
    - `loadTable()` - creates table with data
    - `createTable()` - creates an empty table
    - `query()` - custom defined query. Returns results of query or loads results at the defined destination table
    - `updateSchema()` - updates schema of table
    - `getTableProperties()` - returns parsed table properties
    - `deleteTable()`
    - `copyTable()`
    - `deleteDataset()`
    - `createDataset()`
    - `getDatasetTables()`

### import fringe_web_driver
- `WebDriver()` - default instantiation with a crome web driver. Requires a chrome web driver in PATH.
    - `quit()`
    - `downloadFile()` - works with chrome web driver. Buggy with Firefox web driver. Returns the filename of the downloaded file. 
