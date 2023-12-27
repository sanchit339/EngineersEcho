from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import UserRegisterForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid(): #pass the parameter of the username and password
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created Succesfully for {username}!')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {'form': form})
