from django.contrib import admin
from .models import TopImage, BlogModel, StockExist, StockData
# Register your models here.
admin.site.register(TopImage)
admin.site.register(BlogModel)
admin.site.register(StockExist)
admin.site.register(StockData)