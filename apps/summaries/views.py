from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .models import Summary


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "summaries/top.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        summary = Summary()
        context["total"] = summary.total()
        context["monthly_list"] = summary.calc(interval="monthly")
        context["daily_list"] = summary.calc(interval="daily")

        return context
