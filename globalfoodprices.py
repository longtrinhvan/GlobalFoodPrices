#ĐỒ ÁN MÔN HỌC
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd 
import numpy as np
import speech_recognition as sr50tvl
from gtts import gTTS
import playsound
import os

# Thiết lập font và padding
font = ("Arial Narrow", 11)
path = "C:\\Users\\longt\\ĐỒ ÁN MÔN HỌC\\global_food_prices.csv"
str_title = "EDA MODEL - Bản phân tích dữ liệu giá lương thực thế giới"
array_replace = {"adm0_id": "ID quốc gia",
                        "adm0_name": "Quốc gia",
                        "adm1_id": "ID địa phương",
                        "adm1_name": "Tên địa phương",
                        "mkt_id": "ID thị trường",
                        "mkt_name": "Tên thị trường",
                        "cm_id": "ID mua hàng",
                        "cm_name": "Hàng đã mua",
                        "cur_id": "ID tiền tệ",
                        "cur_name": "Tên đồng tiền",
                        "pt_id": "ID loại thị trường",
                        "pt_name": "Loại thị trường",
                        "um_id": "ID phép đo",
                        "um_name": "Đơn vị",
                        "mp_month": "Tháng được ghi",
                        "mp_year": "Năm ghi",
                        "mp_price": "Giá thanh toán",
                        "mp_commoditysource": "Nguồn cung cấp thông tin"}


tvl50_FILE = "tvl50.mp3"  
tvl50_DIR = 'C:\\Users\\longt\\ĐỒ ÁN MÔN HỌC\\BÁO CÁO BUỔI 8'  

os.makedirs(tvl50_DIR, exist_ok=True)


def Lenh(): # NHẬP ÂM THANH TỪ MICROPHONE
    r = sr50tvl.Recognizer()
    with sr50tvl.Microphone() as Source:
        #hiệu chỉnh mic để chuẩn bị nói
        messagebox.showinfo("Nhắc nhở", "Hieu chinh nhieu trươc khi noi!")
        r.adjust_for_ambient_noise(Source, duration=1)
        #nhận lời nói ra lệnh từ người dùng thông qua MIc [mặc định] lưu dữ liệu âm thanh vào audio_data
        messagebox.showinfo("Cảnh báo", "Bấm OK để bắt đầu Chọn lệnh bằng tiếng Việt, trong 3s" )
        audio_data = r.record(Source, duration = 3)
        try:
            vlenh = r.recognize_google(audio_data,language="vi")
        except: 
            vlenh = "Quý vị nói gì nghe không rõ...!"
        # xuất kết quả ra  
        messagebox.showinfo("Quý vị đã nói là", format(vlenh)) 
        vText = gTTS(text=vlenh, lang = 'vi')
        #vFile = '50TVL.mp3'
        vText.save(tvl50_FILE)
        playsound.playsound(tvl50_DIR)    


def build_parent_frame(window):
    parent_frame = tk.Frame(window)
    parent_frame.pack(fill="both", expand=True)
    return parent_frame

def student_information(parent_frame):
    # Tạo frame chứa text thông tin sinh viên
    text_frame = ttk.Frame(parent_frame, borderwidth=2, relief="groove", style="My.TFrame")
    text_frame.pack(side="top", padx=10, pady=10, anchor="nw")

    text = tk.Text(text_frame, height=4, wrap="none", bg="yellow", font=font)
    text.insert("1.0", "ĐỒ ÁN: LẬP TRÌNH PYTHON PHÂN TÍCH DỮ LIỆU LƯƠNG THỰC THẾ GIỚI\n")
    text.insert("2.0", "TRƯỜNG: ĐẠI HỌC SƯ PHẠM KỸ THUẬT THÀNH PHỐ HỒ CHÍ MINH\n")
    text.insert("3.0", "SINH VIÊN: TRỊNH VĂN LONG\n")
    text.insert("4.0", "LỚP: 16110ISA\n")
    text.pack(side="left", padx=10, pady=10, anchor="nw")
    text.pack(side="top", padx=10, pady=10, anchor="nw")

    # Tạo style với thuộc tính border_radius
    style = ttk.Style()
    style.configure("My.TFrame", border_radius=10)
    
def exit_program():
    if messagebox.askyesno("Thoát", "Bạn có chắc bạn muốn thoát?"):
        window.destroy()

# Tạo frame chứa các nút nhấn
def frame_button(parent_frame):
    button_frame = tk.Frame(parent_frame)
    button_frame.pack(side="top", padx=0, anchor="nw")

    # Tạo các nút nhấn trên button_frame
    button_exit = tk.Button(button_frame, text="Thoát", font=font, fg="black", command=exit_program)
    button_exit.pack(side="left", padx=10)

    button_voice = tk.Button(button_frame, text="Trợ lý giọng nói của bạn", font=font, command = Lenh, fg="black")
    button_voice.pack(side="left", padx=10)

    button_eda = tk.Button(button_frame, text="Phân tích EDA", font=font, fg="black")
    button_eda.pack(side="left", padx=10)

