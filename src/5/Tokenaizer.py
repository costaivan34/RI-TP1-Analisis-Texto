#!/usr/bin/env python
# -*- coding: latin-1 -*-
import re
import operator
import sys
from os import listdir
from os.path import join,isdir,isfile
from unicodedata import normalize
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
#Variables Globales
dirpath = " "
minTerm = 0
maxTerm = 0
steammer= " "
vacias_path = " "
token = 0

lenTermino = 0
doc_procesados = 0
cant_tokens = 0
cant_terminos = 0
avg_tokens_doc = 0
avg_terminos_doc = 0
term_freq_1 = 0
#global largo_promedio_tok-mas_corto
#global largo_promedio_tok-mas_largo
#global largo_promedio_term-mas_corto
#global largo_promedio_term-mas_largo

vocabulario = []
vocabulario_DF = {}
vocabulario_CF = {}
lista_vacias=[]


def writeArchivo(path,string):
	with open(path, "w", encoding="utf-8") as g:
		g.write("{\n"+ string +"}")
	g.close()
	print("Archivo:"+path+" ha sido exportado con exito")

def generarTerminosTXT(v,v_cf,v_df):
	s = ("{\n")
	for word in v_cf:
		s = s + ("'"+word+"' : { 'CF':"+str(v_cf[word])+", 'DF':"+str(v_df[word])+"},\n")
	s =s +("}")
	writeArchivo("terminos-"+ steammer +".txt",s)

def generarEstadisticasTXT():
	s = ("{\n")
	s = s + ("{'doc_procesados': "+str(doc_procesados)+",\n'cant_tokens':"+str(cant_tokens)+",\n'cant_terminos':"+str(cant_terminos)+",\n'avg_tokens_doc' :"+str(avg_tokens_doc)+",\n'avg_terminos_doc' :"+ str(avg_terminos_doc)+",\n'largo_promedio_term' :" +str(lenTermino)+",\n'mas_corto' : { 'tokens':"+ str("-")+", 'terminos': "+str("-") +"},\n'mas_largo' : { 'tokens': "+str("-") + ", 'terminos': "+str("-")+"},\n'term_freq_1': "+str(term_freq_1)+ "}")
	s =s +("}")
	writeArchivo("estadisticas-"+ steammer +".txt",s)
 
def generarFrecuenciasTXT(v_cf):
	top_10_sort = sorted(vocabulario_CF.items(), key=operator.itemgetter(1), reverse=True)
	top_10_sort=top_10_sort[:10]
	s = ("{\n")
	i=0
	for word in top_10_sort:
		i+=1
		s = s + ("{'"+str(i)+"': {'"+str(word[0])+"': {'CF':"+ str(word[1])+"} },\n" )
	s =s +("}")
	top_10_sort = sorted(vocabulario_CF.items(), key=operator.itemgetter(1), reverse=False)
	top_10_sort=top_10_sort[:10]
	s =s + ("{\n")
	i=0
	for word in top_10_sort:
		i+=1
		s = s + ("{'"+str(i)+"': {'"+str(word[0])+"': {'CF':"+ str(word[1])+"} },\n" )
	s =s +("}")
	writeArchivo("frecuencias-"+ steammer +".txt",s)	

#carga las palabras vacias de archivo vacias_path
def cargar_palabras_vacias(vaciaspath) :
	lista = []
	separador = '\n'
	if not isdir(vaciaspath) and isfile(vaciaspath) :
		print("Cargando palabras vacias")
		with open(vaciaspath, "r", encoding="utf-8") as f:
			for line in f.readlines():
				line= line.split(separador)[0]
				line=line.replace('á','a')
				line=line.replace('é','e')
				line=line.replace('í','i')
				line=line.replace('ó','o')
				line=line.replace('ú','u')
				line=line.replace('ü','u') 
				lista.append(line)
		f.close()
	else:
		print("Sin palabras vacias")
	return lista

#quita las palabras vacias de la lista de tokens
def sacar_palabras_vacias(lista_tokens):
	lista = []
	for palabra in lista_tokens :
		if palabra not in lista_vacias:
			lista.append(palabra)
	return lista


