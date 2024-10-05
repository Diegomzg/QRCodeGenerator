import qrcode
from PIL import Image, ImageDraw

# Datos que se codificarán en el QR
data = "https://www.example.com"

# Crear una instancia de QRCode con personalización
qr = qrcode.QRCode(
    version=1,  # controla el tamaño del QR Code (1 a 40)
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # nivel de corrección de errores (L, M, Q, H)
    box_size=10,  # tamaño de cada "caja" del QR code
    border=4,  # tamaño del borde
)

# Agregar datos al QR Code
qr.add_data(data)
qr.make(fit=True)

# Crear una imagen del QR Code con colores personalizados
img = qr.make_image(fill_color="blue", back_color="white")

# Convertir a modo RGBA para poder agregar una imagen con transparencia
img = img.convert("RGBA")

# Añadir un logotipo en el centro del QR Code
logo = Image.open("CDC.png")  # Cambia "path/to/logo.png" por la ruta a tu logotipo

# Redimensionar el logotipo
basewidth = 50  # Define el ancho deseado del logotipo
wpercent = (basewidth / float(logo.size[0]))  # Calcula el porcentaje de reducción
hsize = int((float(logo.size[1]) * float(wpercent)))  # Calcula la altura manteniendo la proporción
logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)  # Redimensiona el logotipo

# Calcular la posición (x, y) para centrar el logotipo en la imagen del código QR
box = (
    img.size[0] // 2 - logo.size[0] // 2,  # Coordenada X para centrar horizontalmente
    img.size[1] // 2 - logo.size[1] // 2   # Coordenada Y para centrar verticalmente
)

# Pegar el logotipo en el código QR
img.paste(logo, box, logo)  # El tercer argumento es una máscara para manejar la transparencia

# Modificar la forma de los módulos (puntos) del QR Code
def draw_circle(draw, x, y, size, fill):
    draw.ellipse((x, y, x + size, y + size), fill=fill)

# Crear una nueva imagen para dibujar los círculos
img_with_circles = Image.new("RGBA", img.size, "white")
draw = ImageDraw.Draw(img_with_circles)

# Dibujar círculos en lugar de cuadrados
pixels = img.load()
box_size = 10  # Tamaño de cada módulo (debe coincidir con el box_size del QRCode)

for y in range(0, img.size[1], box_size):
    for x in range(0, img.size[0], box_size):
        if pixels[x, y][0] == 0:  # Negro en el QR original
            draw_circle(draw, x, y, box_size, "blue")

# Pegar el logotipo en el QR modificado
img_with_circles.paste(logo, box, logo)

# Agregar un borde decorativo (opcional)
border_width = 20
border_color = "gold"
img_with_border = Image.new("RGBA", (img_with_circles.size[0] + 2 * border_width, img_with_circles.size[1] + 2 * border_width), border_color)
img_with_border.paste(img_with_circles, (border_width, border_width))

# Guardar la imagen
img_with_border.save("codigo_qr_personalizado.png")

# Mostrar la imagen
img_with_border.show()
