from .models import Order


def orders_for_user(user):
    return Order.objects.filter(user=user)
