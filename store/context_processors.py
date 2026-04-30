from django.conf import settings
from .cart import Cart


def cart_context(request):
    try:
        cart = Cart(request)
        cart_count = len(cart)
    except Exception:
        cart_count = 0

    return {
        "cart_count": cart_count,

        "STORE_NAME": getattr(settings, "STORE_NAME", "Raffay Kids Corner"),
        "STORE_PHONE_DISPLAY": getattr(settings, "STORE_PHONE_DISPLAY", "+92 370 1670717"),
        "WHATSAPP_NUMBER": getattr(settings, "WHATSAPP_NUMBER", "923701670717"),
        "STORE_EMAIL": getattr(settings, "STORE_EMAIL", "rafaykidscorner@gmail.com"),
        "STORE_LOCATION": getattr(settings, "STORE_LOCATION", "Pakistan"),
    }