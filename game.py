# ---------------------------------------------------------------
# Clue: The Game
# Autor: Rodríguez Jauregui Jared - 22110373
# ---------------------------------------------------------------

# ==================== IMPORTACIONES ====================
import tkinter as tk  # Librería principal para la interfaz gráfica
from tkinter import ttk, messagebox, simpledialog  # Componentes modernos y cuadros de diálogo
import random  # Para generar elementos aleatorios (solución del crimen)
from PIL import ImageTk, Image  # Para manejar imágenes (logo del juego)
from tkinter.font import Font  # Para personalizar fuentes de texto
from tkinter import PhotoImage  # Para mostrar imágenes en la interfaz

# ==================== PALETA DE COLORES ====================
# Colores modernos en modo oscuro (dark mode)
DARK_BG = "#121212"        # Color de fondo principal (casi negro)
CARD_BG = "#1E1E1E"        # Fondo para tarjetas de personajes/armas/lugares
ACCENT_BLUE = "#4FC3F7"    # Azul claro para botones principales
ACCENT_GREEN = "#81C784"   # Verde para acciones positivas (éxito)
ACCENT_ORANGE = "#FFB74D"  # Naranja para advertencias
ACCENT_RED = "#E57373"     # Rojo para errores o peligro
TEXT_WHITE = "#E0E0E0"     # Texto principal (blanco suave)
TEXT_SECONDARY = "#9E9E9E" # Texto secundario (gris claro)
HIGHLIGHT = "#03A9F4"      # Azul brillante para elementos destacados

# ==================== CLASE GAMEDATA ====================
class GameData:
    """Clase que maneja todos los datos del juego: personajes, armas, lugares y la solución"""
    
    def __init__(self):
        """Constructor: inicializa los datos al crear una instancia del juego"""
        self.cargar_datos()  # Carga los datos iniciales
        self.solucion = {}   # Diccionario para guardar la solución correcta del crimen
        
    def cargar_datos(self):
        """Carga/Inicializa todos los datos del juego en diccionarios estructurados"""
        
        # Diccionario de personajes sospechosos con sus características:
        # Formato: "Nombre": [Descripción, Emoji, Pista oculta]
        self.personajes = {
            "Laura Salinas": ["Chef famosa", "🔪", "Tiene un tatuaje de un cuchillo"],
            "Eduardo Torres": ["Empresario millonario", "💼", "Siempre lleva un maletín"],
            "Renata Cruz": ["Actriz de teatro", "🎭", "Fue vista discutiendo con la víctima"],
            "Dr. Samuel Rivas": ["Cirujano plástico", "💉", "Tenía acceso a medicamentos peligrosos"],
            "Carlos Mendoza": ["Fotógrafo", "📸", "Tiene fotos comprometedoras de varios invitados"]
        }

        # Diccionario de lugares posibles donde ocurrió el crimen:
        # Formato: "Lugar": [Emoji, Descripción]
        self.lugares = {
            "Biblioteca antigua": ["📚", "Está en el ala este de la mansión"],
            "Cocina principal": ["🔪", "Todos los cuchillos están afilados"],
            "Sala de juegos": ["🎲", "Hay manchas sospechosas en la alfombra"],
            "Habitación secreta": ["🔍", "Solo algunos invitados conocían su ubicación"],
            "Sótano": ["🕯️", "La luz falla frecuentemente"]
        }

        # Diccionario de armas posibles utilizadas en el crimen:
        # Formato: "Arma": [Emoji, Descripción]
        self.armas = {
            "Candelabro": ["🕯️", "Pesado y contundente"],
            "Cuchillo de cocina": ["🔪", "Filudo y preciso"],
            "Estatua de mármol": ["🗿", "Pesada y difícil de mover"],
            "Pistola antigua": ["🔫", "Ruidoso pero efectivo"],
            "Jeringa con veneno": ["💉", "Silencioso y letal"]
        }

        # Lista de motivos posibles para el crimen:
        self.motivos = [
            "Venganza por un pasado oscuro",
            "Cobertura de un secreto inconfesable",
            "Herida de amor no correspondido",
            "Ambición desmedida por dinero",
            "Accidente que se convirtió en crimen"
        ]
    
    def generar_solucion(self):
        """Genera una nueva solución aleatoria para el crimen"""
        self.solucion = {
            'culpable': random.choice(list(self.personajes.keys())),  # Elige personaje aleatorio
            'arma': random.choice(list(self.armas.keys())),           # Elige arma aleatoria
            'lugar': random.choice(list(self.lugares.keys())),        # Elige lugar aleatorio
            'motivo': random.choice(self.motivos)                     # Elige motivo aleatorio
        }
        return self.solucion  # Devuelve la solución generada

