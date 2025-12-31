import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class InterfazGrafica:
    # Inicializa la ventana principal y todos los componentes visuales
    def __init__(self, titulo="Afinador de Instrumentos Musicales"):
        self.ventana = tk.Tk()
        self.ventana.title(titulo)
        self.ventana.geometry("900x700")
        self.ventana.resizable(False, False)
        
        self.colores = {
            'afinado': '#00ff00',
            'cerca': '#ffff00',
            'desafinado': '#ff0000',
            'sin_audio': '#808080'
        }
        
        self.crear_componentes()
        
    # Crea todos los widgets y elementos visuales de la interfaz
    def crear_componentes(self):
        marco_principal = tk.Frame(self.ventana, bg='#2b2b2b')
        marco_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.etiqueta_titulo = tk.Label(
            marco_principal,
            text="AFINADOR DE INSTRUMENTOS",
            font=('Arial', 20, 'bold'),
            bg='#2b2b2b',
            fg='white'
        )
        self.etiqueta_titulo.pack(pady=10)
        
        marco_dispositivo = tk.Frame(marco_principal, bg='#2b2b2b')
        marco_dispositivo.pack(pady=5)
        
        etiqueta_dispositivo = tk.Label(
            marco_dispositivo,
            text="Micrófono:",
            font=('Arial', 10),
            bg='#2b2b2b',
            fg='#aaaaaa'
        )
        etiqueta_dispositivo.pack(side=tk.LEFT, padx=5)
        
        self.combo_dispositivos = ttk.Combobox(
            marco_dispositivo,
            state='readonly',
            width=70,
            font=('Arial', 9)
        )
        self.combo_dispositivos.pack(side=tk.LEFT, padx=5)
        self.callback_cambio_dispositivo = None
        
        marco_nota = tk.Frame(marco_principal, bg='#2b2b2b')
        marco_nota.pack(pady=10)
        
        # Etiqueta para nota en notacion inglesa
        self.etiqueta_nota_ingles = tk.Label(
            marco_nota,
            text="--",
            font=('Arial', 48, 'bold'),
            bg='#2b2b2b',
            fg='white'
        )
        self.etiqueta_nota_ingles.pack()
        
        # Etiqueta para nota en notacion espanola
        self.etiqueta_nota_espaniol = tk.Label(
            marco_nota,
            text="--",
            font=('Arial', 36),
            bg='#2b2b2b',
            fg='#aaaaaa'
        )
        self.etiqueta_nota_espaniol.pack()
        
        self.etiqueta_frecuencia = tk.Label(
            marco_nota,
            text="0.0 Hz",
            font=('Arial', 16),
            bg='#2b2b2b',
            fg='#aaaaaa'
        )
        self.etiqueta_frecuencia.pack()
        
        marco_medidor = tk.Frame(marco_principal, bg='#2b2b2b')
        marco_medidor.pack(pady=20)
        
        self.canvas_medidor = tk.Canvas(
            marco_medidor,
            width=600,
            height=80,
            bg='#1a1a1a',
            highlightthickness=0
        )
        self.canvas_medidor.pack()
        
        self.etiqueta_cents = tk.Label(
            marco_medidor,
            text="0 cents",
            font=('Arial', 14),
            bg='#2b2b2b',
            fg='white'
        )
        self.etiqueta_cents.pack(pady=5)
        
        self.figura_espectro = Figure(figsize=(8, 3), facecolor='#2b2b2b')
        self.eje_espectro = self.figura_espectro.add_subplot(111)
        self.eje_espectro.set_facecolor('#1a1a1a')
        self.eje_espectro.set_xlabel('Frecuencia (Hz)', color='white')
        self.eje_espectro.set_ylabel('Magnitud', color='white')
        self.eje_espectro.tick_params(colors='white')
        self.eje_espectro.grid(True, alpha=0.3)
        
        self.canvas_espectro = FigureCanvasTkAgg(self.figura_espectro, marco_principal)
        self.canvas_espectro.get_tk_widget().pack(pady=10)
        
        self.etiqueta_estado = tk.Label(
            marco_principal,
            text="Esperando audio...",
            font=('Arial', 12),
            bg='#2b2b2b',
            fg='white'
        )
        self.etiqueta_estado.pack(pady=10)
        
        self.dibujar_medidor_inicial()
    
    # Dibuja el medidor de afinacion inicial en posicion neutral
    def dibujar_medidor_inicial(self):
        self.canvas_medidor.delete("all")
        
        self.canvas_medidor.create_line(50, 40, 550, 40, fill='#555555', width=2)
        
        for i in range(-50, 51, 10):
            x = 300 + (i * 5)
            altura = 15 if i % 20 == 0 else 10
            self.canvas_medidor.create_line(x, 40, x, 40 - altura, fill='#888888', width=1)
            
            if i % 20 == 0:
                self.canvas_medidor.create_text(
                    x, 60, 
                    text=str(i), 
                    fill='#aaaaaa', 
                    font=('Arial', 9)
                )
        
        self.canvas_medidor.create_line(300, 20, 300, 60, fill='white', width=3)
        self.canvas_medidor.create_polygon(300, 15, 295, 25, 305, 25, fill='white')
    
    # Actualiza el medidor con la desviacion actual en cents
    def actualizar_medidor(self, cents, color):
        self.canvas_medidor.delete("all")
        
        self.canvas_medidor.create_line(50, 40, 550, 40, fill='#555555', width=2)
        
        for i in range(-50, 51, 10):
            x = 300 + (i * 5)
            altura = 15 if i % 20 == 0 else 10
            self.canvas_medidor.create_line(x, 40, x, 40 - altura, fill='#888888', width=1)
            
            if i % 20 == 0:
                self.canvas_medidor.create_text(
                    x, 60, 
                    text=str(i), 
                    fill='#aaaaaa', 
                    font=('Arial', 9)
                )
        
        cents_limitados = max(-50, min(50, cents))
        posicion_x = 300 + (cents_limitados * 5)
        
        self.canvas_medidor.create_line(posicion_x, 20, posicion_x, 60, fill=color, width=3)
        self.canvas_medidor.create_polygon(
            posicion_x, 15, 
            posicion_x - 5, 25, 
            posicion_x + 5, 25, 
            fill=color
        )
    
    # Actualiza el espectro de frecuencias con nuevos datos
    def actualizar_espectro(self, frecuencias, magnitudes, frecuencia_detectada=None):
        self.eje_espectro.clear()
        self.eje_espectro.plot(frecuencias, magnitudes, color='#00aaff', linewidth=1)
        
        if frecuencia_detectada is not None:
            self.eje_espectro.axvline(
                x=frecuencia_detectada, 
                color='#ff0000', 
                linestyle='--', 
                linewidth=2,
                label=f'Detectada: {frecuencia_detectada:.1f} Hz'
            )
            self.eje_espectro.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white')
        
        self.eje_espectro.set_facecolor('#1a1a1a')
        self.eje_espectro.set_xlabel('Frecuencia (Hz)', color='white')
        self.eje_espectro.set_ylabel('Magnitud', color='white')
        self.eje_espectro.tick_params(colors='white')
        self.eje_espectro.grid(True, alpha=0.3)
        self.canvas_espectro.draw()
    
    # Actualiza todos los elementos de la interfaz con nueva informacion de afinacion
    def actualizar_interfaz(self, info_afinacion, frecuencias=None, magnitudes=None):
        nota = info_afinacion.get('nota', '--')
        nota_espaniol = info_afinacion.get('nota_espaniol', '--')
        frecuencia = info_afinacion.get('frecuencia_detectada', 0.0)
        cents = info_afinacion.get('cents', 0.0)
        estado = info_afinacion.get('estado', 'sin_audio')
        
        color = self.colores.get(estado, self.colores['sin_audio'])
        
        if nota is None:
            self.etiqueta_nota_ingles.config(text="--", fg='white')
            self.etiqueta_nota_espaniol.config(text="--", fg='#aaaaaa')
            self.etiqueta_frecuencia.config(text="Sin senal")
            self.etiqueta_cents.config(text="-- cents")
            self.etiqueta_estado.config(text="Esperando audio...")
            self.dibujar_medidor_inicial()
        else:
            self.etiqueta_nota_ingles.config(text=nota, fg=color)
            self.etiqueta_nota_espaniol.config(text=nota_espaniol, fg=color)
            self.etiqueta_frecuencia.config(text=f"{frecuencia:.2f} Hz")
            self.etiqueta_cents.config(text=f"{cents:+.1f} cents", fg=color)
            
            if estado == 'afinado':
                texto_estado = "AFINADO"
            elif estado == 'cerca':
                texto_estado = "AJUSTAR" if cents > 0 else "AJUSTAR"
            else:
                texto_estado = "DESAFINADO"
            
            self.etiqueta_estado.config(text=texto_estado, fg=color)
            self.actualizar_medidor(cents, color)
        
        if frecuencias is not None and magnitudes is not None:
            self.actualizar_espectro(frecuencias, magnitudes, frecuencia)
    
    # Inicia el bucle principal de la interfaz grafica
    def iniciar(self):
        self.ventana.mainloop()
    
    # Cierra la ventana de la interfaz
    def cerrar(self):
        self.ventana.quit()
        self.ventana.destroy()
    
    # Configura la lista de dispositivos disponibles en el combobox
    def configurar_dispositivos(self, dispositivos, indice_actual=None):
        nombres = [f"{d['nombre']}" for d in dispositivos]
        self.combo_dispositivos['values'] = nombres
        self.dispositivos_info = dispositivos
        
        if indice_actual is not None:
            for i, d in enumerate(dispositivos):
                if d['indice'] == indice_actual:
                    self.combo_dispositivos.current(i)
                    break
        elif len(dispositivos) > 0:
            self.combo_dispositivos.current(0)
    
    # Establece la funcion callback para cuando se cambie el dispositivo
    def establecer_callback_cambio_dispositivo(self, callback):
        self.callback_cambio_dispositivo = callback
        self.combo_dispositivos.bind('<<ComboboxSelected>>', self._manejar_cambio_dispositivo)
    
    # Maneja el evento de cambio de dispositivo en el combobox
    def _manejar_cambio_dispositivo(self, evento):
        if self.callback_cambio_dispositivo:
            indice_seleccionado = self.combo_dispositivos.current()
            if 0 <= indice_seleccionado < len(self.dispositivos_info):
                dispositivo_info = self.dispositivos_info[indice_seleccionado]
                self.callback_cambio_dispositivo(dispositivo_info['indice'])
