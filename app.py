import bot
from tkinter import ttk
from tkinter import *


def set_start_acc(start_acc):
    bot.start_acc = start_acc


class Application(Frame):
    def __init__(self, parent):
        super().__init__(parent, borderwidth=45)
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        self.parent.title("OnlyBot")
        self.pack(fill=BOTH, expand=1)

        self.f_top = LabelFrame(self, text=" ----- Функционал -----")
        self.f_bot = LabelFrame(self, text=" ----- Выбор акканута для старта -----")

        self.btn_command1 = Button(self.f_top,
                                   text="Работа со старыми моделями",
                                   width=25,
                                   height=2,
                                   bg="lightblue",
                                   fg="black",
                                   command=bot.old_models
                                   )

        self.btn_command2 = Button(self.f_top,
                                   text="Работа с новыми моделями",
                                   width=25,
                                   height=2,
                                   bg="lightblue",
                                   fg="black",
                                   command=bot.new_models
                                   )

        self.combo_box = ttk.Combobox(self.f_bot,
                                      width=50,
                                      height=20,
                                      values=[value[:2] for value in bot.accounts])

        self.f_top.pack()
        self.f_bot.pack()
        self.btn_command1.pack(padx=12, side=LEFT, expand=True)
        self.btn_command2.pack(padx=12, side=RIGHT, expand=True)
        self.combo_box.pack(expand=1)
        self.combo_box.bind("<<ComboboxSelected>>", lambda _: set_start_acc(self.combo_box.current()))
        self.combo_box.current(0)
