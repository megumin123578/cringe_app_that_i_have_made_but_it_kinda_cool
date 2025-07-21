
import os 
import pandas as pd 
import gspread
from google.oauth2.service_account import Credentials
from module import auto_concat, get_list_video, excel_to_sheet 


EXCEL_FILE = 'temp1.xlsx'
CSV_FILE = 'data_spidey.csv'
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
CREDS_FILE = "sheet.json"
SHEET_NAME = 'Auto_concat_vids_ver2'  
OUTPUT_DIR = r"D:\output_spidey"

def clear_excel_file(excel_file):
    try:
        columns = ['first vids', 'desired length', 'output directory', 'number_of_vids', 'status']
        empty_df = pd.DataFrame(columns=columns)
        empty_df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"Cleared existing content in Excel file: {excel_file}")
    except Exception as e:
        print(f"Error clearing Excel file '{excel_file}': {e}")

def copy_from_ggsheet_to_excel(gspread_client, sheet_name, excel_file,idx):
    try:
        spreadsheet = gspread_client.open(sheet_name)
        worksheet = spreadsheet.get_worksheet(idx)
        data = worksheet.get_all_values()

        if not data:
            print("Google Sheet is empty!")
            return
        
        columns = data[0]  
        values = data[1:]  
        df = pd.DataFrame(values, columns=columns)
        clear_excel_file(excel_file)
        df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"Successfully copied data from Google {sheet_name} to Excel file {excel_file}")
    except Exception as e:
        print(f"Error copying data from Google Sheet to Excel: {e}")


def pre_process_data(file):
    df = pd.read_excel(file)
    filtered_df = df[
        df['input'].notna() &
        df['status'].str.lower().eq('auto')
    ]
    return filtered_df, df




def excel_to_sheet(excel_file: str, sheet_name: str, gspread_client=None, idx=2):
    """
    Upload nội dung Excel local lên lại Google Sheet (ghi đè sheet1).
    """
    try:
        if gspread_client is None:
            creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
            gspread_client = gspread.authorize(creds)

        spreadsheet = gspread_client.open(sheet_name)
        worksheet = spreadsheet.get_worksheet(idx)

        df = pd.read_excel(excel_file)
        worksheet.clear()
        set_with_dataframe(worksheet, df, include_index=False, include_column_header=True, resize=True)
        print(f"Uploaded Excel -> Google Sheet '{sheet_name}'.")
    except Exception as e:
        print(f"excel_to_sheet error: {e}")


def main():
    results = []

    try:
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
        gc = gspread.authorize(creds)
        copy_from_ggsheet_to_excel(gc, SHEET_NAME, EXCEL_FILE,2)
    except Exception as e:
        print(f"Error in main execution: {e}")
        return

    
    try:

        suitable_df, original_df = pre_process_data(EXCEL_FILE)
        if suitable_df.empty:
            print("No suitable data found for processing (status='auto' with non-null 'input').")
            return

       
        if CSV_FILE is None:
            print("Failed to load data from CSV. Exiting.")
            return


        for i in range(len(suitable_df)):
            results = get_list_video(suitable_df[i],CSV_FILE )
        
    except Exception as e:
        print(f"Error: {e}") 

    # Bước 3: Ghép video + cập nhật Excel
    for ls in results:
        name = ls['name']
        filename = f"{name}_Spidey_ghep.mp4"
        output_path = os.path.join(OUTPUT_DIR, filename)
        auto_concat(ls['selected_files'], output_path)

        group_index = ls['group_index']
        row_index = suitable_df.index[group_index]

        current_value = original_df.at[row_index, 'output directory']
        if pd.isna(current_value) or str(current_value).strip().lower() == 'nan' or current_value == "":
            original_df.at[row_index, 'output directory'] = output_path
        else:
            original_df.at[row_index, 'output directory'] = f"{current_value}\n{output_path}"

        original_df.at[row_index, 'status'] = 'Done'
        original_df.at[row_index, 'number_of_vids'] = 1

    #Lưu file Excel & cập nhật Google Sheet
    try:
        if 'number_of_vids' in original_df.columns:
            original_df = original_df.drop(columns=['number_of_vids'])
        original_df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
        print("Saved all Excel content into Excel file")
        excel_to_sheet(EXCEL_FILE, SHEET_NAME)
        print("Updated Google Sheet.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()