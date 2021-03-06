from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, DetailView
from . models import Score, User, Credit
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'accounts/main.html')


class UserDetail(LoginRequiredMixin,DetailView):
    model = User
    template_name = "accounts/personal_cabinet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_score'] = self.object.user_score.exclude(score_card=None)
        context['all_score_credit'] = self.object.user_score.exclude(score_credit=None)
        context['deposits'] = self.object.user_score.filter(score_card=None)
        return context

    def get_object(self):
        return self.request.user


class PaymentsShedule(DetailView):
    model = Credit
    template_name = "accounts/payment_schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments_info'] = self.object.credit_payments_info.all().order_by("id")
        return context

