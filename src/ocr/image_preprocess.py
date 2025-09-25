from PIL import Image, ImageOps


def to_grayscale(img: Image.Image) -> Image.Image:
    """Converte para escala de cinza."""
    return img.convert("L")


def enhance_contrast(img: Image.Image, cutoff: int = 1) -> Image.Image:
    """Ajusta contraste automaticamente."""
    return ImageOps.autocontrast(img, cutoff=cutoff)


def binarize(img: Image.Image, threshold: int = 145) -> Image.Image:
    """Binariza imagem: pixels abaixo do threshold ficam pretos, acima ficam brancos."""
    return img.point(lambda x: 0 if x < threshold else 255)


def preprocess_image(img: Image.Image) -> Image.Image:
    """
    Pipeline de pré-processamento padrão.
    - Escala de cinza
    - Aumento de contraste
    - Binarização
    """
    img = to_grayscale(img)
    img = enhance_contrast(img, cutoff=1)
    img = binarize(img, threshold=145)
    return img
