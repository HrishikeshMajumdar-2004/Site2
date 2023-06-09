from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import requests,json
# Create your views here.

@login_required(login_url='login')
def HomePage(request):
    return render (request,'index.html')

api_key = '3e6058fa53c74e00a191d3dbb30c4902';
api_url = 'https://emailvalidation.abstractapi.com/v1/?api_key=' + api_key

def is_valid_email(data):
    # print(data["is_valid_format"]["value"])
    # if(data["is_valid_format"]["value"]):
    #     print("Hi")
    if data["is_valid_format"]["value"] and data["is_mx_found"]["value"] and data["is_smtp_valid"]["value"] :
        if not data["is_catchall_email"]["value"] and not data["is_role_email"]["value"] and not data["is_disposable_email"]["value"] :
            return True
    return False


def validate_email(email):
    response = requests.get(api_url + "&email="+email)
    my_bytes_value=response.content
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    # print(my_json)

    # Load the JSON to a Python list & dump it back out as formatted JSON
    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(data)
    is_valid = is_valid_email(data)
    if not is_valid:
        return False
    return True
            
def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if User.objects.filter(username = uname).first():
            return HttpResponse("Username already exist! Please try some other username.")
        
        # try:
        #     validate_email(email)
        # except ValidationError as e:
        #     return HttpResponse("Invalid Email", e)
        
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already Registered!!")
            
        if len(uname)>20:
            return HttpResponse("Username must be under 20 charcters!!")
        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        
        check_email=validate_email(email)
        if not check_email:
            return HttpResponse("Invalid Email!!")
        
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        

    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')