from PIL import Image, ImageFilter, ImageOps


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Etapas:
    1. Converte para escala de cinza.
    2. Aumenta o contraste.
    3. Aplica nitidez.
    4. Transforma em preto e branco.
    """

    gray_image = ImageOps.grayscale(image)

    contrasted_image = ImageOps.autocontrast(gray_image)

    sharpened_image = contrasted_image.filter(ImageFilter.SHARPEN)

    threshold = 180
    binary_image = sharpened_image.point(
        lambda pixel: 255 if pixel > threshold else 0
    )

    return binary_image