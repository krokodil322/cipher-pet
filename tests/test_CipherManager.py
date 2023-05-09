from cipher_manager import CipherManager


cipher_manager = CipherManager()
test_data = ['abrakadabra\n', '1234567890\n', 'qwerty12345\n']
filename = 'test.txt'


# тест метода loader
cipher_manager.loader(data=test_data, filename=filename, mod_load='w')
# проверяем то, что функция loader записала
with open('test.txt', 'r', encoding='utf-8') as file:
	data = file.readlines()
	assert len(test_data) == len(data) and all(i1 == i2 for i1, i2 in zip(test_data, data)), (
		f'Метод loader отработал неверно! \n'
		f'Данные которые записывались: {test_data} \n'
		f'Данные которые записались: {data}'
	)

# тест метода unloader
cipher_manager.loader(data=test_data, filename=filename, mod_load='w')
data_loader = list(cipher_manager.unloader(filename=filename))
assert len(data_loader) == len(test_data) and all(i1 == i2 for i1, i2 in zip(test_data, data)), (
	f'Метод unloader отработал неверно! \n'
	f'Данные которые записала функция loader: {test_data} \n'
	f'Данные которые извлекла функция unloader: {data_loader}'
)


# тест методов encrypt_text и decrypt_text
generator_row = cipher_manager.unloader(filename=filename)
encrypt_data = cipher_manager.encrypt_text(generator_row)
decrypt_data = list(cipher_manager.decrypt_text(encrypt_data))
assert len(test_data) == len(decrypt_data) and all(i1 == i2 for i1, i2 in zip(test_data, decrypt_data)), (
	'Какой-то из методов: (encrypt_text, decrypt_text) отработал неверно!'
)
