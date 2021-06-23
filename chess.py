#!/usr/bin/env python3

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys

from pynput.keyboard import Key, Controller

q = queue.Queue()
keyboard = Controller()

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
    frase = frase.replace('hey', 'K')
    frase = frase.replace('real', 'K')
    frase = frase.replace('rey', 'K')
    frase = frase.replace('majestade', 'K')

    #Dama 
    frase = frase.replace('dama', 'Q')
    frase = frase.replace('drama', 'Q')
    frase = frase.replace('damha', 'Q')
    frase = frase.replace('dá1a', 'Q')

    #Torre 
    frase = frase.replace('torre', 'R')

    #Cavalo 
    frase = frase.replace('cavalo', 'N')

    #Bispo
    frase = frase.replace('bispo', 'B')
    return frase

def nomes_colunas(frase):
    frase = frase.replace('alfa', '1')
    frase = frase.replace('alpha', '1')
    frase = frase.replace('abelha', '1')

    frase = frase.replace('beta', 'b')
    frase = frase.replace('bravo', 'b')
    frase = frase.replace('brava', 'b')

    frase = frase.replace('charlie', 'c')   
    frase = frase.replace('casa', 'c')   

    frase = frase.replace('delta', 'd')
    frase = frase.replace('disco', 'd')

    frase = frase.replace('eco', 'e')   
    frase = frase.replace('écom', 'e')   
    frase = frase.replace('escola', 'e')   
    frase = frase.replace('empresa', 'e')   

    frase = frase.replace('fogo', 'f')  
    frase = frase.replace('faca', 'f')  

    frase = frase.replace('gato', 'g') 
    frase = frase.replace('gol', 'g') 

    frase = frase.replace('hotel', 'h') 
    frase = frase.replace('hospital', 'h') 

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
    if (frase =='roquegrande') or (frase =='rockgrande') or (frase =='roquegrand') or (frase =='rockgrand'):
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

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 4000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate, '["cavalo bispo torre rei dama abelha bravo canal delta empresa faca gato hotel um hum dois tres quatro cinco seis sete oito roque pequeno grande", "[unk]"]')
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    fraseLimpa = limpar_frase(rec.Result())
                    if (fraseLimpa == 'cancela'):
                        count = 0
                        while (count < 50):   
                            count = count + 1
                            keyboard.press(Key.backspace)
                            keyboard.release(Key.backspace)
                    else:
                        if (fraseLimpa != ''):
                          print(fraseLimpa)
                          keyboard.type(fraseLimpa)
                          keyboard.press(Key.enter)
                          keyboard.release(Key.enter)                    
                if dump_fn is not None:

                    dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))