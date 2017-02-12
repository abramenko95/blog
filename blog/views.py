from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from userprofile.models import UserProfile
from userprofile.forms import UserForm
from django import forms
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
import math

def post_list(request, page_number=1):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = posts.reverse()
    current_page = Paginator(posts, 10)
    return render(request, 'blog/post_list.html', {'posts': current_page.page(page_number)})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def user_list(request):
    users = User.objects.all()
    return render(request, 'blog/user_list.html', {'users': users})

def user_detail(request, user_id, page_number=1):
    posts = Post.objects.filter(published_date__lte=timezone.now(), author_id=user_id).order_by('published_date')
    posts = posts.reverse()
    current_page = Paginator(posts, 10)
    user = get_object_or_404(User, id=user_id)
    try:
        profile = UserProfile.objects.get(id=user_id)
    except:
        profile = get_object_or_404(User, id=user_id)
    return render(request, 'blog/user_detail.html', {'user' : user, 'profile' : profile, 'posts': current_page.page(page_number)})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def addlike(request, post_id):

    try:
            if post_id in request.COOKIES:
                redirect('/')
            else:
                post = Post.objects.get(id=post_id)
                post.likes += 1
                post.save()
                response = redirect('/')
                response.set_cookie(post_id, "test")
                return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')

def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('registration/register.html', args)

def edit_user(request, profile_id):
    user = User.objects.get(pk=request.user.id)
    user_form = UserForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=(
        'middle_name',
        'phone_number',
        'about',
        'avatar'),
                                                 widgets={
                                                     'middle_name': forms.TextInput(
                                                         attrs={'class': 'form-control', 'required': ''}),
                                                     'phone_number': forms.TextInput(
                                                         attrs={'class': 'form-control', 'required': ''}),
                                                     'about': forms.TextInput(
                                                         attrs={'class': 'form-control', 'required': ''}),
                                                 })
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return redirect('user_detail', user_id=request.user.id)

        return render(request, "blog/edit_profile.html", {
            "noodle": profile_id,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied
