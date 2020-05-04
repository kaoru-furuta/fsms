import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.edit import FormMixin

from fruits.models import Fruit

from .forms import SaleForm, UploadFileForm
from .models import Sale


@login_required
def delete(request):
    if request.method != "POST":
        return redirect("sales:top")

    count = 0

    for k, v in request.POST.items():
        if not k.startswith("option-") or v != "delete":
            continue
        id_ = int(k.replace("option-", ""))
        try:
            sale = Sale.objects.get(id=id_)
        except Sale.DoesNotExist:
            pass  # nothing to do
        else:
            sale.delete()
            count += 1

    if count:
        messages.error(request, "販売情報が削除されました", extra_tags="danger")

    return redirect("sales:top")


class IndexView(SuccessMessageMixin, LoginRequiredMixin, FormMixin, ListView):
    paginate_by = 10
    template_name = "sales/top.html"
    form_class = UploadFileForm
    success_url = reverse_lazy("sales:top")
    success_message = "販売情報が一括登録されました"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = UploadFileForm

        return context

    def get_queryset(self):
        return Sale.objects.order_by("-sold_at").all()

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        try:
            uploaded_file = form.cleaned_data["file"].read().decode("utf-8")
            reader = csv.reader(uploaded_file.splitlines())
        except Exception as e:
            messages.error(self.request, e)
            return super().form_valid(form)

        for i, row in enumerate(reader, 1):
            fruit = Fruit.objects.filter(name=row[0]).first()
            form = SaleForm(
                {
                    "fruit_list": fruit.id if fruit else None,
                    "number": row[1],
                    "sold_at": row[3],
                }
            )
            if form.is_valid():
                form.instance.fruit = fruit
                form.instance.amount = fruit.price * form.instance.number
                form.save()
            else:
                messages.error(self.request, f"{i} 行目でエラーです。")

        return super().form_valid(form)


class NewView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "sales/form.html"
    success_url = reverse_lazy("sales:top")
    success_message = "販売情報が登録されました"

    def form_valid(self, form):
        fruit = Fruit.objects.get(id=self.request.POST["fruit_list"])
        form.instance.fruit = fruit
        form.instance.amount = fruit.price * form.instance.number

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({"title": "販売情報登録", "submit_text": "登録"})

        return context


class EditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = "sales/form.html"
    success_url = reverse_lazy("sales:top")
    success_message = "販売情報が編集されました"

    def form_valid(self, form):
        fruit = Fruit.objects.get(id=self.request.POST["fruit_list"])
        form.instance.fruit = fruit
        form.instance.amount = fruit.price * form.instance.number

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({"title": "販売情報編集", "submit_text": "編集"})

        return context
