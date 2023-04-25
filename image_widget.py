import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, Canvas
from panel import *
from Draw import *

class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, create_img, import_func):
        super().__init__(master=parent)

        self.parent = parent
        self.create_img= create_img
        self.import_func = import_func
        self.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')

        self.btn_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.btn_frame.pack(expand=True)

        self.new_win = None
        self.newbtn = ctk.CTkButton(self.btn_frame, text="New File")
        self.newbtn.grid(row=0, column=0, sticky='nsew', pady=10)
        self.newbtn.bind('<Button-1>', self.info_input)

        self.openbtn = ctk.CTkButton(self.btn_frame, text="Open Image")
        self.openbtn.grid(row=1, column=0, sticky='nsew', pady=10)
        self.openbtn.bind('<Button-1>', self.open_dialog)

    def info_input(self, event):
        if self.new_win is None or not self.new_win.winfo_exists():
            self.new_win = ctk.CTkToplevel(self.parent, width=200, height=300)
            self.new_win.resizable(0, 0)
            self.new_win.focus()

            self.input_width = ctk.IntVar(value=300)
            self.input_height = ctk.IntVar(value=200)

            SliderPanel(self.new_win, "Width", self.input_width, 0, 2000)
            SliderPanel(self.new_win, "Height", self.input_height, 0, 2000)

            self.color_info = {
                'red': ctk.StringVar(value='255'),
                'green': ctk.StringVar(value='255'),
                'blue': ctk.StringVar(value='255'),
                'hex' : ctk.StringVar(value='#FFF')
            }
            ColorPanel(self.new_win, self.color_info)

            self.submit_btn = ctk.CTkButton(self.new_win, text="Create")
            self.submit_btn.pack(pady=4, padx=4)
            self.submit_btn.bind('<Button-1>', self.submit)
        else:
            self.new_win.focus()

    def submit(self, event):
        self.create_img(self.input_width.get(), self.input_height.get(), self.color_info)
        self.new_win.destroy()

    def open_dialog(self, event):
        path = filedialog.askopenfile(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.import_func(path.name)

class ImageOutput(Canvas):
    def __init__(self, parent, drawdata, colordata, resize_image, update_pos, reset_pos, update_current):
        super().__init__(master=parent, bg='#242424',
                         bd=0, highlightthickness=0,
                         relief='ridge')
        self.grid(row=0, column=1, sticky='nsew', padx=8, pady=8)

        self.drawdata = drawdata
        self.colordata = colordata
        for data in list(self.drawdata.values()) + list(self.colordata.values()):
            data.trace('w', self.select)

        self.update_current = update_current
        self.draw = DrawCanvas(self, update_current)

        self.bind('<Motion>', update_pos)
        self.bind('<Leave>', reset_pos)
        self.bind('<Configure>', resize_image)

    # create the drawing tools
    def select(self, *args):
        print(self.drawdata['style'].get())
        if self.drawdata['style'].get() == 'Brush':
            self.draw.selectOption = 'Brush'

            self.bind('<B1-Motion>', lambda event, color=self.colordata['hex'].get():
                                    self.draw.draw_circle(event, color))
            self.bind('<ButtonRelease-1>', self.draw.update_new_line)

        elif self.drawdata['style'].get() == 'Line':
            self.draw.selectOption = 'Line'

            self.bind("<Button-1>", lambda event, color=self.colordata['hex'].get(), size=self.drawdata['size'].get():
                                    self.draw.start_line(event, color, size))
            self.bind("<B1-Motion>", self.draw.draw_line)
            self.bind("<ButtonRelease-1>", self.draw.end_select)

        elif self.drawdata['style'].get() == 'Oval':
            self.draw.selectOption = 'Oval'
            self.bind("<Button-1>", lambda event, color=self.colordata['hex'].get(), size=self.drawdata['size'].get():
                                    self.draw.start_oval(event, color, size))
            self.bind("<B1-Motion>", self.draw.draw_oval)
            self.bind("<ButtonRelease-1>", self.draw.end_select)

        elif self.drawdata['style'].get() == 'Rectangle':
            self.draw.selectOption = 'Rectangle'

            self.bind("<Button-1>", lambda event, color=self.colordata['hex'].get(), size=self.drawdata['size'].get():
                                    self.draw.start_rect(event, color, size))
            self.bind("<B1-Motion>", self.draw.draw_rect)
            self.bind("<ButtonRelease-1>", self.draw.end_select)

    # def select_brush():
    #     canvas.bind("<B1-Motion>", draw_brush)
    #
    # def select_eraser():
    #     canvas.bind("<B1-Motion>", erase)
    #
    # def draw_pencil(event):
    #     x, y = event.x, event.y
    #     canvas.create_line(x, y, x+1, y+1, fill="black", width=2)
    #
    # def draw_brush(event):
    #     x, y = event.x, event.y
    #     canvas.create_oval(x, y, x+20, y+20, fill="red", outline="red")
    #
    # def erase(event):
    #     x, y = event.x, event.y
    #     canvas.create_rectangle(x-10, y-10, x+10, y+10, fill="white", outline="white")
    #
    #     self.bind('<B1-Motion>', self.draw_circle)
    #     self.bind('<ButtonRelease-1>',self.draw.update_new_line)
    #
    # def action
    #
    def drawcircle(self, event):
        self.draw.draw_circle(event)
        self.update_current()

    def updatenewline(self, event):
        self.draw.update_new_line(event)
        self.update_current()

class CloseOutput(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(master=parent,
                         command=close_func,
                         text='x', text_color='#FFF',
                         fg_color='transparent',
                         width=40, height=40,
                         corner_radius=0, hover_color='#D43422')
        self.place(relx=0.99, rely=0.01, anchor='ne')

class StateBar(ctk.CTkFrame):
    def __init__(self, parent, vardata):
        super().__init__(master=parent, fg_color='transparent')
        self.grid(row=1, column=1, sticky='nsew')

        self.vardata = vardata
        for var in self.vardata.values():
            var.trace('w', self.update_label)

        self.label1 = ctk.CTkLabel(self, text=self.vardata['pos'].get())
        self.label2 = ctk.CTkLabel(self, text=self.vardata['dim'].get())

        self.label1.pack(side=tk.LEFT, padx=6)
        self.label2.pack(side=tk.RIGHT, padx=6)

    def update_label(self, *args):
        self.label1.configure(text=self.vardata['pos'].get())
        self.label2.configure(text=self.vardata['dim'].get())