from unittest import TestCase, main
from cipher_manager import CipherManager
from GUI_tkinter import MainWindow


class CipherManagerTest(TestCase):
    """Для тестирования класса CipherManager"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cipher = CipherManager()
        self.test_data = (
            'abrakadabra', '1234567890', 'qwerty12345',
            'zxcvcxbsdfa', '#123asdfdsa', '213+_sad_sasdf',
        )
        self.filename = 'test.txt'

    def test_encrypt_text(self):
        """Тест метода encrypt_text"""
        encryption = tuple(self.cipher.encrypt_text(data=self.test_data))
        self.assertEqual(len(encryption), 6)
        self.assertTrue(all(row.startswith("b'gAA") and row.endswith("=='") for row in encryption))

    def test_decrypt_text(self):
        """Тест метода decrypt_text"""
        encryption = self.cipher.encrypt_text(data=self.test_data)
        decryption = tuple(self.cipher.decrypt_text(data=encryption))
        self.assertEqual(len(decryption), 6)
        self.assertTrue(all(i1 == i2 for i1, i2 in zip(decryption, self.test_data)))

    def test_load_encrypted(self):
        """Тест метода load_encrypted"""
        encryption = self.cipher.encrypt_text(data=self.test_data)
        self.cipher.load_encrypted(filename=self.filename, data=encryption)
        with open(self.filename, encoding='utf-8') as file:
            decryption = tuple(self.cipher.decrypt_text(map(str.rstrip, file)))
            self.assertEqual(len(decryption), 6)
            self.assertTrue(all(i1 == i2 for i1, i2 in zip(decryption, self.test_data)))

    def test_unload_encrypted(self):
        """Тест метода unload_encrypted"""
        encryption = self.cipher.encrypt_text(data=self.test_data)
        self.cipher.load_encrypted(filename=self.filename, data=encryption)
        encryption = self.cipher.unload_encrypted(filename=self.filename)
        decryption = tuple(self.cipher.decrypt_text(encryption))
        self.assertEqual(len(decryption), 6)
        self.assertTrue(all(i1 == i2 for i1, i2 in zip(decryption, self.test_data)))

    def test_check(self):
        """Тест метода check"""
        encryption = self.cipher.encrypt_text(data=self.test_data)
        self.cipher.load_encrypted(filename=self.filename, data=encryption)
        status_cipher = self.cipher.check(self.filename)
        self.assertTrue(status_cipher)

        with open(self.filename, 'w', encoding='utf-8') as file:
            file.writelines(self.test_data)

        status_cipher = self.cipher.check(self.filename)
        self.assertTrue(not status_cipher)

    def test_generate_cipher_key(self):
        """Тест метода generate_cipher_key"""
        cipher_key = self.cipher.generate_cipher_key()
        self.assertTrue(type(cipher_key) is bytes)

    def test_to_hash_password(self):
        pswd = 'qwerty123'
        hash_pswd = self.cipher.to_hash_password(pswd)
        self.assertTrue(pswd != hash_pswd)
        hash_pswd2 = self.cipher.to_hash_password(pswd)
        self.assertEqual(hash_pswd, hash_pswd2)

class MainWindowTest(TestCase):
    """Для тестирования класса MainWindow"""
    pass


if __name__ == '__main__':
    main()