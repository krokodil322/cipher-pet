from cipher_manager import CipherManager
from preference import Preference, Config

from tkinter import *
from tkinter import ttk, filedialog, messagebox

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

        # сообщение успешного сохранения файла
        self.save_msg = Label(fg='#006400', text='Файл успешно сохранён!', font = self.config.index_font)

        # создаём текстовое поле
        self.notepad = Text(self.root, font=(self.config.font, self.config.font_size), wrap=WORD)
        self.notepad.pack(fill='both', expand=True)

        # Создание колеса прокрутки по вертикали
        self.scrollbar_y = ttk.Scrollbar(self.notepad, orient=VERTICAL, command=self.notepad.yview)
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
        self.root.bind('<Control-KeyPress>', self.__hot_key_change_font_size)

    def __hot_key_change_font_size(self, event) -> None:
        """
        Принимает event - который передаёся автоматически при нажатии клюбой клавиши.
        Ивент который срабатывает при нажатии клавиш
        Если клавиши CTRL + UP, то увеличивает шрифт на 2
        Если клавиши CTRL + DOWN, то уменьшает шрифт на 2
        Ничего не возвращает
        """
        if event.keycode == 38:
            if self.config.font_size + 2 <= 26:
                self.config.font_size += 2
                self.notepad.config(font=(self.config.font, self.config.font_size))
        elif event.keycode == 40:
            if self.config.font_size - 2 >= 8:
                self.config.font_size -= 2
                self.notepad.config(font=(self.config.font, self.config.font_size))

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

        # пересоздаём и устанавливаем блокнот с новой конфигурацией
        self.notepad.config(font=(self.config.font, self.config.font_size))
        print(self.notepad.config)

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


