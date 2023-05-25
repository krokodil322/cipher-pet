from tkinter import *
from tkinter import ttk, font

import json


# все доступные размеры шрифтов
SIZES = tuple(range(8, 25))


class Config:
    """Для удобства работы со словарём конфига"""
    __slots__ = ('font_size', 'font', 'index_font_size', 'index_font')

    def __init__(
            self,
            font_size: int=12,
            font: str='Calibri',
            index_font_size: int=4,
            index_font: int=32,
        ) -> None:
        self.font_size = int(font_size)
        self.font = font
        self.index_font_size = int(index_font_size)
        self.index_font = int(index_font)

    def get_config(self) -> 'Config':
        """
        Создаёт дефолтный конфиг, если файла config.json не создан;
        Если файл config.json существует, то берёт данные из него;
        Возвращает словарь с набором конфигураций приложения.
        """
        filename = 'config.json'
        try:
            with open(filename, 'r', encoding='utf-8') as json_file:
                return self.__class__(*json.load(fp=json_file).values())
        except FileNotFoundError:
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump({
                'font_size': self.font_size,
                'font': self.font,
                'index_font_size': self.index_font_size,
                'index_font': self.index_font,
            }, fp=json_file, indent=2)
            return self

class Preference:
    def __init__(self, config: Config):
        self.root = Toplevel()
        self.root.title('Вид текста')
        self.root.geometry('400x150')
        self.root.resizable(False, False)

        self.config = config

        # все доступные шрифты
        self.FONTS = font.families()

        # размер шрифта
        self.font_size = ttk.Combobox(self.root, values=SIZES)
        # шрифт
        self.font = ttk.Combobox(self.root, values=self.FONTS)

        # уст-ка стартовых значений
        self.font_size.current(self.config.index_font_size)
        self.font.current(self.config.index_font)

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
        """Создаёт файл config.json в котором выставлены настройки шрифта"""
        with open('config.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.config, fp=json_file, indent=2)

    def save_cfg(self):
        """Сохраняет выбранные конфигурации в config.json"""
        font_size = self.font_size.get()
        font = self.font.get()
        font_size = int(font_size) if font_size else self.config.font_size
        font = font if font else self.config.font
        self.config = {
            'font_size': font_size,
            'font': font,
            'index_font_size': SIZES.index(font_size),
            'index_font': self.FONTS.index(font),
        }
        self.create_cfg_file()
        self.close_cfg()

    def focus(self):
        """
        Фокус на дочернее окно.
        Запрещает доступ к главному окну.
        Если закрыть программу, то и дочернее окно закроется.
        """
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

    def close_cfg(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    config = Config()
    pref = Preference(config=config)
    pref.run()