from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import OTP
import json
import random
from . import mail


@csrf_protect
def index(request):
    return render(request, 'index.html')


@csrf_protect
def otp_verification(request):
    if request.method == "POST" and request.is_ajax():

        # verifying OTP
        otp_1 = request.POST['otp_1']
        otp_2 = request.POST['otp_2']
        otp_3 = request.POST['otp_3']
        otp_4 = request.POST['otp_4']

        otp_entered = "".join([otp_1, otp_2, otp_3, otp_4])
        username = request.POST['username']
        if OTP.objects.filter(username=username, otp_code=otp_entered).exists():
            OTP.objects.get(username=username, otp_code=otp_entered).delete()

            # fetching data from input form
            fullname = request.POST['fullname']
            email = request.POST['email']
            date_of_birth = request.POST['date_of_birth']
            phone_no = request.POST['phone_no']
            gender = request.POST['gender']
            password = request.POST['password1']
            confirm_password = request.POST['password2']
            if gender == "#":
                print("Please Select your gender!")
                return HttpResponse(json.dumps({'result': 6}), content_type='application/json')

            User = get_user_model()
            if password == confirm_password:

                # checking that username is already exists or not
                if User.objects.filter(username=username).exists():
                    print("User name is already taken, Try another username!")
                    return HttpResponse(json.dumps({'result': 1}), content_type='application/json')

                # checking that email is already exists or not
                elif User.objects.filter(email=email).exists():
                    print("Your email id is already registered")
                    return HttpResponse(json.dumps({'result': 2}), content_type='application/json')

                else:
                    # creating user obejct
                    user = User.objects.create_user(username=username, fullname=fullname, email=email,
                                                    phone_no=phone_no, date_of_birth=date_of_birth, gender=gender, password=password)

                    # save the user details or insert user details in database
                    user.save()
                    print("user created with the following details", username,
                          fullname, email, phone_no, date_of_birth, gender, password)

                    return HttpResponse(json.dumps({'result': 3}), content_type='application/json')

            else:
                print("password and confirm password is not matching!")
                return HttpResponse(json.dumps({'result': 4}), content_type='application/json')

        else:
            print("OTP is Wrong!")
            return HttpResponse(json.dumps({'result': 5}), content_type='application/json')
    else:
        return redirect('/')


@csrf_protect
def register(request):
    # getting post requests
    if request.method == "POST" and request.is_ajax():

        # fetching data from input form
        username = request.POST['username']
        fullname = request.POST['fullname']
        email = request.POST['email']
        date_of_birth = request.POST['date_of_birth']
        phone_no = request.POST['phone_no']
        gender = request.POST['gender']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        if gender == "#":
            print("Please Select your gender!")
            return HttpResponse(json.dumps({'result': 6}), content_type='application/json')

        # as we change the default model for user so we will use get_user_model() for getting user model
        User = get_user_model()

        # checking that password and confirm password are matching or not
        if password == confirm_password:

            # checking that username is already exists or not
            if User.objects.filter(username=username).exists():
                print("User name is already taken, Try another username!")
                return HttpResponse(json.dumps({'result': 1}), content_type='application/json')

            # checking that email is already exists or not
            elif User.objects.filter(email=email).exists():
                print("Your email id is already registered")
                return HttpResponse(json.dumps({'result': 2}), content_type='application/json')

            else:

                # sending otp mail
                otp_text = generate_otp_text()
                html_body = """<html lang="en">

<body style="text-align: center;">
    <h1>Your Hemllo Chatting App OTP </h1>
    <p>Please enter the below 4 digit OTP code to complete the verification process.</p>
    <h2 style="color: red;">{}</h2>
    <p>This code is valid for the next 30 minutes.
        Please do not share OTP with anyone. <br><br><br>
        <br>
        
        
        Thank You,<br>
        Team Hemllo Chatting App<br>
        
        If you didn't raise this request, you can ignore it or you can write to hemlo.chatting.app@gmail.com</p>

</body>
</html>""".format(otp_text)

                mail.send_email(email, html_body)
                if OTP.objects.filter(username=username).exists():
                    otp_instance = OTP.objects.get(username=username)
                    otp_instance.otp_code = otp_text
                    otp_instance.save()
                else:
                    otp_instance = OTP.objects.create(
                        username=username, otp_code=otp_text)
                    otp_instance.save()

                return HttpResponse(json.dumps({'result': 3}), content_type='application/json')
        else:
            print("password and confirm password is not matching!")
            return HttpResponse(json.dumps({'result': 4}), content_type='application/json')

    return redirect('/')


@csrf_protect
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
            messages.error(request, "Username and Password in not correct!")

    return redirect('/')


def generate_otp_text():

    res = "".join(map(str, (random.randrange(0, 9, 1) for i in range(4))))
    print("Random OTP is : " + res)

    return res
