from gtts import gTTS
from textblob import TextBlob as tb
from playsound import playsound as ps
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from functools import *
import os
import threading
from ctypes import windll

anchoWin = int(windll.user32.GetSystemMetrics(0)/21)

colBut="#909090"
fuenteButt=("Arial Black",9)

idiomaSelec="es"
idiomaDetect=""
textoIn=""
traduccion=""

raiz = Tk()
raiz.config(bg="#505050")
raiz.title("Traductor")
raiz.resizable(width=0, height=0)

izquierda=Frame(raiz,bg="#505050")
izquierda.grid(row=0,column=0,padx=10)
derecha=Frame(raiz,bg="#505050")
derecha.grid(row=0,column=1)

st1 = ScrolledText(izquierda,width=anchoWin, height=10,font=("Courier New",12),fg="#FF9900",bg="#303030")
st1.grid(row=1, column=0)

st2 = ScrolledText(derecha,width=anchoWin, height=10,font=("Courier New",12),fg="#FF9900",bg="#303030")
st2.grid(row=1, column=0)

def limpiar():
	global textoIn
	st1.delete(1.0,END)
	st2.delete(1.0,END)
	textoIn=""
	botMP3Salida.config(state='disabled')
	botMP3Entrada.config(state='disabled')

def traducir():

	st2.delete(1.0,END)
	texto=tb(textoIn)
	botMP3Salida.config(state='disabled')
	botMP3Entrada.config(state='disabled')
	def tradText():
		global traduccion
		global idiomaDetect
		global idiomaSelec

		if idiomaDetect != idiomaSelec:
			traduccion=str(texto.translate(to=idiomaSelec))
		else:
			traduccion=textoIn
		st2.insert(INSERT, traduccion)
	def audios():
		global textoIn
		global traduccion
	#----- Preparacion del audio de entrada ----------
		tts=gTTS(textoIn,lang=idiomaDetect)
		try:
			if open('mp3In.mp3'):
				os.remove('mp3In.mp3')
		except FileNotFoundError:
			pass
		tts.save('mp3In.mp3')
		botMP3Entrada.config(state='normal')
	#------ Preparacion del audio de salida -----------
		texto=tb(traduccion)
		tts=gTTS(traduccion,lang=idiomaSelec)
		try:
			if open('mp3Out.mp3'):
				os.remove('mp3Out.mp3')
		except FileNotFoundError:
			pass
		tts.save('mp3Out.mp3')
		botMP3Salida.config(state='normal')

	hilo1=threading.Thread(target=tradText)
	hilo2=threading.Thread(target=audios)
	hilo1.start()
	hilo2.start()

def shortcut(event):
	global idiomaDetect
	global textoIn
	if event.char == " " or event.char=="":
		textoIn=st1.get(1.0,END)
		if len(textoIn)>3 :
			idiomaDetect=str(tb(textoIn).detect_language())
			print(idiomaDetect)
			traducir()
raiz.bind("<Key>", shortcut)
def copiar(que):
	raiz.clipboard_clear()
	aClipboard=que.get(1.0,END)
	raiz.clipboard_clear()
	raiz.clipboard_append(aClipboard)
def pegar():
	global textoIn
	global idiomaDetect	
	try:
		deClipBoard=raiz.clipboard_get()
		st1.insert(INSERT,deClipBoard)
		textoIn=st1.get(1.0,END)
		if len(textoIn)>3 :
			idiomaDetect=str(tb(textoIn).detect_language())
			traducir()
	except:
		pass
def escuchar(_que):	
	ps(_que)

def selecIdioma(_sel):
	global idiomaSelec
	global textoIn
	textoIn=st1.get(1.0,END)
	idiomaSelec=_sel
	botones=[esp,ing,ita,rus,por,ger]
	for i in botones:	
		i.config(bg=colBut)
	if _sel == "es": esp.config(bg="#90BB90")
	elif _sel == "en": ing.config(bg="#90BB90")
	elif _sel == "it": ita.config(bg="#90BB90")
	elif _sel == "ru": rus.config(bg="#90BB90")
	elif _sel == "pt": por.config(bg="#90BB90")
	elif _sel == "de": ger.config(bg="#90BB90")
	if len(textoIn)>2:
		traducir()

supIzq=Frame(izquierda)
supIzq.grid(row=0,column=0,sticky="w")
pegar=Button(supIzq,text="Pegar",font=fuenteButt,bg=colBut,command=partial(pegar)).grid(row=0,column=0)
limpiar=Button(supIzq,text="Limpiar",font=fuenteButt,bg=colBut,command=limpiar).grid(row=0,column=2)

supDer=Frame(derecha)
supDer.grid(row=0,column=0,sticky="w")

esp=Button(supDer, text="Español",font=fuenteButt,bg="#90BB90",command=partial(selecIdioma,"es"))
esp.grid(row=0,column=1)
ing=Button(supDer, text="Ingles",font=fuenteButt,bg=colBut,command=partial(selecIdioma,"en"))
ing.grid(row=0,column=2)
ita=Button(supDer, text="Italiano",font=fuenteButt,bg=colBut,command=partial(selecIdioma,"it"))
ita.grid(row=0,column=3)
rus=Button(supDer, text="Ruso",font=fuenteButt,bg=colBut,command=partial(selecIdioma,"ru"))
rus.grid(row=0,column=4)
por=Button(supDer, text="Portugues",font=fuenteButt,bg=colBut,command=partial(selecIdioma,"pt"))
por.grid(row=0,column=5)
ger=Button(supDer, text="Aleman",font=fuenteButt,bg=colBut,command=partial(selecIdioma,"de"))
ger.grid(row=0,column=6)

botonCopiar=Button(derecha,text="copiar",font=fuenteButt,bg=colBut,command=partial(copiar,st2))
botonCopiar.grid(row=0,column=0,sticky="e",padx=16)

infIzq=Frame(izquierda)
infIzq.grid(row=3,column=0,sticky="w")

botMP3Entrada=Button(infIzq,text="Escuchar",state='disabled',font=fuenteButt,bg=colBut,command=partial(escuchar,'mp3In.mp3'))
botMP3Entrada.grid(row=3,column=0)

infDer=Frame(derecha)
infDer.grid(row=3,column=0,sticky="w")

botMP3Salida=Button(infDer,text="Escuchar",state='disabled',font=fuenteButt,bg=colBut,command=partial(escuchar,'mp3Out.mp3'))
botMP3Salida.grid(row=3,column=0)

raiz.mainloop()
os.remove('mp3Out.mp3')
os.remove('mp3In.mp3')
