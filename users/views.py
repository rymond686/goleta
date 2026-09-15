from hashlib import sha256

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import RegistrationForm, StyledAuthenticationForm


LOGIN_ATTEMPT_LIMIT = 5
LOGIN_ATTEMPT_WINDOW_SECONDS = 5 * 60


def _login_attempt_key(request):
    # REMOTE_ADDR avoids trusting spoofable forwarding headers without a known proxy.
    client_ip = request.META.get("REMOTE_ADDR", "unknown")
    username = request.POST.get("username", "").strip().casefold()
    digest = sha256(f"{client_ip}\0{username}".encode()).hexdigest()
    return f"login-attempts:{digest}"


def _record_failed_login(key):
    if cache.add(key, 1, timeout=LOGIN_ATTEMPT_WINDOW_SECONDS):
        return 1

    try:
        return cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=LOGIN_ATTEMPT_WINDOW_SECONDS)
        return 1


class RateLimitedLoginView(LoginView):
    authentication_form = StyledAuthenticationForm
    redirect_authenticated_user = True
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        self.rate_limit_key = _login_attempt_key(request)
        if (
            request.method == "POST"
            and cache.get(self.rate_limit_key, 0) >= LOGIN_ATTEMPT_LIMIT
        ):
            return self._rate_limited_response()
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        attempts = _record_failed_login(self.rate_limit_key)
        response = super().form_invalid(form)
        if attempts >= LOGIN_ATTEMPT_LIMIT:
            response.context_data["rate_limited"] = True
            response.status_code = 429
        return response

    def form_valid(self, form):
        cache.delete(self.rate_limit_key)
        return super().form_valid(form)

    def _rate_limited_response(self):
        form = self.get_form_class()(request=self.request)
        context = self.get_context_data(form=form, rate_limited=True)
        return self.render_to_response(context, status=429)


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")

    return render(request, "registration/register.html", {"form": form})


@login_required
def home(request):
    return render(request, "home.html")
