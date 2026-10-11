from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Post


def post_list(request):
    """لیست همه‌ی پست‌های منتشرشده"""
    posts = Post.objects.filter(is_published=True)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, post_id):
    """جزئیات یک پست"""
    post = get_object_or_404(Post, id=post_id, is_published=True)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_create(request):
    """ساخت پست جدید"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            post = Post.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            messages.success(request, 'پست با موفقیت ساخته شد!')
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, 'عنوان و محتوا الزامی است!')
    
    return render(request, 'blog/post_form.html')


@login_required
def post_edit(request, post_id):
    """ویرایش پست"""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        messages.success(request, 'پست ویرایش شد!')
        return redirect('post_detail', post_id=post.id)
    
    return render(request, 'blog/post_form.html', {'post': post})


@login_required
def post_delete(request, post_id):
    """حذف پست"""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'پست حذف شد!')
        return redirect('post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def signup(request):
    """ثبت‌نام"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد!')
            return redirect('post_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'blog/signup.html', {'form': form})