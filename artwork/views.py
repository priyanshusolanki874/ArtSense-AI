from django.shortcuts import render, redirect
from .forms import ArtworkForm
from .forms import ContactForm
from .models import Artwork
from django.shortcuts import get_object_or_404
from .ai import analyze_artwork
import json
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib import messages
import os

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "contact.html", {"form": ContactForm(), "success": True})
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})

class UserLoginView(LoginView):
    template_name = "login.html"

def signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

@login_required
def upload_artwork(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.user = request.user
            artwork.save()
            return redirect('artwork_detail', pk=artwork.pk)
    else:
        form = ArtworkForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def gallery(request):
    artworks = Artwork.objects.filter(user=request.user).order_by("-uploaded_at")
    return render(request, "gallery.html", {"artworks": artworks})

@login_required
def artwork_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk, user=request.user)
    return render(request, 'artwork_detail.html', {'artwork': artwork})

@login_required
def analyze(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    feedback = analyze_artwork(artwork.image.path)
    print(feedback)
    data = json.loads(feedback)
    artwork.ai_score = data["score"]
    artwork.ai_strengths = "\n".join(data["strengths"])
    artwork.ai_weaknesses = "\n".join(data["weaknesses"])
    artwork.ai_suggestions = "\n".join(data["suggestions"])
    artwork.ai_status = "Completed"
    artwork.save()
    return redirect("artwork_detail", pk=pk)

def user_logout(request):
    logout(request)
    return redirect("home")

@login_required
def delete_artwork(request, pk):
    artwork=get_object_or_404(Artwork, pk=pk, user=request.user)
    if artwork.image:
        if os.path.isfile(artwork.image.path):
            os.remove(artwork.image.path)
    artwork.delete()
    messages.success(request, "Artwork deleted successfully.")
    return redirect("gallery")

@login_required
def edit_artwork(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk, user=request.user)
    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            form.save()
            return redirect("artwork_detail", pk=artwork.pk)
    else:
        form = ArtworkForm(instance=artwork)
    return render(request, "upload.html", {"form": form, "edit": True})
# Create your views here.
