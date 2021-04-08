#!/usr/bin/env python
# -*- coding: latin-1 -*-
import sys
from os import listdir
from os.path import join,isdir,isfile
from nltk.stem import PorterStemmer  

#Variables Globales
global dirpath
global minTerm
global maxTerm
global vacias_path
global cant_doc
global cant_term
global cant_token
global vocabulario



#asigna un numero a cada archivo
def cargar_archivos(path) :
	print("Generando indices de coleccion.")
	print("Generando indices de coleccion..")
	cant_doc = 0
	dic = {}
	if  isdir(dir_path) :
		l=listdir(dir_path)
		for archivo in l  :
			path= join(dir_path,archivo)
			if not isdir(path) :
				cant_doc += 1
				dic[cant_doc] = archivo
	print("Generando indices de coleccion...hecho")
	return dic,cant_doc

	
#genera diccionario de datos 
def lista_archivos_factory(cant):
	dic = {}
	index = 1 
	for index in range(1,cant+1 ) :
		dic[index] = 0
	dic[total] = 0
	return dic
		
#carga las palabras vacias de archivo vacias_path
def cargar_palabras_vacias(vaciaspath) :
	print("Cargando palabras vacias.")
	print("Cargando palabras vacias..")
	lista = []
	if not isdir(vaciaspath) and isfile(vaciaspath) :
		f=open(vaciaspath,"r")
		for line in f.readlines():
			lista.extend(line)
	print("Cargando palabras vacias...hecho")
	return lista


#si hay palabras vacias las quita de la lista de tokens
def sacar_palabras_vacias(lista_tokens,lista_vacias):
	lista_t = []
	if lista_vacias:
		print("No esta vacia")
		for vacia in lista :
			for palabra in lista_tokens :
				if vacia != palabra :
					lista_t.append(palabra)
		return lista_t
	else: 
		return lista_tokens


def set_stemm(lista) :
	stemmer = PorterStemmer()	
	for elem in lista :
		elem = stemmer.stem(elem)
	return lista

#normalizacion de tokens
def tokenizar(line):
	lista = []
	line = line.lower()
	line = line.replace("á","a")
	line = line.replace("é","e")
	line = line.replace("í","i")
	line = line.replace("ó","o")
	line = line.replace("ú","u")	
	line = line.replace("ü","u")
	line = line.replace("ñ","n")	
	line = line.replace("."," ")
	line = line.replace(","," ")
	line = line.replace(":"," ")
	line = line.replace(";"," ")
	line = line.replace("("," ")
	line = line.replace(")"," ")
	line = line.replace("'"," ")
	line = line.replace('"'," ")
	palabra = line.split()	
	for word in palabra :
		if ( ( minTerm  == 0 ) and (  maxTerm == 0 ) ) :
			lista.append(word)
		else:
			if (maxTerm == 0 ):		
				if (len(word)>=minTerm) :
					lista.append(word)
			else:
				if (minTerm == 0 ) :
					if (len(word)<=maxTerm) :
						lista.append(word)
				else :
					if (len(word)>=minTerm)and(len(word)<=maxTerm) :
						lista.append(word)
	return lista

#genera vocabulario
def cargar_vocabulario(lista_terminos, v, nombre,d,terms,promedio):
	valor = 0
	cant_term= terms
	num_doc = list(d.keys())[list(d.values()).index(nombre)]
	#print(num_doc)
	for palabra in lista_terminos :
		if palabra in v:
			promedio[num_doc] += 1
			dicint  = v.get(palabra)
			dicint[num_doc] += 1
			dicint[total] += 1
			v[palabra] = dicint
		else :
			promedio[num_doc] += 1
			dicint = lista_archivos_factory(cant_doc)
			dicint[num_doc] += 1
			dicint[total] += 1
			cant_term += 1
			v[palabra] = dicint
	return cant_term,promedio


#Cantidad de terminos que aparecen solo 1 vez en la coleccion
def cant_uni(v) :
	cant = 0
	for palabra in vocabulario :
		dicint = vocabulario[palabra]
		if (dicint[total] == 1) :
			cant += 1
	return cant
	
#documento mas corto
def shortest_doc(docs) :
	menor = docs[cant_doc]
	index = 1
	for index in range(1,cant_doc +1) :
		#print(str(docs[index]))
		if docs[index] < menor :
			menor = docs[index]		
	return menor

#documento mas largo
def longest_doc(docs):
	mayor = docs[1]
	index = 1
	for index in range(1,cant_doc +1) :
		if docs[index] > mayor :
			mayor = docs[index]		
	return mayor
	
#Largo promedio de un término
def largo_promedio(v) :
	suma = 0
	for palabra in v :
		
		suma = len(palabra)	
	return suma/cant_term

