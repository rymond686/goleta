from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from .forms import OrderSubmissionForm
from .selectors import orders_for_user
from .services import submit_order


@login_required
@require_http_methods(["GET", "POST"])
def order_create(request):
    form = OrderSubmissionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        submit_order(user=request.user, order_data=form.cleaned_data)
        messages.success(request, "订单已提交，当前状态为已寄送。")
        return redirect("order-history")

    return render(request, "orders/order_form.html", {"form": form})


class OrderHistoryView(LoginRequiredMixin, ListView):
    context_object_name = "orders"
    paginate_by = 20
    template_name = "orders/order_history.html"

    def get_queryset(self):
        return orders_for_user(self.request.user)
