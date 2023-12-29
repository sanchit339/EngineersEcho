from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import PostCreateForm, PostUpdateForm
from .models import Post


# Create your views here.
def home(request, pageno):
    posts = Post.objects.all().order_by('-date_posted')
    paginated = Paginator(posts, 5)
    # we have to pass dictionary here
    context = {
        'posts': paginated.get_page(pageno),
        'title': 'Home'
    }
    return render(request, "blog/home.html", context)


def about(request):
    return render(request, 'blog/about.html', {'title': "About Page"})


def detailed_content(request, data):
    post = Post.objects.filter(title=data).first()
    if (post):
        return render(request, 'blog/detailed_content.html', {'post': post})
    else:
        return render(request, 'blog/no_content.html')


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            newPost = Post()  # first create obj then update the obj
            newPost.title = form.cleaned_data.get('title')  # from the updated form
            newPost.content = form.cleaned_data.get('content')  # cleaned data comes from django forms
            newPost.stripped_content = newPost.content[:min(700,len(newPost.content))]  # fetching from new Post
            newPost.author = request.user

            # check for clashes
            already_exist = Post.objects.filter(title=newPost.title).count()
            if already_exist > 0:
                messages.error(request, f'A Post with following title already exists!')
                return redirect('blog-create')
            else:
                newPost.save()
                messages.success(request, f'Post created Successfully!')
                return redirect('blog-detail', newPost.title)
        else:
            messages.error(request, f'Error while Creating Post')
            return redirect('blog-create')
    else:
        form = PostCreateForm()
        return render(request, 'blog/post_create.html', {'form': form})


@login_required
def update_post(request, data):
    gained_post = Post.objects.get(title=data)
    if gained_post.author != request.user:
        messages.error(request, f'error')
        return redirect('blog-home')
    elif request.method == "POST":
        form = PostUpdateForm(request.POST)

        if form.is_valid():
            updatedpost = Post.objects.get(title=data)
            updatedpost.title = request.POST.get('title')
            updatedpost.content = request.POST.get('content')
            updatedpost.stripped_content = updatedpost.content[:min(700, len(updatedpost.content))]
            updatedpost.save()
            messages.success(request, f'Post updated Successfully!')
            return redirect('blog-detail', request.POST.get('title'))
        else:
            messages.error(request, f'Error while updating the post')
            return redirect('blog-update', data)
    else:  # render as it is
        instance1 = Post.objects.get(title=data)
        tempform = PostUpdateForm()
        tempform.fields['title'].initial = instance1.title
        tempform.fields['content'].initial = instance1.content

        return render(request, 'blog/post_update.html', {'form': tempform})


@login_required
def delete_post(request, data):
    gained_post = Post.objects.get(title=data)
    if gained_post.author != request.user:
        messages.error(request, f'error')
        return redirect('blog-home')
    else:
        messages.success(request, f'post Deleted Successfully')
        gained_post.delete()
        return redirect('blog-home')
