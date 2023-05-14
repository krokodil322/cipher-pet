from cipher_manager import CipherManager

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from functools import partial
from random import randint
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
    __title_app = 'CryptoNoteBook'

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
        self.root.title(self.__title_app)
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
        self.btn_save_file = ttk.Button(self.root, text='Сохранить файл',
                                        command=self.save_file, state='disabled')
        self.btn_encrypt_file = ttk.Button(self.root, text='Зашифровать файл',
                                           command=self.encrypt_file, state='disabled')
        self.btn_decrypt_file = ttk.Button(self.root, text='Расшифровать файл ',
                                           command=self.decrypt_file, state='disabled')
        self.btn_open_file.place(x=20, y=10)
        self.btn_create_file.place(x=120, y=10)
        self.btn_save_file.place(x=220, y=10)
        self.btn_encrypt_file.place(x=520, y=10)
        self.btn_decrypt_file.place(x=650, y=10)

        # создаём текстовое поле
        self.notepad = Text(self.root, width=94, height=40)
        self.notepad.place(x=20, y=40)

        # путь к текущему файлу
        self.root_path = None
        # имя текущего файла
        self.filename = None

        # менеджер шифровщика
        self.cipher = CipherManager()

    def unlock_btn(self):
        """
        Разблокирует группу кнопок: btn_save_file, btn_encrypt_file, btn_decrypt_file
        """
        self.btn_save_file['state'] = 'enabled'
        self.btn_encrypt_file['state'] = 'enabled'
        self.btn_decrypt_file['state'] = 'enabled'

    def lock_btn(self):
        """
        Блокирует группу кнопок: btn_save_file, btn_encrypt_file, btn_decrypt_file
        """
        self.btn_save_file['state'] = 'disabled'
        self.btn_encrypt_file['state'] = 'disabled'
        self.btn_decrypt_file['state'] = 'disabled'

    def clear_all(self) -> None:
        """
        Ничего не принимает, ничего не возвращает
        Создаёт/Очищает блокнот атрибута self.notepad
        """
        self.notepad.delete('0.0', END)

    def open_file(self):
        """
        Событие для кнопки btn_open_file.
        Открывает файловый диалог и открывает выбранный файл.
        """
        print(f'Сработал метод open_file')
        fd = filedialog.askopenfile()
        if fd:
            path = fd.name
            # очищаем текстовое поле
            self.clear_all()

            # получаем корень директории открываемого/создаваемого файла и его имя
            self.root_path = '/'.join(path.split('/')[:-1])  # root_path: C:/Users/user/Desktop
            self.filename = path.split('/')[-1]

            # добавляем имя открываемого/создаваемого файла к названию приложения
            self.root.title(f'{self.__title_app} - {self.filename}')

            # разблокируем кнопки
            self.unlock_btn()

            if self.cipher.check(filename=path):
                file = self.cipher.unload_encrypted(filename=path)
                decrypted_data = self.cipher.decrypt_text(file)
                for row in decrypted_data:
                    self.notepad.insert(END, row)
            else:
                with open(path, 'r', encoding='utf-8') as file:
                    for row in file:
                        self.notepad.insert(END, row)

    def create_file(self):
        """
        Событие для кнопки btn_create_file.
        Создаёт новый файл.
        """
        print(f'Сработал метод create_file')
        fd = filedialog.asksaveasfile()
        if fd:
            path = fd.name

            # очищаем текстовое поле
            self.clear_all()

            # получаем корень директории открываемого/создаваемого файла и его имя
            self.root_path = '/'.join(path.split('/')[:-1])  # root_path: C:/Users/user/Desktop
            self.filename = path.split('/')[-1]

            # добавляем имя открываемого/создаваемого файла к названию приложения
            self.root.title(f'{self.__title_app} - {self.filename}')

            # разблокируем кнопки
            self.unlock_btn()

    def save_file(self):
        """
        Событие для кнопки btn_save_file.
        Сохраняет изменения в текущем файле.
        """
        print(f'Сработал метод save_file')
        # готовим путь для сейва
        if self.filename:
            buffer_filename = str(randint(1, 10)) + '.txt'
            path = os.path.join(self.root_path, buffer_filename) # C:/Users/user/Desktop\3.txt

            # получаем и шифруем данные из блокнота
            data = self.notepad.get('1.0', END)
            encrypt_text = self.cipher.encrypt_text(data)

            # загружаем зашифрованные данные по указанному пути
            self.cipher.load_encrypted(filename=path, data=encrypt_text)

            # удаляем старый файл и переименовываем новый как старый
            # это нужно для правильной работы функций генераторов
            old_path = os.path.join(self.root_path, self.filename)
            os.remove(old_path)
            os.rename(path, old_path)

            # блокируем кнопки
            self.lock_btn()

            # очищаем текстовое поле и выводим сообщение
            self.clear_all()
            self.notepad.insert(END, f'Файл {self.filename} успешно зашифрован и сохранён!')

            # убираем старый файл из названия
            self.root.title(self.__title_app)

    def save_file_as(self):
        """
        Событие для кнопки btn_save_file_as.
        Сохраняет файл как.
        """
        print('Сработал метод save_file_as')
        fd = filedialog.asksaveasfile()
        if fd:
            path = fd.name

            # получаем и шифруем данные из блокнота
            data = self.notepad.get('1.0', END)
            encrypt_text = self.cipher.encrypt_text(data)

            # загружаем зашифрованные данные по указанному пути
            self.cipher.load_encrypted(filename=path, data=encrypt_text)

            # блокируем кнопки
            self.lock_btn()

            # очищаем текстовое поле и выводим сообщение
            self.clear_all()
            self.notepad.insert(END, f'Файл {self.filename} успешно зашифрован и сохранён!')

            # убираем старый файл из названия
            self.root.title(self.__title_app)

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


