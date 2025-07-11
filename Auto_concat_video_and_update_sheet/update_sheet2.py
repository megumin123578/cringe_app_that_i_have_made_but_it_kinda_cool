import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def excel_to_sheet():
    df = pd.read_excel("Auto_edit_vids.xlsx", engine="openpyxl")


    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    CREDS_FILE = "sheet.json"  \

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)

    spreadsheet = gc.open("Auto_edit_vids")
    worksheet = spreadsheet.worksheet('Sheet2')  

    worksheet.clear()

    data = [df.columns.values.tolist()] + df.values.tolist()
    data = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()



    worksheet.update("A1", data)  # Ghi bắt đầu từ A1

    print("Đã ghi toàn bộ nội dung Excel vào Google Sheet - Sheet2!")
