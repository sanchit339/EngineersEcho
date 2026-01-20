# 02: Blog App - Complete File-by-File Guide

## what is the blog app?

a self-contained Django app that handles **all blog post functionality**.  
creates, reads, updates, deletes (CRUD) blog posts with pagination.

in Spring Boot terms: this is like having `PostController`, `PostService`, `PostRepository`, and `Post` entity all in one organized package.

---

## directory structure

```
blog/
├── __init__.py              # Python package marker
├── apps.py                  # app configuration
├── admin.py                 # Django admin customization
├── models.py                # database models (Post)
├── views.py                 # business logic (controllers)
├── urls.py                  # URL routing
├── forms.py                 # form definitions
├── tests.py                 # unit tests
├── migrations/              # database migrations
│   ├── __init__.py
│   └── 0001_initial.py
└── templates/blog/          # HTML templates
    ├── home.html
    ├── detailed_content.html
    ├── post_create.html
    ├── post_update.html
    ├── about.html
    └── no_content.html
```

---

## file-by-file breakdown

### 1. `models.py` - THE DATABASE SCHEMA

**what it is:**
- defines database structure
- Django ORM models
- equivalent to JPA entities in Spring Boot

**current code:**
```python
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200, default='')
    content = models.TextField(default='')
    stripped_content = models.TextField(default='.')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.title
```

**field breakdown:**

#### CharField
```python
title = models.CharField(max_length=200, default='')
```
- **what:** short text field
- **max_length:** required, defines column size
- **default:** default value if none provided
- **use for:** names, titles, slugs

**other CharField options:**
```python
# with choices
STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published')]
status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

# unique constraint
slug = models.CharField(max_length=200, unique=True)

# with validation
email = models.CharField(max_length=100, validators=[EmailValidator()])
```

#### TextField
```python
content = models.TextField(default='')
```
- **what:** unlimited text field
- **use for:** long text, descriptions, blog content
- **database:** creates TEXT column

#### DateTimeField
```python
date_posted = models.DateTimeField(default=timezone.now)
```
- **what:** stores date + time
- **default=timezone.now:** sets current time on creation
- **note:** use `timezone.now` (no parentheses) not `timezone.now()`

**other datetime options:**
```python
# auto-set on creation
created_at = models.DateTimeField(auto_now_add=True)

# auto-update on save
updated_at = models.DateTimeField(auto_now=True)

# just date
publish_date = models.DateField()

# just time
meeting_time = models.TimeField()
```

#### ForeignKey (relationships)
```python
author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
```
- **what:** many-to-one relationship
- **ForeignKey:** many posts → one user
- **on_delete=CASCADE:** delete posts when user is deleted
- **like:** `@ManyToOne` in JPA

**on_delete options:**
```python
# CASCADE - delete related objects
author = models.ForeignKey(User, on_delete=models.CASCADE)

# SET_NULL - set to null (requires null=True)
author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

# PROTECT - prevent deletion
category = models.ForeignKey(Category, on_delete=models.PROTECT)

# SET_DEFAULT - set to default value
author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
```

#### __str__ method
```python
def __str__(self):
    return self.title
```
- **what:** string representation of the object
- **shows in:** admin panel, shell, debugging
- **like:** `toString()` in Java

---

**other field types you might use:**

```python
# boolean
is_published = models.BooleanField(default=False)
is_featured = models.BooleanField(default=False)

# numbers
views = models.IntegerField(default=0)
likes = models.PositiveIntegerField(default=0)
rating = models.DecimalField(max_digits=3, decimal_places=2)  # 0.00 to 9.99
price = models.DecimalField(max_digits=10, decimal_places=2)

# files
image = models.ImageField(upload_to='post_images/')
pdf = models.FileField(upload_to='documents/')

# URL
website = models.URLField(max_length=200)

# email
email = models.EmailField()

# JSON (Django 3.1+)
metadata = models.JSONField(default=dict)

# slug (URL-friendly)
slug = models.SlugField(max_length=200, unique=True)

# UUID
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

---

**relationships:**

```python
# One-to-One
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

# Many-to-One (ForeignKey)
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

# Many-to-Many
class Post(models.Model):
    tags = models.ManyToManyField('Tag')
```

---

**model methods:**

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # custom methods
    def get_excerpt(self):
        return self.content[:100] + '...'
    
    def is_recent(self):
        return self.date_posted > timezone.now() - timezone.timedelta(days=7)
    
    # properties
    @property
    def word_count(self):
        return len(self.content.split())
    
    # class Meta
    class Meta:
        ordering = ['-date_posted']  # default order
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        indexes = [
            models.Index(fields=['date_posted', 'author']),
        ]
```

