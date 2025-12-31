import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from captura_audio import CapturaAudio
from procesador_senial import ProcesadorSenial
from detector_notas import DetectorNotas
from interfaz_grafica import InterfazGrafica


class AfinadorInstrumentos:
    # Inicializa el afinador configurando todos los componentes necesarios
    def __init__(self):
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_notas = os.path.join(ruta_base, 'data', 'notas_referencia.json')
        
        self.tasa_muestreo = 44100
        self.tamanio_buffer = 4096
        self.umbral_audio = 0.01
        self.intervalo_actualizacion = 100
        
        self.captura = CapturaAudio(self.tasa_muestreo, self.tamanio_buffer)
        self.procesador = ProcesadorSenial(self.tasa_muestreo, self.tamanio_buffer)
        self.detector = DetectorNotas(ruta_notas)
        self.interfaz = InterfazGrafica()
        
        self.captura.configurar_dispositivo()
        self._configurar_dispositivos_interfaz()
        self.ejecutando = False
    
    # Configura los dispositivos de audio en la interfaz
    def _configurar_dispositivos_interfaz(self):
        dispositivos_entrada = self.captura.obtener_dispositivos_entrada()
        dispositivo_actual = self.captura.dispositivo_entrada
        
        self.interfaz.configurar_dispositivos(dispositivos_entrada, dispositivo_actual)
        self.interfaz.establecer_callback_cambio_dispositivo(self.cambiar_dispositivo)
    
    # Cambia el dispositivo de entrada de audio
    def cambiar_dispositivo(self, indice_dispositivo):
        print(f"Cambiando a dispositivo: {indice_dispositivo}")
        self.captura.configurar_dispositivo(indice_dispositivo)
        
    # Procesa un ciclo completo de captura y analisis de audio
    def procesar_audio(self):
        buffer = self.captura.capturar_buffer()
        
        if buffer is None:
            return None, None, None
        
        if not self.captura.audio_supera_umbral(self.umbral_audio):
            return None, None, None
        
        frecuencia = self.procesador.detectar_frecuencia_fundamental(buffer)
        info_afinacion = self.detector.analizar_frecuencia(frecuencia)
        frecuencias, magnitudes = self.procesador.obtener_espectro_completo(buffer)
        
        return info_afinacion, frecuencias, magnitudes
    
    # Bucle principal que actualiza continuamente la interfaz con datos de audio
    def bucle_principal(self):
        if not self.ejecutando:
            return
        
        info_afinacion, frecuencias, magnitudes = self.procesar_audio()
        
        if info_afinacion is not None:
            self.interfaz.actualizar_interfaz(info_afinacion, frecuencias, magnitudes)
        else:
            info_vacia = {
                'nota': None,
                'frecuencia_detectada': 0.0,
                'frecuencia_referencia': None,
                'cents': 0.0,
                'estado': 'sin_audio'
            }
            self.interfaz.actualizar_interfaz(info_vacia)
        
        self.interfaz.ventana.after(self.intervalo_actualizacion, self.bucle_principal)
    
    # Inicia la ejecucion del afinador
    def iniciar(self):
        print("Iniciando afinador de instrumentos musicales...")
        print("Configuracion:")
        print(f"  Tasa de muestreo: {self.tasa_muestreo} Hz")
        print(f"  Tamanio de buffer: {self.tamanio_buffer} muestras")
        print(f"  Intervalo de actualizacion: {self.intervalo_actualizacion} ms")
        print("\nToca una nota de tu instrumento para comenzar...")
        
        self.ejecutando = True
        self.interfaz.ventana.after(self.intervalo_actualizacion, self.bucle_principal)
        self.interfaz.iniciar()
    
    # Detiene la ejecucion del afinador
    def detener(self):
        self.ejecutando = False
        self.interfaz.cerrar()


def main():
    # Funcion principal que crea e inicia el afinador
    try:
        afinador = AfinadorInstrumentos()
        afinador.iniciar()
    except KeyboardInterrupt:
        print("\nAfinador detenido por el usuario")
    except Exception as e:
        print(f"Error al ejecutar el afinador: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
