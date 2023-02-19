from django.contrib import admin
from .models import CsvFile, CandleData

# Register your models here.

@admin.register(CsvFile)
class CsvUploaderAdmin(admin.ModelAdmin):
    list_display = ('csv_file',)
    

@admin.register(CandleData)
class CandleDataAdmin(admin.ModelAdmin):
    list_display = ('open', 'close', 'low', 'high', 'date')