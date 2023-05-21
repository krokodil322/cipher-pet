from cipher_manager import CipherManager
from preference import Preference, Config

from tkinter import *
from tkinter import ttk, filedialog, messagebox

from cryptography.fernet import InvalidToken
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

    def __init__(self, config: Config):
        # окно
        self.root = Tk()
        self.root.title(self.__title_app)
        self.root.geometry(f'800x710')
        self.root.resizable(False, False)

        self.root.protocol('WM_DELETE_WINDOW', self.exit)

        # конфиг приложения
        self.config = config

        # меню окна
        self.menu = Menu(self.root)
        struct_menu = {
            'Файл': (
                ('Новый файл', self.create_file), ('Открыть файл', self.open_file),
                ('Сохранить', self.save_file), ('Сохранить как', self.save_file_as)
            ),
            'Вид': (
                ('Оформление', self.preferences),
            ),
            'О программе': (
                ('Справка', partial(self.about, flag='reference')), ('О программе', partial(self.about, flag='about'))
            ),
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
        self.btn_open_file.place(x=20, y=10)
        self.btn_create_file.place(x=120, y=10)
        self.btn_save_file.place(x=220, y=10)

        # сообщение успешного сохранения файла
        self.save_msg = Label(fg='#006400', text='Файл успешно сохранён!', font=self.config.font)

        # создаём текстовое поле
        self.notepad = Text(self.root, width=94, height=40, font=f'{self.config.font} {self.config.font_size}')
        self.notepad.place(x=20, y=40)

        # путь к текущему файлу
        self.root_path = None

        # имя текущего файла
        self.filename = None

        # статус сохранения файла
        self.save_status = True

        # менеджер шифровщика
        self.cipher = CipherManager()

    def exit(self):
        """
        Этот метод отрабатывает, когда пользователь выходит из программы.
        """
        if not self.save_status:
            if messagebox.askokcancel("Quit", "Вы не сохранили файл. Вы действительно хотите выйти?"):
                self.root.destroy()
        else:
            self.root.destroy()

    def clear_text(self):
        """
        Ничего не принимает, ничего не возвращает
        Создаёт/Очищает блокнот атрибута self.notepad
        """
        self.notepad.delete('0.0', END)
        if self.save_status:
            self.save_msg.place_forget()

    def open_file(self):
        """
        Событие для кнопки btn_open_file.
        Открывает файловый диалог и открывает выбранный файл.
        """
        fd = filedialog.askopenfile()
        if fd:
            path = fd.name
            # очищаем текстовое поле
            self.clear_text()

            # получаем корень директории открываемого/создаваемого файла и его имя
            self.root_path = '/'.join(path.split('/')[:-1])  # root_path: C:/Users/user/Desktop
            self.filename = path.split('/')[-1]

            # добавляем имя открываемого/создаваемого файла к названию приложения
            self.root.title(f'{self.__title_app} - {self.filename}')

            # статус сохранения файла
            self.save_status = False

            # разблокируем кнопку сейва
            self.btn_save_file['state'] = 'enabled'

            # если файл зашифрован
            if self.cipher.check(filename=path):
                file = self.cipher.unload_encrypted(filename=path)
                try:
                    decrypted_data = self.cipher.decrypt_text(file)
                    for row in decrypted_data:
                        self.notepad.insert(END, row)
                except InvalidToken:
                    message = f'Файл с именем {self.filename} зашифрован другим ключом.'
                    self.notepad.insert(END, message)
                    # чтобы не всплывало окно при закрытии программы
                    self.save_status = True
            else:
                with open(path, 'r', encoding='utf-8') as file:
                    for row in file:
                        self.notepad.insert(END, row)

    def create_file(self):
        """
        Событие для кнопки btn_create_file.
        Создаёт новый файл.
        """
        fd = filedialog.asksaveasfile()
        if fd:
            path = fd.name

            # очищаем текстовое поле
            self.clear_text()

            # получаем корень директории открываемого/создаваемого файла и его имя
            self.root_path = '/'.join(path.split('/')[:-1])  # root_path: C:/Users/user/Desktop
            self.filename = path.split('/')[-1]

            # статус сохранения файла
            self.save_status = False

            # добавляем имя открываемого/создаваемого файла к названию приложения
            self.root.title(f'{self.__title_app} - {self.filename}')

            # разблокируем кнопку сейва
            self.btn_save_file['state'] = 'enabled'

    def save_file(self):
        """
        Событие для кнопки btn_save_file.
        Сохраняет изменения в текущем файле.
        """
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

            # блокируем кнопку сейва
            self.btn_save_file['state'] = 'disabled'

            # статус сохранения файла
            self.save_status = True

            # убираем старый файл из названия
            self.root.title(self.__title_app)

            # выводим на экран сообщение об успешном сохранении
            self.save_msg.place(x=500, y=10)

    def save_file_as(self):
        """
        Событие для кнопки btn_save_file_as.
        Сохраняет файл как.
        """
        fd = filedialog.asksaveasfile()
        if fd:
            path = fd.name

            # получаем и шифруем данные из блокнота
            data = self.notepad.get('1.0', END)
            encrypt_text = self.cipher.encrypt_text(data)

            # загружаем зашифрованные данные по указанному пути
            self.cipher.load_encrypted(filename=path, data=encrypt_text)

            # блокируем кнопки
            self.btn_save_file['state'] = 'disabled'

            # статус сохранения файла
            self.save_status = True

            # убираем старый файл из названия
            self.root.title(self.__title_app)

            # выводим на экран сообщение об успешном сохранении
            self.save_msg.place(x=500, y=10)

    def preferences(self):
        """
        Метод оконного меню, отвечает за внешний вид окна и шрифта.
        """
        # открываем дочернее окно
        pref = Preference(config=self.config)
        pref.focus()

        # получаем обновлённый конфиг
        self.config = self.config.get_config()

        # получим текст из блокнота
        text = self.notepad.get('1.0', END)

        # пересоздаём и устанавливаем блокнот с новой конфигурацией
        self.notepad = Text(self.root, width=94, height=40, font=(self.config.font, self.config.font_size))
        self.notepad.place(x=20, y=40)
        # не забываем вставить в него старый текст
        self.notepad.insert(END, text)

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


