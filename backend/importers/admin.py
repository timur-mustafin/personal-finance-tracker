
from django.contrib import admin
from .models import ImportSession

admin.site.register(ImportSession)
from .models import BankProfile, ImportDedup
admin.site.register(BankProfile)
admin.site.register(ImportDedup)