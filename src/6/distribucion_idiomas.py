import re
import operator
import sys
from os import listdir
from os.path import join,isdir,isfile

frecuency_en = {}
frecuency_fr = {}
frecuency_it = {}

def generar_frecuencias(dir_path):
  letras_procesadas = 0
  total=0
  frecuency = {}
  if not isdir(dir_path) :
    with open(dir_path, "r", encoding="utf-8", errors='ignore') as f:
      for line in f.readlines():
        line = line.lower()
        for caracter in line:
          if re.match(r"([a-z])", caracter):
            if( caracter in frecuency):
              frecuency[caracter] = frecuency[caracter] + 1
              letras_procesadas += 1
            else:
              frecuency[caracter] =  1
            letras_procesadas += 1
      for caracter in frecuency:
        frecuency[caracter] = frecuency[caracter] /letras_procesadas
    f.close()
  return frecuency      

def cargar_prueba(dir_path):
  pruebas = []
  if not isdir(dir_path) :
    with open(dir_path, "r", encoding="utf-8", errors='ignore') as f:
      for line in f.readlines():
        line = line.lower()
        pruebas.append(line)
    f.close()
  return pruebas

def cargar_soluciones(dir_path):
  soluciones = []
  if not isdir(dir_path) :
    with open(dir_path, "r", encoding="utf-8", errors='ignore') as f:
      for line in f.readlines():
        line = line.split()
        soluciones.append(line[1])
    f.close()
  return soluciones

def calcular_frecuencias(pruebas):
  resultados = []
  letras_procesadas = 0
  frecuency = {}
  for line in pruebas:
    for caracter in line:
      if re.match(r"([a-z])", caracter):
        if( caracter in frecuency ):
          frecuency[caracter] = frecuency[caracter] + 1
          letras_procesadas += 1
        else:
          frecuency[caracter] =  1
          letras_procesadas += 1
    for caracter in frecuency:
      frecuency[caracter] = frecuency[caracter] /letras_procesadas
    resultados.append(frecuency)
    frecuency = {}
    letras_procesadas = 0
  return resultados



def eficiencia_modelo(resultados,solv):
  positivo = 0
  for i in range(0,len(resultados)):
    if resultados[i] == solv[i]:
      positivo = positivo + 1
  p = positivo / len(resultados)
  return p

def probar_modelo(test,en,fr,it):
  resultados = []
  res_en = {}
  res_fr = {}
  res_it = {}
  en_cof = 0
  fr_cof = 0
  it_cof = 0
  for dist in test:
    for obj in dist:
      res_en[obj] =  en[obj] - dist[obj] 
      res_fr[obj] = fr[obj] - dist[obj]  
      res_it[obj] =  it[obj] - dist[obj] 
      en_cof = en_cof + res_en[obj]
      fr_cof = fr_cof +  res_fr[obj]
      it_cof = it_cof + res_it[obj]
    if ((en_cof > fr_cof) and (en_cof > it_cof) ):
      resultados.append("English")
    if ((fr_cof > en_cof) and (fr_cof > it_cof) ):
      resultados.append("French")
    if ((it_cof > fr_cof) and (it_cof >en_cof ) ):
      resultados.append("Italian")
    res_en = {}
    res_fr = {}
    res_it = {}
    en_cof = 0
    fr_cof = 0
    it_cof = 0  
  return resultados


def main():
	#inicio del programa
	#Cargo variables globales con los argv
  dir_path_tr_en = sys.argv[1]
  dir_path_tr_fr = sys.argv[2]
  dir_path_tr_it = sys.argv[3]
  dir_path_test = sys.argv[4]
  dir_path_sol = sys.argv[5]
  
  frecuency_en = generar_frecuencias(dir_path_tr_en)
  frecuency_fr = generar_frecuencias(dir_path_tr_fr)
  frecuency_it = generar_frecuencias(dir_path_tr_it)
  eficiencia = 0.0
  test_set = cargar_prueba(dir_path_test)
  solv_set = cargar_soluciones(dir_path_sol)
  test_frecuency = calcular_frecuencias(test_set)
  resultados = probar_modelo(test_frecuency,frecuency_en,frecuency_fr,frecuency_it)
  eficiencia = eficiencia_modelo(resultados,solv_set)
  print("El porcentaje de acierto del modelo es de :"+str(eficiencia))
  
if __name__ == "__main__":
    main()