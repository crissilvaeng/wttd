from django.http.response import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import render
from django.core import mail
from django.contrib import messages

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if not form.is_valid():
            return render(request, 'subscribe.html', {'form': form})
        body = render_to_string('emails/subscribe.txt', form.cleaned_data)
        mail.send_mail('Confirmação de inscrição', body, 'contato@eventex.com.br',
                       ['contato@eventex.com.br', form.cleaned_data['email']])
        messages.success(request, 'Inscrição realizada com sucesso!')
        return HttpResponseRedirect('/inscricao/')
    context = {'form': SubscriptionForm()}
    return render(request, 'subscribe.html', context)