#promedio
def promedio(d) :
	suma = 0
	for index in range(1,cant_doc +1) :
		suma +=	d[index] 
	return suma/cant_doc

#top10
def top10(v,orden) :
	top = []
	for palabra in vocabulario :
		dicint = vocabulario[palabra]
		elemento = [palabra,dicint[total]]
		top.append(elemento)
	top.sort(key=lambda x: x[1],reverse = orden)	
	top = top[:10]
		
	return top


#copiar top10
def cargar_frecuencias(topA,topD) :
	print("Generando archivo 'frecuencias.txt'..")
	g=open("frecuencias.txt","w")
	g.write("La lista de los 10 terminos mas frecuentes: \n")
	for l in topA :
		g.write(str(l[0])+" "+str(l[1])+"\n")		
	g.write("La lista de los 10 terminos menos frecuentes:\n")
	for l in topD :
		g.write(str(l[0])+" "+str(l[1])+"\n")		
	g.close()
	print("Generando archivo 'frecuencias.txt'...hecho")



#copia las estadisticas a un archivo
def cargar_estadist() :
	print("Generando archivo 'estadisticas.txt'..")
	g=open("estadisticas.txt","w")
	g.write("Cantidad de documentos analizados:"+ str(cant_doc)+"\n")
	g.write("Cantidad de tokens encontrados:"+ str(cant_token)+"\n")
	g.write("Cantidad de terminos encontrados:"+ str(cant_term)+"\n")
	g.write("Promedio de terminos por documento:"+ str(promedio_terms)+"\n")
	g.write("Largo promedio de un termino:"+ str(promedio_len)+"\n")
	g.write("Cantidad de terminos del documento mas corto:"+ str(cant_short)+"\n")
	g.write("Cantidad de terminos del documento mas largo:"+ str(cant_long)+"\n")
	g.write("Cantidad de terminos que aparecen solo 1 vez en la coleccion : "+ str(uni_term)+"\n")

	g.close()
	print("Generando archivo 'estadisticas.txt'...hecho")

#copia el vocabulario a un archivo
def cargar_Aterminos(vocabulario):
	print("Generando archivo 'terminos.txt'.")
	s = "PALABRAS | "
	index = 1
	for index in range(1,cant_doc+1) :
		s = s + str(index) +" | "
	g=open("archivo.txt","w")
	s += "TOTAL \n"
	g.write(s)
	for palabra in vocabulario :
		s = str(palabra) + " | " 
		dicint = vocabulario[palabra]
		for valor in dicint :
			v= dicint[valor]
			s = s + str(v) +" | "
		s += '\n'
		g.write(s) 
	g.close()
	print("Generando archivo 'terminos.txt'...hecho")


#Cargo variables globales con los argv
dir_path = sys.argv[1]
minTerm = int(sys.argv[2])
maxTerm = int(sys.argv[3])
vacias_path = sys.argv[4]

#inicio del programa
cant_token = 0
cant_term = 0
cant_doc = 0
cant_short = 0
cant_long = 0
promedio_terms = 0
promedio_tokens = 0
promedio_len = 0
uni_term = 0
top10A = []
top10D = []
lista_vacias = []
lista_tokens = []
vocabulario = {}
dic_archivos,cant_doc = cargar_archivos(dir_path)
total = cant_doc
lista_vacias = cargar_palabras_vacias(vacias_path) 
promedio_doc= lista_archivos_factory(cant_doc)
print("Verificando directorio.")
print("Verificando directorio..")
if  isdir(dir_path) :
	print("Verificando directorio...hecho")
	l=listdir(dir_path)
	for archivo in l  :
		path= join(dir_path,archivo)
		if not isdir(path) :
			f=open(path,"r")		
			for line in f.readlines():
				lista_tokens= lista_tokens + tokenizar(line)
				cant_token += len(lista_tokens)
				lista_tokens = sacar_palabras_vacias(lista_tokens, lista_vacias) 
				lista_tokens = set_stemm(lista_tokens)
			cant_term,promedio_doc = cargar_vocabulario(lista_tokens,vocabulario,archivo,dic_archivos,cant_term,promedio_doc)
			lista_tokens = []
			print("Analizando archivo:" + archivo +"...hecho")
			#vocabulario = sorted(vocabulario)
promedio_terms = promedio(promedio_doc)
cant_short = shortest_doc(promedio_doc)
cant_long = longest_doc(promedio_doc)
promedio_len =	largo_promedio(vocabulario)
uni_term = cant_uni(vocabulario)
cargar_Aterminos(vocabulario)
cargar_estadist()
cargar_frecuencias(top10(vocabulario,True),top10(vocabulario,False))
print("finalizando...")
print("finalizando...hecho")

