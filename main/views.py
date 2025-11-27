from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Media
from .forms import MediaForm

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    # Remove the old form handling since we're using EmailJS now
    return render(request, 'main/contact.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'main/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

@login_required
def gallery(request):
    if request.user.is_superuser:
        media_files = Media.objects.all().order_by('-uploaded_at')
    else:
        media_files = Media.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    
    return render(request, 'main/gallery.html', {'media_files': media_files})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        media_files = Media.objects.all().order_by('-uploaded_at')
        total_uploads = media_files.count()
    else:
        media_files = Media.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
        total_uploads = media_files.count()
    
    return render(request, 'main/dashboard.html', {
        'media_files': media_files,
        'total_uploads': total_uploads
    })

@login_required
def upload(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                media = form.save(commit=False)
                media.uploaded_by = request.user
                media.save()
                messages.success(request, f'{media.media_type.title()} uploaded successfully!')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Error uploading file: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MediaForm()
    
    return render(request, 'main/upload.html', {'form': form})

@login_required
def delete_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    
    if media.uploaded_by != request.user and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete this file.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        media.delete()
        messages.success(request, 'File deleted successfully!')
    
    return redirect('dashboard')

@login_required
def profile(request):
    user_media_count = Media.objects.filter(uploaded_by=request.user).count()
    
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'main/profile.html', {
        'user_media_count': user_media_count
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password changed successfully! Please login again.')
            return redirect('login')
    
    return render(request, 'main/change_password.html')
