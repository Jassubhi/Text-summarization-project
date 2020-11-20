from django.shortcuts import redirect
from django.shortcuts import render
import speech_recognition as sr
import time
import webbrowser
import playsound
import os
import random
from gtts import gTTS
from time import ctime
# from FF_db import get_user_info
from wikipedia import wikipedia

from text_project import settings


def voice(request):
    print("Hello")
    context = {}
    if request.POST.get('voiceBtn'):
        ray_speak("Greetings! How may I help you? ")
        voice_data = record_audio()
        print_data = respond(voice_data)
        context['print_data'] = print_data
        return render(request, 'voice/voice.html', context)
    return render(request, 'voice/voice.html')


r = sr.Recognizer()


def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            ray_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
            print(voice_data)
        except sr.UnknownValueError:
            ray_speak("Sorry, I could not understand")
        except sr.RequestError:
            ray_speak("Sorry, Please contact the support team")
        return voice_data


def ray_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def respond(voice_data):
    if 'what is your name' in voice_data:
        ray_speak('My name is Ray')
        return "Hello this is ray"
    if 'What time is it' in voice_data:
        ray_speak(ctime())
        return "This is option 2"
    if 'Google search' in voice_data:
        search = record_audio('What do you want to search for')
        url = 'https://.google.com/search?q=' + search
        webbrowser.get().open(url)
        ray_speak('Here is what I found for ' + search)
        return search
    if 'Wikipedia search' in voice_data:
        search = record_audio("What do you want to search in wikipedia")
        results = wikipedia.summary(search, sentences=3)
        ray_speak('Here is what I found in Wikipedia, ' + results)
        return results
    if 'find location' in voice_data:
        location = record_audio('Which location do you want to search')
        url = 'https://google.nl/maps/place/' + location + '/&amp'
        webbrowser.get().open(url)
        ray_speak('Here is the location of ' + location)
        return location
    if 'PDF' in voice_data:
        ray_speak("Which pdf do you want to open")
        pdf = record_audio("Which pdf do you want to open")
        ray_speak("opening pdf")
        power = settings.MEDIA_ROOT + "\\" + pdf + ".pdf"
        os.startfile(power)
    if 'presentation' in voice_data:
        ray_speak("opening ppt")
        power = settings.MEDIA_ROOT + "/Text Summarization Sprint 2.pptx"
        os.startfile(power)
    if 'file' in voice_data:
        ray_speak("opening file")
        appli = r"text/views.py"
        os.startfile(appli)
        return "File opened"