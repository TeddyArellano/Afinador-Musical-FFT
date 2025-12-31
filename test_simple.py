import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
from procesador_senial import ProcesadorSenial

print("=== Test de detección con Librosa (piptrack) ===\n")

# Crear procesador
procesador = ProcesadorSenial(tasa_muestreo=44100, tamanio_buffer=4096)

# Test 1: Señal de 440 Hz (LA4)
print("Test 1: Generando señal de 440 Hz (LA4)")
t = np.linspace(0, 4096/44100, 4096, endpoint=False)
audio_440 = np.sin(2 * np.pi * 440 * t) * 0.3

freq_fft = procesador.detectar_frecuencia_fundamental(audio_440, usar_librosa=False)
freq_librosa = procesador.detectar_frecuencia_fundamental(audio_440, usar_librosa=True)

print(f"  FFT detectó: {freq_fft:.2f} Hz" if freq_fft else "  FFT: No detectó")
print(f"  Librosa detectó: {freq_librosa:.2f} Hz" if freq_librosa else "  Librosa: No detectó")
print(f"  Error FFT: {abs(freq_fft - 440):.2f} Hz" if freq_fft else "  N/A")
print(f"  Error Librosa: {abs(freq_librosa - 440):.2f} Hz" if freq_librosa else "  N/A")

# Test 2: Señal de 261.63 Hz (DO4)
print("\nTest 2: Generando señal de 261.63 Hz (DO4)")
audio_261 = np.sin(2 * np.pi * 261.63 * t) * 0.3

freq_fft = procesador.detectar_frecuencia_fundamental(audio_261, usar_librosa=False)
freq_librosa = procesador.detectar_frecuencia_fundamental(audio_261, usar_librosa=True)

print(f"  FFT detectó: {freq_fft:.2f} Hz" if freq_fft else "  FFT: No detectó")
print(f"  Librosa detectó: {freq_librosa:.2f} Hz" if freq_librosa else "  Librosa: No detectó")
print(f"  Error FFT: {abs(freq_fft - 261.63):.2f} Hz" if freq_fft else "  N/A")
print(f"  Error Librosa: {abs(freq_librosa - 261.63):.2f} Hz" if freq_librosa else "  N/A")

# Test 3: Señal de 82.41 Hz (MI2 - cuerda grave de guitarra)
print("\nTest 3: Generando señal de 82.41 Hz (MI2)")
audio_82 = np.sin(2 * np.pi * 82.41 * t) * 0.3

freq_fft = procesador.detectar_frecuencia_fundamental(audio_82, usar_librosa=False)
freq_librosa = procesador.detectar_frecuencia_fundamental(audio_82, usar_librosa=True)

print(f"  FFT detectó: {freq_fft:.2f} Hz" if freq_fft else "  FFT: No detectó")
print(f"  Librosa detectó: {freq_librosa:.2f} Hz" if freq_librosa else "  Librosa: No detectó")
print(f"  Error FFT: {abs(freq_fft - 82.41):.2f} Hz" if freq_fft else "  N/A")
print(f"  Error Librosa: {abs(freq_librosa - 82.41):.2f} Hz" if freq_librosa else "  N/A")

print("\n=== Tests completados ===")