# ==================== CLASE PRINCIPAL DEL JUEGO ====================
class ClueGame:
    """Clase principal que controla la interfaz gráfica y la lógica del juego"""
    
    def __init__(self, root):
        """Inicializa la ventana principal y configura el juego"""
        self.root = root  # Ventana principal de tkinter
        self.root.title("🕵️‍♀️ Mystery Murder Game")  # Título de la ventana
        self.root.state('zoomed')  # Maximiza la ventana al iniciar
        self.root.configure(bg=DARK_BG)  # Establece el color de fondo
        
        # Configuración inicial
        self.setup_styles()  # Define los estilos visuales
        self.load_logo_images()  # Carga las imágenes del logo
        
        # Datos del juego
        self.game_data = GameData()  # Crea una instancia de GameData para manejar la información
        
        # Variables de estado del juego
        self.intentos = 0  # Contador de intentos del jugador
        
        # Interfaz inicial
        self.menu_principal()  # Muestra el menú principal

    def load_logo_images(self):
        """Carga las imágenes del logo en diferentes tamaños para el menú y el juego"""
        try:
            # Intenta cargar la imagen original
            original_img = Image.open("clue.png")
            
            # Crea versión grande para el menú principal (350x120 píxeles)
            self.logo_large = ImageTk.PhotoImage(original_img.resize((350, 120), Image.LANCZOS))
            
            # Crea versión mediana para la ventana de juego (250x90 píxeles)
            self.logo_medium = ImageTk.PhotoImage(original_img.resize((250, 90), Image.LANCZOS))
        except Exception as e:
            # Si hay error al cargar la imagen, usa texto alternativo
            print(f"Error cargando logo: {e}")
            self.logo_large = None
            self.logo_medium = None

    def setup_styles(self):
        """Configura los estilos visuales de la interfaz"""
        
        # Fuentes personalizadas
        self.title_font = Font(family="Helvetica", size=24, weight="bold")  # Fuente para títulos
        self.label_font = Font(family="Helvetica", size=14)  # Fuente para etiquetas
        self.button_font = Font(family="Helvetica", size=12)  # Fuente para botones
        
        # Configuración del estilo general
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Usa el tema 'clam' de tkinter
        
        # Estilo base
        self.style.configure('.', background=DARK_BG, foreground=TEXT_WHITE)
        self.style.configure('TFrame', background=DARK_BG)
        self.style.configure('TLabel', background=DARK_BG, foreground=TEXT_WHITE)
        self.style.configure('TNotebook', background=DARK_BG)
        
        # Estilo para radio buttons (opciones de selección)
        self.style.configure('TRadiobutton', 
                           background=CARD_BG, 
                           foreground=TEXT_WHITE,
                           font=self.label_font)
        
        # Estilo para las pestañas (notebook tabs)
        self.style.configure('TNotebook.Tab', 
                           background=CARD_BG,
                           foreground=ACCENT_BLUE,
                           padding=[10, 5],
                           font=('Helvetica', 10, 'bold'))
        
        # Mapeo de estados para pestañas (colores al seleccionar)
        self.style.map('TNotebook.Tab',
                      background=[('selected', DARK_BG), ('active', "#2E2E2E")],
                      foreground=[('selected', ACCENT_BLUE), ('active', TEXT_WHITE)])

    def menu_principal(self):
        """Crea y muestra la ventana del menú principal"""
        
        # Crea una nueva ventana para el menú
        self.menu_window = tk.Toplevel(self.root)
        self.menu_window.title("Clue")  # Título de la ventana
        self.menu_window.geometry("600x400")  # Tamaño de la ventana
        self.menu_window.configure(bg=DARK_BG)  # Color de fondo
        
        # Frame principal para organizar elementos
        main_frame = tk.Frame(self.menu_window, bg=DARK_BG)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Mostrar el logo (si se cargó correctamente)
        if self.logo_large:
            logo_label = tk.Label(
                main_frame,
                image=self.logo_large,
                bg=DARK_BG
            )
            logo_label.pack(pady=(0, 30))  # Espaciado inferior
        else:
            # Alternativa si no hay imagen: mostrar texto
            tk.Label(
                main_frame,
                text="🔍 MYSTERY MURDER GAME",
                font=self.title_font,
                bg=DARK_BG,
                fg=ACCENT_BLUE
            ).pack(pady=(0, 30))

        # Frame para los botones del menú
        button_frame = tk.Frame(main_frame, bg=DARK_BG)
        button_frame.pack(pady=20)

        # Botón "Jugar"
        tk.Button(
            button_frame,
            text="Jugar",
            command=self.iniciar_juego,  # Al hacer clic, inicia el juego
            bg=ACCENT_BLUE,
            fg=DARK_BG,
            font=self.button_font,
            bd=0,  # Sin borde
            padx=20,  # Espaciado horizontal
            pady=10,  # Espaciado vertical
            activebackground=HIGHLIGHT  # Color al hacer clic
        ).pack(side="left", padx=10)  # Posición a la izquierda

        # Botón "Salir"
        tk.Button(
            button_frame,
            text="Salir",
            command=self.root.quit,  # Cierra la aplicación
            bg=ACCENT_RED,
            fg=DARK_BG,
            font=self.button_font,
            bd=0,
            padx=20,
            pady=10,
            activebackground="#D32F2F"  # Rojo oscuro al hacer clic
        ).pack(side="left", padx=10)

    def iniciar_juego(self):
        """Inicializa un nuevo juego con una solución aleatoria"""
        
        # Cierra la ventana del menú si está abierta
        if hasattr(self, 'menu_window') and self.menu_window.winfo_exists():
            self.menu_window.destroy()
        
        # Genera una nueva solución aleatoria
        self.game_data.generar_solucion()
        self.intentos = 0  # Reinicia el contador de intentos
        
        # Crea la interfaz del juego
        self.crear_interfaz_juego()

    def crear_interfaz_juego(self):
        """Configura la interfaz principal del juego"""
        
        # Crea una nueva ventana para el juego
        self.juego_window = tk.Toplevel(self.root)
        self.juego_window.title("Resolver el crimen")  # Título
        self.juego_window.geometry("1000x700")  # Tamaño
        self.juego_window.configure(bg=DARK_BG)  # Color de fondo

        # Frame principal para organizar elementos
        main_frame = ttk.Frame(self.juego_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame para el encabezado (logo y contador de intentos)
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Mostrar logo en la ventana de juego (versión mediana)
        if self.logo_medium:
            logo_label = tk.Label(
                header_frame,
                image=self.logo_medium,
                bg=DARK_BG
            )
            logo_label.pack(side=tk.LEFT)  # Alineado a la izquierda
        else:
            # Alternativa con texto si no hay imagen
            tk.Label(
                header_frame,
                text="🔍 MYSTERY MURDER GAME",
                font=self.title_font,
                bg=DARK_BG,
                fg=ACCENT_BLUE
            ).pack(side=tk.LEFT)

        # Etiqueta para mostrar el número de intentos
        self.intentos_label = tk.Label(
            header_frame,
            text=f"INTENTOS: {self.intentos}",
            font=("Helvetica", 12, "bold"),
            bg=DARK_BG,
            fg=ACCENT_ORANGE
        )
        self.intentos_label.pack(side=tk.RIGHT)  # Alineado a la derecha

        # Historia/contexto del juego
        story_label = tk.Label(
            main_frame,
            text=("Un misterioso crimen ha ocurrido en la mansión Salinas. "
                  "Como detective estrella, tu misión es descubrir quién fue el culpable, "
                  "qué arma usó y dónde sucedió el crimen. ¡Buena suerte!"),
            font=("Helvetica", 12),
            wraplength=800,  # Ancho máximo antes de saltar de línea
            justify="center",  # Texto centrado
            bg=DARK_BG,
            fg=TEXT_WHITE
        )
        story_label.pack(pady=(0, 20))  # Espaciado inferior

        # Notebook (pestañas) para organizar las categorías
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Variables para almacenar las selecciones del jugador
        self.eleccion_culpable = tk.StringVar()  # Almacena el personaje seleccionado
        self.eleccion_arma = tk.StringVar()      # Almacena el arma seleccionada
        self.eleccion_lugar = tk.StringVar()     # Almacena el lugar seleccionado

        # Crear las pestañas para cada categoría
        self.crear_pestana("SOSPECHOSOS", self.game_data.personajes, self.eleccion_culpable)
        self.crear_pestana("ARMAS", self.game_data.armas, self.eleccion_arma)
        self.crear_pestana("LUGARES", self.game_data.lugares, self.eleccion_lugar)

        # Frame para los botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        # Botón "Resolver Caso" (verifica la solución)
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

        # Botón "Obtener Pista" (muestra una pista)
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

        # Botón "Volver al Menú" (regresa al menú principal)
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

        # Botón "Nuevo Juego" (reinicia con nueva solución)
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
        """Crea una pestaña con scroll para mostrar las opciones de una categoría"""
        
        # Frame principal para la pestaña
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=titulo)  # Añade la pestaña al notebook

        # Canvas y scrollbar para permitir desplazamiento
        canvas = tk.Canvas(frame, bg=DARK_BG, highlightthickness=0)  # Canvas sin borde
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)  # Barra de desplazamiento
        scrollable_frame = ttk.Frame(canvas)  # Frame que contendrá los elementos

        # Configura el canvas para que sea scrollable
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")  # Ajusta la región de desplazamiento
            )
        )

        # Añade el frame scrollable al canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)  # Conecta el scrollbar al canvas

        # Crea un RadioButton para cada elemento en la categoría
        for item, detalles in datos.items():
            emoji = detalles[0]  # Obtiene el emoji del elemento
            descripcion = f"{emoji} {item} - {detalles[1]}"  # Crea la descripción completa
            
            # RadioButton para seleccionar el elemento
            rb = ttk.Radiobutton(
                scrollable_frame,
                text=descripcion,
                variable=variable,
                value=item,
                style='TRadiobutton'
            )
            rb.pack(anchor="w", padx=10, pady=5, fill=tk.X)  # Alineado a la izquierda

        # Empaqueta el canvas y el scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def verificar_solucion(self):
        """Verifica si la solución propuesta por el jugador es correcta"""
        
        # Obtiene las selecciones del jugador
        seleccion = {
            'culpable': self.eleccion_culpable.get(),  # Personaje seleccionado
            'arma': self.eleccion_arma.get(),          # Arma seleccionada
            'lugar': self.eleccion_lugar.get()         # Lugar seleccionado
        }
        
        # Verifica que el jugador haya seleccionado todas las opciones
        if not all(seleccion.values()):
            self.mostrar_mensaje("Advertencia", "¡Debes seleccionar un sospechoso, un arma y un lugar!", False)
            return
        
        # Incrementa el contador de intentos
        self.intentos += 1
        self.intentos_label.config(text=f"INTENTOS: {self.intentos}")
        
        # Compara las selecciones con la solución correcta
        correcto = all(seleccion[k] == self.game_data.solucion[k] for k in seleccion)
        
        if correcto:
            self.mostrar_victoria()  # Muestra pantalla de victoria
        else:
            self.mostrar_pistas(seleccion)  # Muestra pistas sobre el error

    def mostrar_victoria(self):
        """Muestra la pantalla de victoria con la solución correcta"""
        
        solucion = self.game_data.solucion  # Obtiene la solución correcta
        
        # Construye el mensaje de victoria con los detalles
        msg = (f"🎉 ¡FELICIDADES! Resolviste el caso en {self.intentos} intento(s).\n\n"
               f"🔪 Culpable: {solucion['culpable']} ({self.game_data.personajes[solucion['culpable']][1]})\n"
               f"💣 Arma: {solucion['arma']} ({self.game_data.armas[solucion['arma']][1]})\n"
               f"🏛️ Lugar: {solucion['lugar']} ({self.game_data.lugares[solucion['lugar']][1]})\n"
               f"📖 Motivo: {solucion['motivo']}")
        
        # Muestra el mensaje en un popup especial
        self.mostrar_mensaje_con_continuar("¡Caso Resuelto!", msg, True)

    def mostrar_pistas(self, seleccion):
        """Muestra pistas sobre qué está mal en la solución del jugador"""
        
        pistas = []  # Lista para almacenar las pistas
        
        # Compara cada selección con la solución correcta
        for clave, valor in seleccion.items():
            if valor != self.game_data.solucion[clave]:
                pistas.append(f"❌ El {clave} no es {valor}")
        
        # Añade una pista adicional después de 3 intentos
        if self.intentos >= 3:
            pistas.append("\n💡 Pista adicional: " + self.obtener_pista_aleatoria())
        
        # Construye el mensaje final
        msg = ("🔍 Pistas para tu próxima investigación:\n\n" +
               "\n".join(pistas) +
               "\n\nSigue intentando, detective...")
        
        # Muestra el mensaje en un popup
        self.mostrar_mensaje_con_continuar("Caso No Resuelto", msg, False)

    def obtener_pista_aleatoria(self):
        """Genera una pista aleatoria sobre la solución correcta"""
        
        opciones = [
            f"El culpable {self.game_data.personajes[self.game_data.solucion['culpable']][2]}",
            f"El arma {self.game_data.armas[self.game_data.solucion['arma']][1].lower()}",
            f"El lugar {self.game_data.lugares[self.game_data.solucion['lugar']][1].lower()}",
            f"El motivo involucraba {random.choice(['dinero', 'amor', 'venganza', 'un secreto'])}"
        ]
        return random.choice(opciones)  # Devuelve una pista aleatoria

    def mostrar_pista(self):
        """Muestra una pista específica al jugador"""
        
        # No da pistas si no ha intentado resolver
        if self.intentos == 0:
            self.mostrar_mensaje("Pista", "Primero intenta resolver el caso para obtener pistas.", False)
            return
        
        # Obtiene y muestra una pista aleatoria
        pista = self.obtener_pista_aleatoria()
        self.mostrar_mensaje("💡 Pista", pista, None)

    def volver_al_menu(self):
        """Cierra la ventana de juego y regresa al menú principal"""
        self.juego_window.destroy()  # Cierra la ventana de juego
        self.menu_principal()       # Muestra el menú principal

    def reiniciar_juego(self):
        """Reinicia el juego con una nueva solución aleatoria"""
        self.juego_window.destroy()  # Cierra la ventana actual
        self.iniciar_juego()         # Inicia un nuevo juego

    def mostrar_mensaje(self, titulo, mensaje, es_exito):
        """Muestra un mensaje básico con icono según el resultado"""
        
        # Determina el icono y color según el tipo de mensaje
        icono = "✅" if es_exito else "❌" if es_exito is False else "💡"
        color = ACCENT_GREEN if es_exito else ACCENT_RED if es_exito is False else ACCENT_BLUE
        
        # Muestra el mensaje usando messagebox de tkinter
        messagebox.showinfo(titulo, f"{icono} {mensaje}")

    def mostrar_mensaje_con_continuar(self, titulo, mensaje, es_exito):
        """Muestra un mensaje personalizado con botones de acción"""
        
        # Crea una ventana emergente personalizada
        popup = tk.Toplevel(self.juego_window if hasattr(self, 'juego_window') else self.root)
        popup.title(titulo)  # Título de la ventana
        popup.geometry("500x300")  # Tamaño
        popup.configure(bg=CARD_BG)  # Color de fondo
        
        # Determina icono y color según el resultado
        icono = "✓" if es_exito else "✗" if es_exito is False else "💡"
        color = ACCENT_GREEN if es_exito else ACCENT_ORANGE if es_exito is False else ACCENT_BLUE
        
        # Muestra el icono grande
        tk.Label(
            popup,
            text=icono,
            font=("Helvetica", 50),
            bg=CARD_BG,
            fg=color
        ).pack(pady=(20, 10))
        
        # Muestra el mensaje principal
        tk.Label(
            popup,
            text=mensaje,
            font=("Helvetica", 12),
            wraplength=450,  # Ancho máximo antes de saltar de línea
            justify="left",  # Alineación izquierda
            bg=CARD_BG,
            fg=TEXT_WHITE
        ).pack(pady=10, padx=20)
        
        # Frame para los botones
        button_frame = tk.Frame(popup, bg=CARD_BG)
        button_frame.pack(pady=10)
        
        # Botón "Continuar" (cierra el popup)
        tk.Button(
            button_frame,
            text="CONTINUAR",
            command=popup.destroy,  # Cierra la ventana
            bg=color,
            fg=DARK_BG,
            font=("Helvetica", 12, "bold"),
            bd=0,
            padx=20,
            pady=5,
            activebackground=HIGHLIGHT if color == ACCENT_BLUE else "#66BB6A" if color == ACCENT_GREEN else "#FB8C00"
        ).pack(side=tk.LEFT, padx=10)
        
        # Botón "Nuevo Juego" solo aparece en victoria
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
        
        # Hace que el popup sea modal (el usuario debe interactuar primero)
        popup.grab_set()
        popup.wait_window()

# ==================== INICIO DEL PROGRAMA ====================
if __name__ == "__main__":
    root = tk.Tk()          # Crea la ventana principal de tkinter
    app = ClueGame(root)    # Inicia nuestra aplicación ClueGame
    root.withdraw()         # Oculta la ventana principal temporalmente
    root.mainloop()         # Inicia el bucle principal de la aplicación