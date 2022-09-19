from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import get_object_or_404

from . import models


User = get_user_model()


class ChatListView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'messenger/chat-list.html'


class CallListView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'messenger/call-list.html'


class ChatDetailView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'messenger/chat-detail.html'
    extra_context = {}

    def get(self,request,*args,**kwargs):
        peer = get_object_or_404(User,id=kwargs['peer_id'])

        if not (
            chat := models.Chat.objects\
                .filter(participants__in=[request.user])\
                .filter(participants__in=[peer])\
                .first()
        ):
            chat = models.Chat.objects.create()
            chat.participants.set([request.user,peer])

        self.extra_context.update({
            'peer': peer,
            'chat': chat
        })

        return super().get(request,*args,**kwargs)