from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import FruitForm
from .models import Fruit


class IndexView(LoginRequiredMixin, ListView):
    template_name = "fruits/top.html"

    def get_queryset(self):
        return Fruit.objects.order_by("-updated_at").all()


class NewView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Fruit
    form_class = FruitForm
    template_name = "fruits/form.html"
    success_url = reverse_lazy("fruits:top")
    success_message = "%(name)s が登録されました"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({"title": "果物登録", "submit_text": "登録"})

        return context


class EditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Fruit
    form_class = FruitForm
    template_name = "fruits/form.html"
    success_url = reverse_lazy("fruits:top")
    success_message = "%(name)s が編集されました"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({"title": "果物編集", "submit_text": "編集"})

        return context


@login_required
def delete(request, pk):
    if request.method == "POST":
        try:
            fruit = Fruit.objects.get(id=pk)
        except Fruit.DoesNotExist:
            pass  # nothing to do
        else:
            fruit.delete()
            messages.error(request, f"{fruit.name} が削除されました")

    return redirect("fruits:top")
