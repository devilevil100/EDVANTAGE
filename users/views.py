from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from .models import User_profile, Tutor, Room, Message
from django.contrib.auth import logout
from django.shortcuts import redirect

def signup(request):
    if request.method == "POST":
        password = request.POST['password']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = email
        location = request.POST['location'] 
        designation = request.POST['designation']
        if designation == "s":
            if User.objects.filter(username=username).exists():
                return render(request, 'index.html', {"error1": "The Email Already Exists."})
            newuser = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname)
            newuserp = User_profile(user=newuser, location=location)
            newuserp.save()
            login(request, newuser)
            request.session["name"] = email
            return redirect(f'users:dashboard')
        else:
            resume = request.FILES['resume']
            degree = request.FILES['degree']
            verify = request.FILES['verify']
            if User.objects.filter(username=username).exists():
                return render(request, 'index.html', {"terror1": "The Email Already Exists."})
            
            newuser = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname)
            newtutor = Tutor(user=newuser, location=location, resume=resume, degree=degree,verify=verify)
            newtutor.save()
            login(request, newuser)
            request.session["name"] = email
            return redirect("users:dashboard")
    return redirect(f'users:home')

 
def slogin(request):
    if request.method == "POST":
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=email).exists():
            userr = User.objects.get(username=email)
            if userr.check_password(password):
                request.session["name"] = email
                login(request, userr)
                return redirect(f'users:dashboard')
            return render(request, 'index.html', {"lerror1": "Password is incorrect"})
        return render(request, 'index.html', {"lerror1": "Email not registered"})
    
    return redirect(f'users:home')

def tlogin(request):
    if request.method == "POST":
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=email).exists():
            userr = User.objects.get(username=email)
            if userr.check_password(password):
                if Tutor.objects.filter(user=userr).exists():
                    request.session["name"] = email
                    login(request, userr)
                    return redirect(f'users:dashboard')
                else:
                    return render(request, 'index.html', {"lerror1": "You are registered as a student"})
            return render(request, 'index.html', {"lerror1": "Password is incorrect"})
        return render(request, 'index.html', {"lerror1": "Email not registered"})
    
    return redirect(f'users:home')
def logoutt(request):
    logout(request)
    return redirect('users:home')

@login_required
def dashboard_view(request):
    if Tutor.objects.filter(user=request.user).exists():
        tutor = Tutor.objects.get(user=request.user)
        if tutor.approved == False:
            return render(request, 'dashboard.html', {"approved": False, "tutor": "yes", 'room_name': "example", "user_id": request.user.id})
        else:
            listofmsg = []
            roomm = []
            for item in User_profile.objects.all():
                if not Room.objects.filter(user1=request.user, user2= item.user).exists():
                    Roomm = Room(user1=request.user, user2=item.user, name=str(request.user.id)+str(item.user.id))
                    Roomm.save()
            for rooom in Room.objects.all():
                if rooom.user1 == request.user:
                    for message in Message.objects.all():
                        if message.room == rooom:
                            listofmsg.append(message)
                    roomm.append(rooom)
            return render(request, 'dashboard.html', {"approved": True, "tutor": "yes", 'room_name': "example", "user_id": request.user.id, "rooms": roomm, "msgs":listofmsg})
    else:
        roomm = []
        listofmsg = []
        for rooom in Room.objects.all():
                if rooom.user2 == request.user:
                    roomm.append(rooom)
                    for message in Message.objects.all():
                        if message.room == rooom:
                            listofmsg.append(message)
        return render(request, 'dashboard.html', {'room_name': "example", "user_id": request.user.id, "rooms":roomm, "msgs":listofmsg})


def home_view(request):
    if request.user.is_authenticated:
        return redirect("users:dashboard")
    else:
	    return render(request, 'index.html')
