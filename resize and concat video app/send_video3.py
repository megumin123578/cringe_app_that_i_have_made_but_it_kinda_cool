import requests
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class VideoUploadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Upload Video to n8n")
        self.root.geometry("500x300")
        
        # Webhook URL
        self.webhook_url = "http://localhost:5678/webhook-test/http://localhost:5678/webhook/from-python"
        
        # Tạo giao diện
        self.setup_ui()
        
    def setup_ui(self):
        # Frame chính
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")
        
        # Label hiển thị tiêu đề
        tk.Label(main_frame, text="Upload Video", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Frame cho chọn file
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill="x", pady=10)
        
        # Entry hiển thị đường dẫn
        self.path_var = tk.StringVar()
        path_entry = tk.Entry(file_frame, textvariable=self.path_var, width=40)
        path_entry.pack(side="left", padx=(0, 5))
        
        # Nút chọn file
        tk.Button(file_frame, text="Chọn video", command=self.choose_file).pack(side="left")
        
        # Nút gửi
        tk.Button(main_frame, text="Gửi video", command=self.upload_video, width=20).pack(pady=10)
        
        # Text area hiển thị trạng thái
        self.status_text = tk.Text(main_frame, height=5, width=50)
        self.status_text.pack(pady=10)
        
    def choose_file(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file video",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )
        if file_path:
            self.path_var.set(file_path)
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"Đã chọn: {os.path.basename(file_path)}\n")
            
    def upload_video(self):
        video_path = self.path_var.get()
        
        if not video_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn file video trước!")
            return
            
        try:
            with open(video_path, "rb") as video_file:
                files = {
                    "video": (os.path.basename(video_path), video_file, "video/mp4")
                }
                data = {
                    "title": "Tự động gửi video",
                    "description": "Gửi từ Python + tkinter"
                }
                
                self.status_text.insert(tk.END, "Đang gửi video...\n")
                self.root.update()
                
                response = requests.post(self.webhook_url, data=data, files=files)
                
                self.status_text.insert(tk.END, f"Trạng thái: {response.status_code}\n")
                self.status_text.insert(tk.END, f"Phản hồi: {response.text}\n")
                
                if response.status_code == 200:
                    messagebox.showinfo("Thành công", "Video đã được gửi thành công!")
                else:
                    messagebox.showerror("Lỗi", f"Gửi thất bại với mã: {response.status_code}")
                    
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
            self.status_text.insert(tk.END, f"Lỗi: {str(e)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoUploadApp(root)
    root.mainloop()