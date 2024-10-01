from django.contrib import admin
from .models import TopsisAnalysis, TopsisResult

# Register your models here.
class TopsisAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'weights', 'impacts')  # Customize columns to display
    search_fields = ['user__username', 'date']

# Register TopsisResult model
class TopsisResultAdmin(admin.ModelAdmin):
    list_display = ('analysis', 'topsis_score', 'rank')
    search_fields = ['analysis__user__username']

# Register the models with the admin site
admin.site.register(TopsisAnalysis, TopsisAnalysisAdmin)
admin.site.register(TopsisResult, TopsisResultAdmin)