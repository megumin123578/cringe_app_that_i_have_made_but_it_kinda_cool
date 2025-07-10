import pandas as pd
import numpy as np
import random
import os
import gspread
from google.oauth2.service_account import Credentials
from module5 import auto_concat, find_first_vid
from datetime import datetime
from update_sheet import excel_to_sheet
import os


EXCEL_FILE = 'Auto_edit_vids.xlsx'
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
CREDS_FILE = "sheet.json"  
SHEET_NAME = 'Auto_edit_vids'  
OUTPUT_DIR = 'D:\script\output'
MAX_AGE_SECONDS = 137 * 24 * 60 * 60  # Chỉ chọn video cũ hơn 137 ngày

############ UPDATE EXCEL DATA #############
def clear_excel_file(excel_file):
    try:
        columns = ['stt', 'file_path', 'duration', 'lastest_used_value', 'first vids', 
                   'desired length', 'output directory', 'number_of_vids', 'status']
        empty_df = pd.DataFrame(columns=columns)
        

        empty_df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"Cleared existing content in Excel file: {excel_file}")
    except Exception as e:
        print(f"Error clearing Excel file '{excel_file}': {e}")

def copy_from_ggsheet_to_excel(gspread_client, sheet_name, excel_file):
    try:

        spreadsheet = gspread_client.open(sheet_name)
        worksheet = spreadsheet.sheet1

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

############ PREPROCESS DATA #############

def pre_process_data(file):
    df = pd.read_excel(file)
    filtered_df = df[
        df['first vids'].notna() &
        df['desired length'].notna() &
        df['status'].str.lower().eq('auto')
    ]
    return filtered_df, df

def convert_time_to_seconds(time_str):
    try:
        if isinstance(time_str, (int, float)):
            return float(time_str)
        parts = time_str.strip().split(':')
        parts = [int(p) for p in parts]
        if len(parts) == 3:
            return parts[0] * 3600 + parts[1] * 60 + parts[2]
        elif len(parts) == 2:
            return parts[0] * 60 + parts[1]
        elif len(parts) == 1:
            return int(parts[0])
        else:
            return 0
    except:
        return 0

def prepare_original_data(original_df):
    durations = np.array([convert_time_to_seconds(d) for d in original_df['duration']])
    last_used = np.array([convert_time_to_seconds(t) for t in original_df['lastest_used_value']])
    file_paths = original_df['file_path'].tolist()
    return durations, last_used, file_paths

def generate_video_lists(suitable_df, original_df, durations, last_used, file_paths):
    results = []

    for i in range(len(suitable_df)):
        num_lists = int(suitable_df.iloc[i]['number_of_vids'])
        desired_length = float(suitable_df.iloc[i]['desired length']) * 60

        first_vid_number = int(suitable_df.iloc[i]['first vids'])

        first_vd = find_first_vid(first_vid_number)
        first_path, first_duration = first_vd[0], convert_time_to_seconds(first_vd[1])
        if not first_path:
            print(f"Không tìm thấy video đầu tiên cho {first_vid_number}")
            continue

        for list_index in range(num_lists):
            available_indexes = [
                idx for idx in range(len(original_df))
                if last_used[idx] >= MAX_AGE_SECONDS
            ]

            total_duration = first_duration
            selected_indexes = []
            selected_paths = [first_path]  # bắt đầu bằng path từ find_first_vid

            while available_indexes and total_duration < desired_length:
                chosen_index = random.choice(available_indexes)
                total_duration += durations[chosen_index]
                selected_indexes.append(chosen_index)
                selected_paths.append(file_paths[chosen_index])
                available_indexes.remove(chosen_index)

            results.append({
                'group_index': i,
                'list_number': list_index + 1,
                'selected_files': selected_paths,
                'total_duration': total_duration
            })

    return results
def format_and_print_results(results):
    for item in results:
        minutes = int(item['total_duration']) // 60
        seconds = int(item['total_duration']) % 60
        print(f"\nList {item['list_number']}:")
        print(f"Total duration: {minutes:02}:{seconds:02}")
        print("Files:")
        for f in item['selected_files']:
            print("  ", f)
    
def main():
    #get data from sheet to excel 
    try:
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
        gc = gspread.authorize(creds)

        copy_from_ggsheet_to_excel(gc, SHEET_NAME, EXCEL_FILE)

    except Exception as e:
        print(f"Error in main execution: {e}")
    
    df = pd.read_excel(EXCEL_FILE)
    # print(df.head())


    #preprocess data --> return list of directories

    try:
        suitable_df, original_df = pre_process_data(EXCEL_FILE)
        if suitable_df.empty:
            print("Return None")
            return
        durations, last_used, file_paths = prepare_original_data(original_df)
        results = generate_video_lists(suitable_df, original_df, durations, last_used, file_paths)
        format_and_print_results(results)

    except FileNotFoundError:
        print(f"Error: File '{EXCEL_FILE}' not found.")
    except KeyError as e:
        print(f"Error: Missing column {e} in the Excel file.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


    
    ###########################concat video############################################
    for ls in results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # format: 20250707_142512
        filename = f"{timestamp}.mp4"
        output_path = os.path.join(OUTPUT_DIR, filename)  # ./output/20250707_142512.mp4
        auto_concat(ls['selected_files'], output_path)

        group_index = ls['group_index']
        row_index = suitable_df.index[group_index]  # Lấy index gốc từ suitable_df

        current_value = original_df.at[row_index, 'output directory']
        if pd.isna(current_value) or str(current_value).strip().lower() == 'nan' or current_value == "":
            original_df.at[row_index, 'output directory'] = output_path
        else:
            original_df.at[row_index, 'output directory'] = f"{current_value}\n{output_path}"[0:]
        
        original_df.at[row_index, 'status'] = 'Done'
    try:
        original_df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
        print("Saved all Excel content into Google Sheet.")
    except Exception as e:
        print(f"Error: {e}")

    #update to sheet
    excel_to_sheet()
    

if __name__ == '__main__':
    main()