from django.shortcuts import render
from django import forms
from .pj import teach_evaluate
from django.http import HttpResponse
# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

def index(request):
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            msg = teach_evaluate(request.POST['username'], request.POST['password'])
            return render(request, 'response.html', {'message':msg})
    else:
        form = UserForm()
        return render(request, 'index.html', {'form': form})