from .models import Order


def submit_order(*, user, order_data):
    return Order.objects.create(
        user=user,
        sample_name=order_data["sample_name"],
        sample_type=order_data["sample_type"],
        project_type=order_data["project_type"],
    )
