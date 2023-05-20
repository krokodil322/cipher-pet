from tkinter import *
from tkinter import ttk, font, colorchooser

from functools import partial
import json


class Preference:
    def __init__(self):
        self.root = Tk()
        self.root.title('Внешний вид')
        self.root.geometry('400x300')
        self.root.resizable(False, False)

        # цвет рамки окна
        self.frame_color = None
        # цвет фона текстового поля(блокнота)
        self.back_color = None
        # цвет текста(шрифта)
        self.font_color = None
        # размер шрифта
        self.font_size = ttk.Combobox(self.root, values=tuple(range(8, 25)))
        # шрифт
        self.font = ttk.Combobox(self.root, values=font.families())

        # лэйблы
        self.lbl_back_color = ttk.Label(self.root, text='Цвет фона блокнота')
        self.lbl_frame_color = ttk.Label(self.root, text='Цвет фоновой рамки')
        self.lbl_font_color = ttk.Label(self.root, text='Цвет текста')
        self.lbl_font_size = ttk.Label(self.root, text='Размер текста')
        self.lbl_font = ttk.Label(self.root, text='Шрифт')

        # кнопки активации лэйблов
        self.btn_change_back_color = ttk.Button(self.root, text='Выбрать цвет',
                                                command=partial(self.change_color, 'back'))
        self.btn_change_frame_color = ttk.Button(self.root, text='Выбрать цвет',
                                                 command=partial(self.change_color, 'frame'))
        self.btn_change_font_color = ttk.Button(self.root, text='Выбрать цвет',
                                                command=partial(self.change_color, 'font'))

        # уст-ка лэйблов
        self.lbl_back_color.place(x=20, y=20)
        self.lbl_frame_color.place(x=20, y=60)
        self.lbl_font_color.place(x=20, y=100)
        self.lbl_font_size.place(x=20, y=140)
        self.lbl_font.place(x=20, y=180)

        # уст-ка кнопок активации лэйблов
        self.btn_change_back_color.place(x=240, y=20)
        self.btn_change_frame_color.place(x=240, y=60)
        self.btn_change_font_color.place(x=240, y=100)
        self.font_size.place(x=240, y=140)
        self.font.place(x=240, y=180)

        # создание и уст-ка кнопок сохранения и выхода окна конфига
        self.btn_save_cfg = ttk.Button(self.root, text='Сохранить', command=self.save_cfg)
        self.btn_close_cfg = ttk.Button(self.root, text='Закрыть', command=self.close_cfg)
        self.btn_save_cfg.place(x=300, y=240)
        self.btn_close_cfg.place(x=200, y=240)

    def change_color(self, flag: str):
        print(f'Сработал метод change_color с флагом {flag}')

        __flags = ('back', 'frame', 'font')
        if flag not in __flags:
            raise ValueError(f'Недоступный флаг - {flag}. Все доступные флаги: {__flags}')
        _, hx = colorchooser.askcolor()
        if hx:
            if flag == 'back':
                self.back_color = hx
            elif flag == 'frame':
                self.frame_color = hx
            elif flag == 'font':
                self.font_color = hx

    def save_cfg(self):
        print('Сработал метод save_cfg')

        data = {
            'back_color': self.back_color,
            'frame_color': self.frame_color,
            'font_color': self.font_color,
            'font_size': self.font_size.get(),
            'font': self.font.get(),
        }
        with open('config.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, fp=json_file, indent=2)

    def close_cfg(self):
        print('Сработал метод close_cfg')

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    pref = Preference()
    pref.run()