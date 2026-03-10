from django.contrib import admin
from django.db.models import Count
from .models import Voter, Party, Vote, VotingSession
from .utils import generate_qr


from django.utils.html import format_html




admin.site.register(Party)
admin.site.register(Vote)
admin.site.register(VotingSession)

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('name', 'voter_id', 'has_voted')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        generate_qr(obj.voter_id)

    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="80" height="80" />',
                obj.qr_code.url
            )
        return "No QR"

    qr_preview.short_description = "QR Code"