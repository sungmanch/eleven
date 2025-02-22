from django.shortcuts import render

# Create your views here.


def talk_to_eleven(request):
    return render(request, "calling/talk_to_eleven.html")
