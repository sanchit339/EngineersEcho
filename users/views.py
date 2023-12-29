from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from .forms import UserUpdateForm, ProfileUpdateForm
from blog.models import Post
from django.core.paginator import Paginator


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
            messages.success(request, f'Your Profile is Updated!')
            redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


def another_user_profile(request, data, pageno=1):
    the_other_user = User.objects.filter(username=data).first()
    if (the_other_user):
        their_post = Post.objects.filter(author=the_other_user).order_by('-date_posted')
        their_post = Paginator(their_post, 5)

        info = {
            'other_user': the_other_user,
            'posts': their_post.get_page(pageno)
        }
        return render(request, 'users/other_profile.html', info)
    else:
        return render(request, 'users/no_user.html')


def search_user(request):
    if request.method == 'POST':
        data = request.POST.get('user_name')  # get the username from the request
        return redirect('another_user-profile', data=data)
    else:
        return render(request, 'blog-home')
