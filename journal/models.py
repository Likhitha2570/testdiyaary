from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class customerReviews(models.Model):
    name=models.CharField(max_length=15)
    email=models.CharField(max_length=50)
    phone=models.IntegerField( )
    review=models.TextField()
    date=models.DateField()
    class Meta: 
        verbose_name_plural = "customerReviews"  #to avoid adding extra 's' in database  table name
    def __str__(self):       #to get name in database
        return self.name
 
class diaryentries(models.Model):
      
      user = models.ForeignKey(User,on_delete = models.CASCADE)
      dailydate=models.DateField(auto_now_add=False,auto_now=False)
      dailytime=models.TimeField()
      place=models.CharField(max_length=150,blank=True,null=True)
      title=models.CharField(max_length=150,blank=True,null=True)
      dailyentry=models.CharField(max_length=1500)
      check_box=models.BooleanField(default=False)
      image=models.ImageField(upload_to="myimages",blank=True,null=True)
        
      date=models.DateField(auto_now_add=True,auto_now=False,blank=True) 
      class Meta:
        verbose_name_plural = "diaryentries" 
      def __str__(self):       #to get name in database
        return self.title 
        
      def save(self, *args, **kwargs):
        if not self.user_id:
            # set default value for user_id
            self.user_id = self.user.id
        super(diaryentries, self).save(*args, **kwargs)

 
class Imagesuploader(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     Allimages=models.ImageField(upload_to="myimages") 
     date=models.DateTimeField(auto_now_add=True)
     caption=models.TextField(max_length=100)      
     class Meta:
        verbose_name_plural = "Imagesuploader" 
        def __str__(self):       #to get name in database
          return self.caption 