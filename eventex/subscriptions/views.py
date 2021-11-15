from django.template.loader import render_to_string
from django.shortcuts import render
from django.core import mail
from django.conf import settings

from django.http.response import HttpResponse, HttpResponseRedirect
from django.views import View

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscribeView(View):
    def get(self, request):
        return render(request, 'subscribe.html', {'form': SubscriptionForm()})

    def post(self, request):
        form = SubscriptionForm(request.POST)

        if not form.is_valid():
            return render(request, 'subscribe.html', {'form': form})

        subscription = Subscription.objects.create(**form.cleaned_data)

        body = render_to_string('emails/subscribe.txt', {'subscription': subscription})
        mail.send_mail('Confirmação de inscrição', body, settings.DEFAULT_FROM_EMAIL,
                       [settings.DEFAULT_FROM_EMAIL, subscription.email])

        return HttpResponseRedirect(f'/inscricao/{subscription.pk}/')


def details(request):
    return HttpResponse()
