from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Profile
from .forms import InboxNewMessageForm
from .models import *

f = Fernet(settings.ENCRYPT_KEY)


@login_required
def inbox_view(request, conversation_id=None):
    my_conversations = Conversation.objects.filter(participants=request.user)
    if conversation_id:
        conversation = get_object_or_404(my_conversations, id=conversation_id)
        latest_message = conversation.messages.first()
        if conversation.is_seen == False and latest_message.sender != request.user:
            conversation.is_seen = True
            conversation.save()
    else:
        conversation = None
    context = {
        'conversation': conversation,
        'my_conversations': my_conversations,
    }
    return render(request, 'inbox/inbox.html', context)


@login_required
def search_users(request):
    letters = request.GET.get('search_user')
    if request.htmx:
        if len(letters) > 0:
            profiles = Profile.objects.filter(realname__icontains=letters).exclude(realname=request.user.profile.realname)
            users_id = profiles.values_list('user', flat=True)
            users = User.objects.filter(
                Q(username__icontains=letters) | Q(id__in=users_id)).exclude(username=request.user.username)
            context = {
                'users': users,
            }
            return render(request, 'inbox/list_searchuser.html', context)
        else:
            return HttpResponse('')
    else:
        raise Http404()


@login_required
def new_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    new_message_form = InboxNewMessageForm()

    if request.method == 'POST':
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            message_original = form.cleaned_data['body']
            message_bytes =  message_original.encode('utf-8')
            message_encrypted = f.encrypt(message_bytes)
            message_decoded = message_encrypted.decode('utf-8')
            message.body = message_decoded

            message.sender = request.user
            my_conversation = request.user.conversations.all()
            for c in my_conversation:
                if recipient in c.participants.all():
                    message.conversation = c
                    message.save()
                    c.lastmessage_created = timezone.now()
                    c.is_seen = False
                    c.save()
                    return redirect('inbox:inbox', c.id)
            new_conversation = Conversation.objects.create()
            new_conversation.participants.add(request.user, recipient)
            new_conversation.save()
            message.conversation = new_conversation
            message.save()
            return redirect('inbox:inbox', new_conversation.id)

    context = {
        'recipient': recipient,
        'new_message_form': new_message_form,
    }
    return render(request, 'inbox/form_newmessage.html', context)


@login_required
def new_reply(request, conversation_id):
    new_message_form = InboxNewMessageForm()
    my_conversations = request.user.conversations.all()
    conversation = get_object_or_404(my_conversations, id=conversation_id)

    if request.method == 'POST':
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            message_original = form.cleaned_data['body']
            message_bytes =  message_original.encode('utf-8')
            message_encrypted = f.encrypt(message_bytes)
            message_decoded = message_encrypted.decode('utf-8')
            message.body = message_decoded

            message.sender = request.user
            message.conversation = conversation
            message.save()
            conversation.lastmessage_created = timezone.now()
            conversation.is_seen = False
            conversation.save()
            return redirect("inbox:inbox", conversation.id)

    context = {
        'conversation': conversation,
        'new_message_form': new_message_form,
    }
    return render(request, 'inbox/form_newreply.html', context)


def notify_newmessage(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    last_message = conversation.messages.first()
    if conversation.is_seen == False and last_message.sender != request.user:
        return render(request, 'inbox/notify_icon.html', {})
    else:
        return HttpResponse('')


def notify_inbox(request):
    my_conversations = Conversation.objects.filter(participants=request.user, is_seen=False)
    for c in my_conversations:
        latest_message = c.messages.first()
        if latest_message.sender != request.user:
            return render(request, 'inbox/notify_icon.html', {})
    return HttpResponse('')


from django.http import HttpResponse


