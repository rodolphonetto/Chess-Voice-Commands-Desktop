#Comando para compilar

pyinstaller --noconsole --add-data="C:\Users\Rodolpho\AppData\Local\Programs\Python\Python38\Lib\site-packages\vosk;./vosk" --icon=icon.ico chess.py -F
