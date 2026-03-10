from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # login
    path("login/", views.login_view, name="login"),

    # QR scan & verification
    path("scan/", views.scan_qr, name="scan"),
    path("verify/<str:voter_id>/", views.verify_voter, name="verify"),
    path("scan/<str:voter_id>/", views.verify_voter, name="scan"),

    # mobile + otp
    path("mobile/", views.mobile_verify, name="mobile_verify"),
    path("otp/", views.otp_verify, name="otp_verify"),

    # voting
    path("vote/", views.vote, name="vote"),
    path("submit/", views.submit_vote, name="submit"),

    # success & results
    path("success/", views.success_page, name="success"),
    path("results/", views.results, name="results"),

    # QR generation (admin/testing)
    path("generate-qr/", views.generate_vote_qr, name="generate_qr"),
]
