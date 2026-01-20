# 03: Users App - Complete File-by-File Guide

## what is the users app?

handles **user authentication and profile management**.  
registration, login, logout, password reset, and user profiles.

in Spring Boot terms: like having `UserController`, `AuthenticationController`, `UserService`, and `SecurityConfig` all organized together.

---

## directory structure

```
users/
├── __init__.py              # Python package marker
├── apps.py                  # app configuration
├── admin.py                 # admin customization
├── models.py                # Profile model (extends User)
├── views.py                 # user-related views
├── urls.py                  # user routing
├── forms.py                 # user forms (registration, profile)
├── signals.py               # Django signals (auto-create profiles)
├── tests.py                 # unit tests
├── migrations/              # database migrations
└── templates/users/         # HTML templates
    ├── register.html
    ├── login.html
    ├── logout.html
    ├── profile.html
    ├── other_profile.html
    ├── password_reset.html
    └── ...
```

---

## file-by-file breakdown

### 1. `models.py` - EXTENDING USER MODEL

**what it is:**
- extends Django's built-in User model
- adds extra fields (like profile picture)
- one-to-one relationship with User

**current code:**
```python
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'
```

**breakdown:**

#### OneToOneField
```python
user = models.OneToOneField(User, on_delete=models.CASCADE)
```
- **what:** one user → one profile
- **on_delete=CASCADE:** delete profile when user is deleted
- **like:** `@OneToOne` in JPA
- **access:** `user.profile.image` or `profile.user.username`

#### ImageField
```python
image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
```
- **what:** stores image files
- **default:** fallback image if none uploaded
- **upload_to:** subdirectory in MEDIA_ROOT
- **requires:** `Pillow` library (`pip install Pillow`)

**storage:**
- development: saves to `media/profile_pics/`
- production (your setup): saves to AWS S3

---

**Django's built-in User model:**
```python
from django.contrib.auth.models import User

# fields:
# - username
# - first_name
# - last_name
# - email
# - password (hashed)
# - is_staff
# - is_active
# - is_superuser
# - last_login
# - date_joined

# usage:
user = User.objects.create_user(username='john', email='john@example.com', password='pass123')
user.set_password('newpass')  # hashes password
user.check_password('pass123')  # returns True/False
```

---

