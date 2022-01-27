from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,CreateView,DeleteView,DetailView

from . import forms

# Create your views here.
class SignUp(CreateView):
	form_class = forms.UserCreateForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'