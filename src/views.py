from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.contrib.auth import authenticate,login,logout
from .models import Chat
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import openai
from openai import OpenAI
from decouple import config
import os


client = OpenAI(
    api_key=config('API_KEY')
    )

# Create your views here.
def register_user(request):
    if request.method == "POST":
        print("fond login mehtod post")
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            print("already exist")
            messages.error(request, "Username already exists. Please choose another one.")
        else:
            print(username,email,password)
            user = User.objects.create_user(username=username,email=email,password=password)
            print(user)
            login(request,user)
            return redirect('chatroom')
    else:
        return render(request,'register.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('chatroom')
        else:
            messages.error(request,"Invalid credentials")
            return redirect('login')
    else:
        return render(request,'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def chatroom(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        question = request.POST.get('question')
        if len(question) != 0:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": question,
                        }
                    ],
                )
                bot_response = response.choices[0].message.content
                obj, created = Chat.objects.get_or_create(
                    user=request.user,
                    messageInput=question,
                    bot_response=bot_response,
                )
            except openai.APIConnectionError as e:
                messages.warning(request, f"Failed to connect to OpenAI API, check your internet connection")

    chat = Chat.objects.filter(user=request.user)
    return render(request,'chatroom.html',{'chats':chat})