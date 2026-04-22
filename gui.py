import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import sys

class PDFImageExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 图片提取工具")
        self.root.geometry("600x500")
        
        # 设置窗口最小尺寸
        self.root.minsize(500, 400)

        # 变量
        self.pdf_path = tk.StringVar()
        self.output_dir = tk.StringVar(value="extracted_images")
        self.run_in_terminal = tk.BooleanVar(value=False)
        
        # UI 布局
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # PDF 文件选择
        tk.Label(main_frame, text="选择 PDF 文件:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        pdf_entry = tk.Entry(main_frame, textvariable=self.pdf_path, width=50)
        pdf_entry.grid(row=1, column=0, sticky="we", padx=(0, 10))
        tk.Button(main_frame, text="浏览...", command=self.browse_pdf).grid(row=1, column=1)

        # 输出目录选择
        tk.Label(main_frame, text="输出目录:").grid(row=2, column=0, sticky="w", pady=(15, 5))
        output_entry = tk.Entry(main_frame, textvariable=self.output_dir, width=50)
        output_entry.grid(row=3, column=0, sticky="we", padx=(0, 10))
        tk.Button(main_frame, text="浏览...", command=self.browse_output).grid(row=3, column=1)

        # 选项
        tk.Checkbutton(main_frame, text="在外部终端中运行 (可以看到彩色输出)", variable=self.run_in_terminal).grid(row=4, column=0, sticky="w", pady=5)

        # 运行按钮
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, sticky="we", pady=10)
        
        self.run_btn = tk.Button(btn_frame, text="开始提取图片", command=self.start_extraction, 
                                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), pady=8)
        self.run_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.open_dir_btn = tk.Button(btn_frame, text="打开输出目录", command=self.open_output_dir, pady=8)
        self.open_dir_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # 日志显示
        tk.Label(main_frame, text="运行日志:").grid(row=6, column=0, sticky="w")
        self.log_area = scrolledtext.ScrolledText(main_frame, height=12, wrap=tk.WORD)
        self.log_area.grid(row=7, column=0, columnspan=2, sticky="nsew")
        
        # 设置行权重，使日志区域可扩展
        main_frame.grid_rowconfigure(7, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def browse_pdf(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if filename:
            self.pdf_path.set(filename)

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            # 自动在选择的目录后拼接 extracted_images
            final_dir = os.path.join(directory, "extracted_images")
            self.output_dir.set(final_dir)

    def open_output_dir(self):
        out = self.output_dir.get()
        if os.path.exists(out):
            if os.name == 'nt':
                os.startfile(out)
            else:
                subprocess.run(['xdg-open', out])
        else:
            messagebox.showwarning("提示", "目录尚不存在，请先运行提取任务。")

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def start_extraction(self):
        pdf = self.pdf_path.get()
        out = self.output_dir.get()

        if not pdf:
            messagebox.showwarning("警告", "请先选择一个 PDF 文件！")
            return

        if not os.path.exists(pdf):
            messagebox.showerror("错误", f"找不到文件: {pdf}")
            return

        # 禁用按钮防止重复点击
        self.run_btn.config(state=tk.DISABLED, text="正在提取...")
        self.log_area.delete(1.0, tk.END)
        self.log(f"开始提取任务...")
        self.log(f"输入文件: {pdf}")
        self.log(f"输出目录: {out}")
        self.log("-" * 30)

        # 在新线程中运行，避免 GUI 卡死
        thread = threading.Thread(target=self.run_command, args=(pdf, out))
        thread.daemon = True
        thread.start()

    def run_command(self, pdf, out):
        try:
            # 构造命令
            if self.run_in_terminal.get():
                if os.name == 'nt':
                    # Windows: 使用 start cmd /k 弹出新窗口并保持
                    cmd = f'start cmd /k "{sys.executable}" pdf_image_extraction.py -i "{pdf}" -o "{out}"'
                    os.system(cmd)
                    self.root.after(0, self.log, "已在外部终端中启动。")
                    self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL, text="开始提取图片"))
                    return
                else:
                    # Linux/Mac: 尝试不同的终端模拟器 (这里简单处理)
                    self.root.after(0, self.log, "外部终端仅支持 Windows，正在回退到内置日志。")
            
            # 使用 sys.executable 确保使用相同的 Python 解释器
            cmd = [sys.executable, "pdf_image_extraction.py", "-i", pdf, "-o", out]
            
            # 运行命令并实时捕获输出
            # 在 Windows 上，命令行输出通常使用系统编码（如 GBK），直接用 utf-8 可能会崩溃
            import locale
            system_encoding = locale.getpreferredencoding()
            
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                encoding=system_encoding,
                errors='replace', # 如果个别字符还是无法解码，替换它而不是崩溃
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            for line in process.stdout:
                self.root.after(0, self.log, line.strip())

            process.wait()
            
            if process.returncode == 0:
                self.root.after(0, lambda: messagebox.showinfo("完成", "图片提取任务已成功完成！"))
            else:
                self.root.after(0, lambda: messagebox.showerror("错误", "提取过程中发生错误，请查看日志。"))

        except Exception as e:
            self.root.after(0, self.log, f"发生异常: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("异常", f"运行出错: {str(e)}"))
        
        finally:
            self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL, text="开始提取图片"))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFImageExtractorGUI(root)
    root.mainloop()
