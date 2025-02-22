from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Eleven, Profile

# Create your views here.


class UserProfileForm(forms.Form):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
        ("prefer_not_to_say", "Prefer not to say"),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    age = forms.IntegerField(min_value=18, max_value=120)
    location = forms.CharField(max_length=100)


class ElevenForm(forms.Form):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
        ("prefer_not_to_say", "Prefer not to say"),
    ]

    MOOD_CHOICES = [
        ("calm", "Calm"),
        ("chill", "Chill"),
        ("classy", "Classy"),
        ("professional", "Professional"),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    mood = forms.ChoiceField(choices=MOOD_CHOICES)


@login_required
def profile_setup(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # Get the cleaned data
            gender = form.cleaned_data["gender"]
            age = form.cleaned_data["age"]
            location = form.cleaned_data["location"]

            # Update the user's profile
            profile = Profile()
            profile.user = request.user
            profile.gender = gender
            profile.age = age
            profile.location = location
            profile.save()

            messages.success(request, "Profile updated successfully!")
            return redirect("index")  # Replace with your desired redirect
    else:
        form = UserProfileForm()

    return render(request, "accounts/forms.html", {"form": form})


def eleven_setup(request):
    if request.method == "POST":
        form = ElevenForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data["gender"]
            mood = form.cleaned_data["mood"]

            if Eleven.objects.filter(user=request.user).exists():
                eleven = Eleven.objects.get(user=request.user)
                eleven.gender = gender
                eleven.mood = mood
                eleven.save()
            else:
                eleven = Eleven()
                eleven.user = request.user
                eleven.gender = gender
                eleven.mood = mood
                eleven.save()

            messages.success(request, "Eleven setup successfully!")
            return redirect("calling:talk")
    else:
        form = ElevenForm()

    return render(request, "accounts/eleven_setup.html", {"form": form})