---

### 2. `views.py` - THE CONTROLLERS

**what it is:**
- business logic layer
- handles HTTP requests/responses
- like Spring Boot Controllers + Services

**views explained:**

#### home view (list + pagination)
```python
def home(request, pageno):
    posts = Post.objects.all().order_by('-date_posted')
    paginated = Paginator(posts, 5)
    context = {
        'posts': paginated.get_page(pageno),
        'title': 'Home'
    }
    return render(request, "blog/home.html", context)
```

**breakdown:**
- `Post.objects.all()` - fetch all posts (like `postRepository.findAll()`)
- `.order_by('-date_posted')` - sort descending (`-` means DESC)
- `Paginator(posts, 5)` - 5 posts per page
- `context` - data passed to template
- `render()` - render template with context

**other querying methods:**

```python
# get all
posts = Post.objects.all()

# filter (WHERE clause)
posts = Post.objects.filter(author=request.user)
posts = Post.objects.filter(title__icontains='django')  # case-insensitive LIKE
posts = Post.objects.filter(date_posted__gte=some_date)  # >=

# get one (raises exception if not found)
post = Post.objects.get(id=1)

# get or 404
from django.shortcuts import get_object_or_404
post = get_object_or_404(Post, id=1)

# first/last
post = Post.objects.filter(author=user).first()  # returns None if empty
post = Post.objects.filter(author=user).last()

# exclude
posts = Post.objects.exclude(status='draft')

# chaining
posts = Post.objects.filter(author=user).exclude(status='draft').order_by('-date_posted')

# count
count = Post.objects.filter(author=user).count()

# exists
has_posts = Post.objects.filter(author=user).exists()

# values (returns dict)
posts = Post.objects.values('title', 'content')

# select_related (JOIN for ForeignKey)
posts = Post.objects.select_related('author').all()

# prefetch_related (for ManyToMany)
posts = Post.objects.prefetch_related('tags').all()

# aggregate
from django.db.models import Count, Avg
Post.objects.aggregate(total=Count('id'), avg_views=Avg('views'))

# annotate
posts = Post.objects.annotate(comment_count=Count('comments'))
```

---

#### post_create view (form handling)
```python
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            newPost = Post()
            newPost.title = form.cleaned_data.get('title')
            newPost.content = form.cleaned_data.get('content')
            newPost.stripped_content = newPost.content[:min(700, len(newPost.content))]
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
```

**breakdown:**
- `@login_required` - decorator, must be logged in
- `request.method == 'POST'` - check if form submission
- `form.is_valid()` - validate form data
- `form.cleaned_data` - validated, cleaned data
- `request.user` - currently logged-in user
- `messages.success()` - flash message (shows once)
- `redirect()` - redirect to another URL

**alternative approaches:**

**approach 1: save form directly**
```python
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # create but don't save yet
            post.author = request.user
            post.save()
            return redirect('blog-detail', post.id)
    else:
        form = PostCreateForm()
    return render(request, 'blog/post_create.html', {'form': form})
```

**approach 2: class-based view**
```python
from django.views.generic import CreateView

class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_create.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

---

#### update_post view
```python
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
        instance1 = Post.objects.get(title=data)
        tempform = PostUpdateForm()
        tempform.fields['title'].initial = instance1.title
        tempform.fields['content'].initial = instance1.content
        return render(request, 'blog/post_update.html', {'form': tempform})
```

**better approach:**
```python
@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # check ownership
    if post.author != request.user:
        return HttpResponseForbidden("You can't edit this post")
    
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('blog-detail', pk=post.pk)
    else:
        form = PostUpdateForm(instance=post)
    
    return render(request, 'blog/post_update.html', {'form': form})
```

**class-based approach:**
```python
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'blog/post_update.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
```

---

#### delete_post view
```python
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
```

**class-based approach:**
```python
from django.views.generic import DeleteView

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
```

---

### 3. `urls.py` - ROUTING

**current code:**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, {"pageno": 1}, name='blog-home'),
    path('<int:pageno>', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/create/', views.post_create, name='blog-create'),
    path('post/<data>/', views.detailed_content, name='blog-detail'),
    path('post/<data>/update/', views.update_post, name='blog-update'),
    path('post/<data>/delete/', views.delete_post, name='blog-delete')
]
```

