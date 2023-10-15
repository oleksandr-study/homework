import sys
from pathlib import Path
import shutil
import os
import re


if len(sys.argv) != 2:
    print("Enter only 2 arguments please!")
    quit()

Workfolder = Path(sys.argv[1])
print(Workfolder)

if not Workfolder.exists():
    
    print("Folder doesn`t exists")
    quit()

cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
translation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

dictionary = {}
    
for c, t in zip(cyrillic_symbols, translation):
    dictionary[ord(c)] = t
    dictionary[ord(c.upper())] = t.upper()

def normalize(filename):
    newfilename = filename.casefold()
    newfilename = newfilename.translate(dictionary)
    newfilename = re.sub(r"\W", "_", newfilename)
    return newfilename

def foldersearch(path):
# Сначала переносим файлы в соответствующие папки
    for object in path.iterdir():
        if object.is_dir():
            if object.name == "audio" or object.name == "video" or object.name == "images" or object.name == "documents" or object.name == "archives":
                next
            else:
                if len(os.listdir(object)) == 0:
                    object.rmdir()
                else:
                    foldersearch(object)
        if object.is_file():
            # Перенос и переименование картинок
            if object.suffix == '.jpeg' or object.suffix == '.png' or object.suffix == '.jpg' or object.suffix == '.svg':
                newname = normalize(object.name.split(".")[0])
                suff = object.name.split(".")[1]
                newfolder = Workfolder.joinpath("images")
                os.replace(object, newfolder.joinpath(f"{newname}.{suff}"))
                print(normalize(object.name.split(".")[0]))
            # Перенос и переименование видео файлов
            if object.suffix == '.avi' or object.suffix == '.mp4' or object.suffix == '.mov' or object.suffix == '.mkv':
                newname = normalize(object.name.split(".")[0])
                suff = object.name.split(".")[1]
                newfolder = Workfolder.joinpath("video")
                os.replace(object, newfolder.joinpath(f"{newname}.{suff}"))
                print(normalize(object.name.split(".")[0]))
            # Перенос и переименование документов
            if object.suffix == '.doc' or object.suffix == '.docx' or object.suffix == '.txt' or object.suffix == '.pdf' or object.suffix == '.xlsx' or object.suffix == '.pptx':
                newname = normalize(object.name.split(".")[0])
                suff = object.name.split(".")[1]
                newfolder = Workfolder.joinpath("documents")
                os.replace(object, newfolder.joinpath(f"{newname}.{suff}"))
                print(normalize(object.name.split(".")[0]))
            # Перенос и переименование аудиофайлов
            if object.suffix == '.mp3' or object.suffix == '.ogg' or object.suffix == '.wav' or object.suffix == '.amr':
                newname = normalize(object.name.split(".")[0])
                suff = object.name.split(".")[1]
                newfolder = Workfolder.joinpath("audio")
                os.replace(object, newfolder.joinpath(f"{newname}.{suff}"))
                print(normalize(object.name.split(".")[0]))
            # Распаковка и переименование архивов
            if object.suffix == '.zip':
                newname = normalize(object.name.split(".")[0])
                newfolder = Workfolder.joinpath("archives")
                shutil.unpack_archive(object, newfolder.joinpath(f"{newname}"))
            if object.suffix == '.gz':
                newname = normalize(object.name.split(".")[0])
                newfolder = Workfolder.joinpath("archives")
                shutil.unpack_archive(object, newfolder.joinpath(f"{newname}"))
            if object.suffix == '.tar':
                newname = normalize(object.name.split(".")[0])
                newfolder = Workfolder.joinpath("archives")
                shutil.unpack_archive(object, newfolder.joinpath(f"{newname}"))
# Удаляем пустые папки после переноса файлов
    for object in path.iterdir():
        print(object)
        if object.is_dir():
            if object.name == "audio" or object.name == "video" or object.name == "images" or object.name == "documents" or object.name == "archives":
                next
            else:
                if len(os.listdir(object)) == 0:
                    object.rmdir()
                else:
                    foldersearch(object)    

foldersearch(Workfolder)
