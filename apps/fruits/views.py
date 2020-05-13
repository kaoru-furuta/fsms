from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.edit import FormMixin

from .forms import FruitForm, SearchForm
from .models import Fruit


class IndexView(LoginRequiredMixin, FormMixin, ListView):
    template_name = "fruits/top.html"
    form_class = SearchForm

    def get_queryset(self):
        form = SearchForm(self.request.GET)

        if not form.is_valid():
            return Fruit.objects.order_by("-updated_at")

        query = Fruit.objects

        if form.cleaned_data.get("name"):
            query = query.filter(name__icontains=form.cleaned_data.get("name"))

        return query.order_by("-updated_at")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = SearchForm(self.request.GET)

        return context


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
def delete(request):
    if request.method != "POST":
        return redirect("fruits:top")

    for k, v in request.POST.items():
        if not k.startswith("option-") or v != "delete":
            continue
        id_ = int(k.replace("option-", ""))
        try:
            fruit = Fruit.objects.get(id=id_)
        except Fruit.DoesNotExist:
            pass  # nothing to do
        else:
            fruit.delete()
            messages.error(request, f"{fruit.name} が削除されました", extra_tags="danger")

    return redirect("fruits:top")


# from django.http import FileResponse
# ...
# ...
#
# def download(request, pk):
#     upload_file = get_object_or_404(UploadFile, pk=pk)
#     file = upload_file.file  # ファイル本体
#     return FileResponse(file)
