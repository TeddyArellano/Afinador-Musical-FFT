# Afinador de Instrumentos Musicales

Afinador en tiempo real para instrumentos musicales usando FFT y Python. Detecta la frecuencia fundamental del audio, identifica la nota musical y muestra visualmente la desviación en cents con un espectro de frecuencias.

## Características

- Detección automática de nota musical mediante FFT
- Interfaz gráfica con espectro de frecuencias en tiempo real
- Medidor visual de afinación con indicador de cents
- Selector de dispositivos de entrada de audio
- Soporte para guitarra, piano, violín y otros instrumentos
- Indicadores de color según precisión (verde/amarillo/rojo)

## Instalación y Uso

```bash
pip install -r requirements.txt
python main.py
```

**Dependencias**: numpy, scipy, sounddevice, matplotlib

**Uso**: Selecciona tu dispositivo de audio del menú, toca una nota cerca del micrófono y observa la detección en tiempo real

## Estructura del Proyecto

```
Afinador_Instrumentos_Musicales/
├── main.py                      # Punto de entrada principal
├── requirements.txt             # Dependencias del proyecto
├── data/
│   └── notas_referencia.json   # Frecuencias de notas estándar
└── src/
    ├── captura_audio.py        # Módulo de captura de audio
    ├── procesador_senial.py    # Procesamiento y FFT
    ├── detector_notas.py       # Detección y comparación de notas
    └── interfaz_grafica.py     # Interfaz gráfica con Tkinter
```

## Fundamentos Técnicos

### Teoría Musical
- **A4 = 440 Hz** (estándar internacional)
- Fórmula de frecuencias: `f = 440 × 2^((n-49)/12)`
- **Cents**: Unidad de medida de afinación (1 semitono = 100 cents)
- Cálculo: `cents = 1200 × log₂(f_detectada / f_referencia)`

**Ejemplo guitarra**: E2 (82.41 Hz), A2 (110 Hz), D3 (146.83 Hz), G3 (196 Hz), B3 (246.94 Hz), E4 (329.63 Hz)

### Algoritmo de Detección

#### Paso 1: Captura de Audio (`captura_audio.py`)
```
Micrófono → Buffer de 4096 muestras → 44100 Hz de frecuencia de muestreo
```

**Código relevante**:
```python
audio = sd.rec(self.tamanio_buffer, samplerate=44100, channels=1)
```

- Captura 4096 muestras de audio (aprox. 93 ms de duración)
- Mono (1 canal) para simplificar el procesamiento

#### Paso 2: Ventana de Hann (`procesador_senial.py`)
```
Buffer crudo → Aplicar ventana Hann → Buffer suavizado
```

**¿Por qué?** Las señales de audio tienen inicio y fin abrupto que causan "fugas espectrales" en la FFT. La ventana de Hann suaviza los bordes.

**Código relevante**:
```python
ventana = get_window('hann', tamanio_buffer)
buffer_ventaneado = buffer_audio * ventana
```

#### Paso 3: Transformada Rápida de Fourier (`procesador_senial.py`)
**Pipeline de procesamiento:**

1. **Captura de Audio** → Buffer de 4096 muestras @ 44100 Hz (93 ms)
2. **Ventana de Hann** → Reduce fugas espectrales en los bordes
3. **FFT** → Descompone señal en componentes de frecuencia
4. **Detección de Pico** → Encuentra frecuencia fundamental (50-2000 Hz)
5. **Identificación de Nota** → Compara con frecuencias estándar
6. **Cálculo de Cents** → Determina desviación respecto a la nota objetivo
7. **Visualización** → Actualiza interfaz con colores según precisión

**Código clave**:
```python
fft_resultado = np.fft.rfft(buffer_ventaneado)
frecuencia_detectada = frecuencias[np.argmax(magnitud_fft)]
cents = 1200 * np.log2(frecuencia_detectada / frecuencia_referencia)
```

**Estados de afinación**:
- ±5 cents → Verde (afinado)
- ±15 cents → Amarillo (cerca)
- Mayor → Rojo (desafinado)

### Parámetros Configurables

```python
tasa_muestreo = 44100              # Hz
tamanio_buffer = 4096               # muestras (resolución ~10.77 Hz)
umbral_audio = 0.01                 # nivel mínimo
intervalo_actualizacion = 100       # ms
```Solución de Problemas

- **No detecta audio**: Verificar micrófono habilitado, seleccionar dispositivo correcto del menú
- **Lectura inestable**: Reducir ruido de fondo, tocar notas sostenidas
- **Frecuencia incorrecta**: Una nota a la vez, evitar armónicos fuertes

## Proyecto

Desarrollo para Procesamiento Digital de Señales - IPN  
Fecha: Enero 2026