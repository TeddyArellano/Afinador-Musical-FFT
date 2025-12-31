import json
import os
import numpy as np


class DetectorNotas:
    # Inicializa el detector cargando las frecuencias de referencia desde archivo JSON
    def __init__(self, ruta_archivo_notas):
        self.notas_referencia = {}
        self.instrumentos = {}
        self.cargar_notas_referencia(ruta_archivo_notas)
        
    # Carga las frecuencias de notas y configuraciones de instrumentos desde archivo
    def cargar_notas_referencia(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                self.notas_referencia = datos.get('notas', {})
                self.instrumentos = datos.get('instrumentos', {})
        except FileNotFoundError:
            print(f"Error: No se encontro el archivo {ruta_archivo}")
        except json.JSONDecodeError:
            print(f"Error: El archivo {ruta_archivo} no es un JSON valido")
    
    # Encuentra la nota mas cercana a la frecuencia detectada
    def encontrar_nota_mas_cercana(self, frecuencia_detectada):
        if frecuencia_detectada is None or frecuencia_detectada <= 0:
            return None, None, None
        
        nota_mas_cercana = None
        diferencia_minima = float('inf')
        frecuencia_nota_cercana = None
        
        for nombre_nota, frecuencia_nota in self.notas_referencia.items():
            diferencia = abs(frecuencia_detectada - frecuencia_nota)
            if diferencia < diferencia_minima:
                diferencia_minima = diferencia
                nota_mas_cercana = nombre_nota
                frecuencia_nota_cercana = frecuencia_nota
        
        return nota_mas_cercana, frecuencia_nota_cercana, diferencia_minima
    
    # Calcula la desviacion en cents entre la frecuencia detectada y la nota de referencia
    def calcular_cents(self, frecuencia_detectada, frecuencia_referencia):
        if frecuencia_detectada is None or frecuencia_referencia is None:
            return 0.0
        if frecuencia_detectada <= 0 or frecuencia_referencia <= 0:
            return 0.0
        
        cents = 1200 * np.log2(frecuencia_detectada / frecuencia_referencia)
        return cents
    
    # Determina el estado de afinacion basado en la desviacion en cents
    def obtener_estado_afinacion(self, cents):
        cents_abs = abs(cents)
        if cents_abs <= 5:
            return "afinado"
        elif cents_abs <= 15:
            return "cerca"
        else:
            return "desafinado"
    
    # Procesa la frecuencia detectada y retorna informacion completa de afinacion
    def analizar_frecuencia(self, frecuencia_detectada):
        nota, frecuencia_ref, diferencia = self.encontrar_nota_mas_cercana(frecuencia_detectada)
        
        if nota is None:
            return {
                'nota': None,
                'frecuencia_detectada': frecuencia_detectada,
                'frecuencia_referencia': None,
                'cents': 0.0,
                'estado': 'sin_audio'
            }
        
        cents = self.calcular_cents(frecuencia_detectada, frecuencia_ref)
        estado = self.obtener_estado_afinacion(cents)
        
        return {
            'nota': nota,
            'frecuencia_detectada': frecuencia_detectada,
            'frecuencia_referencia': frecuencia_ref,
            'cents': cents,
            'estado': estado
        }
    
    # Obtiene las notas correspondientes a un instrumento especifico
    def obtener_notas_instrumento(self, nombre_instrumento):
        return self.instrumentos.get(nombre_instrumento.lower(), [])