**breakdown:**
- `path('', ...)` - matches empty path (root)
- `<int:pageno>` - captures integer as `pageno` parameter
- `<data>` - captures string as `data` parameter
- `name='blog-home'` - URL name for reverse lookup

**URL parameters:**
```python
# integer
path('post/<int:pk>/', views.post_detail)

# string (default)
path('post/<str:slug>/', views.post_detail)

# slug (alphanumeric + hyphens/underscores)
path('post/<slug:slug>/', views.post_detail)

# UUID
path('post/<uuid:id>/', views.post_detail)

# path (matches everything including slashes)
path('files/<path:filepath>/', views.download_file)
```

**class-based views in URLs:**
```python
from .views import PostListView, PostCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('create/', PostCreateView.as_view(), name='blog-create'),
]
```

**reverse URL lookup:**
```python
# in views
from django.urls import reverse
url = reverse('blog-detail', kwargs={'data': post.title})
return redirect('blog-home')

# in templates
{% url 'blog-detail' post.title %}
```

---

### 4. `forms.py` - FORM DEFINITIONS

**current code:**
```python
from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
```

**ModelForm explained:**
- auto-generates form from model
- includes validation
- has `.save()` method
- like Spring Boot DTOs + validation

**field options:**
```python
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # include these fields
        # fields = '__all__'  # all fields
        exclude = ['author', 'date_posted']  # exclude these
        
        # custom widgets
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        
        # custom labels
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
        }
        
        # help text
        help_texts = {
            'title': 'Enter a unique title for your post',
        }
```

**custom validation:**
```python
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters")
        if Post.objects.filter(title=title).exists():
            raise forms.ValidationError("This title already exists")
        return title
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title and content and title.lower() in content.lower():
            raise forms.ValidationError("Title shouldn't be in content")
        return cleaned_data
```

**regular forms (not ModelForm):**
```python
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Only Gmail allowed")
        return email
```

---

### 5. `admin.py` - ADMIN PANEL

**current code:**
```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

**what it does:**
- registers Post model in Django admin
- auto-generates CRUD interface
- accessible at `/admin/`

**customized admin:**
```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # list display
    list_display = ('title', 'author', 'date_posted', 'get_excerpt')
    
    # filters
    list_filter = ('date_posted', 'author')
    
    # search
    search_fields = ('title', 'content')
    
    # ordering
    ordering = ('-date_posted',)
    
    # date hierarchy
    date_hierarchy = 'date_posted'
    
    # read-only fields
    readonly_fields = ('date_posted',)
    
    # custom fields in form
    fields = ('title', 'content', 'author', 'date_posted')
    
    # or fieldsets for grouping
    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'content')
        }),
        ('Metadata', {
            'fields': ('author', 'date_posted'),
            'classes': ('collapse',)
        }),
    )
    
    # custom method
    def get_excerpt(self, obj):
        return obj.content[:50] + '...'
    get_excerpt.short_description = 'Excerpt'
    
    # actions
    actions = ['mark_as_published']
    
    def mark_as_published(self, request, queryset):
        queryset.update(status='published')
    mark_as_published.short_description = 'Mark as published'
```

---

### 6. `apps.py` - APP CONFIGURATION

**current code:**
```python
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
```

**what it does:**
- app metadata
- rarely modified

**advanced usage:**
```python
class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = 'Blog Management'
    
    def ready(self):
        # import signals here
        import blog.signals
```

---

### 7. `tests.py` - UNIT TESTS

**example tests:**
```python
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
    
    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(str(self.post), 'Test Post')
    
    def test_post_list_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
    
    def test_post_create_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/post/create/', {
            'title': 'New Post',
            'content': 'New content'
        })
        self.assertEqual(Post.objects.count(), 2)
```

---

## what else can you add to the blog app?

### comments feature
```python
# models.py
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### tags/categories
```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Post(models.Model):
    # ...
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
```

### views/likes
```python
class Post(models.Model):
    # ...
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    def total_likes(self):
        return self.likes.count()
```

### featured images
```python
class Post(models.Model):
    # ...
    featured_image = models.ImageField(upload_to='post_images/', blank=True, null=True)
```

### post status
```python
class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
```

---

## summary

the blog app handles:
- **models.py** - Post database schema
- **views.py** - CRUD operations (controllers)
- **urls.py** - routing for blog endpoints
- **forms.py** - form validation and rendering
- **admin.py** - admin panel customization
- **templates/** - HTML for blog pages

it's a complete, self-contained feature module.
