from django.contrib import admin

# Register your models here.
from django.contrib import admin
from journal.models import  customerReviews
from journal.models import  diaryentries
from journal.models import  Imagesuploader
# Register your models here.
admin.site.register(customerReviews),
admin.site.register(diaryentries),
@admin.register(Imagesuploader)
class ImageAdmin(admin.ModelAdmin):
    list_display=['Allimages','date','caption']