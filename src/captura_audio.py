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
        return sd.query_devices()
    
    def obtener_dispositivos_entrada(self):
        """Obtiene solo los dispositivos de entrada (micrófonos) con sus nombres e índices."""
        dispositivos = sd.query_devices()
        dispositivos_entrada = []
        nombres_vistos = set()
        
        # Lista de nombres de dispositivos a excluir
        excluir_keywords = [
            'stereo mix',
            'mezcla estéreo', 
            'asignador',
            'controlador primario',
            'primary sound capture',
            'what u hear',
            'wave out mix',
            'loopback'
        ]
        
        apis = sd.query_hostapis()
        
        for i, dispositivo in enumerate(dispositivos):
            # Solo dispositivos con canales de entrada (micrófonos)
            if dispositivo['max_input_channels'] > 0:
                nombre_completo = dispositivo['name'].strip()
                
                # Excluir dispositivos virtuales o del sistema
                nombre_lower = nombre_completo.lower()
                if any(keyword in nombre_lower for keyword in excluir_keywords):
                    continue
                
                nombre_base = nombre_completo
                
                # Priorizar WASAPI sobre otras APIs
                api_info = apis[dispositivo['hostapi']]
                api_name = api_info['name']
                
                # Identificar duplicados del mismo hardware
                clave_dispositivo = nombre_base.lower()
                
                # Solo mantener WASAPI o la primera ocurrencia
                if clave_dispositivo in nombres_vistos:
                    # Si el que ya tenemos no es WASAPI y este sí, reemplazarlo
                    if 'WASAPI' in api_name:
                        # Buscar y reemplazar el dispositivo anterior
                        for j, dev in enumerate(dispositivos_entrada):
                            if dev['nombre'].lower() == clave_dispositivo:
                                dispositivos_entrada[j] = {
                                    'indice': i,
                                    'nombre': nombre_base,
                                    'canales': dispositivo['max_input_channels'],
                                    'api': api_name
                                }
                                break
                    continue
                
                # Agregar el dispositivo
                nombres_vistos.add(clave_dispositivo)
                dispositivos_entrada.append({
                    'indice': i,
                    'nombre': nombre_base,
                    'canales': dispositivo['max_input_channels'],
                    'api': api_name
                })
        
        return dispositivos_entrada
    
    def configurar_dispositivo(self, indice_dispositivo=None):
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
        if self.buffer_actual is not None:
            return np.max(np.abs(self.buffer_actual))
        return 0.0
    
    def audio_supera_umbral(self, umbral=0.01):
        """Verifica si el nivel de audio supera el umbral mínimo especificado."""
        amplitud = self.obtener_amplitud_maxima()
        return amplitud > umbral
