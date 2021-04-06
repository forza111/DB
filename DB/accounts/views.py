from django.shortcuts import render

from django.views.generic import ListView, DetailView
from . models import Score
from django.contrib.auth.decorators import login_required


class ScoreView(ListView):
    model = Score
    queryset = Score.objects.all()
    template_name = 'accounts/main.html'