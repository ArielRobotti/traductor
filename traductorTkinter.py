from gtts import gTTS
from textblob import TextBlob as tb
from playsound import playsound as ps
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from functools import *
import os
import threading

colBut="#909090"
fuenteButt=("Arial Black",9)

idiomaSelec="es"
idiomaDetect=""
textoIn=""

raiz = Tk()
raiz.config(bg="#505050")
raiz.title("Traductor")
raiz.resizable(width=0, height=0)

izquierda=Frame(raiz,bg="#505050")
izquierda.grid(row=0,column=0,padx=10)
derecha=Frame(raiz,bg="#505050")
derecha.grid(row=0,column=1)

st1 = ScrolledText(izquierda, height=10,font=("Courier New",12),fg="white",bg="#303030")
st1.grid(row=1, column=0)

st2 = ScrolledText(derecha, height=10,font=("Courier",12),fg="white",bg="#303030")
st2.grid(row=1, column=0)

def limpiar():
	global textoIn
	st1.delete(1.0,END)
	st2.delete(1.0,END)
	textoIn=""

def traducir():
	global idiomaSelec
	global idiomaDetect

	st2.delete(1.0,END)
	texto=tb(textoIn)
	traduccion=""
	def tradText():
		global traduccion		
		if idiomaDetect != idiomaSelec:
			traduccion=str(texto.translate(to=idiomaSelec))
		else:
			traduccion=textoIn
		st2.insert(INSERT, traduccion)
	def audios():
		global traduccion
	#----- Preparacion del audio de entrada ----------
		tts=gTTS(textoIn,lang=idiomaDetect)
		try:
			if open('mp3In.mp3'):
				os.remove('mp3In.mp3')
		except FileNotFoundError:
			pass
		tts.save('mp3In.mp3')
	#------ Preparacion del audio de salida -----------

		texto=tb(traduccion)
		tts=gTTS(traduccion,lang=idiomaSelec)
		try:
			if open('mp3Out.mp3'):
				os.remove('mp3Out.mp3')
		except FileNotFoundError:
			pass
		tts.save('mp3Out.mp3')
	hilo1=threading.Thread(target=tradText)
	hilo2=threading.Thread(target=audios)
	hilo1.start()
	hilo2.start()

def shortcut(event):
	global idiomaDetect
	global idiomaSelec
	global textoIn
	if event.char == " " or event.char=="":
		textoIn=st1.get(1.0,END)
		if len(textoIn)>3 :
			idiomaDetect=tb(textoIn).detect_language()
			traducir()
raiz.bind("<Key>", shortcut)
def copiar(que):
	raiz.clipboard_clear()
	aClipboard=que.get(1.0,END)
	raiz.clipboard_clear()
	raiz.clipboard_append(aClipboard)
def pegar():
	global textoIn	
	try:
		deClipBoard=raiz.clipboard_get()
		st1.insert(INSERT,deClipBoard)
		textoIn=st1.get(1.0,END)
		if len(textoIn)>3 :
			idiomaDetect=tb(textoIn).detect_language()
			traducir()
	except:
		pass
def escuchar(_que):	
	ps(_que)

def selecIdioma(_sel):
	global idiomaSelec
	idiomaSelec=_sel
	traducir()

supIzq=Frame(izquierda)
supIzq.grid(row=0,column=0,sticky="w")
pegar=Button(supIzq,text="Pegar",font=fuenteButt,bg=colBut,command=partial(pegar)).grid(row=0,column=0)
limpiar=Button(supIzq,text="Limpiar",font=fuenteButt,bg=colBut,command=limpiar).grid(row=0,column=2)

supDer=Frame(derecha)
supDer.grid(row=0,column=0,sticky="w")

esp=Button(supDer, text="Español",font=fuenteButt,bg=colBut,command=partial(selecIdioma,"es")).grid(row=0,column=1)
ing=Button(supDer, text="Ingles",font=fuenteButt,bg=colBut,command=partial(selecIdioma,"en")).grid(row=0,column=2)
ita=Button(supDer, text="Italiano",font=fuenteButt,bg=colBut,command=partial(selecIdioma,"it")).grid(row=0,column=3)
por=Button(supDer, text="Ruso",font=fuenteButt,bg=colBut,command=partial(selecIdioma,"ru")).grid(row=0,column=4)

botonCopiar=Button(derecha,text="copiar",font=fuenteButt,bg=colBut,command=partial(copiar,st2))
botonCopiar.grid(row=0,column=0,sticky="e",padx=16)

infIzq=Frame(izquierda)
infIzq.grid(row=3,column=0,sticky="w")

Button(infIzq,text="Escuchar",font=fuenteButt,bg=colBut,command=partial(escuchar,'mp3In.mp3')).grid(row=3,column=0)

infDer=Frame(derecha)
infDer.grid(row=3,column=0,sticky="w")

Button(infDer,text="Escuchar",font=fuenteButt,bg=colBut,command=partial(escuchar,'mp3Out.mp3')).grid(row=3,column=0)

raiz.mainloop()
os.remove('mp3Out.mp3')
os.remove('mp3In.mp3')
