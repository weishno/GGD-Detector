import tkinter as tk
from tkinter import ttk, messagebox
import pygetwindow as gw
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading

class WindowSelector:
    def __init__(self):
        self.selected_window = None
        self.root = tk.Tk()
        self.root.title("窗口选择器 - GGD-Detector")
        self.root.geometry("800x600")
        
        # 标题
        title_label = tk.Label(self.root, text="选择要监控的窗口", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 刷新按钮
        refresh_btn = tk.Button(self.root, text="刷新窗口列表", command=self.refresh_windows, 
                               bg="#4CAF50", fg="white", font=("Arial", 12))
        refresh_btn.pack(pady=5)
        
        # 窗口列表框
        self.listbox = tk.Listbox(self.root, font=("Arial", 11), height=15)
        self.listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-Button-1>', self.on_select)
        
        # 预览标签
        self.preview_label = tk.Label(self.root, text="双击选择窗口后会显示预览", 
                                      bg="lightgray", height=5)
        self.preview_label.pack(pady=10, padx=10, fill=tk.BOTH)
        
        # 确认按钮
        confirm_btn = tk.Button(self.root, text="确认选择", command=self.confirm_selection,
                               bg="#2196F3", fg="white", font=("Arial", 12))
        confirm_btn.pack(pady=10)
        
        self.refresh_windows()
        
    def refresh_windows(self):
        """刷新窗口列表"""
        self.listbox.delete(0, tk.END)
        self.windows = [w for w in gw.getAllWindows() if w.title.strip()]
        
        for i, window in enumerate(self.windows):
            display_text = f"[{i}] {window.title[:60}]"
            self.listbox.insert(tk.END, display_text)
    
    def on_select(self, event):
        """双击选择窗口"""
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            self.selected_window = self.windows[idx]
            self.show_preview()
    
    def show_preview(self):
        """显示窗口预览"""
        if not self.selected_window:
            return
        
        try:
            # 获取窗口截图
            screenshot = self.capture_window(self.selected_window)
            if screenshot is not None:
                # 缩放预览
                h, w = screenshot.shape[:2]
                scale = min(400 / w, 200 / h)
                preview = cv2.resize(screenshot, (int(w * scale), int(h * scale)))
                
                # 转换为 PIL 格式
                preview_rgb = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(preview_rgb)
                photo = ImageTk.PhotoImage(img_pil)
                
                self.preview_label.config(image=photo, text="")
                self.preview_label.image = photo
        except Exception as e:
            messagebox.showerror("预览错误", f"无法预览窗口: {str(e)}")
    
    def capture_window(self, window):
        """捕获窗口画面"""
        try:
            # 获取窗口坐标
            x, y, w, h = window.left, window.top, window.width, window.height
            
            if w <= 0 or h <= 0:
                return None
            
            # 使用 PIL 截图
            from PIL import ImageGrab
            screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"截图失败: {e}")
            return None
    
    def confirm_selection(self):
        """确认选择"""
        if self.selected_window:
            messagebox.showinfo("选择成功", 
                              f"已选择窗口:\n{self.selected_window.title}\n\n窗口信息已保存到 window_config.txt")
            
            # 保存窗口信息
            with open("window_config.txt", "w", encoding="utf-8") as f:
                f.write(self.selected_window.title)
            
            self.root.destroy()
        else:
            messagebox.showwarning("未选择", "请先双击选择一个窗口")
    
    def run(self):
        """运行窗口选择器"""
        self.root.mainloop()


if __name__ == "__main__":
    selector = WindowSelector()
    selector.run()