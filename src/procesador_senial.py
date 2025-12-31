import numpy as np
from scipy.signal import get_window


class ProcesadorSenial:
    # Inicializa el procesador de señal con parametros de configuracion
    def __init__(self, tasa_muestreo=44100, tamanio_buffer=4096):
        self.tasa_muestreo = tasa_muestreo
        self.tamanio_buffer = tamanio_buffer
        self.ventana = get_window('hann', tamanio_buffer)
        
    # Aplica una ventana de Hann al buffer de audio para reducir fugas espectrales
    def aplicar_ventana(self, buffer_audio):
        return buffer_audio * self.ventana
    
    # Calcula la Transformada Rapida de Fourier del buffer de audio
    def calcular_fft(self, buffer_audio):
        buffer_ventaneado = self.aplicar_ventana(buffer_audio)
        fft_resultado = np.fft.rfft(buffer_ventaneado)
        magnitud_fft = np.abs(fft_resultado)
        return magnitud_fft
    
    # Obtiene el arreglo de frecuencias correspondiente a la FFT
    def obtener_frecuencias(self):
        return np.fft.rfftfreq(self.tamanio_buffer, 1.0 / self.tasa_muestreo)
    
    # Detecta la frecuencia fundamental del audio a partir de la FFT
    def detectar_frecuencia_fundamental(self, buffer_audio, frecuencia_minima=50, frecuencia_maxima=2000):
        magnitud_fft = self.calcular_fft(buffer_audio)
        frecuencias = self.obtener_frecuencias()
        
        mascara = (frecuencias >= frecuencia_minima) & (frecuencias <= frecuencia_maxima)
        frecuencias_filtradas = frecuencias[mascara]
        magnitud_filtrada = magnitud_fft[mascara]
        
        if len(magnitud_filtrada) == 0:
            return None
        
        indice_maximo = np.argmax(magnitud_filtrada)
        frecuencia_detectada = frecuencias_filtradas[indice_maximo]
        magnitud_maxima = magnitud_filtrada[indice_maximo]
        
        if magnitud_maxima < 0.01:
            return None
            
        return frecuencia_detectada
    
    # Obtiene el espectro completo para visualizacion
    def obtener_espectro_completo(self, buffer_audio, limite_frecuencia=1000):
        magnitud_fft = self.calcular_fft(buffer_audio)
        frecuencias = self.obtener_frecuencias()
        
        mascara = frecuencias <= limite_frecuencia
        return frecuencias[mascara], magnitud_fft[mascara]
