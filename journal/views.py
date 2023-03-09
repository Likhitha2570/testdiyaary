from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404,Http404
from django.http import HttpResponse,HttpResponseForbidden
from journal.models import customerReviews,diaryentries ,Imagesuploader
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from .forms import Imageuploaderform
from django.conf import settings
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm,SetPasswordForm 
from .forms import SignUpForm,EditForm,StyleAuthenticationForm


def index(request):
      return render(request,"index.html")



def entries(request):
 if request.user.is_authenticated: 
    if request.method=="POST":  
     dailydate= request.POST.get('dailydate')   
     dailytime= request.POST.get('dailytime')
     place= request.POST.get('myplace') 
     title= request.POST.get('mytitle')
     image=request.POST.get('image')
     dailyentry= request.POST.get('mytext') 
     checkbox=bool(request.POST.get('mycheckbox'))
     user = request.user
     person_diary=diaryentries(user=user,dailydate=dailydate,dailytime=dailytime,place=place,title=title,dailyentry=dailyentry,check_box=checkbox,image=image,date=datetime.today())
     person_diary.save()
     if len(request.FILES)!=0:
       person_diary.image=request.FILES['image']
       person_diary.save()
    return render(request,"entries.html")
 return  redirect('userlogin')  


def mygallery(request):
  if request.user.is_authenticated:   
    if request.method=="POST":
     form =Imageuploaderform(request.POST,request.FILES)
     if form.is_valid():
                # Set the user field of the image to the current user
                image = form.save(commit=False)
                image.user = request.user
                image.save()
                form = Imageuploaderform()
    else:
      form = Imageuploaderform()
    Gallery=Imagesuploader.objects.filter(user=request.user)
    return render(request,"mygallery.html",{'Gallery':Gallery,'form':form}) 
  return  redirect('userlogin')  


 
def reviews(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            review = request.POST.get('review')
            cust_review = customerReviews(name=name, email=email, phone=phone, review=review, date=datetime.today())
            cust_review.save()
             
        allreviews = customerReviews.objects.all()  
        return render(request, "reviews.html", {'allreviews': allreviews})
    return redirect('userlogin')
        
    


def user_signup(request):
  if request.method == "POST":
      fm = SignUpForm(request.POST)
      if fm.is_valid():
          email = fm.cleaned_data.get('email')
          username = fm.cleaned_data.get('username')
          if not email:
              messages.error(request, "Error:  enter a valid email address")
              return redirect('usersignup')
          elif not username:
              messages.error(request, "Error:  enter a valid username")
              return redirect('usersignup')
          elif User.objects.filter(email=email).exists():
              messages.error(request, "Warning: this email id already exists")
              return redirect('usersignup')
          elif User.objects.filter(username=username).exists():
              messages.error(request, "Warning: this username already exists")
              return redirect('usersignup')
          else:
              fm.save()
              messages.success(request, "Your account has been created successfully!")
              return redirect('userlogin')
  else:
      fm = SignUpForm()
  return render(request, "signup.html", {'form': fm})



def myprofile(request):
  if request.user.is_authenticated:
    #for editing
    if request.method=="POST":
      fm=EditForm(request.POST,instance=request.user) 
      if fm.is_valid():
         messages.success(request,"profile has  updated successfully")
         fm.save() 
    else:  
    # for showing profile to user
       fm=EditForm(instance=request.user)
    return render(request,'myprofile.html',{'form':fm})
  else:    
     
     return redirect('userlogin')
  

def user_login(request):
  if not request.user.is_authenticated:
    if request.method=="POST":
      fm=StyleAuthenticationForm(request=request,data=request.POST)
      if fm.is_valid():
        uname=fm.cleaned_data['username'] 
        upass=fm.cleaned_data['password']
        user=authenticate(username=uname,password=upass)
        if user is not None:
          login(request,user)
          messages.success(request,"logged in successfully")
          return redirect('home')
         
    else:      
     fm=StyleAuthenticationForm()
    return render(request,"login.html",{'form':fm})
  else:
    return redirect('home')
  

def changepassword(request):
  if request.method=="POST":
    fm=SetPasswordForm(user=request.user,data=request.POST)
    if fm.is_valid():
      fm.save()
      update_session_auth_hash(request,fm.user)
      messages.success(request,"password has changed successfully")
      return redirect('home')
  else:    
   fm=SetPasswordForm(user=request.user)
  return render(request,"changepassword.html",{'form':fm})    


 

def myentries(request):
    if request.user.is_authenticated:
        myentries = diaryentries.objects.filter(user=request.user)
        if request.method == "POST":
            search_title = request.POST.get('searched')
            fromdate = request.POST.get("searcheddatestart")
            todate = request.POST.get("searcheddateend")
            if search_title:
                myentries = diaryentries.objects.filter(
                    Q(user=request.user)&(
                    Q(title__icontains=search_title) |
                    Q(place__icontains=search_title) |
                    Q(dailyentry__icontains=search_title) |
                    Q(dailydate__icontains=search_title)))
            elif fromdate and todate:
                myentries = diaryentries.objects.filter(
                   Q(user=request.user),dailydate__range=[fromdate, todate])
        data = {'my_entries': myentries}
        return render(request, "myentries.html", data)
    return redirect('userlogin')


def updateentry(request,dailytime):
    diaryentry =diaryentries.objects.get(user=request.user, dailytime=dailytime)
    if request.method == 'POST':
      place= request.POST.get('myplace') 
      title= request.POST.get('mytitle')
      image=request.FILES.get('image')
      dailyentry= request.POST.get('mytext') 
      diaryentry.place = place
      diaryentry.title = title
      diaryentry.dailyentry = dailyentry
      if image:
            diaryentry.image = image
      diaryentry.save()
      return redirect('myentries')
    else:
        return render(request, 'updateentry.html', {'diaryentry': diaryentry})
     
 

def myfavourites(request):
  if request.user.is_authenticated: 
    entries = diaryentries.objects.filter(user=request.user, check_box=True)
    context = {'entries': entries}
    return render(request, 'fav.html',context)
    


def deleteentry(request,dailytime):
    if request.user.is_authenticated:
       if request.method=='POST':
          entry = diaryentries.objects.get(user=request.user, dailytime=dailytime)
          entry.delete()
          return redirect('myentries')      
    return render(request,'myentries.html')


def signout(request):
        logout(request)
        messages.success(request,"you are loggedout!!!")
        return redirect('userlogin') 



def deletemyaccount(request, username):
  if request.user.is_authenticated:
    user = User.objects.get(username=username)
    if request.method == 'GET':
      user.delete()
      return redirect('usersignup')
  return redirect('userlogin')



def deletegallery(request,caption):
    if request.user.is_authenticated:
       if request.method=='POST':
          image = Imagesuploader.objects.get(user=request.user, caption=caption)
          image.delete()
          return redirect('mygallery')      
    return render(request,'mygallery.html')


 

   


