#encoding: utf-8
import numpy as np
from numpy import *
from time import time
import sys
import os
from random import randint,shuffle
import random

from distutils.core import setup, Extension

ejecutable3 = "./tiempo"
archivo_salida3 = "tiempo2.dat"

rango_n= 5,10,15,20,25,30,35,40,45,50,100,150,200,250,300,350,400,450,500,550,600
secu_peajes=5,10,15,20,25,30,35,40,45,50,100,150,200,250,300,350,400,450,500,550,600
maximo_n=200
maximo_peaje=500
#rango_n= 3,4
intancias=200
#intancias=1

def generar_rutas(ciudades,densidad_rutas,max_peaje=150):
	n = int (ciudades)
	m = int(n*(n-1)/2*densidad_rutas)
	#creo las aristas normales
	#print "Normales: "+str(m)+" Premium:"+str(p)
	array_normal=[(i, j) for i in range(n) for j in xrange(i+1,n)]
	array_normal+=[(i, j) for i in range(n) for j in xrange(0,i-1)]
	shuffle(array_normal)
	res=[]
	i=0
	hubo_max_peaje=False
	while(i<m):	
		valor_a=random.randint(0,max_peaje)
		if(i==m-1)and not hubo_max_peaje:
			valor_a=max_peaje
		if(valor_a==max_peaje):
			hubo_max_peaje=True
		if(valor_a<0 or valor_a>max_peaje):
			valor_a=max_peaje/2
		res+=[array_normal[i][0]+1,array_normal[i][1]+1,valor_a]
		i=i+1

	return res,m;


def armarArgumentos(ejecutable,red,repes=10):
	# Esto arma los argumentos para call:
	# 	El primer elemento de la lista es el programa que se va a correr
	# 	El resto son los argumentos para este programa.
	#	O sea, si tenemos la lista l = [exec, a1, a2, a3] y hacemos call(l)
	#   es como si escribiéramos en la terminal exec a1 a2 a3 y apretáramos enter.
	#	Obs: todos tienen que ser strings.
	return [ejecutable] + map(str,red)

usage1 = "\nerror, parametros incorrectos\n\
modo de ejecucion python correr_experimentos.py t|a archivo_casos archivo_salida\n\
t para correr casos de prueba \n\
a para correr instancias aleatorias\n"

if __name__ == '__main__':
	from sys import argv
	from subprocess import call
	if(len(argv)<2):
		print usage1
		sys.exit()
	if(argv[1]=='t'):
		archivo_salida=archivo_salida3
		ejecutable=ejecutable3
		if(len(argv)>=3):
			with open(argv[2],'r') as in_file:
				#terminar archivo_casos
				if(len(argv)>=4):
					archivo_salida=argv[3]
				with open(archivo_salida, 'a') as f:
					for line in in_file:
						path, file_name = os.path.split(argv[2])
						test_name=line.split(" ")[0]
						test=path+"/"+test_name
						sol=line.split(" ",1)[1]
						with open(test,'r') as test_file:
							red=[]
							for linea in test_file:
								linea=linea.rstrip()
								arreglo=linea.split(' ') 
								red+=map(int,arreglo)
							args =  armarArgumentos(ejecutable,red)	
							print "Test "+test_name+" de tamanio: "+str(red[0])+" solucion: "+str(red[1]) 
						 	call(args, stdout=f)
						 	print " "
						test_file.close()
				f.close()
			in_file.close()
			sys.exit()
		else:
			print "error,falta el archivo de entrada"
			sys.exit()
	elif(argv[1]=="a"):
		ejecutable=ejecutable3
		if(len(argv)>=3):
			archivo_salida=argv[2]
		else:
			archivo_salida=archivo_salida3
		prueba_nro=0
		if not os.path.exists(archivo_salida):
			with open(archivo_salida, 'w') as f:
				f.write("ciudades;cantidad rutas;max peaje;solucion;tiempo;\n")
				f.close() 
		with open(archivo_salida, 'a') as f:
			for i in range(5,maximo_n,5):
				for repes in range(intancias): #cantidad de casos distintos para cada K
					for peaje in range(5,maximo_peaje,5): #prueba con distintos peajes
						red=[]
						red+=[i] #defino la cantidad de ciudades
						cant_rutas=random.random()
						rutas,cant_rutas=generar_rutas(i,cant_rutas,peaje)
						red+=[cant_rutas] #defino la cantidad de rutas
						print "prueba:"+str(prueba_nro)
				 		red+=rutas
				 		args =  armarArgumentos(ejecutable,red+rutas)	
				 		call(args,stdout=f)
				 		prueba_nro=prueba_nro+1
		 	f.close()
	else:
		print usage1
		sys.exit()