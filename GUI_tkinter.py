from cipher_manager import CipherManager

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from functools import partial
import os



class SingletonError(Exception):
    """
    Для выбивания пробок при попытке создать 2 объекта класса MainWindow
    """
    pass


class MainWindow:
    """
    Главное окно приложения CryptoNoteBook
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Реализуем паттерн Singleton
        """
        if cls.__instance:
            raise SingletonError('Объект класса MainWindow может быть создан лишь в одном экземпляре!')

        cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        # окно
        self.root = Tk()
        self.root.title('CryptoNoteBook')
        self.root.geometry(f'800x710')
        self.root.resizable(False, False)

        # меню окна
        self.menu = Menu(self.root)
        struct_menu = {
            'Файл': [
                ('Новый файл', self.create_file), ('Открыть файл', self.open_file),
                ('Сохранить', self.save_file), ('Сохранить как', self.save_file_as)
            ],
            'Команды': [
                ('Зашифровать файл', self.encrypt_file), ('Расшифровать файл', self.decrypt_file),
            ],
            'Вид': [
                ('Тема', partial(self.preferences, flag='theme')), ('Шрифт', partial(self.preferences, flag='font')),
                ('Размер шрифта', partial(self.preferences, flag='font-size')),
            ],
            'О программе': [
                ('Справка', partial(self.about, flag='reference')), ('О программе', partial(self.about, flag='about'))
            ],
        }
        for cascade, elem_menu in struct_menu.items():
            submenu = Menu(self.menu, tearoff=0)
            for label, command in elem_menu:
                submenu.add_command(label=label, command=command)
            self.menu.add_cascade(label=cascade, menu=submenu)
        self.root.config(menu=self.menu)

        # кнопки управления
        self.btn_open_file = ttk.Button(self.root, text='Открыть файл', command=self.open_file)
        self.btn_create_file = ttk.Button(self.root, text='Создать файл', command=self.create_file)
        self.btn_save_file = ttk.Button(self.root, text='Сохранить файл', command=self.save_file)
        self.btn_encrypt_file = ttk.Button(self.root, text='Зашифровать файл', command=self.encrypt_file)
        self.btn_decrypt_file = ttk.Button(self.root, text='Расшифровать файл ', command=self.decrypt_file)
        self.btn_open_file.place(x=20, y=10)
        self.btn_create_file.place(x=120, y=10)
        self.btn_save_file.place(x=220, y=10)
        self.btn_encrypt_file.place(x=520, y=10)
        self.btn_decrypt_file.place(x=650, y=10)

        # текстовое поле
        self.notepad = Text(self.root, width=94, height=40)
        self.notepad.place(x=20, y=40)

        #путь к файлу с которым работаем
        self.path = None
        #имя файла с которым работаем
        self.filename = None

        #объект шифровального менеджера и файлов
        self.cipher_manager = CipherManager()


    def open_file(self):
        """
        Событие для кнопки btn_open_file.
        Открывает файловый диалог, открывает выбранный файл и выводит
        его содержимое в текстовое поле атрибута self.notepad.
        """
        print(f'Сработал метод open_file')
        fd = filedialog.askopenfile()
        if fd:
            self.path = str(fd).split("'")[1]
            self.filename = self.path.split('/')[-1]


    def create_file(self):
        """
        Событие для кнопки btn_create_file.
        Создаёт новый файл.
        """
        print(f'Сработал метод create_file')

    def save_file(self):
        """
        Событие для кнопки btn_save_file.
        Сохраняет изменения в текущем файле.
        """
        print(f'Сработал метод save_file')

    def save_file_as(self):
        """
        Событие для кнопки btn_save_file_as.
        Сохраняет файл как.
        """
        print('Сработал метод save_file_as')

    def encrypt_file(self):
        """
        Событие для кнопки btn_encrypt_file.
        Зашифровывает текущий файл.
        """
        print(f'Сработал метод encrypt_file')

    def decrypt_file(self):
        """
        Событие для кнопки btn_decrypt_file
        Расшифровывает текущий файл
        """
        print(f'Сработал метод decrypt_file')

    def preferences(self, flag: str):
        """
        Метод оконного меню, отвечает за внешний вид окна и шрифта.
        Принимает параметр flag типа str значения которого должны входить в список __flags
        """
        __flags = ('theme', 'font', 'font-size')
        if flag not in __flags:
            message = (
                f'Атрибут flag метода preferences может принимать лишь эти значений {__flags}',
                f'Твоё значение flag={flag}'
            )
            raise ValueError(message)
        if flag == 'theme':
            print('Сработал метод preferences с флагом theme')
        elif flag == 'font':
            print('Сработал метод preferences с флагом font')
        elif flag == 'font-size':
            print('Сработал метод preferences с флагом font-size')

    def about(self, flag: str):
        """
        Метод оконного меню, отвечает за информацию об программе.
        Принимает параметр flag типа str значения которого должны входить в список __flags
        """
        __flags = ('reference', 'about')
        if flag not in __flags:
            message = (
                f'Атрибут flag метода about может принимать лишь эти значений {__flags}',
                f'Твоё значение flag={flag}'
            )
            raise ValueError(message)
        if flag == 'reference':
            print('Сработал метод about с флагом reference')
        elif flag == 'about':
            print('Сработал метод about с флагом about')

    def run(self) -> None:
        """
        Запускает главное окно приложения
        """
        self.root.mainloop()


if __name__ == '__main__':
    main_window = MainWindow()
    main_window.run()

