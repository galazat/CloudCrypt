# подключаем все необходимые библиотеки
import sys
import os
import yadisk
import webbrowser
from Blowfish import Swap
from Blowfish import F
from Blowfish import Encrypt
from Blowfish import Decrypt
from Blowfish import GetRoundkeySbox
from Blowfish import CallSkript




print('\n'"--------------------Программа выполняет шифрование и выгрузку данных в облако-----------------")
print("* выберите директорию, все файлы которой будут зашифрованы и выгружены на Яндекс.Диск * "'\n')


y = yadisk.YaDisk("8a2fab6121984fbfac5e8a0a5fe67c01", "de6418c5c0f4448cb3340800bc54a0ac")
url = y.get_code_url() # получаем ссылку с запросом нелюходимых прав
webbrowser.open_new(url) # ссылка открыется в веб-браузере
print("Вы перенаправлены на сайт.")
code = input("Пройдите авторизацию. Впишите полученный код: ")
try:
    response = y.get_token(code) # по коду получается токен
except yadisk.exceptions.BadRequestError:
    print("! Код не правильный !")
    input('Press ENTER to exit')
    sys.exit(1)

y.token = response.access_token # проверяем токен
if y.check_token():
    print("Токен успешно получен. ")
else:
    print("! Токен не получен !")
    sys.exit(1)
y = yadisk.YaDisk(token= y.token)


mode = input("Выгрузить/Скачать данные (upload/download): ") # выбор режима

# режим шифрации и выгрузке данных на Янекс.Диск
if (mode[0] == "в" or mode[0] == "u"):
    mode = "encrypt"
    directory = input("Укажите директорию выгружаемых данных (С:\...): ")
    if (os.path.isdir(directory)):
        try:
            files = os.listdir(directory)
        except:
            print("! ОШИБКА ! (Директории не существует) ")
            input('Press ENTER to exit')
    else:
        files = directory
    endway = directory + "\\" + "Encrypt"
    try:
        os.mkdir(endway)
    except:
        pass
    way = input("Укажите папку на Яндекс.Диске: ")
    try:
        y.mkdir(way)
    except:
        pass
    key = input("Введите ключ шифрования: ")
    for i in files:
        CallSkript(mode, i, key, directory, endway)
        if(os.path.isfile(directory+"\\"+i)):
            try:
                y.upload(endway+"\\"+i+"Enrypted", way + "/" + i + "Enrypted")
                print(i + " --- зашифрован , выгружен на диск: "+ way )
            except:
                print("Файл " +way + "/" + i + "Enrypted" + " уже существет.")

# режим расшифровывания и скачивании данных с Янекс.Диска
elif (mode[0] == "р" or mode[0] == "d"):
    mode = "decryption"
    way = input("Укажите папку на Яндекс.Диске откуда скачаются файлы: ")
    if(y.is_dir(way)):
        try:
            files = y.listdir(way)
        except:
            print("! ОШИБКА ! (Директории не существует) ")
    else:
        files = directory
    directory = input("Укажите папку для сохранения (С:\...): ")
    endway = directory + "\\Decypted"
    endway2 = directory +"\\Enrypted"
    try:
        os.mkdir(endway)
        os.mkdir(endway2)
    except:
        pass
    key = input("Введите ключ шифрования: ")
    for i in files:
        if(y.is_file(way + "/" + i['name'])):
            try:
                y.download(way+"/"+str(i['name']), endway2+"\\"+str(i['name']))
                CallSkript(mode, str(i['name']), key, endway2, endway)
                print(str(i['name']) + " --- скачан, расшифрован: " + endway + "\\")
            except:
                   print("Файл " +directory + "\\" + str(i['name']) + " уже существет.")


input('Press ENTER to exit')


