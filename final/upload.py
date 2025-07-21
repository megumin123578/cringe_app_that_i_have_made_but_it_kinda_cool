import pyautogui
import webbrowser
import time
import os
import pyperclip

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

EXCEL_FILE = 'temp.xlsx'
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
CREDS_FILE = "sheet.json"  
SHEET_NAME = "ver3"

def clear_excel_file(excel_file):
    try:
        columns = ['first vids', 'desired length', 'output directory', 'number_of_vids', 'status']
        empty_df = pd.DataFrame(columns=columns)
        empty_df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"Cleared existing content in Excel file: {excel_file}")
    except Exception as e:
        print(f"Error clearing Excel file '{excel_file}': {e}")


def copy_from_ggsheet_to_excel(gspread_client, sheet_name, excel_file, idx):
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
        df['Channel'].notna() &
        df['output directory'].notna() &
        df['status'].str.lower().eq('upload')
    ]
    return filtered_df, df


# Cấu hình PyAutoGUI
pyautogui.FAILSAFE = True  # Di chuyển chuột vào góc trên bên trái để dừng chương trình
pyautogui.PAUSE = 0.2  # Giảm độ trễ giữa các thao tác từ 0.5s xuống 0.2s

def access_yt_chanel(url):
    print(f"Mở trình duyệt và truy cập: {url}")
    webbrowser.open(url)
    time.sleep(4.5)  

def split_dir(dir):
    #split_dir folder and filename
    folder = os.path.dirname(dir)
    filename = os.path.basename(dir)

    return folder, filename





def main():
    try:
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
        gc = gspread.authorize(creds)
        copy_from_ggsheet_to_excel(gc, SHEET_NAME, EXCEL_FILE, 0)

        filtered_df, full_df = pre_process_data(EXCEL_FILE)
        

    except Exception as e:
        print(f"Error in main execution: {e}")
        return

    for i, row in filtered_df.iterrows():
        title = row['Title']
        description = row['Description']
        output_dir = row['output directory']
        chanel = row['Channel']
        public = row['Public']
        thumbnail = row['Thumbnail']
        for_kids = ['For kids']
        monetization = ['Monetization']
        publish_hour = ['Publish hour']
        publish_date = ['Publish date']


        try:
            #handle chanel url
            if chanel == 'Trabal Car Toys':
                youtube_url = "https://studio.youtube.com/channel/UCZHwy4VlwtaNb3Wsl30CKmQ"
            

            access_yt_chanel(youtube_url)

            folder, filename = split_dir(output_dir) #file mp4 location



            create_button_x, create_button_y = 1650, 150 
            print(f"Move to ({create_button_x}, {create_button_y})")
            pyautogui.moveTo(create_button_x, create_button_y, duration=0.3)  # Giảm từ 1s xuống 0.3s
            pyautogui.click()
            time.sleep(0.5)  

            upload_video_x, upload_video_y = 1650, 200  
            print(f"Move to ({upload_video_x}, {upload_video_y})")
            pyautogui.moveTo(upload_video_x, upload_video_y, duration=0.2)  
            pyautogui.click()
            time.sleep(0.5)

            choose_vid_x, choose_vid_y = 960, 540
            print(f'Move to {choose_vid_x, choose_vid_y}')
            pyautogui.moveTo(choose_vid_x, choose_vid_y, duration=0.2)  
            pyautogui.click()
            time.sleep(0.5)


            ###############################CHOOSE FILE#######################################
            choose_folder_x, choose_folder_y = 693,48
            print(f'Move to {choose_folder_x, choose_folder_y}')
            pyautogui.moveTo(choose_folder_x, choose_folder_y, duration=0.2) 
            pyautogui.click()
            time.sleep(0.5)
            #enter folder
            pyperclip.copy(folder)
            pyautogui.hotkey("ctrl", "v")
            pyautogui.hotkey("enter")

            search_file_x, search_file_y = 926, 46
            print(f'Move to {search_file_x, search_file_y}')
            pyautogui.moveTo(search_file_x, search_file_y, duration=0.2)  
            pyautogui.click()
            time.sleep(0.5)
            #enter filename
            pyperclip.copy(filename)
            pyautogui.hotkey("ctrl", "v")
            pyautogui.hotkey("enter")

            #select file
            select_x, select_y = 228,174
            print(f'Move to {select_x, select_y}')
            pyautogui.moveTo(select_x, select_y, duration=0.2)  
            pyautogui.click()
            time.sleep(0.5)

            select_x, select_y = 786,504
            print(f'Move to {select_x, select_y}')
            pyautogui.moveTo(select_x, select_y, duration=0.2)  
            pyautogui.click()
            time.sleep(0.5)   
            #set delay to avoid mistake
            time.sleep(3)
            ##########################################################################
            
            #Final step
            # Title
            select_x, select_y = 689,407
            print(f'Move to {select_x, select_y}')
            pyautogui.moveTo(select_x, select_y, duration=0.2)  # Giảm từ 0.5s xuống 0.2s
            pyautogui.click()
            time.sleep(0.5) 
            pyperclip.copy(title)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "v")

            # description
            select_x, select_y = 688,652
            print(f'Move to {select_x, select_y}')
            pyautogui.moveTo(select_x, select_y, duration=0.2)  # Giảm từ 0.5s xuống 0.2s
            pyautogui.click()
            time.sleep(0.5) 
            pyperclip.copy(description)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "v")
            
            #thumbnail
            num_lines = description.count('\n') + 1
            #when no change in size
            select_x, select_y = 609,754
            if num_lines < 5:
                print(f'Move to {select_x, select_y}')
                pyautogui.moveTo(select_x, select_y, duration=0.2) 
                pyautogui.click()
                time.sleep(0.5) 
            else:
                scroll_bar_x, scroll_bar_y = 1434, 458 
                distance = (num_lines - 5)*10
                pyautogui.moveTo(scroll_bar_x, scroll_bar_y, duration=0.2) 
                pyautogui.mouseDown()
                pyautogui.moveTo(scroll_bar_x, scroll_bar_y + distance, duration=0.2) 
                pyautogui.mouseUp()


                print(f'Move to {select_x, select_y}')
                pyautogui.moveTo(select_x, select_y, duration=0.2) 
                pyautogui.click()
                time.sleep(0.5) 



        except Exception as e:
            print(f"Lỗi xảy ra: {e}")

if __name__ == "__main__":
    main()