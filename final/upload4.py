import pyautogui
import webbrowser
import time
import os
import pyperclip

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import random

EXCEL_FILE = 'temp.xlsx'
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
CREDS_FILE = "sheet.json"  
SHEET_NAME = "ver3"

def random_delay(min_sec = 0.5, max_sec = 1):
    time.sleep(random.uniform(min_sec, max_sec))

def off_set_(x, y, delta=5):
    rand_x = x + random.randint(-delta, delta)
    rand_y = y + random.randint(-delta, delta)
    pyautogui.moveTo(rand_x, rand_y, duration=random.uniform(0.2, 0.5))
    pyautogui.click()


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
        pyautogui.moveTo(choose_folder_x, choose_folder_y, duration=0.3, tween=pyautogui.easeInOutQuad) 
        pyautogui.click()
        random_delay()
        #enter folder
        pyperclip.copy(folder_dir)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")

        search_file_x, search_file_y = 926, 46
        print(f'Move to {search_file_x, search_file_y}')
        pyautogui.moveTo(search_file_x, search_file_y, duration=0.3, tween=pyautogui.easeInOutQuad)  
        pyautogui.click()
        random_delay()
        #enter filename
        pyperclip.copy(file_name)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")

        #select file
        select_x, select_y = 228,174
        print(f'Move to {select_x, select_y}')
        pyautogui.moveTo(select_x, select_y, duration=0.3, tween=pyautogui.easeInOutQuad)  
        pyautogui.click()
        random_delay()

        select_x, select_y = 786,504
        print(f'Move to {select_x, select_y}')
        pyautogui.moveTo(select_x, select_y, duration=0.3, tween=pyautogui.easeInOutQuad)  
        pyautogui.click()
        random_delay() 
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
            pyautogui.moveTo(create_button_x, create_button_y, duration=0.3, tween=pyautogui.easeInOutQuad)  # Giảm từ 1s xuống 0.3s
            pyautogui.click()
            random_delay()  

            upload_video_x, upload_video_y = 1650, 200  
            print(f"Move to ({upload_video_x}, {upload_video_y})")
            pyautogui.moveTo(upload_video_x, upload_video_y, duration=0.3, tween=pyautogui.easeInOutQuad)  
            pyautogui.click()
            random_delay()

            choose_vid_x, choose_vid_y = 960, 540
            print(f'Move to {choose_vid_x, choose_vid_y}')
            pyautogui.moveTo(choose_vid_x, choose_vid_y, duration=0.3, tween=pyautogui.easeInOutQuad)  
            pyautogui.click()
            random_delay()
            choose_file(folder, filename)


            #Final step
            # Title
            select_x, select_y = 689,407
            print(f'Move to {select_x, select_y}')
            pyautogui.moveTo(select_x, select_y, duration=0.3, tween=pyautogui.easeInOutQuad)  # Giảm từ 0.5s xuống 0.2s
            pyautogui.click()
            random_delay()
            pyperclip.copy(title)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "v")

            # description
            select_x, select_y = 688,652
            print(f'Move to {select_x, select_y}')
            pyautogui.moveTo(select_x, select_y, duration=0.3, tween=pyautogui.easeInOutQuad)  # Giảm từ 0.5s xuống 0.2s
            pyautogui.click()
            random_delay() 
            pyperclip.copy(description)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "v")
            
            #thumbnail
            num_lines = description.count('\n') + 1
            #when no change in size
            select_x, select_y = 609,754
            if num_lines < 5:
                print(f'Move to {select_x, select_y}')
                pyautogui.moveTo(select_x, select_y, duration=0.3, tween=pyautogui.easeInOutQuad) 
                pyautogui.click()
                random_delay() 
            else:
                scroll_bar_x, scroll_bar_y = 1434, 458 
                distance = (num_lines - 5)*11
                print(f'Move to {scroll_bar_x, scroll_bar_y}')
                pyautogui.moveTo(scroll_bar_x, scroll_bar_y, duration=0.3, tween=pyautogui.easeInOutQuad) 
                pyautogui.mouseDown()
                print(f'Move to {scroll_bar_x, scroll_bar_y}')
                pyautogui.moveTo(scroll_bar_x, scroll_bar_y + distance, duration=0.3, tween=pyautogui.easeInOutQuad) 
                pyautogui.mouseUp()


                print(f'Move to {select_x, select_y}')
                pyautogui.moveTo(select_x, select_y, duration=0.3, tween=pyautogui.easeInOutQuad) 
                pyautogui.click()
                random_delay() 
            
            thumb_folder, thumb_filename = split_dir(thumbnail)
            choose_file(thumb_folder, thumb_filename)


            # get to playlist
            print(f'Move to {scroll_bar_x, scroll_bar_y}')
            pyautogui.moveTo(scroll_bar_x, scroll_bar_y, duration=0.3, tween=pyautogui.easeInOutQuad) 
            pyautogui.mouseDown()
            
            time.sleep(1)
            print(f'Move to {scroll_bar_x, 1025 + distance}')
            pyautogui.moveTo(scroll_bar_x, 1025 + distance, duration=0.3, tween=pyautogui.easeInOutQuad) 
            pyautogui.mouseUp()
            
                #open playlist select
            x,y = 650,410
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
            pyautogui.click()
                #check box
            x,y = 560,480
            for _ in range(6):
                print(f'Move to {x,y}')
                time.sleep(random.uniform(1, 2))
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
                pyautogui.click()
                y+=32
                #done
            x,y = 875,820
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
            pyautogui.click()

            #set for kids
            if for_kids:
                x,y = 540,692
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
                pyautogui.click()
            else:
                x,y = 540,726
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
                pyautogui.click()

            #move to monetization
            x,y = 1385,960
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
            pyautogui.click()
            


            #use open cv to locate button for monetization
            location = pyautogui.locateOnScreen('monetization_select.png', confidence=0.8)
            center = pyautogui.center(location)
            pyautogui.click(center)  
            

            if monetization:
                location = pyautogui.locateOnScreen('on_monetization.png', confidence=0.8)     
                center = pyautogui.center(location)
                pyautogui.click(center)  
     
            else:
                location = pyautogui.locateOnScreen('off_monetization.png', confidence=0.8)     
                center = pyautogui.center(location)
                pyautogui.click(center)  
            #confirm monetization
            location = pyautogui.locateOnScreen('confirm_monetization.png', confidence=0.8)     
            center = pyautogui.center(location)
            pyautogui.click(center)  

            #move to next step
            x,y = 1390,960
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
            pyautogui.click()

            

            # if monetization:
            #     print(f'Move to {scroll_bar_x,scroll_bar_y}')
            #     pyautogui.moveTo(scroll_bar_x, scroll_bar_y, duration=0.3, tween=pyautogui.easeInOutQuad) 
            #     pyautogui.mouseDown()
                
            #     time.sleep(1)
            #     print(f'Move to {scroll_bar_x,1025 + distance}')
            #     pyautogui.moveTo(scroll_bar_x, 1025 + distance, duration=0.3, tween=pyautogui.easeInOutQuad) 
            #     pyautogui.mouseUp()

            #     x,y = 545,768
            #     print(f'Move to {x,y}')
            #     pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
            #     pyautogui.click()

            #     x,y = 1200,770
            #     print(f'Move to {x,y}')
            #     pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
            #     pyautogui.click()
            #     time.sleep(3)
            #     #next step
            #     x,y = 1385,960
            #     print(f'Move to {x,y}')
            #     pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
            #     pyautogui.click()


            if not for_kids: #nếu không cho trẻ em thì thêm endscreen
                x,y = 1345,545
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
                pyautogui.click()
                
                time.sleep(1)

                x,y = 625,385
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
                pyautogui.click()

                #modify
                x,y = 1400, 790
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad)
                pyautogui.mouseDown()
                pyautogui.moveTo(x+50, y, duration=0.3, tween=pyautogui.easeInOutQuad)
                pyautogui.mouseUp()

                x,y = 1400, 820
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad)
                pyautogui.mouseDown()
                pyautogui.moveTo(x+50, y, duration=0.3, tween=pyautogui.easeInOutQuad)
                pyautogui.mouseUp()

                #save
                x,y = 1385,230
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
                pyautogui.click()
                time.sleep(1)
                
                #next
                x,y = 1390, 960
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
                pyautogui.click()
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad) 
                pyautogui.click()



            #public stattus

            if public_status == 'Riêng tư':
                x,y = 591, 473
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad)
                pyautogui.click()

            elif public_status == 'Không công khai':
                x,y = 591, 532
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad)
                pyautogui.click()

            elif public_status == 'Công khai':
                x,y = 591,642
                print(f'Move to {x,y}')
                pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad)
                pyautogui.click()

            

            #scroll
            x,y = 1435,463
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad)
            pyautogui.mouseDown()
            print(f'Move to {x,y+300}')
            pyautogui.moveTo(x, y+300, duration=0.3, tween=pyautogui.easeInOutQuad)
            pyautogui.mouseUp()

            #schedule
            x,y = 755, 645
            print(f'Move to {x,y}') #date
            pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad)
            pyautogui.click()
            
            x,y = 695, 580
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad)
            pyautogui.click()
            pyperclip.copy(convert_date(publish_date))
            pyautogui.hotkey('ctrl','a')
            pyautogui.hotkey('ctrl','v')
            pyautogui.hotkey('enter')

            x, y = 772, 574 #hour
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad)
            pyautogui.click()
            pyperclip.copy(publish_hour)
            pyautogui.hotkey('ctrl','a')
            pyautogui.hotkey('ctrl','v')
            pyautogui.hotkey('enter')
            #Done
            x,y = 1375,960
            print(f'Move to {x,y}')
            pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeInOutQuad)
            pyautogui.click()

            #update_exxcel

        except Exception as e:
            print(f"Lỗi xảy ra: {e}")

        #update excel

        #update sheet
        
if __name__ == "__main__":
    main()