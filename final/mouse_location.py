import pyautogui
import time

print("Nhấn Ctrl+C để dừng...\n")
try:
    while True:
        x, y = pyautogui.position()
        print(f"Tọa độ chuột: ({x}, {y})", end='\r')  # Ghi đè dòng cũ
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nĐã dừng.")
