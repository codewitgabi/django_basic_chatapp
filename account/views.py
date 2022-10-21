from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Message
from django.http import JsonResponse
import json


def signup(request):
    if request.user.is_authenticated:
        return redirect('chat')


    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username= username).exists():
                messages.info(request, 'Username already in use')
                return redirect('signup')
            elif User.objects.filter(email= email).exists():
                messages.info(request, 'Email already in use')
                return redirect('login')
            else:
                user = User.objects.create_user(username= username, email= email, password= password2)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')

    context = {}
    return render(request, 'account/signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('chat')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username= username, password= password)

        if user is not None:
            auth.login(request, user)
            return redirect('chat')
        else:
            messages.error(request, 'Incorrect username or password')
            return redirect('login')
        
    context = {}
    return render(request, 'account/login.html', context)
    
    
def logout(request):
	auth.logout(request)
	return redirect("signup")


@login_required(login_url= 'login')
def chat(request):
	chat_messages = Message.objects.all()
	context = {
		'chat_messages': chat_messages,
	}
	return render(request, 'account/chat.html', context)


def sendMessage(request):
	sender = request.user
	data = json.loads(request.body)
	message = data.get("message")
	Message.objects.create(sender= sender, message= message)
	return JsonResponse("message sent", safe= False)
	

def getMessage(request):
	db_messages = Message.objects.all()
	db_messages2 = list(db_messages.values())
	chat_messages = []
	
	for message in db_messages2:
		message["sender_id"] = User.objects.get(id= message["sender_id"]).username
		message["date_sent"] = str(message["date_sent"])[:5]
		chat_messages.append(message)
		
	return JsonResponse({
		"chat_messages": chat_messages}, safe= False)