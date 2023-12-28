from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():  # pass the parameter of the username and password
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created Succesfully for {username}! Login In Now')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
    # we want the current details of the user in the form field (html placeholder)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # here we want instance of the user profile
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request , f'Your Profile is Updated!')
            redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
