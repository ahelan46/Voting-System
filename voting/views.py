import random
import os
import qrcode

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Count

from .models import Voter, Party, Vote, VotingSession


# =========================
# LOGIN
# =========================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_staff:
                return redirect("/admin/")

            return redirect("home")

        messages.error(request, "Invalid username or password")

    return render(request, "voting/login.html")


# =========================
# HOME
# =========================
def home(request):
    return render(request, "voting/home.html")


# =========================
# QR SCAN PAGE
# =========================
def scan_qr(request):
    return render(request, "voting/scan.html")


# =========================
# VERIFY QR (AFTER SCAN)
# =========================
def verify_voter(request, voter_id):
    try:
        voter = Voter.objects.get(voter_id=voter_id)
    except Voter.DoesNotExist:
        return render(request, "voting/invalid.html")

    if voter.has_voted:
        return render(request, "voting/already_used.html")

    # store voter in session
    request.session["voter_id"] = voter.voter_id

    return redirect("mobile_verify")


# =========================
# MOBILE NUMBER PAGE
# =========================
def mobile_verify(request):
    if request.method == "POST":
        otp = random.randint(100000, 999999)

        request.session["otp"] = otp
        print("OTP:", otp)  # TEMP (console)

        return redirect("otp_verify")

    return render(request, "voting/mobile_verify.html")


# =========================
# OTP VERIFY
# =========================
def otp_verify(request):
    if request.method == "POST":
        entered = request.POST.get("otp")
        session_otp = request.session.get("otp")

        if entered == str(session_otp):
            request.session["verified"] = True
            return redirect("vote")
        else:
            return render(request, "voting/otp_verify.html", {
                "error": "Invalid OTP"
            })

    return render(request, "voting/otp_verify.html")


# =========================
# VOTE PAGE
# =========================
def vote(request):
    if not request.session.get("verified"):
        return redirect("mobile_verify")

    voter_id = request.session.get("voter_id")

    if not voter_id:
        return HttpResponse("Unauthorized access")

    voter = Voter.objects.get(voter_id=voter_id)

    if voter.has_voted:
        return HttpResponse("You already voted ❌")

    parties = Party.objects.all()
    return render(request, "voting/vote.html", {"parties": parties})


# =========================
# SUBMIT VOTE
# =========================
def submit_vote(request):
    voter_id = request.session.get("voter_id")
    voter = Voter.objects.get(voter_id=voter_id)

    if voter.has_voted:
        return HttpResponse("Duplicate vote blocked ❌")

    party_id = request.POST.get("party")
    party = Party.objects.get(id=party_id)

    Vote.objects.create(voter=voter, party=party)

    voter.has_voted = True
    voter.save()

    return redirect("success")


# =========================
# SUCCESS PAGE
# =========================
def success_page(request):
    return render(request, "voting/success.html")


# =========================
# RESULTS (ADMIN)
# =========================
def results(request):
    data = Vote.objects.values("party__name").annotate(total=Count("party"))
    return render(request, "voting/results.html", {"data": data})


# =========================
# GENERATE QR (ADMIN / TEST)
# =========================
def generate_vote_qr(request):
    voter = Voter.objects.first()

    vote_url = f"http://127.0.0.1:8000/verify/{voter.voter_id}/"
    qr = qrcode.make(vote_url)

    qr_dir = os.path.join(settings.MEDIA_ROOT, "qr")
    os.makedirs(qr_dir, exist_ok=True)

    qr_path = os.path.join(qr_dir, f"{voter.voter_id}.png")
    qr.save(qr_path)

    return HttpResponse("QR Generated")
