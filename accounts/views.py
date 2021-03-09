from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib import messages
import json


def index(request):
    return render(request, 'index.html')


def register(request):
    #getting post requests
    if request.method == "POST" and request.is_ajax():

        #fetching data from input form
        username            = request.POST['username']
        fullname            = request.POST['fullname']
        email               = request.POST['email']
        date_of_birth       = request.POST['date_of_birth']
        phone_no            = request.POST['phone_no']
        gender              = request.POST['gender']
        password            = request.POST['password1']
        confirm_password    = request.POST['password2']

        #as we change the default model for user so we will use get_user_model() for getting user model
        User = get_user_model()

        #checking that password and confirm password are matching or not
        if password == confirm_password:
            
            #checking that username is already exists or not
            if User.objects.filter(username=username).exists():
                print("User name is already taken, Try another username!")
                return HttpResponse(json.dumps({'result': 1}), content_type='application/json')
            
            #checking that email is already exists or not
            elif User.objects.filter(email=email).exists():
                print("Your email id is already registered")
                return HttpResponse(json.dumps({'result': 2}), content_type='application/json')
            
            else:
                # creating user obejct
                user = User.objects.create_user(username=username, fullname=fullname, email=email , phone_no=phone_no, date_of_birth=date_of_birth, gender=gender, password=password)

                #save the user details or insert user details in database
                user.save()
                print("user created with the following details", username, fullname, email , phone_no, date_of_birth, gender, password)
                return HttpResponse(json.dumps({'result': 3}), content_type='application/json')
        else:
            print("password and confirm password is not matching!")
            return HttpResponse(json.dumps({'result': 4}), content_type='application/json')

    return redirect('/')

def login(request):
    if request.method == "POST":
        username = request.POST['username_in']
        password = request.POST['password_in']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print("you are logged in!")
            return HttpResponse("Logged IN")
        else:
            print("Invalid credentials!")
            messages.error(request,"Username and Password in not correct!")
                    
    return redirect('/')