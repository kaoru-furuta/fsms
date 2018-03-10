import csv
import logging
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView

from fruits.models import Fruit
from .forms import SaleForm, UploadFileForm
from .models import Sale


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'sales/top.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = UploadFileForm
        return context

    def get_queryset(self):
        return Sale.objects.order_by('-sold_at').all()


class NewView(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/form.html'
    success_url = reverse_lazy('sales:top')

    def form_valid(self, form):
        fruit = Fruit.objects.get(id=self.request.POST['fruit_list'])
        form.instance.fruit = fruit
        form.instance.amount = fruit.price * form.instance.number
        return super(NewView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NewView, self).get_context_data(**kwargs)
        context['title'] = '販売情報登録'
        context['submit_text'] = '登録'
        return context


class EditView(LoginRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/form.html'
    success_url = reverse_lazy('sales:top')

    def form_valid(self, form):
        fruit = Fruit.objects.get(id=self.request.POST['fruit_list'])
        form.instance.fruit = fruit
        form.instance.amount = fruit.price * form.instance.number
        return super(EditView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        context['title'] = '販売情報編集'
        context['submit_text'] = '編集'
        return context


@login_required
def upload(request):
    if request.method != 'POST':
        return redirect('sales:top')

    form = UploadFileForm(request.POST, request.FILES)
    if not form.is_valid():
        return redirect('sales:top')

    try:
        uploaded_file = request.FILES['file'].read().decode('utf-8')
        reader = csv.reader(uploaded_file.splitlines())
        for row in reader:
            submit_row(row)
    except Exception as e:
        logging.debug(e)

    return redirect('sales:top')


def submit_row(row):
    if len(row) != 4:
        return

    try:
        fruit = Fruit.objects.get(name=row[0])
    except (Fruit.DoesNotExist, Fruit.MultipleObjectsReturned) as e:
        logging.debug(e)
        return

    try:
        number = int(row[1])
        amount = int(row[2])
    except ValueError as e:
        logging.debug(e)
        return
    else:
        if number <= 0:  # 個数が 0 以下は処理しない
            return

    try:
        sale = Sale()
        sale.fruit = fruit
        sale.number = number
        sale.amount = amount
        sale.sold_at = timezone.make_aware(datetime.strptime(row[3], '%Y-%m-%d %H:%M'))
        sale.save()
    except Exception as e:
        logging.debug(e)


@login_required
def delete(request, pk):
    if request.method == 'POST':
        try:
            sale = Sale.objects.get(id=pk)
        except Sale.DoesNotExist:
            pass  # nothing to do
        else:
            sale.delete()

    return redirect('sales:top')
