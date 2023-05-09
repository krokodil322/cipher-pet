from cryptography.fernet import Fernet
from hashlib import sha256
from typing import Iterator, Iterable


class CipherManager:
    """
        Класс для работы с файлами и их шифрованием.
    """
    __KEY = b"fmSaVgithtX19_JwmOtcXkJ13nxBX-yvSi1XAxm7rdw="
    __CIPHER = Fernet(__KEY)

    @staticmethod
    def loader(data: Iterable, filename: str, mod_load: str='w') -> None:
        """
            Загружает зашифрованные данные в файл в указанном режиме. Возвращает None.
            data: Итерируемый объект с информацией для загрузки в файл;
            filename: Имя файла для загрузки;
            mod_load: Режим записи в файл(дозапись или перезапись) по умолчанию перезапись
        """

        with open(filename, mod_load, encoding="utf-8") as file:
            for row in data:
                # '\n' нужен чтобы unloader понимал, где конец строки
                # и не лепил весь прочитанный файл в одну строку!
                file.write(row + '\n')

    @staticmethod
    def unloader(filename: str) -> Iterator[str]:
        """
            Создаёт генератор который возвращает строки из зашифрованного файла.
            filename - это имя файла который будет читать функция.
        """

        with open(filename, 'r', encoding="utf-8") as file:
            for row in file:
                yield row.rstrip()

    def encrypt_text(self, data: Iterable[str]) -> Iterator[str]:
        """
            Создаёт генератор который шифрует и возвращает строки.
            data - это итерируемый объект элементы которого надо зашифровать
        """
        for row in data:
            yield str(self.__CIPHER.encrypt(row.encode()))

    def decrypt_text(self, data: Iterable[str]) -> Iterator[str]:
        """
            Создаёт генератор который расшифровывает и возвращает строки.
            data - это итерируемый объект элементы которого надо расшифровать
        """
        for row in data:
            if len(row) > 3:
                row = row[2:len(row)-1]
                yield self.__CIPHER.decrypt(row.encode()).decode("utf-8")

    @staticmethod
    def generate_cipher_key() -> bytes:
        """
            Создаёт новый ключ шифрования. Возвращает его в виде байт-строки.
        """
        return Fernet.generate_key()

    @staticmethod
    def to_hash_password(password: str) -> str:
        """
            Хэширует принимаемый пароль и возвращает хэш.
        """
        return sha256(password.encode()).hexdigest()