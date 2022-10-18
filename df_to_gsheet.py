import httplib2
import googleapiclient.discovery


from oauth2client.service_account import ServiceAccountCredentials


# Имя файла с закрытым ключом
CREDENTIALS_FILE = 'creds.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', [
                                                               'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
# Выбираем рабЛимит в объявлении оту с таблицами и 4 версию API
service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)

def df_to_gsheet(df, spreadsheetId):
    service.spreadsheets().values().clear( spreadsheetId=spreadsheetId, range='Sheet1!A1:BG15000').execute()

    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": "Sheet1!B1:BG15000",
                 "majorDimension": "ROWS",
                  "values":
                  [[str(i) for i in df.columns.tolist()]]
                  },
                  {"range": "Sheet1!A2:BG15000",
                 "majorDimension": "COLUMNS",
                  "values":
                  [[str(i) for i in df.index.tolist()]]
                  },
                  {"range": "Sheet1!B2:BG15000",
                 "majorDimension": "COLUMNS",
                  "values":
                  df.T.values.tolist()
                  }]}).execute()
