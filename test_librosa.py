import numpy as np
import librosa
import sounddevice as sd

# Configuracion
tasa_muestreo = 44100
tamanio_buffer = 4096

print("=== Test de Librosa ===")
print(f"Tasa de muestreo: {tasa_muestreo} Hz")
print(f"Tamaño de buffer: {tamanio_buffer} muestras")
print(f"Duración del buffer: {tamanio_buffer/tasa_muestreo:.3f} segundos")
print("\nCapturando audio...")

# Capturar audio
audio = sd.rec(tamanio_buffer, samplerate=tasa_muestreo, channels=1, dtype='float32')
sd.wait()
audio = audio.flatten()

print(f"Audio capturado. Rango: [{audio.min():.3f}, {audio.max():.3f}]")
print(f"RMS: {np.sqrt(np.mean(audio**2)):.4f}")

# Test 1: pyin con diferentes parametros
print("\n--- Test 1: librosa.pyin ---")
try:
    f0, voiced_flag, voiced_probs = librosa.pyin(
        audio, 
        fmin=50, 
        fmax=2000, 
        sr=tasa_muestreo,
        frame_length=2048
    )
    print(f"✓ pyin funcionó")
    print(f"  Frecuencias detectadas: {len(f0)}")
    print(f"  Frecuencias válidas: {np.sum(~np.isnan(f0))}")
    if np.sum(~np.isnan(f0)) > 0:
        frecuencias_validas = f0[~np.isnan(f0)]
        print(f"  Mediana: {np.median(frecuencias_validas):.2f} Hz")
except Exception as e:
    print(f"✗ pyin falló: {e}")

# Test 2: yin simple
print("\n--- Test 2: librosa.yin ---")
try:
    f0_yin = librosa.yin(audio, fmin=50, fmax=2000, sr=tasa_muestreo)
    print(f"✓ yin funcionó")
    print(f"  Frecuencias detectadas: {len(f0_yin)}")
    frecuencias_validas_yin = f0_yin[f0_yin > 0]
    if len(frecuencias_validas_yin) > 0:
        print(f"  Frecuencias válidas: {len(frecuencias_validas_yin)}")
        print(f"  Mediana: {np.median(frecuencias_validas_yin):.2f} Hz")
    else:
        print(f"  No se detectaron frecuencias válidas")
except Exception as e:
    print(f"✗ yin falló: {e}")

# Test 3: piptrack (alternativa)
print("\n--- Test 3: librosa.piptrack ---")
try:
    pitches, magnitudes = librosa.piptrack(y=audio, sr=tasa_muestreo, fmin=50, fmax=2000)
    print(f"✓ piptrack funcionó")
    print(f"  Shape pitches: {pitches.shape}")
    
    # Obtener el pitch dominante por frame
    pitch_dominante = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_dominante.append(pitch)
    
    if len(pitch_dominante) > 0:
        print(f"  Pitches dominantes detectados: {len(pitch_dominante)}")
        print(f"  Mediana: {np.median(pitch_dominante):.2f} Hz")
    else:
        print(f"  No se detectaron pitches dominantes")
except Exception as e:
    print(f"✗ piptrack falló: {e}")

print("\n=== Fin de tests ===")
