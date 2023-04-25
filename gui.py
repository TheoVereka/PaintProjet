import customtkinter as ctk
from image_widget import *
from menu import Menu
from PIL import Image, ImageTk, ImageOps, ImageGrab

class App():
    def __init__(self):
        # Setup
        self.racine = ctk.CTk()
        ctk.set_appearance_mode('dark')
        self.racine.geometry('1000x600')
        self.racine.iconbitmap("./img/paint.ico")
        self.racine.title("Paint Emulator")
        self.racine.minsize(800, 500)
        self.init_parameters()

        # Layout
        self.racine.rowconfigure(0, weight=10, uniform='a')
        self.racine.rowconfigure(1, weight=1, uniform='a')
        self.racine.columnconfigure(0, weight=2, uniform='a')
        self.racine.columnconfigure(1, weight=6, uniform='a')

        # Widget
        self.image_import = ImageImport(self.racine, self.create_img, self.import_image)

        # Canvas variables
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        self.racine.mainloop()

    def init_parameters(self):
        self.edit_vars = {
            'rotate' : ctk.StringVar(value="None"),
            'zoom': ctk.DoubleVar(value=0),
            'flip': ctk.StringVar(value="None"),
            'clip': ctk.StringVar(value="None")
        }

        self.color_vars = {
            'red': ctk.StringVar(value='0'),
            'green': ctk.StringVar(value='0'),
            'blue': ctk.StringVar(value='0'),
            'hex': ctk.StringVar(value='#000000')
        }

        self.draw_vars = {
            'style' : ctk.StringVar(value="Brush"),
            'size' : ctk.DoubleVar(value=1)
        }

        self.state_vars = {
            'pos' : ctk.StringVar(value="0, 0"),
            'dim' : ctk.StringVar()
        }

        # Trace var changes
        for var in self.edit_vars.values():
            var.trace('w', self.manipulate_img)
        for var in self.draw_vars.values():
            var.trace('w', self.draw_img)

    def manipulate_img(self, *args):
        self.get_current_info()

        # Rotate img
        if self.edit_vars['rotate'].get() == 'Left':
            self.image = self.image.rotate(90, expand=True)
            self.image_width, self.image_height = self.image_height, self.image_width
            self.reverse_current_info()
            self.calcul_resize()
        if self.edit_vars['rotate'].get() == 'Right':
            self.image = self.image.rotate(-90, expand=True)
            self.image_width, self.image_height = self.image_height, self.image_width
            self.reverse_current_info()
            self.calcul_resize()

        # Zoom img
        self.image = ImageOps.crop(self.image, self.edit_vars['zoom'].get())

        # Flip
        if self.edit_vars['flip'].get() == 'X':
            self.image = ImageOps.mirror(self.image)
        if self.edit_vars['flip'].get() == 'Y':
            self.image = ImageOps.flip(self.image)
        if self.edit_vars['flip'].get() == 'Both':
            self.image = ImageOps.mirror(self.image)
            self.image = ImageOps.flip(self.image)

        # self.image.show()
        self.place_img()

    def update_pos(self, event):
        self.state_vars['pos'].set(f"{int(event.x * self.origin_width / self.image_width)}, {int(event.y * self.origin_height / self.image_height)}")

    def reset_pos(self, event):
        self.state_vars['pos'].set(f"0, 0")

    def get_current_info(self):
        self.origin_width = self.original.size[0]
        self.origin_height = self.original.size[1]
        self.state_vars['dim'].set(f"{self.origin_width} x {self.origin_height}")

    def reverse_current_info(self):
        self.origin_width, self.origin_height = self.origin_height, self.origin_width
        self.image_ratio = 1 / self.image_ratio
        self.state_vars['dim'].set(f"{self.origin_width} x {self.origin_height}")

    def update_current_img(self):
        # x_root = self.racine.winfo_rootx() + self.image_output.winfo_x()
        # y_root = self.racine.winfo_rooty() + self.image_output.winfo_y()
        # x_canvas = int(x_root * 1.5)
        # y_canvas = int(y_root * 1.5)
        # # print(x1, y1, x2, y2)
        self.image = ImageGrab.grab((self.x_root, self.y_root, self.x_root + self.image_width, self.y_root + self.image_height))
        # self.image.resize(self.origin_width, self.origin_height)
        # img.save("tmp48.png")

    def create_img(self, width, height, colordata):
        self.racine.title("Untitled - Paint")
        print(width, height, colordata['hex'].get())
        self.original = Image.new(mode='RGBA', size=(width, height), color=colordata['hex'].get())
        self.get_current_info()
        
        self.image = self.original
        self.image_ratio = self.image.size[0] / self.image.size[1]  # width / height

        self.image_import.grid_forget()
        self.open_image()
        # for data in colordata.values():
        #     print(data.get())

    def draw_img(self, *args):
        pass

    def import_image(self, path):
        # Change title
        new_title = self.get_filename(path) + " - Paint"
        self.racine.title(new_title)

        self.original = Image.open(path)
        self.get_current_info()

        self.image = self.original
        self.image_ratio = self.origin_width / self.origin_height   # width / height
        # self.image_tk = ImageTk.PhotoImage(self.image)
        # Hide image import button
        self.image_import.grid_forget()
        self.open_image()

    def get_filename(self, path):
        i = len(path) - 1
        filename = ""
        while path[i] != "/" and i >= 0:
            filename = path[i] + filename
            i -= 1

        return filename

    def open_image(self):
        # Open image and create Close button + Menu
        self.image_output = ImageOutput(self.racine, self.draw_vars, self.color_vars,
                                        self.resize_image, self.update_pos,
                                        self.reset_pos, self.update_current_img)
        # self.close_button = CloseOutput(self.racine, self.close_edit)
        self.menu_app = Menu(self.racine, self.edit_vars, self.draw_vars, self.color_vars, self.export_image)
        self.state_bar = StateBar(self.racine, self.state_vars)


    def close_edit(self):
        # Hide image + close button + Menu
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu_app.grid_forget()

        # Recreate import button
        self.image_import = ImageImport(self.racine, self.import_image)

    def resize_image(self, event):
        # Current canvas ratio
        self.canvas_ratio = event.width / event.height

        # Current canvas size
        self.canvas_width = event.width
        self.canvas_height = event.height

        self.calcul_resize()

    def calcul_resize(self):
        # Canvas position
        self.x_root = self.racine.winfo_rootx() + self.image_output.winfo_x() + 1
        self.y_root = self.racine.winfo_rooty() + self.image_output.winfo_y() + 1

        # Resize image
        if self.canvas_ratio > self.image_ratio: # canvas is wider than the image
            self.image_height = int(self.canvas_height)
            self.image_width = int(self.image_height * self.image_ratio)
            self.tmp = int((self.canvas_width - self.image_width) / 2)
            # self.x_root += int((self.canvas_width - self.image_width) / 2)
        else:  # canvas is taller than the image
            self.image_width = int(self.canvas_width)
            self.image_height = int(self.image_width / self.image_ratio)
            # self.tmp = int((self.canvas_height - self.image_height) / 2)
            self.y_root += int((self.canvas_height - self.image_height) / 2)

        self.place_img()

    def place_img(self):
        self.image_output.delete('all')
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        print(self.image_height, self.canvas_height)
        self.image_output.create_image(self.canvas_width/2, self.canvas_height/2, image=self.image_tk)

    def export_image(self, name, file, path):
        export_var = f"{path}/{name}.{file}"
        self.image.save(export_var)
        tk.messagebox.showinfo("Notice", "Save file successfully")
        # print(export_var)
App()