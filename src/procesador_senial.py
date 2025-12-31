import numpy as np
import librosa


class ProcesadorSenial:
    """Procesador de señales de audio usando Librosa para detección de pitch."""
    
    def __init__(self, tasa_muestreo=44100, tamanio_buffer=4096):
        """Inicializa el procesador de señal con parametros de configuracion."""
        self.tasa_muestreo = tasa_muestreo
        self.tamanio_buffer = tamanio_buffer
    
    def detectar_frecuencia_fundamental(self, buffer_audio, frecuencia_minima=50, frecuencia_maxima=2000):
        """
        Detecta la frecuencia fundamental del audio usando librosa.piptrack.
        
        Args:
            buffer_audio: Array de numpy con las muestras de audio
            frecuencia_minima: Frecuencia mínima a detectar en Hz
            frecuencia_maxima: Frecuencia máxima a detectar en Hz
            
        Returns:
            Frecuencia detectada en Hz o None si no se detecta señal
        """
        try:
            # Usar piptrack de librosa para detección de pitch
            pitches, magnitudes = librosa.piptrack(
                y=buffer_audio, 
                sr=self.tasa_muestreo,
                fmin=frecuencia_minima,
                fmax=frecuencia_maxima,
                threshold=0.1
            )
            
            # Obtener el pitch con mayor magnitud en cada frame
            frecuencias_detectadas = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                mag = magnitudes[index, t]
                
                # Solo considerar pitches con magnitud significativa
                if pitch > 0 and mag > 0.01:
                    frecuencias_detectadas.append(pitch)
            
            if len(frecuencias_detectadas) > 0:
                # Usar la mediana para reducir ruido
                return np.median(frecuencias_detectadas)
            
            return None
            
        except Exception as e:
            print(f"Error en detección de frecuencia: {e}")
            return None
    
    def obtener_espectro_completo(self, buffer_audio, limite_frecuencia=1000):
        """
        Calcula el espectro de frecuencias para visualización.
        
        Args:
            buffer_audio: Array de numpy con las muestras de audio
            limite_frecuencia: Frecuencia máxima a mostrar en Hz
            
        Returns:
            Tupla (frecuencias, magnitudes)
        """
        # Calcular FFT para visualización
        fft_resultado = np.fft.rfft(buffer_audio)
        magnitud_fft = np.abs(fft_resultado)
        frecuencias = np.fft.rfftfreq(self.tamanio_buffer, 1.0 / self.tasa_muestreo)
        
        # Filtrar hasta el límite de frecuencia
        mascara = frecuencias <= limite_frecuencia
        return frecuencias[mascara], magnitud_fft[mascara]
