import sounddevice as sd
import numpy as np


class CapturaAudio:
    """Clase para capturar audio desde dispositivos de entrada (micrófonos)."""
    
    def __init__(self, tasa_muestreo=44100, tamanio_buffer=4096):
        """Inicializa el capturador de audio con parámetros de configuración."""
        self.tasa_muestreo = tasa_muestreo
        self.tamanio_buffer = tamanio_buffer
        self.buffer_actual = None
        self.dispositivo_entrada = None
        
    def obtener_dispositivos_disponibles(self):
        """Obtiene y retorna la lista de todos los dispositivos de audio disponibles."""
        return sd.query_devices()
    
    def obtener_dispositivos_entrada(self):
        """Obtiene solo los dispositivos de entrada (micrófonos) con sus nombres e índices."""
        dispositivos = sd.query_devices()
        dispositivos_entrada = []
        
        for i, dispositivo in enumerate(dispositivos):
            # Solo dispositivos con canales de entrada (microfonos)
            if dispositivo['max_input_channels'] > 0:
                # Usar el nombre completo y real del dispositivo
                nombre_completo = dispositivo['name']
                
                dispositivos_entrada.append({
                    'indice': i,
                    'nombre': nombre_completo,
                    'canales': dispositivo['max_input_channels'],
                    'api': dispositivo.get('hostapi', 'Unknown')
                })
        
        return dispositivos_entrada
    
    def configurar_dispositivo(self, indice_dispositivo=None):
        """Configura el dispositivo de entrada de audio a utilizar."""
        if indice_dispositivo is not None:
            self.dispositivo_entrada = indice_dispositivo
        else:
            try:
                # Intentar obtener el dispositivo por defecto
                dispositivo_default = sd.default.device[0]
                if dispositivo_default >= 0:
                    self.dispositivo_entrada = dispositivo_default
                else:
                    # Si el default es -1, buscar el primer dispositivo de entrada disponible
                    dispositivos = self.obtener_dispositivos_entrada()
                    if len(dispositivos) > 0:
                        self.dispositivo_entrada = dispositivos[0]['indice']
                    else:
                        self.dispositivo_entrada = None
            except:
                # Si falla, buscar el primer dispositivo de entrada disponible
                dispositivos = self.obtener_dispositivos_entrada()
                if len(dispositivos) > 0:
                    self.dispositivo_entrada = dispositivos[0]['indice']
                else:
                    self.dispositivo_entrada = None
    
    def capturar_buffer(self):
        """Captura un buffer de audio del micrófono y lo retorna."""
        try:
            audio = sd.rec(
                self.tamanio_buffer,
                samplerate=self.tasa_muestreo,
                channels=1,
                dtype='float32',
                device=self.dispositivo_entrada
            )
            sd.wait()
            self.buffer_actual = audio.flatten()
            return self.buffer_actual
        except Exception as e:
            print(f"Error al capturar audio: {e}")
            return None
    
    def obtener_amplitud_maxima(self):
        """Retorna la amplitud máxima del buffer actual."""
        if self.buffer_actual is not None:
            return np.max(np.abs(self.buffer_actual))
        return 0.0
    
    def audio_supera_umbral(self, umbral=0.01):
        """Verifica si el nivel de audio supera el umbral mínimo especificado."""
        amplitud = self.obtener_amplitud_maxima()
        return amplitud > umbral
