from django.contrib import admin

from .models import *


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    pass


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass
