import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pyasn1.type.univ import Null
import requests
from time import sleep

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)


def inspect_table(number):
    try:
        sheet = client.open("Morrison#" + str(number)).sheet1
    except:
        return
    response = requests.get('http://morrison-api.herokuapp.com/api/getcourse/students/')
    json_data = json.loads(response.text)
    records = sheet.get_all_records()
    filtered_records = [d for d in json_data if d['group'] == 'Morrison#' + str(number)]
    for item in filtered_records:
        if not item['teacher']:
            continue
        row = []
        for k in item:
            if k != 'old':
                row.append(item[k] if item[k] else '')
        if not any(d['ID'] == item['id'] for d in records):
            sheet.append_row(row)
        else:
            update_record(item, filtered_records, sheet)
        sleep(2.5)
    print("Done")

def update_record(item, filtered_records, sheet):
    row = []
    for k in item:
        if k != 'old':
            row.append(item[k] if item[k] else '')
    if not any(d['ID'] == item['id'] for d in filtered_records):
        print("No such student")
    else:
        rownum = sheet.col_values(1).index(str(item["id"])) + 1
        col = 1
        for k in row:
            sheet.update_cell(rownum, col, k)
            col += 1
            sleep(0.5)

# inspect_table(48)

# for i in range(1, 40):
#     inspect_table(i)

for i in range(6, 8):
    inspect_table(i)