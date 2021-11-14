from django.template.loader import render_to_string
from django.shortcuts import render
from django.core import mail
from django.contrib import messages
from django.conf import settings

from django.http.response import HttpResponseRedirect
from django.views import View

from eventex.subscriptions.forms import SubscriptionForm


class SubscribeView(View):
    def get(self, request):
        return render(request, 'subscribe.html', {'form': SubscriptionForm()})

    def post(self, request):
        form = SubscriptionForm(request.POST)

        if not form.is_valid():
            return render(request, 'subscribe.html', {'form': form})

        body = render_to_string('emails/subscribe.txt', form.cleaned_data)
        mail.send_mail('Confirmação de inscrição', body, settings.DEFAULT_FROM_EMAIL,
                       [settings.DEFAULT_FROM_EMAIL, form.cleaned_data['email']])
        messages.success(request, 'Inscrição realizada com sucesso!')

        return HttpResponseRedirect('/inscricao/')