def tree_view(frame, show_data, is_analysis):
    
    # Tạo một Frame để chứa Treeview
    tree_frame = ttk.Frame(frame, width=980)
    tree_frame.pack_propagate(0)
    tree_frame.pack(side="top", padx=10, pady=10, fill='both', expand=True)

    # Tạo một Treeview trong Frame
    treeview = insert_data_treeview(tree_frame, show_data, is_analysis)
    
    frame_height = treeview.winfo_reqheight()
    tree_frame.configure(height=frame_height)

    # Tạo một Frame riêng để chứa thanh Scrollbar ngang và dọc
    scrollbar_frame = ttk.Frame(frame)
    scrollbar_frame.pack(side="top", fill='both', expand=True)

    # Tạo một Scrollbar ngang cho Treeview
    xscrollbar = ttk.Scrollbar(scrollbar_frame, orient="horizontal", command=treeview.xview)
    xscrollbar.pack(side="bottom", fill="x")

    # Thiết lập Scrollbar để cuộn Treeview
    treeview.configure(xscrollcommand=xscrollbar.set)

    return treeview

def insert_data_treeview(tree_frame, show_data, is_analysis):
     # Tạo một Treeview trong Frame
    treeview = ttk.Treeview(tree_frame)
    
    treeview.configure(height = 8)
    
     # Tạo các cột trong Treeview
    treeview["columns"] = tuple(show_data.columns)

    # Đặt tên cho các cột
    for column in show_data.columns:
        treeview.column(column, width=100, anchor="w")
        treeview.heading(column, text=column, anchor="w")

    # Thêm dữ liệu vào Treeview
    for index, row in show_data.iterrows():
        treeview.insert("", index, text=index+1, values=tuple(row))

    # Thiết lập độ rộng cho cột thứ tự
    treeview.column("#0", width=60)
    if(is_analysis == 1):
        treeview.column("#1", width=150)
        treeview.configure(height=4)

    # Thiết lập tiêu đề cho cột thứ tự
    treeview.heading("#0", text="Thứ tự")

    # Sau đó hiển thị Treeview
    treeview.pack(side="top", fill="x", expand=True)
    
    return treeview;

def analysis(col):
    count = len(col) 
    null= col.isnull().sum()
    notnull = col.notnull().sum()
    phantramnull = round(null/count * 100, 2)
    result = pd.Series({"Tổng số dòng":count,"Số dòng có data":notnull,"số dòng không có data":null,"Tỷ lệ null":phantramnull})
    return result

# Tạo một cửa sổ Tkinter
window = tk.Tk()

# Thiết lập tiêu đề cho cửa sổ
window.title(str_title)

# Thiết lập kích thước cho cửa sổ
window.geometry("1000x500")
window.resizable(tk.FALSE, tk.FALSE)


# Tạo frame cha
parent_frame = build_parent_frame(window)

# Tạo frame chứa text thông tin sinh viên
student_information(parent_frame)

# Tạo frame chứa các nút nhấn
frame_button(parent_frame)

# Tạo canvas từ parent_frame
canvas = tk.Canvas(parent_frame)
canvas.pack(side='left', fill='both', expand=True)

# Tạo eda_frame trong canvas
eda_frame = ttk.Frame(canvas)
eda_frame.pack(side='left', fill='both', expand=True)

data = pd.read_csv(path, low_memory=False)

# Đổi tên cột
data = data.rename(columns = array_replace)

# Hiển thị chỉ n dòng đầu tiên
n=20
show_data = data.head(n)

# Hiển thị dữ liệu sau khi đã đổi tên cột
tree_view(eda_frame, show_data, 0)

# Phân tích data null
result_analysis = data.apply(analysis)
result_analysis_df = result_analysis.reset_index().rename(columns={'index': "Thành phần phân tích", 0: 'result'})
tree_view(eda_frame, result_analysis_df, 1)

# Xóa xử lý những cột không có giá trị
data = data.drop(columns=["Nguồn cung cấp thông tin","ID quốc gia","ID mua hàng","ID tiền tệ"],axis=1)
show_data = data.head(n)

# Hiển thị dữ liệu sau khi đã xử lý
tree_view(eda_frame, show_data, 0)

# Tạo scrollbar cho parent_frame
scrollbar = ttk.Scrollbar(parent_frame, orient='vertical', command=canvas.yview)
scrollbar.pack(side='right', fill='y')

canvas.configure(yscrollcommand=scrollbar.set)
canvas.create_window((0, 0), window=eda_frame, anchor='nw')
eda_frame.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')))

# Chạy vòng lặp chính của ứng dụng để hiển thị cửa sổ
window.mainloop()
