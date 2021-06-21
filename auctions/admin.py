from django.contrib import admin
from .models import Gremio, Category, Listing
# Register your models here.

admin.site.register(Gremio)
admin.site.register(Category)
admin.site.register(Listing)