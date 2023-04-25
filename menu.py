import customtkinter as ctk
from panel import *

class Menu(ctk.CTkTabview):
    def __init__(self, parent, edit_vars, draw_vars, color_vars, export_func):
        super().__init__(master=parent)
        self.grid(row=0, column=0, rowspan=2, sticky='nsew', pady=8, padx=8)

        # Tabs
        self.add('Edit')
        self.add('Draw')
        self.add('TextCogn.')
        self.add('Export')

        # Widget
        EditFrame(self.tab('Edit'), edit_vars)
        DrawFrame(self.tab('Draw'), draw_vars, color_vars)
        TextCognFrame(self.tab('TextCogn.'))
        ExportFrame(self.tab('Export'), export_func)

class EditFrame(ctk.CTkFrame):
    def __init__(self, parent, edit_vars):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        # SliderPanel(self, 'Rotation', edit_vars['rotate'], 0, 360)
        SliderPanel(self, 'Zoom', edit_vars['zoom'], 0, 200)
        SegmentPanel(self, 'Invert', edit_vars['rotate'], ["Left", "Right"])
        SegmentPanel(self, 'Invert', edit_vars['flip'], ["None", "X", "Y", "Both"])
        SegmentPanel(self, 'Clipboard', edit_vars['clip'], ["None", "Cut", "Copy", "Paste"])
        RevertButton(self,
                     (edit_vars['rotate'], "None"),
                     (edit_vars['zoom'], 0),
                     (edit_vars['flip'], "None"),
                     (edit_vars['clip'], "None"))

class DrawFrame(ctk.CTkFrame):
    def __init__(self, parent, draw_vars, color_vars):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        # SwitchPanel(self, (var, text), (var, text),....)
        DropdownPanel(self, draw_vars['style'], ['Brush', 'Line', 'Rectangle', 'Oval', 'Eraser'])
        SliderPanel(self, 'Size', draw_vars['size'], 0.1, 50)
        ColorPanel(self, color_vars)

class TextCognFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent, export_func):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        # Data
        self.name_var = ctk.StringVar()
        self.file_var = ctk.StringVar(value=".jpg")
        self.path_var = ctk.StringVar()

        # Widgets
        FileNamePanel(self, self.name_var, self.file_var)
        FilePathPanel(self, self.path_var)
        SaveButton(self, export_func, self.name_var, self.file_var, self.path_var)