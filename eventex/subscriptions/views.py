from django.http.response import HttpResponse
from django.shortcuts import render

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscribe.html', context)
