

import pyautogui

location = pyautogui.locateOnScreen('search_file.png', confidence=0.8)
if location:
    x, y = pyautogui.center(location) 
    print(x,y)
    pyautogui.moveTo(x,y)