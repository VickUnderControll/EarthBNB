import pyimgur
import requests
from io import BytesIO
import tempfile

CLIENT_ID = "c6477493c9d3414"
#secreto: 88b3846fe47b1cc01e17a1872aaafc7333c7adcb
im = pyimgur.Imgur(CLIENT_ID)

def upload_image_to_imgur(image_data):
    """
    Sube una imagen a Imgur y devuelve el enlace de la imagen subida.
    """
    try:
        # Guarda la imagen temporalmente en un archivo
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(image_data)
        # Sube la imagen desde el archivo temporal a Imgur
        uploaded_image = im.upload_image(temp_file.name, title="Título de la imagen")
        image_link = uploaded_image.link
        # Borra el archivo temporal después de subir la imagen
        temp_file.close()
        return image_link
    except Exception as e:
        # Manejar errores al subir la imagen a Imgur
        print(f"Error al subir imagen a Imgur: {e}")
        return None

def download_image_from_imgur(image_link):
    """
    Descarga una imagen de Imgur dado su enlace.
    Devuelve los datos binarios de la imagen descargada.
    """
    try:
        response = requests.get(image_link)
        image_data = BytesIO(response.content).getvalue()
        return image_data
    except Exception as e:
        # Manejar errores al descargar la imagen de Imgur
        print(f"Error al descargar imagen de Imgur: {e}")
        return None
