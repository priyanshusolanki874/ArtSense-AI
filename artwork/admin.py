from django.contrib import admin
from .models import Artwork


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'ai_score',
        'ai_status',
        'uploaded_at'
    )

    list_filter = (
        'ai_status',
    )

    search_fields = (
        'title',
    )
# Register your models here.
