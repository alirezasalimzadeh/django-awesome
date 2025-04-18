from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from accounts.forms import *
from inbox.forms import InboxNewMessageForm
from posts.forms import ReplyCreateForm


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()

    posts = profile.user.posts.all()

    if request.htmx:
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            replyform = ReplyCreateForm()
            return render(request, 'snippets/loop_profile_comments.html', {'comments': comments, 'replyform': replyform})
        elif 'liked-posts' in request.GET:
            posts = profile.user.likedposts.order_by('-likedpost__created')
        return render(request, 'snippets/loop_profile_posts.html', {'posts': posts})

    new_message_form = InboxNewMessageForm()
    context = {
        'profile': profile,
        'posts': posts,
        'new_message_form': new_message_form,
    }
    return render(request, 'account/profile.html', context)


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated')
            return redirect("profile")

    if request.path == reverse("profile-onboarding"):
        template = 'account/profile_onboarding.html'
    else:
        template = 'account/profile_edit.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Profile Deleted, what a pity')
        return redirect("posts:home")
    return render(request, 'posts/profile_delete.html')
