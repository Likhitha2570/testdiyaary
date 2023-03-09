from django import forms
from .models import Imagesuploader
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
 
 
 
         

class Imageuploaderform(forms.ModelForm):
 class Meta:
    model= Imagesuploader
    exclude = ['user']
    fields='__all__'
    labels={'Allimages':''}
    widgets = {
            'Allimages': forms.FileInput(attrs={'class': 'uploadimage'}),
            'caption': forms.Textarea(attrs={'class': 'caption', 'rows': 2})
        }


#to extend more fields in signup form we created this class
class SignUpForm(UserCreationForm):
   password2=forms.CharField(label='confirm password',widget=forms.PasswordInput)#here we have to mention things related to UserCreationForm
   email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-sm','placeholder': 'john@gmail.com','style':'text-align:center'}))
   first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm','placeholder': 'enter your firstname','style':'text-align:center',}))
   last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm','placeholder': 'enter your lastname','style':'text-align:center',}))
    
   class Meta:  #meta class will connect with forms and model
      model= User
      fields=['username','first_name','last_name','email']#it is imp to mention username even though it is inherited for passwords
      labels={'email':'Email'} #it is used to edit labels in forms and these belongs to user
       
    #   labels={'password':''}
   def __init__(self,*args,**kwargs)  :
      super(SignUpForm,self).__init__(*args,**kwargs)
      
      self.fields['username'].widget = forms.TextInput(attrs={
             
            'class': 'form-control form-control-sm',
             'style':'text-align:center',
            'placeholder': 'enter your name'})
      self.fields['password1'].widget = forms.PasswordInput(attrs={
              
            'class': 'form-control form-control-sm',
             'style':'text-align:center',
            'placeholder': 'enter your password'})
      self.fields['password2'].widget = forms.PasswordInput(attrs={
             
            'class': 'form-control form-control-sm',
             'style':'text-align:center',
            'placeholder':  'confirm your password',
            })

     
class EditForm(UserChangeForm)  :
   email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-sm', 'style':'text-align:center',}))
   first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm','style':'text-align:center',}))
   last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'style':'text-align:center',}))
   username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'style':'text-align:center',}))
   date_joined=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control form-control-sm', 'style':'text-align:center',}))
   password=None   #as we get hash passwords 
   class Meta:
      model=User
      fields=['username','first_name','last_name','email','date_joined'] 
      labels={'email':'Email'} 
       


class StyleAuthenticationForm(AuthenticationForm):
    
         
         username=forms.CharField(widget=forms.TextInput(attrs={'class':'col-xs-8','style': 'margin: 10px 10px 10px 100px;'}))
         password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'col-xs-8','style': 'margin: 10px 10px 10px 100px;'}))
         class Meta:
               model=User
            
       
           
           
             
       