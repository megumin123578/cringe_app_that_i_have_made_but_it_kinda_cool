import pyautogui

# Tìm vị trí của nút "Upload" trên màn hình
location = pyautogui.locateOnScreen('monetization_select.png', confidence=0.8)
if location:
    center = pyautogui.center(location)
    pyautogui.click(center)
else:
   	print("Không tìm thấy nút Upload!")
