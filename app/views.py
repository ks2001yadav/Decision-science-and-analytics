from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import  RegisterForm,MeetingForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .models import Meet,Profile
import random
import http.client
from django.conf import settings
from twilio.rest import Client
# Create your views here.


def send_otp(mobile , otp):
      account_sid = 'AC3b06dafd01e28c4f20b012c816253445'
      auth_token  = ' 4a523db91df701ed755588baa1c19d4d '
      client = Client(account_sid, auth_token)
      message = client.messages.create(
                                        body=f'Hi , your verification code is {otp}.',
                                        from_='+19205572637',
                                        to=f'+91{mobile}'
                                    )
      print(message.sid)
      return None

def home(request):
    return render(request,'home.html')

# class CustomerRegistrationView(View):
#     def get(self,request):
#         form=CustomerRegistrationForm()
#         return render(request,'customerregistration.html',{'form':form})
#     def post(self,request):
#         form=CustomerRegistrationForm(request.POST)
#         if form.is_valid():
#             messages.success(request,'Congratulations!! You are registered successfully')
#             # form.save()
#             user = form.save( commit= False)
#             user.save()
#         return render(request,'customerregistration.html',{'form':form})


class AddMeetingView(View):
    def get(self,request):
        form=MeetingForm()
        return render(request,'addmeet.html',{'form':form})
    def post(self,request):

        form=MeetingForm(request.POST)
        if form.is_valid():
            starting_time = request.POST.get('starting_time')
            ending_time = request.POST.get('ending_time')
            meeting_link = request.POST.get('meeting_link')
            description = request.POST.get('description')
            messages.success(request,'Congratulations!! Meeting add successfully')
            # form.save()
            # user = form.save( commit= False)
            meet = Meet(starting_time=starting_time, ending_time = ending_time,meeting_link=meeting_link, description = description)
            meet.save()
        return render(request,'addmeet.html',{'form':form})


def listmeet(request):

    data = Meet.objects.all()
   
    stu = {
    "s": data
    }
   
    return render(request,"listmeet.html",stu)


def edit(request,id):
    meeting = Meet.objects.filter(id=id)[0] 
    Meet.objects.filter(id=id).delete()
    form=MeetingForm()
    return render(request, 'edit.html', {'meeting':meeting,'form':form})  

def delete(request,id):
    Meet.objects.filter(id=id).delete()
    data = Meet.objects.all()
   
    stu = {
    "s": data
    }
    messages.success(request,'Congratulations!! Meeting deleted successfully')
    return render(request,'home.html') 

def update(request,id):
 
    # if request.method == 'POST':
    #     pi = meet.objects.get(id=id)
    #     fm = MeetingForm(request.POST, instance=pi)
    #     if fm.is_valid():
    #         fm.save()
    # else:
    #     pi = User.objects.get(id=id)
    #     fm = MeetingForm(instance=pi)
    # return render(request,'edit.html', {'form':fm}) 

    if request.method == 'POST':
        starting_time = request.POST.get('starting_time')
        ending_time = request.POST.get('ending_time')
        meeting_link = request.POST.get('meeting_link')
        description = request.POST.get('description')
        meet = Meet(starting_time=starting_time, ending_time = ending_time,meeting_link=meeting_link, description = description)
        meet.save()
        
    return redirect('/listmeet')  

def otp(request):
    print("FUNCTION CALLED")
    mobile=request.session['mobile']
    print(mobile)
    if request.method=='POST':
        check_user=Profile.objects.filter(mobile=mobile).first()
        otp=request.POST.get('otp')
        print(otp)
        if otp==check_user.otp:
            messages.success(request,f'Hi {check_user.username}, login successfully')
            #login(request)
            return redirect('/')
        else:
            messages.error(request,'You have entered wrong otp')
            return render(request,'otp.html')
    context={'mobile':mobile}
    return render(request,'otp.html',context)

def mobile(request):
     
    if request.method=='POST':
        mobile=request.POST.get('mobile')
        check_user=Profile.objects.filter(mobile=mobile).first()
        if check_user:
            otp=check_user.otp
            # SMS_BACKEND = 'sms.backends.twilio.SmsBackend'
            send_otp(mobile,otp)
            request.session['mobile']=mobile
            messages.success(request,'OTP send Successfully')
            return redirect('/otp')
        else:
            messages.success(request,'Sorry, You are not registered with this mobile number')
            return redirect('/mobile')
    return render(request,'mobile.html')

class RegisterView(View):
    def get(self,request):
       form=RegisterForm()
       return render(request, 'register.html',{'form':form})  
    
    def post(self,request):
       form=RegisterForm(request.POST)
       email=request.POST.get('email')
       #if(User.objects.filter(email=email).first()):
           #messages.info(request,'Email already exits')
           #return render(request,'register.html',{'form':form})
       otp=str(random.randint(1000,9999))
       if form.is_valid():
       
           email=request.POST.get('email')
           mobile=request.POST.get('mobile')
           name=request.POST.get('username')

           check_user=User.objects.filter(email=email).first()
           check_profile=Profile.objects.filter(mobile=mobile).first()
           if check_user or check_profile :
               messages.success(request,'User already exits')
               return render(request,'register.html',{'form':form})

           profile=Profile(username=name,email=email,mobile=mobile,otp=otp)
           profile.save()

           messages.success(request,'Congratulations, registered successfully')
           form.save()
       return render(request, 'register.html',{'form':form})

def otp(request):
    print("FUNCTION CALLED")
    mobile=request.session['mobile']
    print(mobile)
    if request.method=='POST':
        check_user=Profile.objects.filter(mobile=mobile).first()
        otp=request.POST.get('otp')
        print(otp)
        if otp==check_user.otp:
            messages.success(request,f'Hi {check_user.username}, login successfully')
            #login(request)
            return redirect('/')
        else:
            messages.error(request,'You have entered wrong otp')
            return render(request,'otp.html')
    context={'mobile':mobile}
    return render(request,'otp.html',context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                #login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,template_name = "login.html", context={"form":form})