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


def convert_date(input_date):
    date_splited = input_date.split('/')

    pl_date = f'{date_splited[0]} thg {date_splited[1]}, 20{date_splited[2]}'

    return pl_date

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
pyautogui.FAILSAFE = True  
pyautogui.PAUSE = 0.2

def access_yt_chanel(url):
    print(f"Mở trình duyệt và truy cập: {url}")
    webbrowser.open(url)
    time.sleep(4.5)  

def split_dir(dir):
    #split_dir folder and filename
    folder = os.path.dirname(dir)
    filename = os.path.basename(dir)

    return folder, filename


def choose_file(folder_dir, file_name):
        ###############################CHOOSE FILE#######################################
        choose_folder_x, choose_folder_y = 693,48
        print(f'Move to {choose_folder_x, choose_folder_y}')
        pyautogui.moveTo(choose_folder_x, choose_folder_y, duration=0.3) 
        pyautogui.click()
        time.sleep(0.5)
        #enter folder
        pyperclip.copy(folder_dir)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")

        search_file_x, search_file_y = 926, 46
        print(f'Move to {search_file_x, search_file_y}')
        pyautogui.moveTo(search_file_x, search_file_y, duration=0.3)  
        pyautogui.click()
        time.sleep(0.5)
        #enter filename
        pyperclip.copy(file_name)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")

        #select file
        select_x, select_y = 228,174
        print(f'Move to {select_x, select_y}')
        pyautogui.moveTo(select_x, select_y, duration=0.3)  
        pyautogui.click()
        time.sleep(0.5)

        select_x, select_y = 786,504
        print(f'Move to {select_x, select_y}')
        pyautogui.moveTo(select_x, select_y, duration=0.3)  
        pyautogui.click()
        time.sleep(0.5)   
        #set delay to avoid mistake
        time.sleep(3)
        ##########################################################################
        


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
        public_status = row['Public']
        thumbnail = row['Thumbnail']
        for_kids = row['For kids']
        monetization = row['Monetization']
        publish_hour = row['Publish hour']
        publish_date = row['Publish date']


        print(monetization)
        print(for_kids)
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
            pyautogui.moveTo(upload_video_x, upload_video_y, duration=0.3)  
            pyautogui.click()
            time.sleep(0.5)

            choose_vid_x, choose_vid_y = 960, 540
            print(f'Move to {choose_vid_x, choose_vid_y}')
            pyautogui.moveTo(choose_vid_x, choose_vid_y, duration=0.3)  
            pyautogui.click()
            time.sleep(0.5)

            choose_file(folder, filename)


            #Final step
            # Title
            select_x, select_y = 689,407
            print(f'Move to {select_x, select_y}')
            pyautogui.moveTo(select_x, select_y, duration=0.3)  # Giảm từ 0.5s xuống 0.2s
            pyautogui.click()
            time.sleep(0.5) 
            pyperclip.copy(title)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "v")

            # description
            select_x, select_y = 688,652
            print(f'Move to {select_x, select_y}')
            pyautogui.moveTo(select_x, select_y, duration=0.3)  # Giảm từ 0.5s xuống 0.2s
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
                pyautogui.moveTo(select_x, select_y, duration=0.3) 
                pyautogui.click()
                time.sleep(0.5) 
            else:
                scroll_bar_x, scroll_bar_y = 1434, 458 
                distance = (num_lines - 5)*11
                print(f'Move to {scroll_bar_x, scroll_bar_y}')
                pyautogui.moveTo(scroll_bar_x, scroll_bar_y, duration=0.3) 
                pyautogui.mouseDown()
                print(f'Move to {scroll_bar_x, scroll_bar_y}')
                pyautogui.moveTo(scroll_bar_x, scroll_bar_y + distance, duration=0.3) 
                pyautogui.mouseUp()


                print(f'Move to {select_x, select_y}')
                pyautogui.moveTo(select_x, select_y, duration=0.3) 
                pyautogui.click()
                time.sleep(0.5) 
            
            thumb_folder, thumb_filename = split_dir(thumbnail)
            choose_file(thumb_folder, thumb_filename)


            # get to playlist
            print(f'Move to {scroll_bar_x, scroll_bar_y}')
            pyautogui.moveTo(scroll_bar_x, scroll_bar_y, duration=0.3) 
            pyautogui.mouseDown()
            
            time.sleep(1)
            print(f'Move to {scroll_bar_x, 1025 + distance}')
            pyautogui.moveTo(scroll_bar_x, 1025 + distance, duration=0.3) 
            pyautogui.mouseUp()
            
                #open playlist select
            x,y = 650,410
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3) 
            pyautogui.click()
                #check box
            x,y = 560,480
            for _ in range(6):
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()
                y+=32
                #done
            x,y = 875,820
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3) 
            pyautogui.click()

            #set for kids
            if for_kids:
                x,y = 540,692
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()
            else:
                x,y = 540,726
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()

            #move to monetization
            x,y = 1385,960
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3) 
            pyautogui.click()

            if not for_kids:
                x,y = 725,535
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()
                if monetization:
                    x,y = 560,525
                    print(f'Move to {x,y}')
                    pyautogui.moveTo(x, y, duration=0.3) 
                    pyautogui.click()
                elif monetization == False:
                    x,y = 560,570
                    print(f'Move to {x,y}')
                    pyautogui.moveTo(x, y, duration=0.3) 
                    pyautogui.click()
                x,y = 875,625
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()
            else:
                time.sleep(15)
                x,y = 700,632
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()
                if monetization:
                    x,y = 560,625
                    print(f'Move to {x,y}')
                    pyautogui.moveTo(x, y, duration=0.3) 
                    pyautogui.click()
                else:
                    x,y = 560,670
                    print(f'Move to {x,y}')
                    pyautogui.moveTo(x, y, duration=0.3) 
                    pyautogui.click()

                x,y = 870,720
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()

            x,y = 1390,960
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3) 
            pyautogui.click()

            if monetization:
                print(f'Move to {scroll_bar_x,scroll_bar_y}')
                pyautogui.moveTo(scroll_bar_x, scroll_bar_y, duration=0.3) 
                pyautogui.mouseDown()
                
                time.sleep(1)
                print(f'Move to {scroll_bar_x,1025 + distance}')
                pyautogui.moveTo(scroll_bar_x, 1025 + distance, duration=0.3) 
                pyautogui.mouseUp()

                x,y = 545,768
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()

                x,y = 1200,770
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()
                time.sleep(3)
                #next step
                x,y = 1385,960
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()

            if not for_kids: #nếu không cho trẻ em thì thêm endscreen
                x,y = 1345,545
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()
                
                time.sleep(1)

                x,y = 625,385
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()

                #modify
                x,y = 1400, 790
                pyautogui.moveTo(x, y, duration=0.3)
                pyautogui.mouseDown()
                pyautogui.moveTo(x+50, y, duration=0.3)
                pyautogui.mouseUp()

                x,y = 1400, 820
                pyautogui.moveTo(x, y, duration=0.3)
                pyautogui.mouseDown()
                pyautogui.moveTo(x+50, y, duration=0.3)
                pyautogui.mouseUp()

                #save
                x,y = 1385,230
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()
                time.sleep(1)
                
                #next
                x,y = 1390, 960
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3) 
                pyautogui.click()



            #public stattus

            if public_status == 'Riêng tư':
                x,y = 591, 473
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3)
                pyautogui.click()

            elif public_status == 'Không công khai':
                x,y = 591, 532
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3)
                pyautogui.click()

            elif public_status == 'Công khai':
                x,y = 591,642
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3)
                pyautogui.click()

            

            #scroll
            x,y = 1435,463
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3)
            pyautogui.mouseDown()
            print(f'Move to {x,y+300}')
            pyautogui.moveTo(x, y+300, duration=0.3)
            pyautogui.mouseUp()

            #schedule
            x,y = 755, 645
            print(f'Move to {x,y}') #date
            pyautogui.moveTo(x, y, duration=0.3)
            pyautogui.click()
            
            x,y = 695, 580
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3)
            pyautogui.click()
            pyperclip.copy(convert_date(publish_date))
            pyautogui.hotkey('ctrl','a')
            pyautogui.hotkey('ctrl','v')
            pyautogui.hotkey('enter')

            x, y = 772, 574 #hour
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3)
            pyautogui.click()
            pyperclip.copy(publish_hour)
            pyautogui.hotkey('ctrl','a')
            pyautogui.hotkey('ctrl','v')
            pyautogui.hotkey('enter')
            #Done
            x,y = 1375,960
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3)
            pyautogui.click()

            #update_exxcel

        except Exception as e:
            print(f"Lỗi xảy ra: {e}")

        #update sheet
        
if __name__ == "__main__":
    main()