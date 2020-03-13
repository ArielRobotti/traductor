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
	st1.delete(1.0,END)
	st2.delete(1.0,END)

def traducir(destino,_select):
	destino.delete(1.0,END)
	textoIn=st1.get(1.0,END)
	texto=tb(textoIn)
	traduccion=""
	def tradText():
		global traduccion		
		if texto.detect_language() != _select:
			traduccion=str(texto.translate(to=_select))
		else:
			traduccion=texto
		destino.insert(INSERT, traduccion)
	def audios():
		global texto
		global traduccion
	#----- Preparacion del audio de entrada ----------
		tts=gTTS(textoIn,lang=tb(textoIn).detect_language())
		try:
			if open('mp3In.mp3'):
				os.remove('mp3In.mp3')
		except FileNotFoundError:
			pass
		tts.save('mp3In.mp3')
	#------ Preparacion del audio de salida -----------

		texto=tb(traduccion)
		tts=gTTS(traduccion,lang=texto.detect_language())
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

def copiar(que):
	aClipboard=que.get(1.0,END)
	raiz.clipboard_clear()
	raiz.clipboard_append(aClipboard)
def pegar(donde):	
	try:
		deClipBoard=raiz.clipboard_get()
		donde.insert(INSERT,deClipBoard)
		raiz.clipboard_clear()
	except:
		pass
def escuchar(_que):	
	ps(_que)
supIzq=Frame(izquierda)
supIzq.grid(row=0,column=0,sticky="w")
pegar=Button(supIzq,text="Pegar",font=fuenteButt,bg=colBut,command=partial(pegar,st1)).grid(row=0,column=0)
limpiar=Button(supIzq,text="Limpiar",font=fuenteButt,bg=colBut,command=limpiar).grid(row=0,column=2)

supDer=Frame(derecha)
supDer.grid(row=0,column=0,sticky="w")

esp=Button(supDer, text="Español",font=fuenteButt,bg=colBut,command=partial(traducir,st2,"es")).grid(row=0,column=1)
ing=Button(supDer, text="Ingles",font=fuenteButt,bg=colBut,command=partial(traducir,st2,"en")).grid(row=0,column=2)
ita=Button(supDer, text="Italiano",font=fuenteButt,bg=colBut,command=partial(traducir,st2,"it")).grid(row=0,column=3)
por=Button(supDer, text="Ruso",font=fuenteButt,bg=colBut,command=partial(traducir,st2,"ru")).grid(row=0,column=4)

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


