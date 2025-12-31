import sounddevice as sd
import numpy as np


class CapturaAudio:
    # Inicializa el capturador de audio con parametros de configuracion
    def __init__(self, tasa_muestreo=44100, tamanio_buffer=4096):
        self.tasa_muestreo = tasa_muestreo
        self.tamanio_buffer = tamanio_buffer
        self.buffer_actual = None
        self.dispositivo_entrada = None
        
    # Obtiene y retorna la lista de dispositivos de audio disponibles
    def obtener_dispositivos_disponibles(self):
        return sd.query_devices()
    
    # Obtiene solo los dispositivos de entrada con sus nombres e indices
    def obtener_dispositivos_entrada(self):
        dispositivos = sd.query_devices()
        dispositivos_entrada = []
        
        for i, dispositivo in enumerate(dispositivos):
            if dispositivo['max_input_channels'] > 0:
                nombre_completo = dispositivo['name']
                nombre_limpio = self._limpiar_nombre_dispositivo(nombre_completo)
                
                dispositivos_entrada.append({
                    'indice': i,
                    'nombre': nombre_limpio,
                    'canales': dispositivo['max_input_channels']
                })
        
        return dispositivos_entrada
    
    # Limpia y acorta el nombre del dispositivo para mejor legibilidad
    def _limpiar_nombre_dispositivo(self, nombre):
        if '(' in nombre:
            nombre = nombre.split('(')[0].strip()
        
        if nombre.startswith('Microphone'):
            nombre = nombre.replace('Microphone', 'Microfono')
        
        nombre = nombre.replace('  ', ' ')
        
        if len(nombre) > 50:
            nombre = nombre[:47] + '...'
        
        return nombre if nombre else 'Dispositivo de audio'
    
    # Configura el dispositivo de entrada de audio a utilizar
    def configurar_dispositivo(self, indice_dispositivo=None):
        if indice_dispositivo is not None:
            self.dispositivo_entrada = indice_dispositivo
        else:
            try:
                self.dispositivo_entrada = sd.default.device[0]
                if self.dispositivo_entrada < 0:
                    self.dispositivo_entrada = None
            except:
                self.dispositivo_entrada = None
    
    # Captura un buffer de audio del microfono y lo retorna
    def capturar_buffer(self):
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
    
    # Retorna la amplitud maxima del buffer actual
    def obtener_amplitud_maxima(self):
        if self.buffer_actual is not None:
            return np.max(np.abs(self.buffer_actual))
        return 0.0
    
    # Verifica si el nivel de audio supera el umbral minimo especificado
    def audio_supera_umbral(self, umbral=0.01):
        amplitud = self.obtener_amplitud_maxima()
        return amplitud > umbral