#normalizacion de tokens
def tokenizar(line):
	token=["»","<",">",".","·",",",":",";","!","¡","¿","?","#","$","%","&","/","(",")","[","]","{","}","+","-","*","_","|","°","=","'",'"']
	lista = []
	#print("linea del archivo:"+line)
	line = line.lower()
	for t in token:
		line=line.replace(t,' ')	
	line = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", line), 0, re.I)
	line = normalize( 'NFC', line)
	line = line.split()
	for word in line :
		#print("linea :"+word)
		globals()['cant_tokens']  += 1
		if ( ( minTerm  == 0 ) and (  maxTerm == 0 ) ) :
			lista.append(word)
		else:
			if (len(word)>=minTerm)and(len(word)<=maxTerm) :
				lista.append(word)
	return lista


def cargar_vocabulario(document) :
	#para cada lista de documento hacer 
	#SINO existe la palabra entonces la agrego al vocabulario con DF=1 Y CF=1
	#SI existe la palabra entonces CF++ y DF++  
	for word in document :
		if word in vocabulario_CF :
			globals()['vocabulario_CF'][word] = globals()['vocabulario_CF'][word]+1
			globals()['cant_terminos'] += 1 
			globals()['lenTermino'] = globals()['lenTermino'] + len(word)
		else:
			globals()['vocabulario_CF'][word] = 1
			globals()['cant_terminos'] += 1 
			globals()['lenTermino'] = globals()['lenTermino'] + len(word)
	vistas = []
	for word in document :
		if word not in vistas:
				vistas.append(word)
	for word in vistas :
		if not (word in vocabulario_DF ): 
				globals()['vocabulario_DF'][word] = 1
		else:
			globals()['vocabulario_DF'][word]= globals()['vocabulario_DF'][word] + 1
	#print("Actualizando Vocabulario")
 
def cant_uni() :
	cant = 0
	for palabra in vocabulario_CF :
		if (vocabulario_CF[palabra] == 1) :
			cant += 1
	return cant


def generar_docs(dirname):
	docs = []
	files = listdir(dirname)
	for file in files:
		doc = []
		new = False
		if not isdir(dirname+'/'+file):
			with open(dirname+'/'+file,'r', encoding='utf-8', errors='ignore') as f:
				foundw = False				
				for line in f.readlines():					
					if new:
						doc = []
						new = False
						globals()['doc_procesados']  += 1
					if line.strip() == '.W':
						foundw = True
					else:
						if foundw:
							if not line.strip() == '.X':
								line = tokenizar(line)
								for word in line:
									doc.append(word)
							else:
								foundw = False
								new = True
								docs.append(doc)																							
	return docs	


def porter_stemming(lista_doc):
	lista=[]
	stemmer = PorterStemmer()
	for doc in lista_doc:
		for word in doc:
			lista.append(stemmer.stem(word))
	return lista
  
def lancaster_stemming(lista_doc):
	lista=[]
	stemmer = LancasterStemmer()
	for doc in lista_doc:
		for word in doc:
			lista.append(stemmer.stem(word))
	return lista

def main():
	#inicio del programa
	#Cargo variables globales con los argv
	dir_path = sys.argv[1]
	minTerm = int(sys.argv[2])
	maxTerm = int(sys.argv[3])
	vacias_path = sys.argv[4]
	globals()['steammer'] = sys.argv[5]
	lista_vacias = cargar_palabras_vacias(vacias_path)
	
	#tokens-largo_promedio_term-mas_corto
	#tokens-largo_promedio_term-mas_largo
	#terminos-largo_promedio_term-mas_corto
	#terminos-largo_promedio_term-mas_largo
	vocabulario = []
	vocabulario_DF = {}
	vocabulario_CF = {}
	lista_vacias=[]
 
	documentos = generar_docs(dir_path)
	d = []
	for doc in documentos:
		doc = sacar_palabras_vacias(doc)
		d.append(doc)
	documentos = d
	if(steammer=="porter"):
		porter = porter_stemming(documentos)
		globals()['steammer'] ="porter"
		cargar_vocabulario(porter)
	else:
		lancaster = lancaster_stemming(documentos)
		globals()['steammer'] ="lancaster"
		cargar_vocabulario(lancaster)
	globals()['avg_tokens_doc'] = cant_tokens / doc_procesados
	globals()['avg_terminos_doc'] = cant_terminos / doc_procesados
	globals()['lenTermino'] = globals()['lenTermino'] / cant_terminos
	globals()['term_freq_1']  = cant_uni()
	generarTerminosTXT(vocabulario,vocabulario_CF,vocabulario_DF)
	generarEstadisticasTXT()
	#print("------------------------------------------------------------")
	#print("------------------------------------------------------------")
	print("finalizando...")
	print("finalizando...hecho")


if __name__ == "__main__":
    main()