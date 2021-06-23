import time
import speech_recognition as sr
from pynput.keyboard import Key, Controller

keyboard = Controller()
#Função que altera nomes das peças por letras
def nomes_pecas(frase):
    #Rei
    frase = frase.replace('rei', 'K')
    frase = frase.replace('hey', 'K')
    frase = frase.replace('real', 'K')
    frase = frase.replace('rey', 'K')

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

    frase = frase.replace('beta', 'b')
    frase = frase.replace('bravo', 'b')

    frase = frase.replace('charlie', 'c')   
    frase = frase.replace('casa', 'c')   

    frase = frase.replace('delta', 'd')
    frase = frase.replace('disco', 'd')

    frase = frase.replace('eco', 'e')   
    frase = frase.replace('écom', 'e')   
    frase = frase.replace('escola', 'e')   
    frase = frase.replace('estrela', 'e')   

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

    return frase

#Função que limpa a frase
def limpar_frase(frase):
    frase = frase.replace(' ', '').lower()
    frase = nomes_pecas(frase)
    frase = numerais(frase)
    frase = nomes_colunas(frase)
    frase = erros_entendimento(frase)
    frase = roques(frase)

    return frase

# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        print("Buscando...")
        frase = recognizer.recognize_google(audio, language='pt-BR')
        fraseLimpa = limpar_frase(frase)
        if (frase == 'cancela'):
            count = 0
            while (count < 50):   
                count = count + 1
                keyboard.press(Key.backspace)
                keyboard.release(Key.backspace)
        else:
            print(fraseLimpa)
            keyboard.type(fraseLimpa)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
#r.energy_threshold = 5000
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
    print("Programa iniciado: ")
# start listening in the background (note that we don't have to do this inside a `with` statement)

stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds
for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
#stop_listening(wait_for_stop=False)

# do some more unrelated things
while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping