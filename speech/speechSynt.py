from gtts import gTTS
import os

def makeSpeech(text):
    mytext = text
    
    language = 'ru'

    myobj = gTTS(text=mytext, lang=language, slow=False)

    nbFiles = len(os.listdir("speech"))

    name = "speech/" + str(nbFiles) + ".mp3"
    myobj.save(name)
    return name