**extending the Profile model:**

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    # add more fields
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(max_length=200, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    github = models.CharField(max_length=50, blank=True)
    
    # preferences
    email_notifications = models.BooleanField(default=True)
    newsletter = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    # custom methods
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def followers_count(self):
        return self.followers.count()
```

---

**alternative: custom User model**

instead of Profile, you can create a complete custom user:

```python
# users/models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.username

# settings.py
AUTH_USER_MODEL = 'users.CustomUser'
```

**when to use custom user:**
- starting a new project
- need to change authentication (email instead of username)
- need fields directly on User model

**when to use Profile:**
- existing project
- don't want to mess with Django's User
- just adding extra info

---

### 2. `signals.py` - AUTO-CREATE PROFILES

**what it is:**
- Django signals = event-driven programming
- automatically create Profile when User is created
- like Spring's `@EventListener`

**current code:**
```python
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
```

**breakdown:**

#### post_save signal
```python
@receiver(post_save, sender=User)
```
- **what:** runs after User is saved
- **sender=User:** only for User model
- **created:** True if new object, False if update

#### create_profile function
```python
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```
- **what:** creates Profile when new User is created
- **instance:** the User object that was saved
- **created=True:** only runs for new users

#### save_profile function
```python
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
```
- **what:** saves profile whenever user is saved
- **ensures:** profile is always in sync

---

**registering signals:**

signals must be imported to work. two ways:

**method 1: in apps.py (recommended)**
```python
# users/apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'
    
    def ready(self):
        import users.signals  # import signals here
```

**method 2: in __init__.py**
```python
# users/__init__.py
default_app_config = 'users.apps.UsersConfig'
```

---

**other signals:**

```python
# pre_save - before saving
from django.db.models.signals import pre_save

@receiver(pre_save, sender=User)
def normalize_email(sender, instance, **kwargs):
    if instance.email:
        instance.email = instance.email.lower()

# pre_delete - before deleting
from django.db.models.signals import pre_delete

@receiver(pre_delete, sender=User)
def delete_user_files(sender, instance, **kwargs):
    if instance.profile.image:
        instance.profile.image.delete()

# post_delete - after deleting
@receiver(post_delete, sender=Profile)
def delete_profile_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
```

---

### 3. `forms.py` - USER FORMS

**current code:**
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
```

---

#### UserRegisterForm

```python
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```

**what it does:**
- extends Django's `UserCreationForm`
- adds email field (not in base form)
- includes password validation
- **password1:** password field
- **password2:** confirmation field

**customization:**
```python
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4:
            raise forms.ValidationError("Username must be at least 4 characters")
        return username
```

---

#### UserUpdateForm & ProfileUpdateForm

```python
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
```

**why two forms?**
- one for User model (username, email)
- one for Profile model (image)
- allows updating both in one view

**enhanced version:**
```python
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'location', 'website']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
```

---

### 4. `views.py` - USER CONTROLLERS

**current views:**

#### register view
```python
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # creates User + Profile (via signals)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created Successfully for {username}! Login In Now')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {'form': form})
```

**breakdown:**
- GET request: show empty form
- POST request: validate + save
- `form.save()` creates User
- signals auto-create Profile
- redirect to home after success

**enhanced version:**
```python
from django.contrib.auth import login

def register(request):
    if request.user.is_authenticated:
        return redirect('blog-home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            messages.success(request, f'Welcome {user.username}!')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {'form': form})
```

---

#### profile view (update)
```python
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
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
```

**breakdown:**
- `@login_required`: must be logged in
- two forms: UserUpdateForm + ProfileUpdateForm
- `request.FILES`: for image upload
- `instance=request.user`: pre-populate with current data

**note:** missing `return` before `redirect('profile')` - should be `return redirect('profile')`

---

#### another_user_profile view
```python
def another_user_profile(request, data, pageno=1):
    the_other_user = User.objects.filter(username=data).first()
    if the_other_user:
        their_post = Post.objects.filter(author=the_other_user).order_by('-date_posted')
        their_post = Paginator(their_post, 5)
        
        info = {
            'other_user': the_other_user,
            'posts': their_post.get_page(pageno)
        }
        return render(request, 'users/other_profile.html', info)
    else:
        return render(request, 'users/no_user.html')
```

**what it does:**
- shows another user's profile + their posts
- with pagination (5 posts per page)

**better approach:**
```python
def another_user_profile(request, username, pageno=1):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(pageno)
    
    context = {
        'profile_user': user,
        'posts': page_obj,
        'is_own_profile': request.user == user
    }
    return render(request, 'users/other_profile.html', context)
```

---

#### search_user view
```python
def search_user(request):
    if request.method == 'POST':
        data = request.POST.get('user_name')
        return redirect('another_user-profile', data=data)
    else:
        return render(request, 'blog-home')
```

**what it does:**
- gets username from form
- redirects to that user's profile

**alternative: actual search**
```python
def search_user(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)[:10] if query else []
    
    context = {
        'query': query,
        'users': users
    }
    return render(request, 'users/search_results.html', context)
```

---

### 5. `urls.py` - USER ROUTING

**current code:**
```python
from django.urls import path
from . import views as user_view
from django.contrib.auth import views as auth_view

urlpatterns = [
    # custom views
    path('register/', user_view.register, name='register'),
    path('profile/', user_view.profile, name='profile'),
    path('profile/<data>', user_view.another_user_profile, name="another_user-profile"),
    path('profile/<data>/<int:pageno>', user_view.another_user_profile, name="another_user_profilee"),
    path('search_user/', user_view.search_user, name="search_user"),
    
    # Django auth views
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name="users/logout.html"), name='users-logout'),
    
    # password reset
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name="users/password_reset.html"), name="reset_password"),
    path('password-reset/done', auth_view.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name="password_reset_confirm"),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"),
]
```

**breakdown:**

#### custom views
- `register/` - user registration
- `profile/` - own profile
- `profile/<username>` - other user's profile
- `search_user/` - user search

#### Django's built-in auth views

**LoginView:**
```python
path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name='login')
```
- handles login logic
- you just provide the template
- automatically handles authentication

**LogoutView:**
```python
path('logout/', auth_view.LogoutView.as_view(template_name="users/logout.html"), name='users-logout')
```
- logs user out
- shows logout confirmation

**PasswordResetView (4-step process):**
1. **PasswordResetView** - enter email
2. **PasswordResetDoneView** - email sent confirmation
3. **PasswordResetConfirmView** - enter new password (from email link)
4. **PasswordResetCompleteView** - password changed confirmation

---

**other auth views:**

```python
# password change (for logged-in users)
path('password-change/', auth_view.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
path('password-change/done/', auth_view.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
```

---

### 6. `admin.py` - ADMIN CUSTOMIZATION

**current code:**
```python
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
```

**enhanced version:**
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# unregister the default User admin
admin.site.unregister(User)
# register customized User admin
admin.site.register(User, UserAdmin)

# or register Profile separately
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website')
    search_fields = ('user__username', 'user__email')
```

---

## what else can you add to users app?

### follow/followers system
```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    
    def follow(self, user):
        self.followers.add(user)
    
    def unfollow(self, user):
        self.followers.remove(user)
    
    def is_following(self, user):
        return self.followers.filter(id=user.id).exists()
```

### email verification
```python
from django.core.mail import send_mail
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4)

# send verification email on registration
def send_verification_email(user):
    link = f"http://yoursite.com/verify/{user.profile.verification_token}/"
    send_mail(
        'Verify your email',
        f'Click here: {link}',
        'from@example.com',
        [user.email]
    )
```

### social auth (Google, GitHub, etc.)
```python
# install: pip install social-auth-app-django

# settings.py
INSTALLED_APPS = [
    'social_django',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

# urls.py
path('oauth/', include('social_django.urls', namespace='social')),
```

### user roles/permissions
```python
from django.contrib.auth.models import Group, Permission

# create groups
admin_group = Group.objects.create(name='Admins')
moderator_group = Group.objects.create(name='Moderators')

# assign permissions
permission = Permission.objects.get(codename='delete_post')
moderator_group.permissions.add(permission)

# assign user to group
user.groups.add(moderator_group)

# check in views
if request.user.groups.filter(name='Moderators').exists():
    # allow action
```

### two-factor authentication (2FA)
```python
# install: pip install django-otp
INSTALLED_APPS = [
    'django_otp',
    'django_otp.plugins.otp_totp',
]

MIDDLEWARE = [
    'django_otp.middleware.OTPMiddleware',
]
```

---

## summary

the users app handles:
- **models.py** - Profile model (extends User)
- **signals.py** - auto-create profiles
- **forms.py** - registration, profile update forms
- **views.py** - register, profile, search views
- **urls.py** - user routes + Django auth views
- **admin.py** - admin customization

it's a complete authentication + profile management system.
