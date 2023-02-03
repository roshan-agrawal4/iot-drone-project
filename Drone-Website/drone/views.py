import json
from django.shortcuts import redirect, render
import pyrebase
import requests
import sys, errno  
# from  firebase import firebase
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import credentials,db
from threading import Thread
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

cred = credentials.Certificate("D:/droneNetworking/drone-system-iot-firebase-adminsdk-selsr-36021455d8.json")
firebase_admin.initialize_app(cred,{
	'databaseURL':"https://drone-system-iot-default-rtdb.firebaseio.com"
	})
# firebase = firebase.FirebaseApplication('https://drone-system-iot-default-rtdb.firebaseio.com',None)


# config = {
# "apiKey": "AIzaSyBhIVn3prbiF0XWw5xqV2UtnSFVcm6Qocg",
#   "authDomain": "drone-system-iot.firebaseapp.com",
#   "databaseURL": "https://drone-system-iot-default-rtdb.firebaseio.com",
#   "projectId": "drone-system-iot",
#   "storageBucket": "drone-system-iot.appspot.com",
#   "messagingSenderId": "101869826123",
#   "appId": "1:101869826123:web:d11da3d9d6566fd54b5dce",
#   "measurementId": "G-H6MH5YHNXY"
#   }
# firebase=pyrebase.initialize_app(config)
# authe = firebase.auth()
# database=firebase.database()

ref = db.reference('gps')
ref2 = db.reference('ultrasonic')
# data=dict()
# def on_data_added(event):
#     print(event.data)
#     latitude = data['Latitude']
#     longitude = data['Longitude']
    
    # data = event.data.popitem()[1]
    # print("data: ",data['Latitude'])
    

# def listen_for_data():
#     try:
#         ref.listen(on_data_added)
#     except KeyboardInterrupt:
#         print("Stopping data listening...")

# def index(request):
#     listen_thread = Thread(target=listen_for_data)
#     listen_thread.start()
#     return render(request,"drone/index.html")
@login_required
def home_page(request):

    try:
        data = ref.order_by_child('timestamp').limit_to_last(1).get()
        ultrasonic_data=ref2.order_by_child('timestamp').limit_to_last(1).get()
        data_fields = data[list(data.keys())[0]]
        ultrasonic_fields=ultrasonic_data[list(ultrasonic_data.keys())[0]]
        Latitude = data_fields['Latitude']
        Longitude = data_fields['Longitude']
        Distance= ultrasonic_fields['Obst_dist']
        timestamp = data_fields['timestamp']
        print("Latitude:", Latitude)
        print("Longitude:", Longitude)
        print('Timestamp:',timestamp)
        print("Distance",Distance)
        # return final_data
        # ref.listen(on_data_added)
    except KeyboardInterrupt:
        print("Stopping data listening...")
    return render(request,"drone/home.html",{"Latitude":Latitude,"Longitude":Longitude,"Distance":Distance,"timestamp":timestamp})
    
@login_required
def check_drone_status(request): 
    try:
        data = ref.order_by_child('timestamp').limit_to_last(1).get()
        ultrasonic_data=ref2.order_by_child('timestamp').limit_to_last(1).get()
        ultrasonic_fields=ultrasonic_data[list(ultrasonic_data.keys())[0]]
        data_fields = data[list(data.keys())[0]]
        Latitude = data_fields['Latitude']
        Longitude = data_fields['Longitude']
        timestamp = data_fields['timestamp']
        Distance= ultrasonic_fields['Obst_dist']
        
        print("Latitude:", Latitude)
        print("Longitude:", Longitude)
        print('Timestamp:',timestamp)
        print("Distance",Distance)
        # return final_data
        # ref.listen(on_data_added)
        data= {'Latitude':Latitude,'Longitude':Longitude,"Distance":Distance}
        return JsonResponse(data)
    except KeyboardInterrupt:
        print("Stopping data listening...")



def index(request):
    return render(request,'drone/index.html')


def signup_page(request):
    print("Entered signup page")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        myUser = User.objects.create_user(username,email,password)
        myUser.save()
        print(myUser," user saved")
        messages.success(request,"Your account has been successfully created.")
        return redirect('login')

    return render(request,'drone/signup.html')

def login_page(request):
    print("Entered login page")
    if request.method == "POST":
        user = request.POST['username']
        passw = request.POST['password']

        user = authenticate(username=user, password=passw)
        print(user)
        if user is not None:
            login(request,user)
            # return render(request,'drone/home.html')
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!")

    return render(request,'drone/login.html')


def sign_out(request):
    logout(request)
    messages.success(request, "Logged Out successfully")
    return redirect('/')

