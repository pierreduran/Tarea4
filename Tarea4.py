#!/usr/bin/env python
# coding: utf-8

# In[1]:


### Pierre Durán Guzmán
### B42323
### Tarea 4 - Grupo 01


# In[2]:


#Importamos la librerías a utilizar
import numpy as np
from scipy import stats
from scipy import signal
from scipy import integrate
import matplotlib.pyplot as plt
import pandas as pd


# In[3]:


#Importar los archivos csv de los 10.000 bits
bits = np.array(pd.read_csv("bits10k.csv",header=None))


# In[4]:


'''
PUNTO 1)

Crear un esquema de modulación BPSK para los bits presentados. Esto implica asignar una forma de onda 
sinusoidal normalizada (amplitud unitaria) para cada bit y luego una concatenación de todas estas 
formas de onda.

'''

#Primero, obtenemos la cantidad de bits
N=len(bits)

#Segundo definimos la frecuencia de operación
f=5000 #Hz

#Entonces, el periodo de operación es
T=1/f

#Numero de puntos de muestreo por periodo
p=50

#Puntos de muestreo
ts=np.linspace(0, T, p)

# Creación de la forma de onda de la portadora
sinu=np.sin(2*np.pi*f*ts)

#Ajuste de imagenes
plt.rcParams["figure.figsize"] = 12.8, 9.6

# Visualización de la forma de onda de la portadora
plt.plot(ts, sinu)
plt.plot(ts, -sinu)
plt.title("Forma de onda sinusoidal normalizada")
plt.ylabel("Magnitud / pu")
plt.xlabel("Periodo / s")
plt.show()

# Frecuencia de muestreo
fs=p/T

# Creación de la línea temporal para toda la señal Tx
tx=np.linspace(0, N*T, N*p)

# Inicializar el vector de la señal modulada Tx
senal = np.zeros(tx.shape)

# Creación de la señal modulada BPSK
for k, b in enumerate(bits):
    if b==1:
        senal[k*p:(k+1)*p] = sinu
    else:
        senal[k*p:(k+1)*p] = -sinu
        
plt.plot(senal[0:5*p])
plt.title("Esquema de modulación BPSK")
plt.ylabel("Magnitud / pu")
plt.xlabel("Periodo / s")
plt.show()


# In[5]:


'''
PUNTO 2)
Calcular la potencia promedio de la señal modulada generada.
'''
# Potencia instantánea
Pinst = senal**2

# Potencia promedio a partir de la potencia instantánea (W)
Ps = integrate.trapz(Pinst, tx) / (N * T)

print("La potencia promedio de la señal modulada generada es:",Ps, "W")


# In[6]:


'''
PUNTO 3)

Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) con una relación señal 
a ruido (SNR) desde -2 hasta 3 dB.
'''

'''
En este caso se toma un valor establecido dentro del intervalo dado
con el fin de obtener una sola gráfica que nos permita
observar el comportamiento del canal ruidoso.
'''
# Relación señal-a-ruido deseada
SNR=0

# Potencia del ruido para SNR y potencia de la señal dada
Pn = Ps/(10**(SNR / 10))

# Desviación estándar del ruido
sigma = np.sqrt(Pn)

# Crear ruido
ruido = np.random.normal(0, sigma, senal.shape)

# Simular "el canal": señal recibida
Rx = senal + ruido

# Visualización de los primeros bits recibidos
plt.plot(Rx[0:5*p])
plt.title("Canal ruidoso del tipo AWGN con un SNR de 2dB")
plt.ylabel("Magnitud / pu")
plt.xlabel("Periodo / s")
plt.show()


# In[7]:


'''
PUNTO 4)
Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), 
antes y después del canal ruidoso.
'''
# Antes del canal ruidoso
fw, PSD = signal.welch(senal, fs, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.title("Densidad espectral de potencia antes del canal ruidoso")
plt.xlabel("Frecuencia / Hz")
plt.ylabel("Densidad espectral de potencia / V^2/Hz")
plt.show()

# Después del canal ruidoso
fw, PSD = signal.welch(Rx, fs, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.title("Densidad espectral de potencia después del canal ruidoso con SNR=2dB")
plt.xlabel("Frecuencia / Hz")
plt.ylabel("Densidad espectral de potencia / V^2/Hz")
plt.show()


# In[8]:


'''
PUNTO 5)
Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits 
(BER, bit error rate) para cada nivel SNR.
'''
# Relación señal a ruido (SNR) desde -2 hasta 3 dB
SNR2=np.linspace(-2,3,6)

#Inicialización del BER
BER=np.zeros(SNR2.shape)

# Pseudo-energía de la onda original
Es=np.sum(sinu**2)

# Señal de ruido para cada valor del vector SNR
for i in range(len(SNR2)):
    Pn2=Ps/(10**(SNR2[i]/10))
    sigma2=np.sqrt(Pn2)
    ruido2=np.random.normal(0,sigma2,senal.shape)
    Rx2=senal+ruido2
    
# Decodificación de la señal por detección de energía
    bitsRx=np.zeros(bits.shape)
    for k, b in enumerate(bits):
        Ep2=np.sum(Rx2[k*p:(k+1)*p]*sinu)
        if Ep2 > Es/2:
            bitsRx[k] = 1
        else:
            bitsRx[k] = 0
    err = np.sum(np.abs(bits - bitsRx))
    BER[i]=err/N
    print('Hay un total de {} errores en {} bits para una tasa de error de {} para SNR de {}.'.format(err, N, BER[i],SNR2[i]))


# In[9]:


'''
PUNTO 6)
Graficar BER versus SNR.
'''
plt.plot(SNR2,BER)
plt.title("Grafica BER versus SNR")
plt.xlabel("SNR / dB")
plt.ylabel("BER")
plt.show()

