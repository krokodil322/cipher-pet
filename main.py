from cipher_manager import CipherManager
from preference import Preference, Config, SIZES

from tkinter import *
from tkinter import filedialog, messagebox

from cryptography.fernet import InvalidToken
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

        # изменяем ивент при закрытии окна
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

        # создаём текстовое поле
        self.notepad = Text(self.root, font=(self.config.font, self.config.font_size), wrap=WORD)
        self.notepad.pack(fill='both', expand=True)

        # Создание колеса прокрутки по вертикали
        self.scrollbar_y = Scrollbar(self.notepad, orient=VERTICAL, width=5,
                                     cursor='arrow', command=self.notepad.yview)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)
        self.notepad.config(yscrollcommand=self.scrollbar_y.set)

        # путь к текущему файлу
        self.root_path = None

        # имя текущего файла
        self.filename = None

        # статус сохранения файла
        self.save_status = True

        # менеджер шифровщика
        self.cipher = CipherManager()

        # событие для кобминаций клавиш
        self.root.bind('<Control-KeyPress>', self.__hot_keys)
        self.menu = Menu(self.root, tearoff=0)
        self.menu.add_command(label="Вырезать", command=self.cut_text)
        self.menu.add_command(label="Копировать", command=self.copy_text)
        self.menu.add_command(label="Вставить", command=self.paste_text)
        self.menu.add_command(label="Удалить", command=self.delete_text)
        self.notepad.bind("<Button-3>", self.show_popup)

        self.notepad.event_add('<<Paste>>', '<Control-igrave>')
        self.notepad.event_add("<<Copy>>", "<Control-ntilde>")

    def __hot_keys(self, event) -> None:
        """
        Принимает event - который передаётся автоматически при нажатии любой клавиши.
        Ивенты которые срабатывает при нажатии клавиш
            Если клавиши CTRL + UP, то увеличивает шрифт на 2
            Если клавиши CTRL + DOWN, то уменьшает шрифт на 2

            Если клавиши CTRL + C, то срабатывает копирование выделенной области
            Если клавиши CTRL + V, то вставляет текст из буфера обмена в указанное место

        Ничего не возвращает
        """
        # изменение размера шрифта
        if event.keycode == 38:
            if self.config.font_size + 2 <= 24:
                self.config.font_size += 2
                self.config.index_font_size = SIZES.index(self.config.font_size)
                self.notepad.config(font=(self.config.font, self.config.font_size))
        elif event.keycode == 40:
            if self.config.font_size - 2 >= 8:
                self.config.font_size -= 2
                self.config.index_font_size = SIZES.index(self.config.font_size)
                self.notepad.config(font=(self.config.font, self.config.font_size))
        elif event.keycode == 86 and event.keysym != 'v':
            self.paste_text()
        elif event.keycode == 67 and event.keysym != 'c':
            self.copy_text()

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
                print('Файл открываеся?')
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

    def save_file(self):
        """
        Событие для кнопки btn_save_file.
        Сохраняет изменения в текущем файле.
        """
        # готовим путь для сейва
        if self.filename:
            path = os.path.join(self.root_path, self.filename) # C:/Users/user/Desktop\3.txt

            # получаем и шифруем данные из блокнота
            data = self.notepad.get('1.0', END)
            encrypt_text = tuple(self.cipher.encrypt_text(data))

            # загружаем зашифрованные данные по указанному пути
            self.cipher.load_encrypted(filename=path, data=encrypt_text)

            # статус сохранения файла
            self.save_status = True

            # убираем старый файл из названия
            self.root.title(self.__title_app)

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
            encrypt_text = tuple(self.cipher.encrypt_text(data))

            # загружаем зашифрованные данные по указанному пути
            self.cipher.load_encrypted(filename=path, data=encrypt_text)

            # статус сохранения файла
            self.save_status = True

            # убираем старый файл из названия
            self.root.title(self.__title_app)

    def preferences(self):
        """
        Метод оконного меню, отвечает за внешний вид окна и шрифта.
        """
        # открываем дочернее окно
        pref = Preference(config=self.config)
        # фокус на дочернее окно
        pref.focus()

        # просто получаем обновлённый конфиг из объекта класса Preference
        self.config = pref.config

        # пересоздаём и устанавливаем блокнот с новой конфигурацией
        self.notepad.config(font=(self.config.font, self.config.font_size))

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

    """КОНТЕКСТНОЕ МЕНЮ"""
    def show_popup(self, event):
        """Выводит контекстное меню"""
        self.menu.post(event.x_root, event.y_root)

    def cut_text(self):
        """Копирует и удаляет выделенный текст"""
        self.copy_text()
        self.delete_text()

    def copy_text(self):
        """Копирует выделенный текст"""
        print('Сработал метод copy_text')
        selection = self.notepad.tag_ranges(SEL)
        if selection:
            self.root.clipboard_clear()
            text_zone = self.notepad.get(*selection)
            self.root.clipboard_append(text_zone)

    def paste_text(self):
        """Вставляет текст из буфера обмена"""
        print('Сработал метод paste_text')
        self.notepad.insert(INSERT, self.root.clipboard_get())

    def delete_text(self):
        """Удаляет выделенный текст"""
        selection = self.notepad.tag_ranges(SEL)
        if selection:
            self.notepad.delete(*selection)
