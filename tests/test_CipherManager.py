from cipher_manager import CipherManager
import csv
import os


cipher_manager = CipherManager()
test_data = ['abrakadabra', '1234567890', 'qwerty12345']
filename = 'test.txt'

# тест метода loader
cipher_manager.loader(data=test_data, filename=filename, mod_load='w')
# проверяем то, что функция loader записала
with open('test.txt', 'r', encoding='utf-8') as file:
    data = list(map(str.rstrip, file.readlines()))
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


test_data = ['abrakadabra', '1234567890', 'qwerty12345', 'qweasdSVerbereq', 'asdasdwggWFGWEfsf']
cipher_manager.loader(data=test_data, filename=filename, mod_load='w')
filedata = cipher_manager.unloader(filename=filename)
crypto_data = cipher_manager.encrypt_text(filedata)
fileload = 'test2.txt'
cipher_manager.loader(data=crypto_data, filename=fileload, mod_load='w')
os.remove(filename)
os.rename(fileload, filename)
crypto_data = list(cipher_manager.unloader(filename=filename))
result_data = list(cipher_manager.decrypt_text(crypto_data))
assert len(test_data) == len(result_data) and all(i1 == i2 for i1, i2 in zip(result_data, test_data)), (
        'Какой-то из методов: (encrypt_text, decrypt_text) отработал неверно!'
    )


#результат показал, что функции класса CipherManager памяти почти не жрут.
# тут сделай тест с биг датой, проследи за оперативой
# filename = 'test_data.csv'

# скриптик генерит csv-шку размером ~350 МБ
# можно поиграться с аргументов height и width для изменения размера файла
# headers = ['A', 'B', 'C', 'D', 'E', 'F']
# width = len(headers)
# height = 1_000_000
#
# with open(filename, 'w', encoding='utf-8', newline='') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(headers)
#     for _ in range(width):
#         for _ in range(height):
#             value = [''.join(map(str, range(0, 9)))] * width
#             writer.writerow(value)


# filedata = cipher_manager.unloader(filename=filename)
# crypto_data = cipher_manager.encrypt_text(filedata)
# fileload = 'test_data2.txt'
# cipher_manager.loader(data=crypto_data, filename=fileload, mod_load='w')
# os.remove(filename)
# os.rename(fileload, filename)

print('Все тесты успешно прошли!')