#!/bin/python3
import fitz
from gtts import gTTS
from pydub import AudioSegment
import os
from time import sleep
import time

def pdftotxt(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text+=page.get_text()
    with open('book.txt', 'w') as f:
        f.write(text.replace("\n"," "))

def tts(txt,name,count):
    language = 'en'
    begin = time.time()

    while True:
        try:
            myobj = gTTS(txt)
            myobj.save("./auds/aud_" + str(name) + ".mp3")
            break

        except:
            print("Something Went Wrong While Converting one audio Please Wait for a while")
            sleep(20)

    end = time.time()
    sec = end - begin
    sec = int(sec)
    rem = ((count * sec)/3000)/60
    print("[+] "+ str(name) + " DONE    TOOK TIME : " + str(sec) + " s")
    print(" Esitmated Remaining Time : " + str(rem/60) + " hr" if rem > 60 else " Esitmated Remaining Time : " + str(rem) + " min")
    sleep(15)

def merge(name):
    aud = AudioSegment.empty()
    for i in range(name):
        aud += AudioSegment.from_mp3("./auds/aud_" + str(i) + ".mp3")
        print("[+] "+ str(i) + "AUDIO ADDED")
    aud.export("./book.mp3", format = "mp3")
    os.system('rm ./auds/*')       
if __name__=='__main__':
    path_aud = input('Enter PDF File : ')
    pdftotxt(path_aud)
    with open('./book.txt') as book:
        lis = book.readlines()
    text  = ' '.join(lis)
    sind = 0
    eind = sind + 3000
    name = 50
    count = len(text)
    for i in text:
        count-=3000
        if(eind > len(text)):
            print("[+] LAST ONE")
            tts(text[sind:len(text)],name,count)
            break
        tts(text[sind:eind],name,count)
        name+=1
        sind = eind
        eind += 3000
    merge(name)