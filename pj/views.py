from django.shortcuts import render
from django import forms
from .pj import teach_evaluate
from django.http import HttpResponse
import logging
# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label='学号')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

def index(request):
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            msg = teach_evaluate(request.POST['username'], request.POST['password'])
            logging.warning("USERNAME: " + request.POST['username'])
            for item in msg:
                logging.warning(item.encode('ascii'))
            return render(request, 'response.html', {'message':msg})
    else:
        form = UserForm()
        return render(request, 'index.html', {'form': form})