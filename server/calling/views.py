from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.


def talk_to_eleven(request):
    return render(request, "calling/talk_to_eleven.html")


@login_required
def chatting(request):
    return render(request, "calling/chatting.html")
