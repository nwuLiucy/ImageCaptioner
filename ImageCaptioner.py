import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class PhotoViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("ImageCaptioner")
        self.root.geometry("1000x600+100+100")

        # 创建左侧的图片列表区域并添加滚动条
        left_frame = tk.Frame(self.root, width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # 创建左侧的图片列表区域顶部的文件夹选择按钮，并使其居中对齐
        left_frame_top = tk.Frame(left_frame)
        left_frame_top.pack(side=tk.TOP, fill=tk.X)
        self.folder_button = tk.Button(left_frame_top, text="选择文件夹", command=self.load_images)
        self.folder_button.pack(side=tk.LEFT, padx=10, pady=10)

        # 在文件夹选择按钮右边添加一个标签和下拉框，表示窗口的显示宽度
        self.display_width_label = tk.Label(left_frame_top, text="显示宽度")
        self.display_width_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.display_width_var = tk.StringVar(value="600")
        self.display_width_options = tk.OptionMenu(left_frame_top, self.display_width_var, *[str(width) for width in range(400, 1201, 100)])
        self.display_width_options.pack(side=tk.LEFT, padx=10, pady=10)

        scrollbar = tk.Scrollbar(left_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(left_frame, width=40, height=35, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.show_selected_image)
        scrollbar.config(command=self.listbox.yview)

        # 创建右侧的图片显示区域
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.image_label = tk.Label(right_frame, text="请选择一张图片")
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # 在图片显示区域下方添加一个文字标签、一个文本输入框、一个确认按钮以及两个下拉框
        input_frame = tk.Frame(right_frame)
        input_frame.pack(fill=tk.X)
        self.label = tk.Label(input_frame, text="标注")
        self.label.pack(side=tk.LEFT, padx=10)
        self.text_input = tk.Entry(input_frame)
        self.text_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
        self.text_input.bind("<Return>", lambda event: self.add_caption_to_image(self.current_index, self.text_input.get()) if self.text_input.get().strip() != "" else None)
        self.confirm_button = tk.Button(input_frame, text="确认", command=lambda: self.add_caption_to_image(self.current_index, self.text_input.get()) if self.text_input.get().strip() != "" else None)
        self.confirm_button.pack(side=tk.LEFT, padx=10)

        # 字号标签
        self.font_size_label = tk.Label(input_frame, text="字号")
        self.font_size_label.pack(side=tk.LEFT, padx=10)

        # 字号下拉框
        self.font_size_var = tk.StringVar(value="100")
        self.font_size_options = tk.OptionMenu(input_frame, self.font_size_var, *[str(size) for size in range(20, 151, 10)])
        self.font_size_options.pack(side=tk.LEFT, padx=10)

        # 字体颜色标签
        self.font_color_label = tk.Label(input_frame, text="字体颜色")
        self.font_color_label.pack(side=tk.LEFT, padx=10)

        # 字体颜色下拉框
        self.font_color_var = tk.StringVar(value="黑色")
        self.color_options = {"黑色": "black", "红色": "red", "蓝色": "blue", "绿色": "green"}
        self.font_color_options = tk.OptionMenu(input_frame, self.font_color_var, *self.color_options.keys())
        self.font_color_options.pack(side=tk.LEFT, padx=10)
        self.font_color_options['menu'].delete(0, 'end')
        for text, color in self.color_options.items():
            def command_factory(text=text, color=color):
                return lambda: (self.font_color_var.set(text), self.font_color_options.config(foreground=color))
            self.font_color_options['menu'].add_command(label=text, command=command_factory(text, color), foreground=color)
        # 保持选中后的颜色
        self.font_color_options.config(foreground=self.color_options[self.font_color_var.get()])
        self.font_color_var.trace_add("write", lambda *args: self.font_color_options.config(foreground=self.color_options[self.font_color_var.get()]))
        
        # 创建底部的图片切换按钮区域并绑定键盘事件
        bottom_frame = tk.Frame(right_frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.prev_button = tk.Button(bottom_frame, text="上一张", command=self.show_prev_image)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True)
        
        # 在两个按钮之间添加一个描述组件
        self.shortcut_label = tk.Label(bottom_frame, text="使用快捷键 Ctrl+Left 或 Ctrl+Right 切换图片")
        self.shortcut_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.next_button = tk.Button(bottom_frame, text="下一张", command=self.show_next_image)
        self.next_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True)
        
        # 修改键盘事件绑定逻辑，同时按下Ctrl+left切换到上一张，同时按下Ctrl+right切换到下一张
        self.root.bind("<Control-Left>", lambda event: self.show_prev_image())
        self.root.bind("<Control-Right>", lambda event: self.show_next_image())

    def load_images(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.listbox.delete(0, tk.END)
            self.image_files = [file for file in os.listdir(folder_path) if file.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))]
            for file in self.image_files:
                self.listbox.insert(tk.END, file)
            self.current_folder = folder_path

    def show_selected_image(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.show_image(index)

    def show_image(self, index):
        file_path = os.path.join(self.current_folder, self.image_files[index])
        image = Image.open(file_path)
        # 根据图片的宽度和高度决定以哪个为标准进行缩放
        window_width = int(self.display_width_var.get())
        window_height = window_width * 0.75  # 假设窗口的显示高度为750
        width_ratio = window_width / float(image.size[0])
        height_ratio = window_height / float(image.size[1])
        scale_percent = min(width_ratio, height_ratio)  # 选择缩放比例较小的一方，以保证图片完整显示在窗口内
        new_width = int((float(image.size[0]) * float(scale_percent)))
        new_height = int((float(image.size[1]) * float(scale_percent)))
        image = image.resize((new_width, new_height), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        self.current_index = index
        self.listbox.selection_clear(0, tk.END)  # 清除之前的选中状态
        self.listbox.selection_set(index)  # 设置当前图片为选中状态
        self.listbox.see(index)  # 确保当前选中的图片在列表框中可见

    def show_prev_image(self):
        if hasattr(self, 'current_index') and self.current_index > 0:
            self.show_image(self.current_index - 1)
            self.text_input.delete('0', 'end')

    def show_next_image(self):
        if hasattr(self, 'current_index') and self.current_index < len(self.image_files) - 1:
            self.show_image(self.current_index + 1)
            self.text_input.delete('0', 'end')
    
    def add_caption_to_image(self, index, caption):
        font_path = 'simsun.ttc'  # 字体文件路径，确保你有这个字体文件或者替换为其他字体
        font_size = int(self.font_size_var.get()) # 根据下拉框选项确定字号大小
        font_color = self.color_options[self.font_color_var.get()] # 根据下拉框选项确定字体颜色
        line_spacing = 10 # 行间距
        # 加载原始图片
        file_path = os.path.join(self.current_folder, self.image_files[index])
        original_image = Image.open(file_path)
        image_width, image_height = original_image.size  
    
        # 加载字体并计算文字大小  
        font = ImageFont.truetype(font_path, font_size)  
        _, text_height = font.getsize(caption) 
        # 初始化变量  
        lines = []  
        current_line = ""  
        # 逐个字符检查文本，并确定何时换行  
        for char in caption:  
            proposed_line = current_line + char  
            line_width, _ = font.getsize(proposed_line)  
            
            # 如果添加新字符后超出图片宽度，则换行  
            if line_width > image_width-20:  # 左右缩进10
                lines.append(current_line)  
                current_line = char  
            else:  
                current_line = proposed_line  
                
        # 添加最后一行（如果有的话）  
        if current_line:  
            lines.append(current_line)  
    
        # 根据行数和字体高度计算图片的总高度  
        line_height = font.getsize('中')[1]  # 使用'中'字来获取行高
        text_height = len(lines) * line_height + (len(lines) - 1) * line_spacing + line_height  # 留出一些行间距     
    
        # 创建一个新的图片，高度为原图高度加上文字高度和一些间距  
        total_height = image_height + text_height  
        new_image = Image.new('RGB', (image_width, total_height), color='white')  
    
        # 将原图粘贴到新图上  
        new_image.paste(original_image, (0, 0))  
    
        # 在新图上绘制标注文字  
        draw = ImageDraw.Draw(new_image)   
        current_height = image_height  
        for line in lines:  
            line_width, line_height = font.getsize(line)    
            x = 10  # 左对齐
            y = current_height + line_height  # 垂直居中，基于当前行的基线  
            draw.text((x, y - line_height / 2), line, fill = font_color, font=font)  
            current_height += line_height + line_spacing  # 留出一些行间距   
        
        output_folder = os.path.join(self.current_folder, '标注后的图片') # 标注后的图片保存路径
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_path = os.path.join(output_folder, self.image_files[index])
        # 保存新图片  
        new_image.save(output_path)
        # 保存成功后弹窗提示
        self.text_input.delete('0', 'end') # 先清空内容，再输出提示信息
        self.text_input.insert('0', f"图片已保存至 {output_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoViewer(root)
    root.mainloop()