#RODRIGUEZ JAUREGUI JARED 22110373

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
from PIL import ImageTk, Image
from tkinter.font import Font
from tkinter import PhotoImage

# Paleta de colores moderna
DARK_BG = "#121212"        # Fondo principal oscuro
CARD_BG = "#1E1E1E"        # Fondo de tarjetas y elementos
ACCENT_BLUE = "#4FC3F7"    # Azul claro para botones principales
ACCENT_GREEN = "#81C784"   # Verde para acciones positivas
ACCENT_ORANGE = "#FFB74D"  # Naranja para advertencias
ACCENT_RED = "#E57373"     # Rojo suave para errores
TEXT_WHITE = "#E0E0E0"     # Texto principal
TEXT_SECONDARY = "#9E9E9E" # Texto secundario
HIGHLIGHT = "#03A9F4"      # Destacado (azul más intenso)

class GameData:
    """Clase para manejar todos los datos del juego"""
    def __init__(self):
        self.cargar_datos()
        self.solucion = {}
        
    def cargar_datos(self):
        """Inicializa los datos del juego"""
        self.personajes = {
            "Laura Salinas": ["Chef famosa", "🔪", "Tiene un tatuaje de un cuchillo"],
            "Eduardo Torres": ["Empresario millonario", "💼", "Siempre lleva un maletín"],
            "Renata Cruz": ["Actriz de teatro", "🎭", "Fue vista discutiendo con la víctima"],
            "Dr. Samuel Rivas": ["Cirujano plástico", "💉", "Tenía acceso a medicamentos peligrosos"],
            "Carlos Mendoza": ["Fotógrafo", "📸", "Tiene fotos comprometedoras de varios invitados"]
        }

        self.lugares = {
            "Biblioteca antigua": ["📚", "Está en el ala este de la mansión"],
            "Cocina principal": ["🔪", "Todos los cuchillos están afilados"],
            "Sala de juegos": ["🎲", "Hay manchas sospechosas en la alfombra"],
            "Habitación secreta": ["🔍", "Solo algunos invitados conocían su ubicación"],
            "Sótano": ["🕯️", "La luz falla frecuentemente"]
        }

        self.armas = {
            "Candelabro": ["🕯️", "Pesado y contundente"],
            "Cuchillo de cocina": ["🔪", "Filudo y preciso"],
            "Estatua de mármol": ["🗿", "Pesada y difícil de mover"],
            "Pistola antigua": ["🔫", "Ruidoso pero efectivo"],
            "Jeringa con veneno": ["💉", "Silencioso y letal"]
        }

        self.motivos = [
            "Venganza por un pasado oscuro",
            "Cobertura de un secreto inconfesable",
            "Herida de amor no correspondido",
            "Ambición desmedida por dinero",
            "Accidente que se convirtió en crimen"
        ]
    
    def generar_solucion(self):
        """Genera una nueva solución aleatoria"""
        self.solucion = {
            'culpable': random.choice(list(self.personajes.keys())),
            'arma': random.choice(list(self.armas.keys())),
            'lugar': random.choice(list(self.lugares.keys())),
            'motivo': random.choice(self.motivos)
        }
        return self.solucion

class ClueGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🕵️‍♀️ Mystery Murder Game")
        self.root.state('zoomed')
        self.root.configure(bg=DARK_BG)
        
        # Configurar estilo
        self.setup_styles()
        
        # Cargar imágenes del logo (solo para menú y juego)
        self.load_logo_images()
        
        # Datos del juego
        self.game_data = GameData()
        
        # Variables de estado
        self.intentos = 0
        
        # Crear menú principal
        self.menu_principal()

    def load_logo_images(self):
        """Carga las imágenes del logo para menú y juego"""
        try:
            original_img = Image.open("clue.png")
            # Tamaño grande para menú principal
            self.logo_large = ImageTk.PhotoImage(original_img.resize((350, 120), Image.LANCZOS))
            # Tamaño mediano para ventana de juego
            self.logo_medium = ImageTk.PhotoImage(original_img.resize((250, 90), Image.LANCZOS))
        except Exception as e:
            print(f"Error cargando logo: {e}")
            self.logo_large = None
            self.logo_medium = None

    def setup_styles(self):
        """Configura los estilos visuales"""
        self.title_font = Font(family="Helvetica", size=24, weight="bold")
        self.label_font = Font(family="Helvetica", size=14)
        self.button_font = Font(family="Helvetica", size=12)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configuración principal
        self.style.configure('.', background=DARK_BG, foreground=TEXT_WHITE)
        self.style.configure('TFrame', background=DARK_BG)
        self.style.configure('TLabel', background=DARK_BG, foreground=TEXT_WHITE)
        self.style.configure('TNotebook', background=DARK_BG)
        self.style.configure('TRadiobutton', background=CARD_BG, foreground=TEXT_WHITE, font=self.label_font)
        
        # Estilo de las pestañas
        self.style.configure('TNotebook.Tab', 
                           background=CARD_BG, 
                           foreground=ACCENT_BLUE,
                           padding=[10, 5],
                           font=('Helvetica', 10, 'bold'))
        self.style.map('TNotebook.Tab',
                     background=[('selected', DARK_BG), ('active', "#2E2E2E")],
                     foreground=[('selected', ACCENT_BLUE), ('active', TEXT_WHITE)])

    def menu_principal(self):
        """Crea la ventana de inicio con el logo"""
        self.menu_window = tk.Toplevel(self.root)
        self.menu_window.title("Clue")
        self.menu_window.geometry("600x400")
        self.menu_window.configure(bg=DARK_BG)
        
        # Frame principal para centrar contenido
        main_frame = tk.Frame(self.menu_window, bg=DARK_BG)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Mostrar logo en el menú principal
        if self.logo_large:
            logo_label = tk.Label(
                main_frame,
                image=self.logo_large,
                bg=DARK_BG
            )
            logo_label.pack(pady=(0, 30))
        else:
            # Fallback si no carga la imagen
            tk.Label(
                main_frame,
                text="🔍 MYSTERY MURDER GAME",
                font=self.title_font,
                bg=DARK_BG,
                fg=ACCENT_BLUE
            ).pack(pady=(0, 30))

        button_frame = tk.Frame(main_frame, bg=DARK_BG)
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Jugar",
            command=self.iniciar_juego,
            bg=ACCENT_BLUE,
            fg=DARK_BG,
            font=self.button_font,
            bd=0,
            padx=20,
            pady=10,
            activebackground=HIGHLIGHT
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Salir",
            command=self.root.quit,
            bg=ACCENT_RED,
            fg=DARK_BG,
            font=self.button_font,
            bd=0,
            padx=20,
            pady=10,
            activebackground="#D32F2F"
        ).pack(side="left", padx=10)

    def iniciar_juego(self):
        """Inicializa un nuevo juego"""
        if hasattr(self, 'menu_window') and self.menu_window.winfo_exists():
            self.menu_window.destroy()
        self.game_data.generar_solucion()
        self.intentos = 0
        self.crear_interfaz_juego()

    def crear_interfaz_juego(self):
        """Configura la interfaz del juego con logo"""
        self.juego_window = tk.Toplevel(self.root)
        self.juego_window.title("Resolver el crimen")
        self.juego_window.geometry("1000x700")
        self.juego_window.configure(bg=DARK_BG)

        # Frame principal
        main_frame = ttk.Frame(self.juego_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Encabezado con logo
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Mostrar logo en la ventana de juego
        if self.logo_medium:
            logo_label = tk.Label(
                header_frame,
                image=self.logo_medium,
                bg=DARK_BG
            )
            logo_label.pack(side=tk.LEFT)
        else:
            tk.Label(
                header_frame,
                text="🔍 MYSTERY MURDER GAME",
                font=self.title_font,
                bg=DARK_BG,
                fg=ACCENT_BLUE
            ).pack(side=tk.LEFT)

        self.intentos_label = tk.Label(
            header_frame,
            text=f"INTENTOS: {self.intentos}",
            font=("Helvetica", 12, "bold"),
            bg=DARK_BG,
            fg=ACCENT_ORANGE
        )
        self.intentos_label.pack(side=tk.RIGHT)

        # Historia
        story_label = tk.Label(
            main_frame,
            text=("Un misterioso crimen ha ocurrido en la mansión Salinas. "
                  "Como detective estrella, tu misión es descubrir quién fue el culpable, "
                  "qué arma usó y dónde sucedió el crimen. ¡Buena suerte!"),
            font=("Helvetica", 12),
            wraplength=800,
            justify="center",
            bg=DARK_BG,
            fg=TEXT_WHITE
        )
        story_label.pack(pady=(0, 20))

        # Notebook (pestañas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Variables de selección
        self.eleccion_culpable = tk.StringVar()
        self.eleccion_arma = tk.StringVar()
        self.eleccion_lugar = tk.StringVar()

        # Crear pestañas con colores mejorados
        self.crear_pestana("SOSPECHOSOS", self.game_data.personajes, self.eleccion_culpable)
        self.crear_pestana("ARMAS", self.game_data.armas, self.eleccion_arma)
        self.crear_pestana("LUGARES", self.game_data.lugares, self.eleccion_lugar)

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        tk.Button(
            button_frame,
            text="🔎 Resolver Caso",
            command=self.verificar_solucion,
            bg=ACCENT_BLUE,
            fg=DARK_BG,
            font=self.button_font,
            bd=0,
            padx=20,
            pady=10,
            activebackground=HIGHLIGHT
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="💡 Obtener Pista",
            command=self.mostrar_pista,
            bg=ACCENT_GREEN,
            fg=DARK_BG,
            font=self.button_font,
            bd=0,
            padx=20,
            pady=10,
            activebackground="#66BB6A"
        ).pack(side=tk.LEFT, padx=10)

        # Botón de volver al menú
        tk.Button(
            button_frame,
            text="← Volver al Menú",
            command=self.volver_al_menu,
            bg=TEXT_SECONDARY,
            fg=DARK_BG,
            font=self.button_font,
            bd=0,
            padx=20,
            pady=10,
            activebackground="#616161"
        ).pack(side=tk.RIGHT, padx=5)

        tk.Button(
            button_frame,
            text="🔄 Nuevo Juego",
            command=self.reiniciar_juego,
            bg=ACCENT_ORANGE,
            fg=DARK_BG,
            font=self.button_font,
            bd=0,
            padx=20,
            pady=10,
            activebackground="#FB8C00"
        ).pack(side=tk.RIGHT, padx=5)

    def crear_pestana(self, titulo, datos, variable):
        """Crea una pestaña con scroll para los elementos del juego"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=titulo)

        # Canvas y scrollbar
        canvas = tk.Canvas(frame, bg=DARK_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Radio buttons para cada elemento
        for item, detalles in datos.items():
            emoji = detalles[0]
            descripcion = f"{emoji} {item} - {detalles[1]}"
            
            rb = ttk.Radiobutton(
                scrollable_frame,
                text=descripcion,
                variable=variable,
                value=item,
                style='TRadiobutton'
            )
            rb.pack(anchor="w", padx=10, pady=5, fill=tk.X)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def verificar_solucion(self):
        """Verifica si la solución propuesta es correcta"""
        seleccion = {
            'culpable': self.eleccion_culpable.get(),
            'arma': self.eleccion_arma.get(),
            'lugar': self.eleccion_lugar.get()
        }
        
        if not all(seleccion.values()):
            self.mostrar_mensaje("Advertencia", "¡Debes seleccionar un sospechoso, un arma y un lugar!", False)
            return
        
        self.intentos += 1
        self.intentos_label.config(text=f"INTENTOS: {self.intentos}")
        
        correcto = all(seleccion[k] == self.game_data.solucion[k] for k in seleccion)
        
        if correcto:
            self.mostrar_victoria()
        else:
            self.mostrar_pistas(seleccion)

    def mostrar_victoria(self):
        """Muestra la pantalla de victoria"""
        solucion = self.game_data.solucion
        msg = (f"🎉 ¡FELICIDADES! Resolviste el caso en {self.intentos} intento(s).\n\n"
               f"🔪 Culpable: {solucion['culpable']} ({self.game_data.personajes[solucion['culpable']][1]})\n"
               f"💣 Arma: {solucion['arma']} ({self.game_data.armas[solucion['arma']][1]})\n"
               f"🏛️ Lugar: {solucion['lugar']} ({self.game_data.lugares[solucion['lugar']][1]})\n"
               f"📖 Motivo: {solucion['motivo']}")
        
        self.mostrar_mensaje_con_continuar("¡Caso Resuelto!", msg, True)

    def mostrar_pistas(self, seleccion):
        """Muestra pistas sobre qué está mal en la solución"""
        pistas = []
        for clave, valor in seleccion.items():
            if valor != self.game_data.solucion[clave]:
                pistas.append(f"❌ El {clave} no es {valor}")
        
        # Pista adicional después de 3 intentos
        if self.intentos >= 3:
            pistas.append("\n💡 Pista adicional: " + self.obtener_pista_aleatoria())
        
        msg = ("🔍 Pistas para tu próxima investigación:\n\n" +
               "\n".join(pistas) +
               "\n\nSigue intentando, detective...")
        
        self.mostrar_mensaje_con_continuar("Caso No Resuelto", msg, False)

    def obtener_pista_aleatoria(self):
        """Devuelve una pista aleatoria sobre la solución"""
        opciones = [
            f"El culpable {self.game_data.personajes[self.game_data.solucion['culpable']][2]}",
            f"El arma {self.game_data.armas[self.game_data.solucion['arma']][1].lower()}",
            f"El lugar {self.game_data.lugares[self.game_data.solucion['lugar']][1].lower()}",
            f"El motivo involucraba {random.choice(['dinero', 'amor', 'venganza', 'un secreto'])}"
        ]
        return random.choice(opciones)

    def mostrar_pista(self):
        """Muestra una pista específica al jugador"""
        if self.intentos == 0:
            self.mostrar_mensaje("Pista", "Primero intenta resolver el caso para obtener pistas.", False)
            return
        
        pista = self.obtener_pista_aleatoria()
        self.mostrar_mensaje("💡 Pista", pista, None)

    def volver_al_menu(self):
        """Cierra la ventana de juego y vuelve al menú principal"""
        self.juego_window.destroy()
        self.menu_principal()

    def reiniciar_juego(self):
        """Reinicia el juego con una nueva solución"""
        self.juego_window.destroy()
        self.iniciar_juego()

    def mostrar_mensaje(self, titulo, mensaje, es_exito):
        """Muestra un mensaje personalizado básico"""
        icono = "✅" if es_exito else "❌" if es_exito is False else "💡"
        color = ACCENT_GREEN if es_exito else ACCENT_RED if es_exito is False else ACCENT_BLUE
        messagebox.showinfo(titulo, f"{icono} {mensaje}")

    def mostrar_mensaje_con_continuar(self, titulo, mensaje, es_exito):
        """Muestra un mensaje personalizado con botón de continuar (sin logo)"""
        popup = tk.Toplevel(self.juego_window if hasattr(self, 'juego_window') else self.root)
        popup.title(titulo)
        popup.geometry("500x300")
        popup.configure(bg=CARD_BG)
        
        # Icono (sin logo)
        icono = "✓" if es_exito else "✗" if es_exito is False else "💡"
        color = ACCENT_GREEN if es_exito else ACCENT_ORANGE if es_exito is False else ACCENT_BLUE
        
        tk.Label(
            popup,
            text=icono,
            font=("Helvetica", 50),
            bg=CARD_BG,
            fg=color
        ).pack(pady=(20, 10))
        
        # Mensaje
        tk.Label(
            popup,
            text=mensaje,
            font=("Helvetica", 12),
            wraplength=450,
            justify="left",
            bg=CARD_BG,
            fg=TEXT_WHITE
        ).pack(pady=10, padx=20)
        
        # Frame para botones
        button_frame = tk.Frame(popup, bg=CARD_BG)
        button_frame.pack(pady=10)
        
        # Botón de continuar
        tk.Button(
            button_frame,
            text="CONTINUAR",
            command=popup.destroy,
            bg=color,
            fg=DARK_BG,
            font=("Helvetica", 12, "bold"),
            bd=0,
            padx=20,
            pady=5,
            activebackground=HIGHLIGHT if color == ACCENT_BLUE else "#66BB6A" if color == ACCENT_GREEN else "#FB8C00"
        ).pack(side=tk.LEFT, padx=10)
        
        # Solo mostrar botón de nuevo juego si es victoria
        if es_exito:
            tk.Button(
                button_frame,
                text="NUEVO JUEGO",
                command=lambda: [popup.destroy(), self.reiniciar_juego()],
                bg=ACCENT_BLUE,
                fg=DARK_BG,
                font=("Helvetica", 12, "bold"),
                bd=0,
                padx=20,
                pady=5,
                activebackground=HIGHLIGHT
            ).pack(side=tk.LEFT, padx=10)
        
        popup.grab_set()
        popup.wait_window()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClueGame(root)
    root.withdraw()
    root.mainloop()