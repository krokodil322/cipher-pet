from tkinter import *
from tkinter import ttk, font, colorchooser

from functools import partial
import json


class Preference:
    def __init__(self):
        self.root = Tk()
        self.root.title('Вид текста')
        self.root.geometry('400x150')
        self.root.resizable(False, False)

        # все шрифты
        self.__FONTS = font.families()
        # все размеры шрифтов
        self.__SIZES = tuple(range(8, 25))

        # размер шрифта
        self.font_size = ttk.Combobox(self.root, values=self.__SIZES)
        # шрифт
        self.font = ttk.Combobox(self.root, values=self.__FONTS)

        try:
            with open('config.json', 'r', encoding='utf-8') as json_file:
                self.config = json.load(fp=json_file)
        except FileNotFoundError:
            # иначе создаём конфиг по умолчанию
            self.config = {
                'font_size': 12,
                'font': 'Calibri',
                'index_font_size': self.__SIZES.index(12),
                'index_font': self.__FONTS.index('Calibri')
            }
            self.create_cfg_file()
        # уст-ка стартовых значений
        self.font_size.current(self.config['index_font_size'])
        self.font.current(self.config['index_font'])

        # лэйблы
        self.lbl_font_size = ttk.Label(self.root, text='Размер текста')
        self.lbl_font = ttk.Label(self.root, text='Шрифт')

        # уст-ка лэйблов
        self.lbl_font_size.place(x=20, y=20)
        self.lbl_font.place(x=20, y=60)

        # уст-ка кнопок активации лэйблов
        self.font_size.place(x=240, y=20)
        self.font.place(x=240, y=60)

        # создание и уст-ка кнопок сохранения и выхода окна конфига
        self.btn_save_cfg = ttk.Button(self.root, text='Сохранить', command=self.save_cfg)
        self.btn_close_cfg = ttk.Button(self.root, text='Закрыть', command=self.close_cfg)
        self.btn_save_cfg.place(x=300, y=120)
        self.btn_close_cfg.place(x=200, y=120)

    def create_cfg_file(self):
        """Создаёт файл config.json в котором выставлены настройки шрифтв"""
        with open('config.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.config, fp=json_file, indent=2)

    def save_cfg(self):
        """Сохраняет выбранные конфигурации в config.json"""
        print('Сработал метод save_cfg')
        font_size = self.font_size.get()
        font = self.font.get()
        font_size = int(font_size) if font_size else self.config['font_size']
        font = font if font else self.config['font']
        self.config = {
            'font_size': font_size,
            'font': font,
            'index_font_size': self.__SIZES.index(font_size),
            'index_font': self.__FONTS.index(font),
        }
        self.create_cfg_file()
        self.close_cfg()

    def close_cfg(self):
        print('Сработал метод close_cfg')
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    pref = Preference()
    pref.run()