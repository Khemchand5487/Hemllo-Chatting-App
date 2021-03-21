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

<body>
    <tr>
      <td align="center" bgcolor="#e9ecef">
       
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;padding: 36px 13px 0px;">
          <tr>
            <td align="left" bgcolor="#ffffff">
              <h1 style="background-color:#e9ecef; margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 48px;">Hemllo Chatting App OTP</h1>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <tr>  
      <td align="center" bgcolor="#e9ecef">

        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">

          <!-- start copy -->
          <tr>
            <td align="left" bgcolor="#ffffff" style="padding: 36px 13px 15px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px;">
              <p style="margin: 0;">Please enter the below 4 digit OTP code to complete the verification process.</p>
            </td>
          </tr>
   
          <tr>
            <td align="left" bgcolor="#ffffff">
              <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td align="center" bgcolor="#ffffff" style="padding: 10px;">
                    <table border="0" cellpadding="0" cellspacing="0">
                      <tr>
                        <td align="center" bgcolor="#1a82e2" style="border-radius: 2px;">
                          <a href=" " target="_blank" style="display: inline-block; padding: 10px 30px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 25px; color: #ffffff; text-decoration: none; border-radius: 6px;">{}</a>

                        </td>
                      </tr>
                      
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td align="left" bgcolor="#ffffff" style="padding: 15px 13px 15px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px;">
              <p style="margin: 0;">This code is valid for the next 30 minutes.Please do not share OTP with anyone.</p>
              <p style="margin: 0;">
              </p><br>

              <p style="margin: 0; padding-top: 20px; font-size:14px;">If you didn't raise this request, you can ignore it or you can write to <a href="mailto:hemlo.chatting.app@gmail.com" target="_blank">hemlo.chatting.app@gmail.com</a></p>
            </td>
          </tr>

         <tr>


            <td align="left" bgcolor="#ffffff" style="padding:36px 13px 15px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px; border-bottom: 3px solid #d4dadf">
              <p style="margin: 0;">Thank You,<br>Team Hemllo Chatting App</p>
                          
            </td>
          </tr>

          <tr>
            <td align="center" bgcolor="#e9ecef" style="padding: 12px 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 14px; line-height: 20px; color: #666;">
              <p style="margin: 0; font-size: 12px;">Hemllo Chatting App</p>
              <p style="margin: 0; font-size: 12px;">Chandigarh University, Mohali, Punjab</p>
            </td>
          </tr>

</body>
</html>""".format(otp_text)
                try:
                    mail.send_email(email, html_body)
                except:
                    pass
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
