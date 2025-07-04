import tkinter as tk
from tkinter import filedialog, messagebox
import os
from modules_2 import *



class VideoProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Processing Tool")
        self.root.geometry("600x400")
        
        self.video_paths = []
        self.setup_ui()
        
    def setup_ui(self):
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")
        
        # Label tiêu đề
        tk.Label(main_frame, text="Video Processing", font=("Arial", 16, "bold")).pack(pady=10)
        
        
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill="x", pady=10)
        
       
        self.path_var = tk.StringVar()
        tk.Entry(file_frame, textvariable=self.path_var, width=50).pack(side="left", padx=(70, 5))
        
       
        tk.Button(file_frame, text="Chọn video", command=self.choose_files).pack(side="left", padx =(10,5))
        
        process_frame = tk.Frame(main_frame)
        process_frame.pack(fill="x", pady=10)
        
        tk.Label(process_frame, text="Phương thức:", font=("Arial", 10)).pack(side="left", padx=(100,5))
        
        #lưu phương thức
        self.process_method = tk.StringVar(value="resize")
        
        # Radio buttons cho phương thức
        methods = [
            ("Resize", "resize"),
            ("Ghép video", "concatenate"),
            ("Cả hai", "both")]

        
        for text, value in methods:
            tk.Radiobutton(process_frame, text=text, value=value, variable=self.process_method).pack(side="left", padx=5)
        
        
        tk.Button(main_frame, text="Xử lý video", command=self.process_video, width=20).pack(pady=10)
        
        
        self.status_text = tk.Text(main_frame, height=8, width=60)
        self.status_text.pack(pady=10)
        
    def choose_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Chọn file video",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )
        if file_paths:
            self.video_paths = list(file_paths)
            self.path_var.set("; ".join([os.path.basename(path) for path in self.video_paths]))
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"Đã chọn {len(self.video_paths)} video:\n" + "\n".join([os.path.basename(path) for path in self.video_paths]) + "\n")


    
                    
    def process_video(self):
        if not self.video_paths:
            messagebox.showerror("Lỗi", "Vui lòng chọn ít nhất một file video!")
            return
            
        method = self.process_method.get()
        self.status_text.insert(tk.END, f"Đã chọn phương thức: {method}\n")
        self.status_text.insert(tk.END, f"Danh sách video:\n" + "\n".join(self.video_paths) + "\n")
        
        try:
            self.status_text.insert(tk.END, "Bắt đầu xử lý video...\n")
            self.root.update()
            
            
            if method == "resize":
                for i in range(len(self.video_paths)):
                    resize_video(self.video_paths[i])
            
            elif method == "concatenate":
                concat_video(self.video_paths)
            
            elif method == "both":
                resize_video(concat_video(self.video_paths))


            
            messagebox.showinfo("Thành công", "Xử lý video hoàn tất!")
            self.status_text.insert(tk.END, "Xử lý hoàn tất!\n")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
            self.status_text.insert(tk.END, f"Lỗi: {str(e)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoProcessingApp(root)
    root.mainloop()