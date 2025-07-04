import tkinter as tk
from tkinter import filedialog, messagebox
import os
import math
import ffmpeg
import datetime



################################ FUNCTION ######################################
def get_name(name):
    for i, char in enumerate(str(name)):
        if char == '.':
            name = str(name)[:i].replace(':','_').replace('-','_')
            return name

def simplify_ratio(width, height):
    gcd = math.gcd(width, height)
    return width // gcd, height // gcd

def aspect_ratio(width, height):
    ratio = width / height
    simplified = simplify_ratio(width, height)
    return {
        "width": width,
        "height": height,
        "ratio_decimal": round(ratio, 4),
        "ratio_simplified": f"{simplified[0]}:{simplified[1]}"
    }

def resize_video(input_file):

    temp_name = datetime.datetime.now()

    temp_file = 'temp.mp4'
    output_file = f'{get_name(temp_name)}.mp4'

    probe = ffmpeg.probe(input_file)
    video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')


    original_width = int(video_stream['width'])
    original_height = int(video_stream['height'])

    target_ratio = 4 / 5
    target_width = int(original_height * target_ratio)


    if target_width <= original_width:
        crop_width = target_width
        crop_height = original_height
        crop_x = (original_width - crop_width) // 2
        crop_y = 0
    else:

        crop_width = original_width
        crop_height = int(original_width / target_ratio)
        crop_x = 0
        crop_y = (original_height - crop_height) // 2


    top_border, bottom_border = int((original_height/100) * 20), int((original_height/100) * 20) 

    padded_height = crop_height + top_border + bottom_border

    ffmpeg.input(input_file).output(
        temp_file,
        vf=f'crop={crop_width}:{crop_height}:{crop_x}:{crop_y}',
        vcodec='libx264',
        acodec='aac'
    ).overwrite_output().run()


    ffmpeg.input(temp_file).output(
        output_file,
        vf=f'pad={crop_width}:{padded_height}:0:{top_border}:color=black',
        vcodec='libx264',
        acodec='aac'
    ).overwrite_output().run()

    #delete cropped temp file
    os.remove(temp_file)
    print(f'kich thuoc video goc: {original_width} x {original_height}')
    print(f'kich thuoc video sau crop: {crop_width} x {crop_height}')
    origin_ratio = aspect_ratio(original_width, original_height)
    result = aspect_ratio(crop_width, crop_height)
    print(f"Aspect Ratio video goc: {origin_ratio['ratio_simplified']}")
    print(f"Aspect Ratio sau crop: {result['ratio_simplified']}")


#######################################################################
class VideoProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Processing Tool")
        self.root.geometry("600x400")
        
        self.video_paths = []
        self.setup_ui()
        
    def setup_ui(self):
        # Frame chính
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")
        
        # Label tiêu đề
        tk.Label(main_frame, text="Video Processing", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Frame chọn file
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill="x", pady=10)
        
        # Entry hiển thị đường dẫn
        self.path_var = tk.StringVar()
        tk.Entry(file_frame, textvariable=self.path_var, width=50).pack(side="left", padx=(70, 5))
        
       
        tk.Button(file_frame, text="Chọn video", command=self.choose_files).pack(side="left", padx =(10,5))
        
        process_frame = tk.Frame(main_frame)
        process_frame.pack(fill="x", pady=10)
        
        tk.Label(process_frame, text="Phương thức xử lý:", font=("Arial", 10)).pack(side="left")
        
        # Biến lưu phương thức được chọn
        self.process_method = tk.StringVar(value="resize")
        
        # Radio buttons cho phương thức
        methods = [
            ("Resize", "resize"),
            ("Ghép video", "concatenate"),]
        
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
            
            messagebox.showinfo("Thành công", "Xử lý video hoàn tất!")
            self.status_text.insert(tk.END, "Xử lý hoàn tất!\n")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
            self.status_text.insert(tk.END, f"Lỗi: {str(e)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoProcessingApp(root)
    root.mainloop()