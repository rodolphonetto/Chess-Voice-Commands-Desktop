#!/usr/bin/env python3

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import tkinter
import _thread
import keyboard

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
        print('oi')
    q.put(bytes(indata))

def nomes_pecas(frase):
    #Rei
    frase = frase.replace('rei', 'K')

    #Dama 
    frase = frase.replace('dama', 'Q')

    #Torre 
    frase = frase.replace('torre', 'R')

    #Cavalo 
    frase = frase.replace('cavalo', 'N')

    #Bispo
    frase = frase.replace('bispo', 'B')
    return frase

def nomes_colunas(frase):
    frase = frase.replace('ana', 'a')

    frase = frase.replace('bela', 'b')

    frase = frase.replace('césar', 'c')   

    frase = frase.replace('davi', 'd')
 
    frase = frase.replace('eva', 'e')   
 
    frase = frase.replace('félix', 'f')  

    frase = frase.replace('gustavo', 'g') 

    frase = frase.replace('héctor', 'h') 

    frase = frase.replace('promove', '=')

    return frase

def numerais(frase):
    frase = frase.replace('um', '1')
    frase = frase.replace('hum', '1')
    frase = frase.replace('dois', '2')
    frase = frase.replace('tres', '3')
    frase = frase.replace('três', '3')
    frase = frase.replace('quatro', '4')
    frase = frase.replace('cinco', '5')
    frase = frase.replace('seis', '6')
    frase = frase.replace('sete', '7')
    frase = frase.replace('oito', '8')

    return frase

def erros_entendimento(frase):
    frase = frase.replace('18', 'a8')
    frase = frase.replace('17', 'a7')
    frase = frase.replace('15', 'a5')
    
    return frase

def roques(frase):

    if (frase == 'roquepequeno') or (frase == 'rockpequeno') or (frase == 'rackpequeno'):
        frase = frase.replace(frase, '0-0')
    if (frase =='roquegrande') or (frase =='rockgrande') or (frase =='roquegrand') or (frase =='rockgrand') or (frase =='rockgrade'):
        frase = frase.replace(frase, '0-0-0')

        print (frase)
    return frase

#Função que limpa a frase
def limpar_frase(frase):
    frase = frase.replace(' ', '').lower()
    frase = frase.replace('text', '')
    frase = frase.replace('{', '')
    frase = frase.replace('"', '')
    frase = frase.replace('}', '')
    frase = frase.replace(':', '')
    frase = frase.strip()
    frase = nomes_pecas(frase)
    frase = numerais(frase)
    frase = nomes_colunas(frase)
    frase = erros_entendimento(frase)
    frase = roques(frase)

    return frase

def start_script():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        '-f', '--filename', type=str, metavar='FILENAME',
        help='audio file to store recording to')
    parser.add_argument(
        '-m', '--model', type=str, metavar='MODEL_PATH',
        help='Path to the model')
    parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='input device (numeric ID or substring)')
    parser.add_argument(
        '-r', '--samplerate', type=int, help='sampling rate')
    args = parser.parse_args(remaining)

    try:
        if args.model is None:
            args.model = "model"
        if not os.path.exists(args.model):
            print ("Please download a model for your language from https://alphacephei.com/vosk/models")
            print ("and unpack as 'model' in the current folder.")
            parser.exit(0)
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])

        model = vosk.Model(args.model)

        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None

        with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                                channels=1, callback=callback):
                print('#' * 80)
                print('Press Ctrl+C to stop the recording')
                print('#' * 80)

                rec = vosk.KaldiRecognizer(model, args.samplerate,'["bispo cavalo rei dama torre ana bela césar davi eva félix gustavo héctor rock pequeno grande promove cancela hum um dois tres quatro cinco seis sete oito"]')
                while True:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        fraseLimpa = limpar_frase(rec.Result())
                        if (fraseLimpa == 'cancela'):
                            count = 0
                            while (count < 50):   
                                count = count + 1
                                keyboard.press_and_release('backspace') 
                                last_move['text'] = 'Cancelado'
                        else:
                            if (fraseLimpa != ''):
                                print(fraseLimpa)
                                keyboard.write(fraseLimpa)
                                keyboard.press_and_release('enter')
                                last_move['text'] = fraseLimpa
                    if dump_fn is not None:

                        dump_fn.write(data)

    except KeyboardInterrupt:
        print('\nDone')
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

window = tkinter.Tk()

window.title("Chess Voice Commands")
window.geometry('700x400')

label = tkinter.Label(window, text = "Bem vindo ao chess voice commands!").pack()

tutorial = tkinter.Label(window, text = "Para entrar com um movimento fale o nome da peça, coluna e linha: Cavalo Ana 4", font=('',12))
tutorial.place(x=10, y=70)

tutorial_captura = tkinter.Label(window, text = "Caso a casa destino tenha uma peça adversária será feita a captura", font=('',12))
tutorial_captura.place(x=10, y=100)

tutorial_peoes = tkinter.Label(window, text = "Para avançar peões diga a coluna e a linha: Félix 4", font=('',12))
tutorial_peoes.place(x=10, y=130)

tutorial_peoes_captura = tkinter.Label(window, text = "Para capturar de peão diga a coluna do peão e o destino da captura: Félix Gustavo 5", font=('',12))
tutorial_peoes_captura.place(x=10, y=160)

tutorial_roques = tkinter.Label(window, text = "Para roques diga: Roque grande ou Roque pequeno", font=('',12))
tutorial_roques.place(x=10, y=190)

tutorial_promover = tkinter.Label(window, text = "Para promover diga a casa de promoção seguido de promove peça: Gustavo 8 promove dama", font=('',12))
tutorial_promover.place(x=10, y=220)

tutorial_apagar = tkinter.Label(window, text = "Para apagar movimentos errados diga: cancela", font=('',12))
tutorial_apagar.place(x=10, y=250)

tutorial_colunas = tkinter.Label(window, text = "Nomes das colunas: ana, bela, césar, davi, eva, félix, gustavo, héctor")
tutorial_colunas.place(x=10, y=290)

last_move_label = tkinter.Label(window, text='Último lance jogado:', font=('',12))
last_move_label.place(x=200, y=350)

last_move = tkinter.Label(window, text='-', font=('',48))
last_move.place(x=350, y=320)

_thread.start_new_thread(start_script,())
window.mainloop()