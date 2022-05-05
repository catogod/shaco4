from django.http.response import HttpResponse
from .backend_code.apiproj.gmail_control import gmail_control
from django.shortcuts import redirect, render
import smtplib


def forgot_password(request):
    if request.method == "POST":
        with smtplib.SMTP("smtp.gmail.com") as connection:
            sus_email = "thebestfeederinmid@gmail.com"
            message=f"Subject: Your password!\n\n Hello:{request.POST['username']} , your password is:{request.POST['password']}"
            connection.starttls()
            connection.login(user=sus_email, password="yasuomains0/10")
            connection.sendmail(from_addr=sus_email, to_addrs=f"{request.POST['email_address']}",msg=message)

        gc=gmail_control(user_email=request.POST['email_address'],email_text=message,system_email=sus_email)
        gc.Send_email_info_to_data()#sending the info
        return HttpResponse("the data has been send")
        
    return HttpResponse("forgot pass excepted")

def invite_user_to_become_admin(request):
    if request.method=="POST":
        with smtplib.SMTP("smtp.gmail.com") as connection:
            sus_email = "thebestfeederinmid@gmail.com"
            message=f"Subject: Welcome to our admin group!\n\n this is the admin code:{request.POST['admin_code']}, you may use it to register as admin"
            connection.starttls()
            connection.login(user=sus_email, password="yasuomains0/10")
            connection.sendmail(from_addr=sus_email, to_addrs=f"{request.POST['email_address']}",msg=message)
        gc=gmail_control(admin_username=request.POST['admin_username'],user_email=request.POST['email_address'],email_text=message,system_email=sus_email)
        gc.Send_email_info_to_data()#sending the info
        return HttpResponse("the data has been send")

    return HttpResponse("invite admin excepted")



def Send_user_his_win_info_in_rulate(request):
    if request.method=="POST":
        with smtplib.SMTP("smtp.gmail.com") as connection:
            sus_email = "thebestfeederinmid@gmail.com"
            message=f"Subject: Youre prize!!!\n\n Hello user, your won {request.POST['product']}. This was sent to the this address:{request.POST['user_location']}, the package will arive in 2-3 weeks"
            connection.starttls()
            connection.login(user=sus_email, password="yasuomains0/10")
            connection.sendmail(from_addr=sus_email, to_addrs=f"{request.POST['email_address']}",msg=message)
        gc=gmail_control(user_email=request.POST['email_address'],email_text=message,system_email=sus_email)
        gc.Send_email_info_to_data()#sending the info
        return HttpResponse("the data has been send")

    return HttpResponse("invite admin excepted")




def arara(request):
    return HttpResponse("Open this server to make the API work")