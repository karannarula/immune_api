# -*- coding: utf-8 -*-
from __future__ import print_function
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from create_user.models import Users,Location,CalendarEvents
from create_user.serializers import UserSerializers,LocationSerializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
import random, string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sys
import multiprocessing
from multiprocessing import Process, cpu_count, Manager
import logging
import traceback
import requests
from datetime import timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import json
from django.utils.safestring import SafeText
from django import template
from math import sin, cos, sqrt, atan2, radians
from django.urls import reverse
from django.views import generic
from requests.auth import HTTPBasicAuth
from datetime import datetime,date
from pytz import timezone
import calendar
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import importlib
import time
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

 
# Create your views here.



# @csrf_exempt
# def user_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         user_details = Users.objects.all()
#         users = UserSerializers(user_details, many=True)
#         return JsonResponse(users.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = UserSerializers(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @api_view(['GET', 'POST'])
# def user_list(request,format=None):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         user_details = Users.objects.all()
#         serializer = UserSerializers(user_details, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = UserSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class User_List(APIView):

    def get(self,request,format=None):
        users = Users.objects.all()
        user_serializer = UserSerializers(users, many=True)
        return Response(user_serializer.data)
    def post(self,request,format=None):
        
        user_serializers = UserSerializers(data=request.data)
        if user_serializers.is_valid():
            user_serializers.save()
            return Response(user_serializers.data,status= status.HTTP_201_CREATED)
        return Response(user_serializers.errors,status = status.HTTP_400_BAD_REQUEST)






class User_Insert_Location(APIView):


    def get(self,request,format=None):
        location = Location.objects.all()
        location_serializers = LocationSerializers(location, many=True)
        return Response(location_serializers.data)

    def post(self,request,format=None):
        location_serializers = LocationSerializers(data = request.data)
        event_id = request.data['name']
        print(request.data)

        check_status = request.data['status_bit']
        if check_status==0:
        #print(request.data)
            try:
                check_status_bit = Location.objects.get(name = event_id,status_bit=0)
                if check_status_bit:
                    print("-----------------")
                    pass

            except Location.DoesNotExist:
                if check_status == 0:
                    if location_serializers.is_valid():
                        location_serializers.save()   
                        calendar_google_url = "https://crm.birdtravels.com/api/resource/Event/"+event_id+""
                        current_date_time = datetime.now() + timedelta(hours=5.45)
                        current_date_time = current_date_time.strftime('%Y-%m-%d-%H:%M:%S')

                        data2 = {"starts_on":current_date_time,"api":1}
                        data2 = json.dumps(data2)
                        res2 = requests.put(url=calendar_google_url, verify=False, data =data2)
                        print(res2.text)
                        return Response(location_serializers.data,status= status.HTTP_201_CREATED)
            

        else:
            try:
                check_status_bit = Location.objects.get(name = event_id,status_bit=1)
                if check_status_bit:
                    print("-----------------")
                    pass

            except Location.DoesNotExist:
                if check_status == 1:
                    if location_serializers.is_valid():
                        location_serializers.save()   
                        calendar_google_url = "https://crm.birdtravels.com/api/resource/Event/"+event_id+""
                        current_date_time = datetime.now() + timedelta(hours=5.45)
                        current_date_time = current_date_time.strftime('%Y-%m-%d-%H:%M:%S')

                        data2 = {"ends_on":current_date_time,"api":1}
                        data2 = json.dumps(data2)
                        res2 = requests.put(url=calendar_google_url, verify=False, data =data2)
                        print(res2.text)
                        return Response(location_serializers.data,status= status.HTTP_201_CREATED)

        return JsonResponse({"success":"true"})
        
        
        # if location_serializers.is_valid():
        #     location_serializers.save()
            
        return Response(location_serializers.errors,status = status.HTTP_400_BAD_REQUEST)


class Filter_Map_Data(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        pass


    @csrf_exempt
    def post(self,request,format=None):
        print(request.POST)
        sys.exit()


def display_map(request):

    print(request.method)

    latlongbounds = []
    context = {}
    distance=0
    user_id=0
    email=''
    show_user = 1
    title=''
    get_users = Users.objects.all()
    if request.POST:
        print(request.POST)

        try:
            
            date_range = request.POST['date']
            user_name = request.POST['user_name']

            datetime_object = datetime.strptime(date_range, "%m/%d/%Y")
            user_id = request.POST['user_id']
            

            if user_id!="0":
                email_id = Users.objects.get(id=user_id)
                email=email_id.email
            elif user_name!='':
                email = user_name
                show_user = 1

            
            get_coordinates = Location.objects.filter(email_id=email,created__gte=datetime_object)
            
            
            #converting coordinates in query to dictionaries to be accesible in the map
            for get_dict_coordinates in get_coordinates:
                lat_long_dict={'lat':float(get_dict_coordinates.latitude),'lng':float(get_dict_coordinates.longitude)}
                latlongbounds.append(lat_long_dict)
            
            day_start_lat_longs = Location.objects.filter(email_id=email)[:1].get()
            day_end_lat_longs  = Location.objects.filter(email_id=email).last()
            R = 6373.0
            lat1 = radians(float(day_start_lat_longs.latitude))
            lon1 = radians(float(day_start_lat_longs.longitude))
            lat2 = radians(float(day_end_lat_longs.latitude))
            lon2 = radians(float(day_end_lat_longs.longitude))

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c

        except Exception as e:
            distance=0
            user_id=0
            

        return render(request, 'create_user/test.html', {'lat1':lat1,'lon1':lon1,'distance':distance,'show_user':1,'get_users':get_users,'date_range':date_range,'user_id':user_id,'latlongs':latlongbounds,'email':email,'distance':round(distance,2) })
        
    elif request.GET:
        
        
        try:
            user_id = request.GET.get('user_id')
            web = request.GET.get('web')
            print(type(web))
            if web=="1":
                email_id = Users.objects.get(id=user_id)
                email = email_id.email
                title = email_id.title
                now = datetime.now()
                
                get_coordinates = Location.objects.filter(email_id=email).exclude(index=0)
            else:
                
                email = request.GET.get('user_email')

                from_date = request.GET.get('from_date')

                to_date = request.GET.get('to_date')
                
                
                from_object = datetime.strptime(from_date, "%Y-%m-%d")
                
                to_object = datetime.strptime(to_date, "%Y-%m-%d")
                if from_object != to_object:
                    get_coordinates = Location.objects.filter(email_id=email,created__gt=from_object,created__lte=to_object).exclude(index=0)
                else:
                    get_coordinates = Location.objects.filter(email_id=email,created__gt=from_object).exclude(index=0)

                
            

            

            #converting coordinates in query to dictionaries to be accesible in the map
            for get_dict_coordinates in get_coordinates:
                lat_long_dict={'lat':float(get_dict_coordinates.latitude),'lng':float(get_dict_coordinates.longitude)}
                latlongbounds.append(lat_long_dict)
            print(latlongbounds)
            
            #day_start_lat_longs.latitude = 0.0000
            #day_start_lat_longs.longitude = 0.0000

            show_user = 0
            day_start_lat_longs = Location.objects.filter(email_id=email).exclude(index=0)[:1].get()

            day_end_lat_longs  = Location.objects.filter(email_id=email).exclude(index=0).last()
            R = 6373.0
            lat1 = radians(float(day_start_lat_longs.latitude))
            lon1 = radians(float(day_start_lat_longs.longitude))
            lat2 = radians(float(day_end_lat_longs.latitude))
            lon2 = radians(float(day_end_lat_longs.longitude))

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c
            print(distance)
            
        except Exception as e:
            distance=0
            pass
            
    return render(request, 'create_user/test.html', {'lat1':day_start_lat_longs.latitude,'lon1':day_start_lat_longs.longitude,'distance':distance,'title':title,'show_user':show_user,'get_users':get_users,'user_id':user_id,'latlongs':latlongbounds,'email':email,'distance':round(distance,2) })
    
class Users_View(generic.ListView):
    template_name = 'create_user/users.html'
    context_object_name = 'all_users_list'

    def get_queryset(self):
        return Users.objects.order_by('created')

@api_view(['GET', 'POST','OPTIONS'])
def erp_user_login(request):
    print(request.method)
    
    usr = request.GET['usr']
    pwd = request.GET['pwd']
    response_data = {}
    print(usr)
    
    URL = "http://crm.birdtravels.com/api/method/login"
    PARAMS = {'usr':usr,'pwd':pwd}
    req = requests.get(url = URL, params = PARAMS)
    data = req.text
    print(data)
    

    
    try:
        data_p_type = json.loads(data)
        if data_p_type["message"] == "Logged In" or data_p_type["message"]=='No App' :
            response_data["status"] = 'success'
            response_data["status_bit"] = 1
            response_data["global_url"] = "http://crm.birdtravels.com"

            response_data['sid'] = data_p_type['cookies']
            response_data['user'] = data_p_type['user']
            response_data['designation'] = data_p_type['designation']
    except Exception as e:
        response_data["status"] = 'error'
        response_data["status_bit"] = 0
    print(response_data)
    #sys.exit()
    
    return Response({"message":response_data})  


@api_view(['GET', 'POST','OPTIONS'])
def erp_user_login_covid(request):
    usr = request.GET['usr']
    pwd = request.GET['pwd']
    response_data = {}
    print(usr)
    
    URL = "http://14.98.78.66:1233/api/method/login"
    PARAMS = {'usr':usr,'pwd':pwd}
    req = requests.get(url = URL, params = PARAMS)
    data = req.text
    print(data)
    

    
    try:
        data_p_type = json.loads(data)
        if data_p_type["message"] == "Logged In" or data_p_type["message"]=='No App' :
            response_data["status"] = 'success'
            response_data['sid'] = data_p_type['sid']
    except Exception as e:
        response_data["status"] = 'error'
        response_data["status_bit"] = 0
    print(response_data)
    #sys.exit()
    
    return Response({"message":response_data}) 



@api_view(['GET', 'POST','OPTIONS'])
def insert_temprature(request):
    temprature = request.GET['temprature']
    b_profile = request.GET['b_profile']
    API_ENDPOINT = "http://14.98.78.69:7645/api/resource/Temprature/"
    data = {"temprature":temprature,"mobile_no":b_profile}
    data = json.dumps(data)
    res2 = requests.post(url=API_ENDPOINT, verify=False, data =data)
    return Response({"res":json.loads(res2.text)})
    
@api_view(['GET', 'POST','OPTIONS'])
def insert_timesheet(request):
    timesheetname = request.GET['timesheetname']
    
    parent = request.GET['parent']
    present_date = request.GET['present_date']
    
    if timesheetname!="":
        to_time = request.GET['to_time']
        API_ENDPOINT = "http://14.98.78.66:1233/api/resource/Timesheet Detail/"+timesheetname+""
        print(API_ENDPOINT)
        data = {"bit":2,"api":1,"to_time":to_time}
        print(data)
        data = json.dumps(data)
        res2 = requests.put(url=API_ENDPOINT, verify=False, data =data)
        
        return JsonResponse({"success":"true"})
    else:
        from_time = request.GET['from_time']
        check_timesheet = 'http://14.98.78.66:1233/api/resource/Timesheet/?filters=[["Timesheet","name","=","'+parent+'"]]'
        res3 = requests.get(url=check_timesheet, verify=False)
        res3_res = json.loads(res3.text)
        if len(res3_res['data'])==0:
            
            emp_name = request.GET['employee_name']
            data22 = {"employee":emp_name,"name_set":parent}
            timesheet_url = "http://14.98.78.66:1233/api/resource/Timesheet/"
            data22 = json.dumps(data22)

            res22 = requests.post(url=timesheet_url, verify=False, data =data22)
            

        API_ENDPOINT = "http://14.98.78.66:1233/api/resource/Timesheet Detail/"
        data = {"parent":parent,"doctype":"Timesheet Detail","present_date":present_date,"parenttype":"Timesheet","parentfield":"time_logs","activity_type":"Execution","from_time":from_time,"bit":1}
        data = json.dumps(data)
        
        res2 = requests.post(url=API_ENDPOINT, verify=False, data =data)
        print(res2.text)
        return JsonResponse({"success":"true"})
        
    
    
    
    
@api_view(['GET', 'POST','OPTIONS'])
def insert_profile(request):
    f_name = request.GET['fname']
    lname = request.GET['lname']
    email = request.GET['email']
    phone = request.GET['phone']
    status = request.GET['status']
    API_ENDPOINT = "http://14.98.78.69:7645/api/resource/Personal Profile/"
    data = {"first_name":f_name,"last_name":lname,"email_id":email,"status":status,"mobile_no":phone}
    data = json.dumps(data)
    
    res2 = requests.post(url=API_ENDPOINT, verify=False, data =data)
    return Response({"res":json.loads(res2.text)})    


@csrf_exempt
def insert_lead_user(request):

    
    mobile_no = request.GET['mobile_no']
    lead_name = request.GET['lead_name']
    email_id= request.GET['email_id']
    # MAHATA_API_URL = "http://alpha.mahattaart.com/api/customer"
    # headers = {'X-API-KEY': '3a78ab894457738d803358629ba42506ec9d12b9','Authorization':'Basic ZXJwYWRtaW46I21haGF0dGFlcnBAMzIxIw=='}
    # data2 = {'data': {"first_name":lead_name,"last_name":lead_name,"email_id":email_id,"contact":mobile_no} }
    # data2 = json.dumps(data2)
    # res2 = requests.post(url=MAHATA_API_URL, verify=False, auth=HTTPBasicAuth('erpadmin', '#mahattaerp@321#'),headers=headers,data =data2)
    # response_mahata = res2.text
    # print(response_mahata)
    
    API_ENDPOINT = "http://crm.birdtravels.com/api/resource/Lead/"
    data = {'data': {"lead_name":lead_name,"mobile_no":mobile_no,"email_id":email_id,"requirements_client":"dfddfsfsdfsd f sdfsdfsdfsfsdfsd s f sdf sd fsd d  ds  dfsfsdfsd  fs sf fsd fd"} }
    data = json.dumps(data)
    r = requests.post(url = API_ENDPOINT, data = data)
    pastebin_url = r.text 
    print("The pastebin URL is:%s"%pastebin_url)
    return HttpResponse(pastebin_url)

@csrf_exempt
def insert_india_mart_lead(request):
    URL = "http://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/9871246500/GLUSR_MOBILE_KEY/OTg3MTI0NjUwMCM0MjI1NDc5Mg==/Start_Time/06-JAN-2019/End_Time/22-MAR-2019/"
    req = requests.get(url=URL)
    # data = req.text
    # a = a.replace('null','"a"')
    # a = a.replace('\n','')
    # a = a.replace('\r','')
    # python_datatype = json.loads(a)
    # # print(b[0]['SENDEREMAIL'])
    # # URL = "http://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/9871246500/GLUSR_MOBILE_KEY/OTg3MTI0NjUwMCM0MjI1NDc5Mg==/Start_Time/06-JAN-2019/End_Time/22-MAR-2019/"
    # # req = requests.get(url=URL)
    data = str(req.text)
    print(type(data))
    print(data)


    # if data['Error_Message']:
    #   return HttpResponse(data['Error_Message'])

    data = data.replace('null','"a"')
    data = data.replace('\r','')
    data = data.replace('\a','')
    python_datatype = json.loads(data)
    print(python_datatype)
    print(type(python_datatype))
    return HttpResponse(python_datatype)

    for data_mart in python_datatype:
        print(data_mart)
        
        data_lead = {}
        API_ENDPOINT = "http://crm.birdtravels.com/api/resource/Lead/"
        if data_mart['SENDEREMAIL'] =='a':
            data_mart['SENDEREMAIL'] = data_mart['SENDERNAME']+'rahulsth726@gmail.com'
        data_lead = {'data': {"lead_name":data_mart['SENDERNAME'],"mobile_no":data_mart['MOB'],"email_id":data_mart['SENDEREMAIL'],"requirements_client":"dfddfsfsdfsd f sdfsdfsdfsfsdfsd s f sdf sd fsd d  ds  dfsfsdfsd  fs sf fsd fd"} }
        data_lead = json.dumps(data_lead)
        r = requests.post(url = API_ENDPOINT, data = data_lead)
        print(data_lead)



    return HttpResponse(python_datatype)

@csrf_exempt
def googlecalendar(request):
    
    # Post from erp_next containing event date and event end date with lead name
    
    
    
    try:
        event_end_date = request.POST['end_date']
        split_using_space2 = event_end_date.split(" ")
        split_using_space2.insert(1,"T")
        event_end_date = "".join(split_using_space2)

    except:
        event_end_date =''
    
    
    
    try:
        event_start_date = request.POST['event_dates']
        split_using_space = event_start_date.split(" ")
        split_using_space.insert(1,"T")
        event_start_date1 = "".join(split_using_space)
        
    except Exception as e:
        pass
    #print(event_start_date)

    
    
    group_email_list =  []
    event_name = request.POST['lead_name']
    group_email_address = request.POST['group_email_address']
    
    group_email_address = group_email_address.split(',')

    
    for group in group_email_address:
        group_email_dict =  {}
        group_email_dict = {'email':group}
        group_email_list.append(group_email_dict)



    event_subject = request.POST['lead_name']
    event_description = request.POST['description']
    folllow_up = request.POST['folllow_up']
    email_address = request.POST['lead_email_address']
    #location = request.POST['mobile_no']
    try:
        contact_by = request.POST['contact_by']
    except Exception as e:
        contact_by = ''
    lead_series = request.POST['lead_series']
    SCOPES = ['http://www.googleapis.com/auth/calendar']

    try:
        get_cal_ev = CalendarEvents.objects.get(lead_series = event_subject,event_bit=0)
    except CalendarEvents.DoesNotExist:
        get_cal_ev=0
    

    try:
        get_cal_ev2 = CalendarEvents.objects.get(lead_series = event_subject,event_bit=1)

    except:
        get_cal_ev2=0


    if get_cal_ev!=0:
        update_google_calendar(get_cal_ev,event_name)
        if update_google_calendar(get_cal_ev,event_name):
            print("done")
            

    if get_cal_ev2!=0:
        event_name = "Follow Up For "+event_name
        update_google_calendar2(get_cal_ev,event_name)
        if update_google_calendar2(get_cal_ev,event_name):
            print("done2")

            

    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'create_user/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


    
    print(group_email_list)

    
    if folllow_up =='1':
        event_name = "Follow Up For "+event_name
        email_address = contact_by
        group_email_list = []
        group_email_list.append({'email':contact_by})
        if event_end_date =='':
            print("escaped")
            return JsonResponse({'Event created:': 'Skipped'})
    else:
        
        event_name = event_name
        email_address = email_address


    event = {
  'summary': event_name,
  #'location':location,
  
  'description': event_description,
  'start': {
    'dateTime': event_start_date1,
    'timeZone': 'Asia/Kolkata',
  },
  'end': {
    'dateTime': event_end_date,
    'timeZone': 'Asia/Kolkata',
  },
  'attendees': group_email_list,
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 2},
      {'method': 'popup', 'minutes': 15},
    ],
  },
  
}

    if get_cal_ev == 0:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    else:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created2: %s' % (event.get('htmlLink')))
    #print(folllow_up)

    if folllow_up=='0' and get_cal_ev==0:
        event_cal_model = CalendarEvents(event_id =event.get('id'),lead_name = event_subject,lead_series = event_subject)
        event_cal_model.save()
    else:
        event_subject = "Follow Up For "+event_subject
        if get_cal_ev2 ==0:
            event_cal_model = CalendarEvents(event_id =event.get('id'),lead_name = event_subject,lead_series = event_subject,event_bit=1)
            event_cal_model.save()


    return JsonResponse({'Event created:': event.get('htmlLink')})
    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

def update_google_calendar(get_cal_ev,event_name):
    
    SCOPES = ['http://www.googleapis.com/auth/calendar.readonly']
    creds = None
    event_id = get_cal_ev.event_id
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token1.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'create_user/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token1.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    event['summary'] = event_name
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    return 1
    
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])
    print(event)
    return JsonResponse({'Event created:': event.get('htmlLink')})
    # event_id_url = get_cal_ev.event_id
    # event_id_url = str(event_id_url)
    # print(event_id_url)
    

    # event_id_list = event_id_url.split('?eid=')
    # print(event_id_list)
    
    # event_id = event_id_list[1]
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])
    # print(events)


    # event = service.events().get(calendarId='primary').execute()
    # print(event)
    # event['summary'] = 'Appointment at Somewhere'
    # updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    

def update_google_calendar2(get_cal_ev,event_name):

    SCOPES = ['http://www.googleapis.com/auth/calendar.readonly']
    creds = None
    event_id = get_cal_ev.event_id
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token1.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'create_user/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token1.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    event['summary'] = event_name
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    
    
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])
    print(event)
    return JsonResponse({'Event created:': event.get('htmlLink')})
    
@csrf_exempt
def update_erp_calendar(request):
    try:

        
        
        
        if request.POST['app'] == "1":
            data_app = request.POST['data']
            data_app = json.loads(data_app)
            
            
            subject = data_app['subject']
            starts_on = data_app['starts_on']
            ends_on = data_app['ends_on']
            owner = "Administrator"
            update = data_app['update']
        else:
            data='test'

            subject = request.POST['subject']
            starts_on = request.POST['starts_on']
            ends_on = request.POST['ends_on']
            owner = request.POST['owner']
            update = request.POST['update']
        
        # if update=="1":
        #     sys.exit()

        if update=="1":
            
            
            event_id = request.POST['event_id']
            print(event_id)
            
            
            calendar_google_url = "http://crm.birdtravels.com/api/resource/Event"+event_id+""
            data2 = {"subject":subject,"starts_on":starts_on,"ends_on":ends_on,"event_type":"Public","owner":owner,"color":"red"}
            data2 = json.dumps(data2)
            res2 = requests.put(url=calendar_google_url, verify=False, data =data2)
            return JsonResponse({"success":"true"})
        else:

            calendar_google_url = "http://crm.birdtravels.com/api/resource/Event/"
            data = {"subject":subject,"sid":"39caf9b9de80ce51605856e9c086c07acc647b6f9b8c5ee5113ff045","starts_on":starts_on,"ends_on":ends_on,"event_type":"Public","owner":owner,"color":"red"}
            data = json.dumps(data)
            print(data)

            res2 = requests.post(url=calendar_google_url, verify=False, data =data)
            print(res2.text)
            res_cal = res2.text
            res_cal = json.loads(res_cal)
            event_id = res_cal['data']['name']
        
        
        
        
        return JsonResponse({'event_id': str(event_id)})
    except Exception as e:
        print(e)

@csrf_exempt
def update_erp_calendar2(request):
    try:

        

        subject = request.POST['subject']
        starts_on = request.POST['starts_on']
        ends_on = request.POST['ends_on']
        owner = request.POST['owner']
        update = request.POST['update']
        


        if update=="1":
            print("exsit")
            event_id = request.POST['event_id']
            print(event_id)
            
            calendar_google_url = "https://crm.birdtravels.com/api/resource/Event"+event_id+""
            data2 = {"subject":subject,"starts_on":starts_on,"ends_on":ends_on,"event_type":"Public","owner":owner,"color":"red"}
            data2 = json.dumps(data2)
            res2 = requests.put(url=calendar_google_url, verify=False, data =data2)
            return JsonResponse({"success":"true"})
        else:

            calendar_google_url = "https://crm.birdtravels.com/api/resource/Event/"
            data2 = {"subject":subject,"starts_on":starts_on,"ends_on":ends_on,"event_type":"Public","owner":owner,"color":"red","sid":"39caf9b9de80ce51605856e9c086c07acc647b6f9b8c5ee5113ff045"}
            #data2 = json.dumps(data2)
            #data2 = {"subject":"sethi","starts_on":"2019-05-22 13:32:38.000000","ends_on":"2019-05-25 13:32:38.000000","event_type":"Public"}
            data2 = json.dumps(data2)
            res2 = requests.post(url=calendar_google_url, verify=False, data =data2)
            print(res2.text)
            res_cal = res2.text
            res_cal = json.loads(res_cal)
            event_id = res_cal['data']['name']
        
        
        
        
        return JsonResponse({'event_id': str(event_id)})
    except Exception as e:
        print(e)



class Get_Location_Api(APIView):
    @csrf_exempt
    def get(self,request,format=None):
        email = request.GET.get('email')
        get_coordinates = Location.objects.filter(email_id=email)
        return Response({"event":json.dumps(get_coordinates)})


#class Erp_Calendar(APIView):

#    @csrf_exempt
 #   def get(self,request,format=None):
        #calendar_google_url = "http://crm.birdtravels.com/api/resource/Event"
        #&filters=[["Event","name","=","EV00039"]]
  #      starts_on = request.GET.get('starts_on')
 #       ends_on = request.GET.get('ends_on')
#	#start_time = request.GET.get('start_time')
  #      sid = request.GET.get('sid')
        
   #     calendar_google_url = 'http://crm.birdtravels.com/api/resource/Event?sid='+sid+'&fields=["*"]&filters=[["Event","starts_on",">=","'+starts_on+'"],["Event","starts_on","<=","'+ends_on+'"]]'
        
        #params = {"fields":json.dumps(params_field),"filter":json.dumps(param_filter)}
    #    res2 = requests.get(url=calendar_google_url)
        
 #       return Response({"event":json.loads(res2.text)})
#
  #  @csrf_exempt
   # def post(self,request,format=None):
        
        
        
    #    update = request.data['update']
        # if request.data['app'] == "1":
        #     print(request.data)
        #     customer_name =request.data['customer_name']
        #     description =request.data['description']
            
        #     data_app = request.data['app']
        #     status = request.data['status']
        #     if status =='':
        #         status = 'Scheduled'
        #     #data_app = json.loads(data_app)
            
            
        #     subject = request.data['subject']
        #     starts_on = request.data['starts_on']
        #     ends_on = request.data['ends_on']
            
        #     owner = "Administrator"
        #     #customer_name =request.data['update']
        #     update = request.data['update']
        # else:
        #     subject = request.data['subject']
        #     customer_name =request.data['customer_name']
        #     description =request.data['description']
        #     starts_on = request.data['starts_on']
        #     ends_on = request.data['ends_on']
        #     owner = request.data['owner']
        #     update = request.data['update']

     #   if update=="1":
      #      print(request.data)
       #     #sys.exit()
        #    #airline = request.data['airline']
         #   event_id = request.data['oppor_id']
          #  status = request.data['status']
#
      #      calendar_google_url = "http://crm.birdtravels.com/api/resource/Event/"+event_id+""
 #           #print(calendar_google_url)
  #          #ends_on = ends_on + " 23:59:00"
   #         #sys.exit()
    #        data2 = {"status":status,"api":1}
     #       
            #data2 = {"status":status,"airline":airline,"subject":subject,"starts_on":starts_on,"ends_on":ends_on,"event_type":"Public","owner":owner,"color":"red","customer_name":customer_name,"description":description,"api":1}
       #     data2 = json.dumps(data2)
        #    print(data2)

         #   res2 = requests.put(url=calendar_google_url, verify=False, data =data2)
          #  print(res2.text)
          #  return JsonResponse({"success":"true"})
       # else:
      #      print(type(starts_on))
#            airline = request.data['item_name']
       #     print(type(ends_on))
        #    ends_on = ends_on + " 23:59:00"
         #   print(ends_on)
          #  calendar_google_url = "http://crm.birdtravels.com/api/resource/Event"
           # data = {"status":status,"airline":airline,"subject":subject,"starts_on":starts_on,"ends_on":ends_on,"event_type":"Public","owner":owner,"color":"red","customer_name":customer_name,"description":description,"api":1}
       #     data = json.dumps(data)
           # res2 = requests.post(url=calendar_google_url, verify=False, data =data)    
        #    res_cal = res2.text
         #   print(res_cal)
          #  res_cal = json.loads(res_cal)
           # print(res_cal)
            
            #event_id = res_cal['data']['name']
        

      #  return Response({'event_id': str(event_id)})

#http://crm.birdtravels.com/api/method/businessx.auth.get_role_based_res





class Erp_Calendar(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        #calendar_google_url = "https://crm.birdtravels.com/api/resource/Event"
        #&filters=[["Event","name","=","EV00039"]]
        starts_on = request.GET.get('starts_on')
        ends_on = request.GET.get('ends_on')
        #start_time = request.GET.get('start_time')
        sid = request.GET.get('sid')
        
        calendar_google_url = 'https://crm.birdtravels.com/api/resource/Event?sid='+sid+'&fields=["*"]&filters=[["Event","starts_on",">=","'+starts_on+'"],["Event","starts_on","<=","'+ends_on+'"]]'
        
        #params = {"fields":json.dumps(params_field),"filter":json.dumps(param_filter)}
        res2 = requests.get(url=calendar_google_url)
        
        return Response({"event":json.loads(res2.text)})

    @csrf_exempt
    def post(self,request,format=None):
        customer_name =request.data['name']
        subject= request.data['address_title']
	#customer_name =request.data['customer_name']
        description =request.data['description']
        employee = request.data['usr']
        if request.data['app'] == "1":
            data_app = request.data['app']
            status = request.data['status']
            if status =='':
                status = 'Scheduled'
                color = '#428b46'
            elif status=='Completed':
                color = '#4d4da8'
            elif status=='ReScheduled':
                color = 'a89f45'
            
            
            subject = request.data['address_title']
            starts_on = request.data['starts_on']
            ends_on = request.data['ends_on']
            owner = request.data['usr']
            update = request.data['update']
        else:
            if status =='':
                status = 'Scheduled'
                color = '#428b46'
            elif status=='Completed':
                color = '#4d4da8'
            elif status=='ReScheduled':
                color = 'a89f45'
            subject = request.data['address_title']
            starts_on = request.data['starts_on']
            ends_on = request.data['ends_on']
            owner = request.data['usr']
            update = request.data['update']
        if update=="1":
            
            airline = request.data['airline']
            event_id = request.data['oppor_id']
            territory = request.data['territory']
            calendar_google_url = "https://crm.birdtravels.com/api/resource/Event/"+event_id+""
            
            
            data2 = {"status":status,"territory":territory,"color":color,"user":employee,"product":airline,"subject":subject,"event_type":"Public","owner":owner,"color":"red","customer_name":customer_name,"description":description,"api":1}
            data2 = json.dumps(data2)
            res2 = requests.put(url=calendar_google_url, verify=False, data =data2)
            return JsonResponse({"success":"true"})
        else:
            airline = request.data['item_name']
            start_time = request.data['starts_time']
            starts_on = starts_on + " "+start_time
            ends_on = ends_on + " 23:59:00"
            calendar_google_url = "https://crm.birdtravels.com/api/resource/Event"
            data = {"status":status,"user":employee,"color":color,"product":airline,"subject":subject,"starts_on":starts_on,"ends_on":ends_on,"event_type":"Public","owner":owner,"color":"red","customer_name":customer_name,"description":description,"api":1}
            data = json.dumps(data)
            res2 = requests.post(url=calendar_google_url, verify=False, data =data)    
            res_cal = res2.text
            res_cal = json.loads(res_cal)
            event_id = res_cal['data']['name']
        

        return Response({'event_id': str(event_id)})

class Erp_Calendar_List(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        #calendar_google_url = "http://crm.birdtravels.com/api/resource/Event"
        #&filters=[["Event","name","=","EV00039"]]
        today = datetime.today()
        datem = datetime(today.year, today.month, 1)
        # starts_on = str(datem)
        # print(starts_on)
        
        # ends_on = str(datem)

        # ends_on = ends_on.replace("-01","-31")
        
        
        sid = request.GET.get('sid')
        
        calendar_google_url = 'https://crm.birdtravels.com/api/resource/Event?sid='+sid+'&fields=["*"]'
        
        
        params_field = ["subject"]
        param_filter = [["Event","name","=","EV00039"]]
        params = {"fields":json.dumps(params_field),"filter":json.dumps(param_filter)}
        res2 = requests.get(url=calendar_google_url)
        return Response({"event":json.loads(res2.text)})

    @csrf_exempt
    def post(self,request,format=None):
        
        print(request.data['app'])
        
        

        if request.data['app'] == "1":
            print(request.data)
            
            data_app = request.data['app']
            #data_app = json.loads(data_app)
            
            
            subject = request.data['subject']
            starts_on = request.data['starts_on']
            ends_on = request.data['ends_on']
            owner = "Administrator"
            update = request.data['update']
        else:
            subject = request.data['subject']
            starts_on = request.data['starts_on']
            ends_on = request.data['ends_on']
            owner = request.data['owner']
            update = request.data['update']

        if update=="1":
            
            event_id = request.data['event_id']

            calendar_google_url = "https://crm.birdtravels.com/api/resource/Event/"+event_id+""
            print(calendar_google_url)
            
            data2 = {"subject":subject,"starts_on":starts_on,"ends_on":ends_on,"event_type":"Public","owner":owner,"color":"red","api":1}
            data2 = json.dumps(data2)
            res2 = requests.put(url=calendar_google_url, verify=False, data =data2)
            print(res2.text)
            return JsonResponse({"success":"true"})
        else:

            calendar_google_url = "http://crm.birdtravels.com/api/resource/Event"
            data = {"subject":subject,"starts_on":starts_on,"ends_on":ends_on,"event_type":"Public","owner":owner,"color":"red"}
            data = json.dumps(data)
            res2 = requests.post(url=calendar_google_url, verify=False, data =data)
            print(res2.text)
            
            res_cal = res2.text
            res_cal = json.loads(res_cal)
            print(res_cal)
            
            event_id = res_cal['data']['name']
        

        return Response({'event_id': str(event_id)})

class Role_Based_Auth(APIView):

    def get(self,request,format=None):
        url = "https://crm.birdtravels.com/api/method/businessx.auth.get_role_based_ress?sid=8cf1c641585294be8fdeb61984b76ebcf44da2496269001277c0ef26&email=r@gmail.com"
        
        res2 = requests.get(url=url)
        print(res2.text)
        
        res_json = json.loads(res2.text)

        
        return Response({'response':res_json})


    def post(self,request,format=None):
        pass
class Get_Address_details(APIView):
    @csrf_exempt
    def get(self,request,format=None):
        address_title = request.GET.get('address_data')
        sid = request.GET.get('sid')
        print(address_title)
        event_url = 'https://crm.birdtravels.com/api/resource/Address/'+address_title+'?sid='+sid+''
        
        res2 = requests.get(url=event_url)
        res2 = json.loads(res2.text)
        return Response({"event":res2})

        
class Erp_Calendar_Event(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        event_id = request.GET.get('oppor_id')
        sid = request.GET.get('sid')
        event_url = 'https://crm.birdtravels.com/api/resource/Event?sid='+sid+'&fields=["*"]&filters=[["Event","name","=","'+event_id+'"]]'
        res2 = requests.get(url=event_url)
        print(res2.text)
        sid = request.GET.get('sid')
        res2 = json.loads(res2.text)
        customer_name_lead = 'https://crm.birdtravels.com/api/resource/Contact?sid='+sid+'&fields=["*"]&filters=[["Contact","link_name","=","'+res2['data'][0]['customer_name']+'"]]'
        res1 = requests.get(url=customer_name_lead)
        res1 = json.loads(res1.text)
        
        i=0
        for res in res1['data']:
            res2['data'][0].update({'mobile_no':res['mobile_no'],'email_id':res['email_id'],'contact_person':res['first_name']})
            i+=1
            if i==3:
                break;
            
            
            
        
        
        print(res2)

        return Response({"event":res2})




    def post(self,request,format=None):
        
        event_id = request.data('event_id')
        event_url = 'https://crm.birdtravels.com/api/resource/Event?fields=["*"]&filters=[["Event","name","=","'+event_id+'"]]'
        pass
        #res2 = requests.get(url=event_url)
        #print(res2.text)
        #return Response({"event":json.loads(res2.text)})



class Delete_Event_Api(APIView):
    @csrf_exempt
    def get(self,request,format=None):
        pass

    def post(self,request,format=None):
        print(request.data)
        
        event_id = request.data['oppor_id']

        event_url = 'https://crm.birdtravels.com/api/resource/Event/'+event_id+'?args=1'
        print(event_url)
        
        r = requests.delete(event_url)
        print(r.text)
        
        return Response({"status":json.loads(r.text)})

class Insert_Erp_User(APIView):
    def post(self,request,format=None):
        first_name = request.data['first_name']
        last_name =  request.data['last_name']
        email_id =   request.data['email_id']
        insert_user = 'https://crm.birdtravels.com/api/resource/User'
        data2 = {"first_name":first_name,"last_name":last_name,"api":1,"email_id":email_id}
        data2 = json.dumps(data2)
        res2 = requests.post(url=insert_user,verify=False, data =data2)
        return Response({"address":json.loads(res2.text)})

class Customers_Data_All(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        sid = request.GET.get('sid')
        customer_url = 'https://crm.birdtravels.com/api/resource/Address?sid='+sid+'&fields=["*"]&limit_page_length=10'
        res2 = requests.get(url=customer_url)
        return Response({"event":json.loads(res2.text)})

class Customers_Data(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        sid = request.GET.get('sid')
        customer_url = 'https://crm.birdtravels.com/api/resource/Customer?sid='+sid+'&fields=["*"]&limit_page_length=40'
        res2 = requests.get(url=customer_url)
        return Response({"event":json.loads(res2.text)})

    @csrf_exempt
    def post(self,request,format=None):

        
        try:
             mobile_no = request.data['mobile_no']
        except:
             mobile_no="0000000000"
        try:
            place = request.data['place']
        except:
            place = " "
        try:
            email_id = request.data['email_id']
        except Exception as e:
            print(e)
            email_id = ""
            pass
        customer_name = request.data['customer_name']
        update = request.data['update']

        
     #   data_app = request.data['app']
        #data_app = json.loads(data_app)
        
        
    #    email_id = request.data['email_id']
   #     mobile_no = request.data['mobile_no']
  #      customer_name = request.data['customer_name']
 #       # owner = "Administrator"
#        update = request.data['update']
        

        if update=="1":
            
            customer_id = request.data['customer_id']

            customer_url = "https://crm.birdtravels.com/api/resource/Customer/"+customer_id+""
            print(customer_url)
            data2 = {"email_id":email_id,"mobile_no":mobile_no,"customer_name":customer_name,"api":1,"app":1} 
            data2 = json.dumps(data2)
            res2 = requests.put(url=customer_url, verify=False, data =data2)
            print(res2.text)
            return JsonResponse({"success":"true"})

        else:


            customer_url = "https://crm.birdtravels.com/api/resource/Customer/"
           
            
            data2 = {"email_id":email_id,"mobile_no":mobile_no,"customer_name":customer_name,"api":1}
            data2 = json.dumps(data2)
            res2 = requests.post(url=customer_url, verify=False, data =data2)
            print(res2.text)
            
            return JsonResponse({"success":json.dumps(res2.text)})


class Customer_details(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        sid = request.GET.get('sid')
        customer_name = request.GET.get('customer_name')
        
        event_url = 'https://crm.birdtravels.com/api/resource/Customer/'+customer_name+'?sid='+sid+''
        customer_name_lead = 'https://crm.birdtravels.com/api/resource/Contact?sid='+sid+'&fields=["*"]&filters=[["Contact","link_name","=","'+customer_name+'"]]'
        res2 = requests.get(url=event_url)
        res1 = requests.get(url=customer_name_lead)
        
        res1 = json.loads(res1.text)
        res2 = json.loads(res2.text)
        i=0
        for res in res1['data']:
            res2['data'].update({'mobile_no':res['mobile_no'],'email_id':res['email_id'],'contact_person':res['first_name']})
            i+=1
            if i==3:
                break;
        
        print(res2)
        
        return Response({"event":res2})


class Address_details(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        sid = request.GET.get('sid')
        customer_name = request.GET.get('customer_name')
        print(customer_name)
        
        event_url = 'http://crm.birdtravels.com/api/resource/Address?fields=["*"]&filters=[["Address","link_name","=","'+customer_name+'"]]&sid='+sid+''
        print(event_url)
        
        res2 = requests.get(url=event_url)
        print(res2.text)
        return Response({"address":json.loads(res2.text)})
    
    @csrf_exempt
    def post(self,request,format=None):
        # try:
        address_title = request.data['address_title']
        city = request.data['city']
        owner = request.data['owner']
        print(city)
        place = request.data['place']
        #address_line1 = request.data['address_line1']
        customer_name = request.data['customer_name']
        event_url = 'https://crm.birdtravels.com/api/resource/Address'
        data2 = {"city":city,"address_title":address_title,"api":1,"place":place,"customer_name":customer_name,"address_type":"Office","owner":owner}
        data2 = json.dumps(data2)
        res2 = requests.post(url=event_url,verify=False, data =data2)
        
        return Response({"address":json.loads(res2.text)})
        # except KeyError as e:
        #     return Response({"error":e.args[0]})
        



class Delete_Customer_details(APIView):
    @csrf_exempt
    def get(self,request,format=None):
        customer_name = request.GET.get('customer_name')
        customer_url = "http://crm.birdtravels.com/api/resource/Customer/"+customer_name+""
        print(customer_url)
        
        data2 = {"email_id":email_id,"mobile_no":mobile_no,"customer_name":customer_name,"api":1}
        print(data2)
        r = requests.delete(event_url)
        return Response({"status":r.text})


class Customer_Leads(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        sid = request.GET.get('sid')
        customer_name_lead = 'http://crm.birdtravels.com/api/resource/Lead?fields=["*"]&sid='+sid+''
        res2 = requests.get(url=customer_name_lead)
        print(res2.text)
        return Response({"event":json.loads(res2.text)})

    @csrf_exempt
    def post(self,request,format=None):
        print(request.data)
        
        
        #data_app = request.data['app']
        lead_name = request.data['lead_name']
        email_id = request.data['email_id']
        update = request.data['update']
        print(request.data)
        
        

        if update=="1":
            
            name = request.data['name']
            print(lead_name)
            customer_lead_url = "http://crm.birdtravels.com/api/resource/Lead/"+name+""
            data2 = {"email_id":email_id,"lead_name":lead_name,"api":1} 
            data2 = json.dumps(data2)
            res2 = requests.put(url=customer_lead_url, verify=False, data =data2)
            #print(res2.text)
            return JsonResponse({"success":"true"})

        else:
            customer_lead_url = "http://crm.birdtravels.com/api/resource/Lead/"
            data2 = {"lead_name":lead_name,"email_id":email_id,"api":1}
            data2 = json.dumps(data2)
            res2 = requests.post(url=customer_lead_url, verify=False, data =data2)

            return JsonResponse({"success":json.dumps(res2.text)})



class Lead_details(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        sid = request.GET.get('sid')
        lead_name = request.GET.get('lead_name')
        event_url = 'http://crm.birdtravels.com/api/resource/Lead?sid='+sid+'&fields=["*"]&filters=[["Lead","name","=","'+lead_name+'"]]'
        res2 = requests.get(url=event_url)
        print(res2.text)
        return Response({"event":json.loads(res2.text)})

    @csrf_exempt
    def post(self,request,format=None):
        lead_name = request.data['lead_name']
        print(lead_name)
        
        customer_lead_url = "http://crm.birdtravels.com/api/resource/Lead/"+lead_name+"?args=1"
        res2 = requests.delete(url=customer_lead_url)
        print(res2.text)
        return Response({"lead":json.loads(res2.text)})




class Delete_Opportunity(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        pass

    @csrf_exempt
    def post(self,request,format=None):
        print(request.POST)
        oppor_id = request.data['oppor_id']
        sid = request.data['sid']
        
        
        
        
        customer_lead_url = "http://crm.birdtravels.com/api/resource/Opportunity/"+oppor_id+"?sid="+sid+""
        res2 = requests.delete(url=customer_lead_url)
        print(res2.text)
        return Response({"lead":json.loads(res2.text)})

class Single_Opp_details(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        sid = request.GET.get('sid')
        oppor_id= request.GET.get('oppor_id')
        
        event_url = 'http://crm.birdtravels.com/api/resource/Opportunity?fields=["*"]&filters=[["Opportunity","name","=","'+oppor_id+'"]]'
        res2 = requests.get(url=event_url)
        print(res2.text)
        return Response({"event":json.loads(res2.text)})

    @csrf_exempt
    def post(self,request,format=None):
        enquiry_from = 'Customer'
        start_date = request.data['start_date']
        status = request.data['status']
        end_date = request.data['end_date']
        subject = request.data['subject']
        #company = "Bird Travels Pvt Ltd"
        customer = request.data['custom']
        opportunity_type = 'Sales'
        end_date = request.data['end_date']
        meeting_description = request.data['meeting_description']
        
        item_name = request.data['item_name']
        #company = request.data['company']
        customer_address = request.data['customer_address']
        contact_person = request.data['contact_person']
        territory = request.data['territory']
        contact_email = request.data['email_id']
        #customer_group = request.data['customer_group']
        contact_mobile = request.data['mobile_no']
        company = "Bird Travels Pvt Ltd"
        opp_id = request.data['oppor_id']
        
        # transaction_date = request.data['transaction_date']
        # contact_by = request.data['contact_by']
        contact_date = request.data['next_contact']
        to_discuss = request.data['to_discuss']

        data2 = {"to_discuss":to_discuss,"contact_date":contact_date,"contact_mobile":contact_mobile,"contact_email":contact_email,"territory":territory,"contact_person":contact_person,"customer_address":customer_address,"item_name":item_name,"customer":customer,"meeting_description":meeting_description,"app":1,"enquiry_from":"Customer","start_date":start_date,"company":company,"status":status,"end_date":end_date,"subject":subject,"api":1} 
        data2 = json.dumps(data2)
        event_url = 'http://crm.birdtravels.com/api/resource/Opportunity/'+opp_id+''
        res2 = requests.put(url=event_url, verify=False, data =data2)
        print(res2.text)

        return JsonResponse({"success":"true"})


class Opp_Details(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        sid = request.GET.get('sid')
        
        event_url = 'http://crm.birdtravels.com/api/resource/Opportunity?sid='+sid+'&fields=["*"]'
        print(event_url)
        
        res2 = requests.get(url=event_url)
        
        return Response({"event":json.loads(res2.text)})

    @csrf_exempt
    def post(self,request,format=None):
        print(request.data)
        
        enquiry_from = 'Customer'
        start_date = request.data['start_date']
        status = request.data['status']
        if status == ' ':
            status = "Open"
        end_date = request.data['end_date']
        

        format = "%Y-%m-%d %H:%M:%S %Z%z"
        # Current time in UTC
        now_utc = datetime.now(timezone('UTC'))
        
        now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
        if start_date == ' ':
            start_date = now_asia.strftime(format)
            start_date = start_date[0:10]
            #start_date = "2019-06-27"

        if end_date == ' ':
            end_date = now_asia.strftime(format)
            end_date = end_date[0:10]
        customer = request.data['custom']
        subject = request.data['subject']
        if subject ==' ':
            subject = customer
        
        opportunity_type = 'Sales'
        
        
        meeting_description = request.data['meeting_description']
        item_name = request.data['item_name']
        #company = request.data['company']
        customer_address = request.data['customer_address']
        #contact_by = request.data['contact_by']
        #to_discuss = request.data['to_discuss']
        contact_person = request.data['contact_person']
        territory = request.data['territory']
        try:
            if 'email_id' in request.data:
                contact_email = request.data['email_id']
        #customer_group = request.data['customer_group']
            if 'mobile_no' in request.data:
                contact_mobile = request.data['mobile_no']
        except Exception as e:
            raise e
        
        company = "Bird Travels Pvt Ltd"
        # transaction_date = request.data['transaction_date']
        contact_by = request.data['contact_by']
        if contact_by == ' ':
            contact_by = ''
        
        contact_date = request.data['next_contact']
        to_discuss = request.data['to_discuss']
        item_name = request.data['item_name']

        data2 = {"item_name":item_name,"to_discuss":to_discuss,"contact_date":contact_date,"contact_by":contact_by,"contact_mobile":contact_mobile,"contact_email":contact_email,"contact_person":contact_person,"customer_address":customer_address,"meeting_description":meeting_description,"customer_name":customer,"customer":customer,"territory":territory,"company":company,"enquiry_from":"Customer","start_date":start_date,"opportunity_type":opportunity_type,"status":status,"end_date":end_date,"subject":subject,'customer':customer} 

        data2 = json.dumps(data2)
        
        event_url = 'http://crm.birdtravels.com/api/resource/Opportunity/'
        res2 = requests.post(url=event_url, verify=False, data =data2)
        print(res2.text)
        return JsonResponse({"success":"true"})


class Contact_Details_Customer(APIView):
    @csrf_exempt
    def get(self,request,format=None):
        sid = request.GET.get('sid')
        customer_name = request.GET.get('customer_name')
        customer_name_lead = 'http://crm.birdtravels.com/api/resource/Contact?fields=["*"]&filters=[["Contact","link_name","=","'+customer_name+'"]]'
        res2 = requests.get(url=customer_name_lead)
        print(res2.text)
        return Response({"event":json.loads(res2.text)})


class Contact_Data(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        sid = request.GET.get('sid')
        customer_name_lead = 'http://crm.birdtravels.com/api/resource/Contact?sid='+sid+'fields=["*"]'
        res2 = requests.get(url=customer_name_lead)
        print(res2.text)
        return Response({"event":json.loads(res2.text)})

    @csrf_exempt
    def post(self,request,format=None):
        print(request.data)
        
        #data_app = request.data['app']
        first_name = request.data['first_name']
        email_id = request.data['email_id']
        update = request.data['update']
        salutation = request.data['salutation']
        mobile_no = request.data['mobile_no']
        

        if update=="1":
            
            name = request.data['contact_name']
            
            customer_lead_url = "http://crm.birdtravels.com/api/resource/Contact/"+name+""
            data2 = {"first_name":first_name,"email_id":email_id,"api":1,"salutation":salutation,"mobile_no":mobile_no} 
            data2 = json.dumps(data2)
            res2 = requests.put(url=customer_lead_url, verify=False, data =data2)
            #print(res2.text)
            return JsonResponse({"success":"true"})

        else:
            customer_lead_url = "http://crm.birdtravels.com/api/resource/Contact/"
            data2 = {"first_name":first_name,"email_id":email_id,"api":1,"salutation":salutation,"mobile_no":mobile_no}
            data2 = json.dumps(data2)
            res2 = requests.post(url=customer_lead_url, verify=False, data =data2)
            print(res2.text)
            
            return JsonResponse({"success":json.dumps(res2.text)})


class Contact_Details(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        contact_name = request.GET.get('contact_name')
        print(contact_name)
        
        event_url = 'http://crm.birdtravels.com/api/resource/Contact?fields=["*"]&filters=[["Contact","name","=","'+contact_name+'"]]'
        print(event_url)

        res2 = requests.get(url=event_url)
        print(res2.text)
        return Response({"event":json.loads(res2.text)})

    @csrf_exempt
    def post(self,request,format=None):
        contact_name = request.data['contact_name']
        customer_lead_url = "http://crm.birdtravels.com/api/resource/Contact/"+contact_name+"?args=1"
        res2 = requests.delete(url=customer_lead_url)
        print(res2.text)
        return Response({"lead":json.loads(res2.text)})





class Filter_Data_Doctype(APIView):
    """docstring for ClassName"""
    @csrf_exempt
    def get(self,request,format=None):
        print(request.GET)
        try:
            doctype_name = request.GET.get('doctype_name')
            starts_on = request.GET.get('starts_on')
            ends_on = request.GET.get('ends_on')
            doctype_field_name = request.GET.get('doctype_field_name')
            doctype_field_data= request.GET.get('doctype_field_data')
            try:
                if request.GET.get('state'):
                    state= request.GET.get('state')
                    state = state.replace(" ","")
            except NameError:
                state = ""
            sid = request.GET.get('sid')
            
            operator = request.GET.get('operator')
            
        except Exception as e:
            pass
        if state!='undefined':
            filter_url = 'http://crm.birdtravels.com/api/resource/'+doctype_name+'?sid='+sid+'&fields=["*"]&filters=[["'+doctype_name+'","'+doctype_field_name+'","'+operator+'","'+doctype_field_data+'%"],["Address","state","=","'+state+'"]]'
        else:

            filter_url = 'http://crm.birdtravels.com/api/resource/'+doctype_name+'?sid='+sid+'&fields=["*"]&filters=[["'+doctype_name+'","'+doctype_field_name+'","'+operator+'","'+doctype_field_data+'%"]]'
        print(filter_url)
        res2 = requests.get(url=filter_url)
        print(res2.text)
        return Response({"event":json.loads(res2.text)})


        
        

class Insert_Attendance(APIView):
    @csrf_exempt
    def get(self,request,format=None):
        pass

    @csrf_exempt
    def post(self,request,format=None):
        customer_lead_url = "http://crm.birdtravels.com/api/resource/Attendance/"
        attendance_date = request.data['attendance_date']
        company = request.data['company']
        docstatus = request.data['docstatus']
        sid = request.data['sid']
        data2 = {"employee":"EMP/0001","attendance_date":attendance_date,"company":"KIneticx","status":"Present","docstatus":1,"api":1,"sid":sid}
        data2 = json.dumps(data2)
        res2 = requests.post(url=customer_lead_url, verify=False, data =data2)
        print(res2.text)




class Get_Territories(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        filter_url = 'http://crm.birdtravels.com/api/resource/Territory'


        res2 = requests.get(url=filter_url)
        print(res2.text)
        return Response({"event":json.loads(res2.text)})


class Get_Item(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        sid = request.GET.get('sid')
        filter_url = 'http://crm.birdtravels.com/api/resource/Item?sid='+sid+''


        res2 = requests.get(url=filter_url)
        print(res2.text)
        return Response({"items":json.loads(res2.text)})
        

class Designation_List(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        filter_url = 'http://crm.birdtravels.com/api/resource/Designation'


        res2 = requests.get(url=filter_url)
        print(res2.text)
        return Response({"designation":json.loads(res2.text)})

class Designation_List(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        filter_url = 'http://crm.birdtravels.com/api/resource/Designation'


        res2 = requests.get(url=filter_url)
        
        return Response({"designation":json.loads(res2.text)})



class Get_Lead_Emm(APIView):

    @csrf_exempt
    def post(self,request,format=None):
        
        data = request.data
        
        email = data['email_id']
        mobile_no = data['mobile_no']
        
        to_do_url = "https://emm.kxterp.in/api/resource/Lead/"

        data2 = {"email_id":email,"owner":"mohit@emmemmgroup.com","mobile_no":mobile_no,"api":1,"company_website":data['company'],"lead_name":data['lead_name'],"enquiry":data['comments'],"source":"Website"}
        data2 = json.dumps(data2)
        
        res2 = requests.post(url=to_do_url, verify=False, data =data2)
       
        
        return Response({"success":res2.text})


class ToDo_Single_Item(APIView):


    @csrf_exempt
    def get(self,request,format=None):
        
        todo= request.GET.get('todo')
        
        event_url = 'http://crm.birdtravels.com/api/resource/ToDo?fields=["*"]&filters=[["ToDo","name","=","'+todo+'"]]'
        res2 = requests.get(url=event_url)
        
        return Response({"todo":json.loads(res2.text)})

    @csrf_exempt
    def post(self,request,format=None):
        

        todo = request.data['todo']
        due_date = request.data['due_date']
        description = request.data['description']
        #subject = request.data['description']
        status = request.data['status']
        priority = request.data['priority']
        users = request.data['users']
        to_do_url = "http://crm.birdtravels.com/api/resource/ToDo/"+todo+""

        data2 = {'app':1,'api':1,'description':description,'date':due_date,'status':status,'users':users,'priority':priority}
        data2 = json.dumps(data2)
        print(data2)
        
        res2 = requests.put(url=to_do_url, verify=False, data =data2)
        print(res2.text)
        
        return Response({"success":res2.text})






class ToDo(APIView):

    @csrf_exempt
    def get(self,request,format=None):
        sid =request.GET.get('sid')
        starts_on = request.GET.get('starts_on')
        ends_on = request.GET.get('ends_on')
        print(starts_on)
        print(ends_on)


        filter_url = 'http://crm.birdtravels.com/api/resource/ToDo?sid='+sid+'&fields=["*"]&filters=[["ToDo","date",">=","'+starts_on+'"],["ToDo","date","<=","'+ends_on+'"]]'


        res2 = requests.get(url=filter_url)
        print(res2.text)
        return Response({"todo":json.loads(res2.text)})

    @csrf_exempt
    def post(self,request,format=None):
        print(request.data)

        due_date = request.data['due_date']
        description = request.data['description']
        status = request.data['status']
        priority = request.data['priority']
        to_do_url = "http://crm.birdtravels.com/api/resource/ToDo/"
        owner = request.data['users']
        data2 = {'owner':owner,'priority':priority,'description':description,'date':due_date,'status':status}
        data2 = json.dumps(data2)
        res2 = requests.post(url=to_do_url, verify=False, data =data2)
        return Response({"success":"true"})



class Get_User(APIView):
    @csrf_exempt
    def get(self,request,format=None):
        sid =request.GET.get('sid')
        filter_url = 'http://crm.birdtravels.com/api/resource/User?fields=["email"]'
        res2 = requests.get(url=filter_url)
        print(res2.text)
        return Response({"user":json.loads(res2.text)})


class ToDoDelete(APIView):

    @csrf_exempt
    def post(self,request,format=None):
        todo = request.data['todo']
        to_do_url = "http://crm.birdtravels.com/api/resource/ToDo/"+todo+""


        res2 = requests.delete(url=to_do_url)

        return Response({"todo":json.loads(res2.text)})

class FB_Leads(APIView):
    @csrf_exempt
    def get(self,request,format=None):
        p1 = multiprocessing.Process(target=get_facebook_leads)
        # starting process 1 
        p1.start()
         # wait until process 1 is finished 
        p1.join()

                        
                    
                    
                    

            
        
def get_facebook_leads():
    import re
        
    #fb_api_url = "https://graph.facebook.com/v3.3/496655984413061/leads?access_token=EAAGRCL3LZA0QBAOq90Vn4Lq54eRBGEqxPZAY6zsgnZAZCJrXkC1ZBNXiHfmAlsdHqMRpPCw9ekkEyVwKZAfxIvf8dK8Xe2FtLJM9mYBt9piotO9mmJ03GuaB88994M3Rcc6HNNen3VlqxxV9tkvIxvOZCLbrhPE5EYfojuc4R1nW67jhSrgbJIA"
    #fb_api_url = "https://graph.facebook.com/v3.3/1657944727554586?fields=leadgen_forms{leads.limit(100)}&access_token=EAAGRCL3LZA0QBAE69EJFZCTrJZCub1lQHyoBeGm3VCtLqmZCewgRLhkUTiIUYpkZAeQHYZC8NWvygZAXEUzxMz3u2BT6soPu3DWtzyZC50veH11XKiMgYhPjJdQ14dtRTY7jkg7gtnAxwmEXvhR9yWnKmtC0bUgDqbww6HIQQ1vQhDvlFu7LitcFdSVC2tcpZBPoZD"
    fb_api_url = "https://graph.facebook.com/1657944727554586?fields=leadgen_forms{leads.limit(10000){field_data,created_time,campaign_name,campaign_id}}&access_token=EAAGRCL3LZA0QBABKa1sYpWTZCZBLqi0WxgJjD0XhIGynEZCZCImpSfW6eKilcTgeMwlgreu4Gj58iDvZB4DDoH9TzcvES3VpvZBCuGXREWyZCqUFpny0ZBdlugNmYji3fudRIevAzkPGdWrKELjyV3E4raTSe3NsPflKsYA0njoJwlEbuVDBLct71ZBT6s3sCVtc4ZD"




    res2 = requests.get(url=fb_api_url)
    result = res2.text

    
    #result = result.replace("!@#$%^&*()†[]{};:,./<>?\|`~-=_+", " ")
    jsondata = json.loads(result)
    

    jsondata = jsondata['leadgen_forms']
    

    for res in jsondata['data']:
        
        
        full_name = city = phone_number = email =num_of_travellers=campaign_name=campaign_id=date_of_travel=''
        if 'leads' in res.keys():
            
            for field in res['leads']['data']:
                campaign_id = field['campaign_id']
                campaign_name = field['campaign_name']
                created_time = field['created_time']
                ids = field['id']
                print(ids)
                
                
                for field_data in field['field_data']:
                    
                
                    if field_data['name'] == 'date_of_travel':
                        
                        date_of_travel = field_data['values'][0]
                    
                    if field_data['name'] == 'full_name':
                        
                        full_name = field_data['values'][0]
                    
                    if field_data['name'] == 'city':
                        city = field_data['values'][0]
                        
                        
                    if field_data['name'] == 'phone_number':
                        phone_number = field_data['values'][0]
                        

                    if field_data['name'] == 'number_of_travellers':
                        
                        num_of_travellers = field_data['values'][0]
                    
                    if field_data['name'] == 'email':
                        email = field_data['values'][0]
                
                
                check_lead_url_id = 'https://acchajee.kxterp.in/api/resource/Lead/?fields=["*"]&filters=[["Lead","email_id","=","'+email+'"],["Lead","campaign_id","=","'+campaign_id+'"]]'
                print(check_lead_url_id)
                
                response11 = requests.get(url=check_lead_url_id)
                response_json1 = json.loads(response11.text)
                print(response_json1)
                
                if not response_json1['data']:
                    customer_lead_url = "https://acchajee.kxterp.in/api/resource/Lead/"
                    data2 = {"uni_id":ids,"campaign_name":campaign_name,"facebook_date":created_time,"campaign_id":campaign_id,"current_city":city,"lead_name":full_name,"email_id":email,"api":1,"lead_owner":"Administrator","mobile_no":phone_number,"source": "Facebook leads","adult":num_of_travellers,"tour_date":date_of_travel}
                    data2 = json.dumps(data2)
                    
                    res22 = requests.post(url=customer_lead_url, verify=True, data =data2)
                    print(res22.text)
                else:
                    print("not i nserted")
                    

        




                

        
        
      #  sys.exit()


def next_page_fb_data(url):
    
    res2 = requests.get(url=url)
    result = res2.text
    jsondata = json.loads(result)
    for res in jsondata['data']:
        full_name = city = phone_number = email =''
        for field_data in res['field_data']:
            


           if field_data['name'] == 'full_name':
                
                
                full_name = field_data['values'][0]

           if field_data['name'] == 'city':
                city = field_data['values'][0]
                print(city) 
                
           if field_data['name'] == 'phone_number':
                phone_number = field_data['values'][0]
           if field_data['name'] == 'email':
                email = field_data['values'][0]

        customer_lead_url = "https://acchajee.kxterp.in/api/resource/Lead/"
        data2 = {"lead_name":full_name,"email_id":email,"api":1,"source": "Facebook leads","mobile_no":phone_number,"lead_owner":"Administrator"}
        data2 = json.dumps(data2)
        res22 = requests.post(url=customer_lead_url, verify=False, data =data2)
        print(res22.text)
    if  jsondata['paging']['next']:
        next_page_fb_data(jsondata['paging']['next'])

class Sales_Invoice(APIView):
    @csrf_exempt
    def get(self,request,format=None):
        sales_invoice = "https://crm.birdtravels.com/api/resource/Use%22?limi%22_%22age_%22en%22th=al%22&%22ield%22=[%22email%22,%22name%22]"
        res = requests.get(url = sales_invoice,verify=False)
        s_inv_response = json.loads(res.text)
        s_inv_response = s_inv_response['data']
        print(s_inv_response)
        
        for s in s_inv_response:
            sales_invoice_name = "https://birdadmin.birdtravels.com/users_list/"
            if not s['email']:
                s['email'] = 'test@biradadmin.com'
            print(s['email'])
            data = {"email":s['email'],"title":s['name']}
            print(data)
            
            res2 = requests.post(url=sales_invoice_name,verify=True,data = data)
            print(res2.text)
            #sys.exit()
            
            
        #return HttpResponse(res.text)
    



@api_view(['GET', 'POST','OPTIONS'])
def item_retrieval_api2(request):
    import collections
    parent_list = []
    item_group_api = 'http://14.98.78.69:2233/api/resource/Item%20Group?limit_page_length=100&fields=["*"]&filters=[["Item Group","parent_item_group","=","All Item Groups"]]'
    res = requests.get(url = item_group_api,verify=False)
    response_data = json.loads(res.text)

    item_group_api2 = 'http://14.98.78.69:2233/api/resource/Item%20Group?limit_page_length=&fields=["*"]'
    res2 = requests.get(url = item_group_api2,verify=False)
    response_data2 = json.loads(res2.text)
    
    
    for data in response_data['data']:
        #if data['parent_item_group'] == "All Item Groups":
        parent_list.append(data['name'])
    sub_child_list = []

    sub_resp = {}
    
    
    for dataq in parent_list:
        underscore_str = ""
        resp = {}

        child_resp1 = {}
        for parent in response_data2['data']:

            
            if parent['parent_item_group'] == dataq:
                
                underscore_str = dataq.replace(" ", "_")
                underscore_str = underscore_str.lower()
                child_list = []
                for child in response_data2['data']:

                    if child['parent_item_group'] == parent['name']:
                        child_list.append(child['name'])
                resp[parent['name']] = {'opt':child_list,'name':parent['name']}
                resp.update(resp)
                child_resp1['options'] = resp
        
        sub_resp[dataq] = child_resp1
        sub_resp[dataq]['name'] = dataq
                # resp[dataq] = {'key':underscore_str,'name':dataq,'p':parent['name']}
                # resp[dataq]['options'] = {parent['name']:{}}
                # sub_child_list.append(resp)
           
    
    # for z in sub_child_list:
    #     options_list = []
    #     for x,y in z.items():
            
    #         for r in response_data2['data']:
    #             if r['parent_item_group']==y['p']:
    #                 options_list.append(r['name'])
        
        
    #     y['options'][y['p']]['opt'] = options_list
    #     y['options'][y['p']].update({'name':y['p']})
        
       
    # dict_obj = {}
    # i = 0
    # for dict_key in sub_child_list:
    #     dict_obj.update(dict_key)
        
    od = collections.OrderedDict(sorted(sub_resp.items()))

    return Response({"item_group":od})


class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value


@api_view(['GET', 'POST','OPTIONS'])
def item_detail(request):
    item_group = request.GET['item_group']
    sub_item_group = request.GET['sub_item_group']
    main_item_group = request.GET['main_item_group']
    if item_group=="":
        item_detail_api = 'http://14.98.78.69:2233/api/resource/Item?fields=["*"]&filters=[["Item","sub_category","=","'+sub_item_group+'"],["Item","main_category","=","'+main_item_group+'"]]'
    elif sub_item_group=="":
        item_detail_api = 'http://14.98.78.69:2233/api/resource/Item?fields=["*"]&filters=[["Item","item_group","=","'+item_group+'"],["Item","main_category","=","'+main_item_group+'"]]'
    else:
        item_detail_api = 'http://14.98.78.69:2233/api/resource/Item?fields=["*"]&filters=[["Item","sub_category","=","'+sub_item_group+'"],["Item","item_group","=","'+item_group+'"],["Item","main_category","=","'+main_item_group+'"]]'
        



    res = requests.get(url = item_detail_api,verify=False)
    response_data = json.loads(res.text)
    
    return Response({"item_list":response_data})

@api_view(['GET', 'POST','OPTIONS'])
def single_item_detail(request):
    
    
    name = request.GET['name']
    variant_of = request.GET['variant_of']
    if variant_of != "":
        single_item_api = 'http://14.98.78.69:2233/api/resource/Item?fields=["name"]&filters=[["Item","variant_of","=","'+variant_of+'"]]'
    else:
        single_item_api = 'http://14.98.78.69:2233/api/resource/Item?fields=["name"]&filters=[["Item","name","=","'+name+'"]]'


    res = requests.get(url = single_item_api,verify=False)
    response_data = json.loads(res.text)
    list_of_item = []
    sid = get_sid()
    for z in response_data['data']:
        single_api =  'http://14.98.78.69:2233/api/resource/Item/'+z['name']+'?sid='+sid+''
        res2 = requests.get(url = single_api,verify=False)
        response_data2 = json.loads(res2.text)
        list_of_item.append(response_data2['data'])
    return Response({"item":list_of_item})
   
    
@api_view(['GET', 'POST','OPTIONS'])
def popular_api(request):
    single_item_api = 'http://14.98.78.69:2233/api/resource/Item?fields=["*"]&filters=[["Item","popular_product","=","1"]]&limit_page_length='
    res = requests.get(url = single_item_api,verify=False)
    response_data = json.loads(res.text)
    return Response({"item":response_data})


@api_view(['GET', 'POST','OPTIONS'])
def brands(request):
    
    brands_url = 'http://14.98.78.69:2233/api/resource/Brand?fields=["*"]'
    res = requests.get(brands_url,verify=False)
    response_data = json.loads(res.text)
    return Response({"brands":response_data})

@api_view(['GET', 'POST','OPTIONS'])
def brands_list(request):
    
    id = request.GET['id']
    list_of_brand = id.split(',')
    sid = get_sid()
    brands_list = {}
    for l in list_of_brand:
        brands_url2 = 'http://14.98.78.69:2233/api/resource/Brand/'+l+'?sid='+sid+''
        print(brands_url2)
        res2 = requests.get(brands_url2,verify=False)
        response_data2 = json.loads(res2.text)
        print(response_data2)
        brands_list.update({l:response_data2['data']})

    
    
    return Response({"brands":brands_list})


@api_view(['GET', 'POST','OPTIONS'])
def item(request):
    item_code_2 = request.GET['item_code']
    list_of_brand = item_code_2.split(',')
    brands_list = []
    for l in list_of_brand:
        brands_url = 'http://14.98.78.69:2233/api/resource/Item?fields=["*"]&filters=[["Item","name","=","'+l+'"]]'
        res = requests.get(brands_url,verify=False)
        response_data = json.loads(res.text)
        brands_list.append(response_data['data'])
    return Response({"items":brands_list[0]})



@api_view(['GET', 'POST','OPTIONS'])
def get_tax_information(request):

    sid = get_sid()
    item_code = request.GET['item_code']
    list_of_brand = item_code.split(',')
    res2 = {}
    for l in list_of_brand:
        
        item_detail_api1 = 'http://14.98.78.69:2233/api/resource/Item/'+l+'?sid='+sid+''
        res = requests.get(item_detail_api1,verify=False)
        response_data = json.loads(res.text)
        res1 = {l:response_data['data']['taxes']}
        res2.update(res1)
    
    return Response({"taxes":res2})
        

@api_view(['GET', 'POST','OPTIONS'])
def get_item_details(request):

    sid = get_sid()
    item_code = request.GET['item_code']
    list_of_brand = item_code.split(',')
    res2 = {}
    for l in list_of_brand:
        
        item_detail_api1 = 'http://14.98.78.69:2233/api/resource/Item/'+l+'?sid='+sid+''
        res = requests.get(item_detail_api1,verify=False)
        response_data = json.loads(res.text)
        res1 = {l:response_data['data']}
        res2.update(res1)
    
    return Response({"items":res2})

@api_view(['GET', 'POST','OPTIONS'])
def products(request):
    item_group = request.GET['item_group']
    
    list_of_brand = item_group.split(',')
    brands_list = []
    sub_item_group = request.GET['sub_item_group']
    main_item_group = request.GET['main_item_group']
    start_page_index1 = "0"
    try:
        
        start_page_index = request.GET['start_page_index']
        
        
        last_page_index= 0
        start_page_index1 = str((int(start_page_index)-1)*9 + 1)
        last_page_index = str(9)
    except Exception as e:
        print(e)
        start_page_index = "0"
        last_page_index = "9"

    # print(start_page_index1)
    # print(last_page_index)
    # sys.exit()
    t_length = 0
    for l in list_of_brand:
        item_detail_api1 = 'http://14.98.78.69:2233/api/resource/Item?fields=["*"]&filters=[["Item","item_group","=","'+l+'"],["Item","main_category","=","'+main_item_group+'"],["Item","sub_category","=","'+sub_item_group+'"],["Item","has_variants","=","0"]]&limit_page_length=all'
        

        res1 = requests.get(item_detail_api1,verify=False)
        response_data1 = json.loads(res1.text)
        t_length+=len(response_data1['data'])
    

    for l in list_of_brand:
        item_detail_api = 'http://14.98.78.69:2233/api/resource/Item?fields=["*"]&filters=[["Item","item_group","=","'+l+'"],["Item","main_category","=","'+main_item_group+'"],["Item","sub_category","=","'+sub_item_group+'"],["Item","has_variants","=","0"]]&limit_start='+start_page_index1+'&limit_page_length='+last_page_index+''

        
        res = requests.get(item_detail_api,verify=False)
        response_data = json.loads(res.text)
        if len(response_data['data']) >0:
            
            brands_list.append(response_data['data'])
           

    items = {"items":brands_list[0]}
    items.update({'total_length':t_length})
    return Response(items)
    


@api_view(['GET', 'POST','OPTIONS'])
def login(request):
    usr = request.POST['usr']
    pwd = request.POST['pwd']
    response_data = {}
    print(usr)
    
    URL = "http://14.98.78.69:2233/api/method/login"
    PARAMS = {'usr':usr,'pwd':pwd}
    req = requests.get(url = URL, params = PARAMS)
    data = req.text
    
    try:
        data_p_type = json.loads(data)
        
        
        if data_p_type["message"] == "Logged In" or data_p_type["message"]=='No App' :
            response_data["status"] = 'success'
            response_data['sid'] = data_p_type['sid']
            response_data['full_name'] = data_p_type['full_name']
            response_data['email'] = data_p_type['email']
            USER_API = 'http://14.98.78.69:2233/api/resource/Customer?fields=["*"]&filters=[["Customer","name","=","'+response_data['full_name']+'"]]'
            print(USER_API)
            req2 = requests.get(url = USER_API)
            response_data2 = json.loads(req2.text)
            
            if not response_data2['data']:
                
                API_URL = 'http://14.98.78.69:2233/api/resource/Customer'
                data2 = {"customer_name":data_p_type['full_name'],"owner":data_p_type['email'],"email_id":data_p_type['email']} 
                data2 = json.dumps(data2)
                res2 = requests.post(url=API_URL, verify=False, data =data2)
                print(res2.text)
    except Exception as e:
        
        response_data["status"] = 'error'
        response_data["status_bit"] = 0
    print(response_data)
    #sys.exit()
    
    return Response({"message":response_data})


def get_sid():
    usr = 'administrator'
    pwd = 'KineticX1234'
    response_data = {}
    URL = "http://14.98.78.69:2233/api/method/login"
    PARAMS = {'usr':usr,'pwd':pwd}
    req = requests.get(url = URL, params = PARAMS)
    data = req.text
    try:
        data_p_type = json.loads(data)
        if data_p_type["message"] == "Logged In" or data_p_type["message"]=='No App' :
            response_data["status"] = 'success'
            response_data['sid'] = data_p_type['sid']
            
            if data_p_type['email']:
                response_data['email'] = data_p_type['email']
    except Exception as e:
        response_data["status"] = 'error'
        response_data["status_bit"] = 0
    return response_data['sid']

@api_view(['GET', 'POST','OPTIONS'])
def add_address(request):
    address_line1 = request.POST['address_line1']
    city = request.POST['city']
    address_title = request.POST['address_title']
    pincode = request.POST['pincode']
    email_id = request.POST['email_id']
    phone = request.POST['phone']
    email = request.POST['email']
    state = request.POST['state']
    address_line2 = request.POST['address_line2']
    API_ENDPOINT = "http://14.98.78.69:2233/api/resource/Address"
    customer_name = 'http://14.98.78.69:2233/api/resource/Customer?fields=["name"]&filters=[["Customer", "owner", "=", "'+email+'"]]'
    res = requests.get(url = customer_name,verify=False)
    data_cust = json.loads(res.text)

    data = {"address_line2":address_line2,"state":state,"pincode":pincode,"email_id":email_id,"phone":phone,"owner":email,"address_line1":address_line1,"city":city,"address_title":address_title,"owner":email,"links" : [ { "link_doctype":"Customer", "link_name":data_cust['data'][0]['name']}]}
    data = json.dumps(data)
    res2 = requests.post(url=API_ENDPOINT, verify=False, data =data)
    print(res2.text)
    

    return Response({"res":json.loads(res2.text)})

@api_view(['GET', 'POST','OPTIONS'])
def email_sign_up(request):
    email = request.POST['email']
    full_name = request.POST['full_name']
    API_ENDPOINT = 'http://14.98.78.69:2233/api/method/businessx.core.doctype.user.user.sign_up?email='+email+'&full_name='+full_name+'&&redirect_to='
    res = requests.get(API_ENDPOINT,verify=False)
    print(res.text)
    response_data = json.loads(res.text)

    return Response({"usr":response_data})

@api_view(['GET', 'POST','OPTIONS'])
def get_address(request):
    email = request.GET['email']
    API_ENDPOINT = 'http://14.98.78.69:2233/api/resource/Address?fields=["*"]&filters=[["Address","owner","=","'+email+'"]]'
    res2 = requests.get(url=API_ENDPOINT, verify=False)
    print(res2.text)
    return Response({"address":json.loads(res2.text)})

@api_view(['GET', 'POST','OPTIONS'])
def update_address(request):
    address_line1 = request.POST['address_line1']
    city = request.POST['city']
    address_title = request.POST['address_title']
    email = request.POST['email']
    name = request.POST['name']
    pincode = request.POST['pincode']
    email_id = request.POST['email_id']
    address_line2 = request.POST['address_line2']
    phone = request.POST['phone']
    sid =  request.POST['sid']
    state =  request.POST['state']
    API_ENDPOINT = "http://14.98.78.69:2233/api/resource/Address/"+name+"?sid="+sid+""
    data = {"address_line2":address_line2,"state":state,"pincode":pincode,"email_id":email_id,"phone":phone,"owner":email,"address_line1":address_line1,"city":city,"address_title":address_title,"owner":email,"sid":sid}
    data = json.dumps(data)
    res2 = requests.put(url=API_ENDPOINT, verify=False, data =data)
    print(res2.text)

    return Response({"res":json.loads(res2.text)})

@api_view(['GET', 'POST','OPTIONS'])
def delete_address(request):
    
    event_id = request.data['address_name']
    sid = get_sid()
    event_url = 'http://14.98.78.69:2233/api/resource/Address/'+event_id+'?sid='+sid+''
    r = requests.delete(event_url)
    print(r.text)
    return Response({"status":json.loads(r.text)})


@api_view(['GET', 'POST','OPTIONS'])
def get_sales_invoice(request):
    customer_email = request.GET['email']
    start_page_length = request.GET.get('start_page_length')
    page_limit_length = request.GET.get('limit_page_length')

    sid = get_sid()
    print(sid)
    
    customer_name = get_customer_name(customer_email)
    s_inv_name1 = 'http://14.98.78.69:2233/api/resource/Sales%20Invoice?fields=["name"]&filters=[["Sales%20Invoice","customer","=","'+customer_name+'"]]&limit_page_length=all'
    res21 = requests.get(url = s_inv_name1,verify=False)
    data_cust21 = json.loads(res21.text)
    
    total_length = len(data_cust21['data'])
    s_inv_name = 'http://14.98.78.69:2233/api/resource/Sales%20Invoice?fields=["name"]&filters=[["Sales%20Invoice","customer","=","'+customer_name+'"]]&limit_page_length='+page_limit_length+''
    res2 = requests.get(url = s_inv_name,verify=False)
    data_cust2 = json.loads(res2.text)
    item_data = []
    for orders in data_cust2['data']:
        
        s_inv_data = 'http://14.98.78.69:2233/api/resource/Sales Invoice/'+orders['name']+'?sid='+sid+''
        res3 = requests.get(url = s_inv_data,verify=False)
        data_cust3 = json.loads(res3.text)
        item_data.append(data_cust3['data'])

    return Response({"items":item_data[int(start_page_length):int(page_limit_length)],"count":total_length})


@api_view(['GET', 'POST','OPTIONS'])
def add_to_cart(request):
    email = request.POST['email']
    
    customer_address = request.POST['customer_address']
    customer_name = 'http://14.98.78.69:2233/api/resource/Customer?fields=["name"]&filters=[["Customer", "owner", "=", "'+email+'"]]'
    res = requests.get(url = customer_name,verify=False)
    data_cust = json.loads(res.text)

    API_ENDPOINT2 = "http://14.98.78.69:2233/api/resource/Sales Order"
    items = request.POST['items']
    items = json.loads(items)

    data2 = {"company":"KIneticx","customer":data_cust['data'][0]['name'],"items":items,"docstatus":1,"api":1}
    data2 = json.dumps(data2)
    res22 = requests.post(url=API_ENDPOINT2, verify=False, data =data2)
    res_data = json.loads(res22.text)
    for i in items:
        z = {}
        z = i
        i.update({"sales_order":res_data['data']['name']})
        API_ENDPOINT = "http://14.98.78.69:2233/api/resource/Sales Invoice"

        data = {"order_number":res_data['data']['name'],"customer_address":customer_address,"company":"KIneticx","customer":data_cust['data'][0]['name'],"items":[z ],"payments":[{"mode_of_payment":"Cash"}],"docstatus":1,"api":1}
        data = json.dumps(data)
        res2 = requests.post(url=API_ENDPOINT, verify=False, data =data)
    item_res = json.loads(res22.text)
    API_COUPON_CODE_CHECK = 'http://14.98.78.69:2233/api/resource/Coupon Code?fields=["status"]&filters=[["Coupon Code","customer","=","'+data_cust['data'][0]['name']+'"]]'
    res_check = requests.get(url=API_COUPON_CODE_CHECK,verify=False)
    res_check1 = json.loads(res_check.text)
    
    if len(res_check1['data']) > 0:
        if res_check1['data'][0]['status'] == "Disabled":
            API_COUPON_CODE = 'http://14.98.78.69:2233/api/resource/Coupon Code'
            #?fields=["name"]&filters=[["Coupon Code",""]]
            import datetime as d1
            x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(7))
            today = date.today()
            date_1 = d1.datetime.strptime(str(today), "%Y-%m-%d")
            end_date = date_1 + d1.timedelta(days=30)
            end_ = end_date.strftime("%Y-%m-%d")
            data_coupon = {"code_number":x.upper(),"code_type":"Customer","customer":data_cust['data'][0]['name'],"discount_percentage":"20","order_id":res_data['data']['name'],"valid_upto":end_,"status":"Enabled"}
            data_coupon = json.dumps(data_coupon)
            res25 = requests.post(url=API_COUPON_CODE, verify=False, data =data_coupon)
            res_25_check = json.loads(res25.text)
            item_res.update({"coupon":res_25_check['data']})
    else:
        API_COUPON_CODE = 'http://14.98.78.69:2233/api/resource/Coupon Code'
        #?fields=["name"]&filters=[["Coupon Code",""]]
        import datetime as d1
        x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(7))
        today = date.today()
        date_1 = d1.datetime.strptime(str(today), "%Y-%m-%d")
        end_date = date_1 + d1.timedelta(days=30)
        end_ = end_date.strftime("%Y-%m-%d")
        data_coupon = {"code_number":x.upper(),"code_type":"Customer","customer":data_cust['data'][0]['name'],"discount_percentage":"20","order_id":res_data['data']['name'],"valid_upto":end_,"status":"Enabled"}
        data_coupon = json.dumps(data_coupon)
        res25 = requests.post(url=API_COUPON_CODE, verify=False, data =data_coupon)
        res_25_check = json.loads(res25.text)
        item_res.update({"coupon":res_25_check['data']})

    return Response({"items":item_res})
    
    
    
    # API_ENDPOINT = "http://14.98.78.69:2233/api/resource/Sales Invoice"
    # data = {"customer_address":customer_address,"company":"KIneticx","customer":data_cust['data'][0]['name'],"items":items,"payments":[{"mode_of_payment":"Cash"}],"docstatus":1,"api":1}
    # data = json.dumps(data)
    # res2 = requests.post(url=API_ENDPOINT, verify=False, data =data)
    # print(res2.text)
    


class Profile(APIView):
    @csrf_exempt
    def get(self,request,format=None):
        email = request.GET.get('email')
        API_URL = 'http://14.98.78.69:2233/api/resource/User?fields=["*"]&filters=[["User","email","=","'+email+'"]]'
        
        res2 = requests.get(url=API_URL)
        return Response({"user":json.loads(res2.text)})

    def post(self, request, format=None):
        profession = request.data['profession']
        qualification = request.data['qualification']
        bio = request.data['bio']
        gender = request.data['gender']
        phone = request.data['phone']
        birth_date = request.data['birth_date']
        location = request.data['location']
        name = request.data['email']
        sid = get_sid()
        API_URL = "http://14.98.78.69:2233/api/resource/User/"+name+"?sid="+sid+""
        data2 = {"gender":gender,"profession":profession,"qualification":qualification,"bio":bio,"phone":phone,"birth_date":birth_date,"location":location} 
        data2 = json.dumps(data2)
        res2 = requests.put(url=API_URL, verify=False, data =data2)
        return Response({"user":"Updated Successfully"})
        
# class Profile(APIView):
#     @csrf_exempt
#     def get(self,request,format=None):
#         email = request.GET.get('email')
#         sid = get_sid()
#         API_URL = "http://14.98.78.69:2233/api/resource/User/"+email+"?sid="+sid+""
        

        
#         res2 = requests.get(url=API_URL)
#         return Response({"user":json.loads(res2.text)})

class Rating(APIView):
    @csrf_exempt
    def get(self,request,format=None):
        item_name = request.GET.get('item_code')
        try:
            next_rate = request.GET.get('next_rate')
            next_rate = str(next_rate)
        except:
            next_rate = "3"
        API_URL = 'http://14.98.78.69:2233/api/resource/Ratings?fields=["*"]&filters=[["Ratings","item_code","=","'+item_name+'"]]&limit_start='+next_rate+'&limit_page_length=3'
        res2 = requests.get(url=API_URL)
        response_data = json.loads(res2.text)
        API_URL2 = 'http://14.98.78.69:2233/api/resource/Ratings?fields=["*"]&filters=[["Ratings","item_code","=","'+item_name+'"]]&limit_page_length=all'
        res22 = requests.get(url=API_URL2)
        response_data2 = json.loads(res22.text)
        review_rate = {"rating_1":0,"rating_2":0,"rating_3":0,"rating4":0,"rating_5":0}
        r1,p1,s1 =0,0,0
        r2,p2,s2 =0,0,0
        r3,p3,s3 =0,0,0
        r4,p4,s4 =0,0,0
        r5,p5,s5 =0,0,0
        for res in response_data2['data']:
            if res['review_rate'] =="1":
                r1+=1

            if res['review_rate'] =="2":
                r2+=1
            if res['review_rate'] =="3":
                r3+=1
            if res['review_rate'] =="4":
                r4+=1
            if res['review_rate'] =="5":
                r5+=1
        s1 = 1*r1
        s2 = 2*r2
        s3 = 3*r3
        s4 = 4*r4
        s5 = 5*r5
        total = s1+s2+s3+s4+s5
        total_r = r1+r2+r3+r4+r5
        average = total/total_r
        average_dict = {"average":round(average,1)}
        #sys.exit()

        review_rate = {"review":{"rating_1":r1,"rating_2":r2,"rating_3":r3,"rating_4":r4,"rating_5":r5}}
       
        response_data.update(review_rate)
        response_data.update(average_dict)
        return Response({"rating":response_data})
    def post(self,request,format=None):
        data = request.data
        data = json.dumps(data)
        data2 = json.dumps(data)
        
        API_URL = 'http://14.98.78.69:2233/api/resource/Ratings'
        res2 = requests.post(url=API_URL, verify=False, data =data)
        print(res2.text)
        return Response({"rating":"Updated Successfully"})

        

class Website_Slider(APIView):
    @csrf_exempt
    def get(self,request,format=None):
        page =  request.GET.get('page')
        sid = get_sid()
        API_URL = 'http://14.98.78.69:2233/api/resource/Website%20Slideshow?fields=["name"]&filters=[["Website Slideshow","page","=","'+page+'"]]'
        res2 = requests.get(url=API_URL)
        response_data = json.loads(res2.text)
        dict_ = {}
        image_list =[]
        for res in response_data['data']:
            
            API_URL_ = 'http://14.98.78.69:2233/api/resource/Website Slideshow/'+res['name']+'?sid='+sid+''
            res22 = requests.get(url=API_URL_ )
            response_data_ = json.loads(res22.text)
            list_of_images = []
            for images in response_data_['data']['slideshow_items']:
                list_of_images.append(images['image'])
            dict_1 = {res['name']:list_of_images}
            
            dict_.update(dict_1)
            
            
        return Response({"images":dict_})

class Image_Upload(APIView):
    def post(self,request,format=None):
        sid = get_sid()
        data = request.data
        data = json.dumps(data)
        API_URL = 'http://14.98.78.69:2233/api/method/businessx.handler.uploadfile1?sid='+sid+''

        res2 = requests.post(url=API_URL, verify=False, data =data)
        if request.data['upload']==1:

            image_res = json.loads(res2.text)
            data1 = request.data
            APi_User = 'http://14.98.78.69:2233/api/resource/User/'+data1['docname']+''
            data2 = {'user_image':image_res['message']['file_url']}
            data3 = json.dumps(data2)
            res21 = requests.put(url=APi_User, verify=False, data =data3)
        
        

        print(res2.text)
        res = json.loads(res2.text)
        print(res['message']['file_url'])
        return Response({"rating":res['message']['file_url']})


class Cover_Image_Upload(APIView):
    def post(self,request,format=None):
        sid = get_sid()
        data = request.data
        data = json.dumps(data)
        API_URL = 'http://14.98.78.69:2233/api/method/businessx.handler.uploadfile1?sid='+sid+''

        res2 = requests.post(url=API_URL, verify=False, data =data)
        image_res = json.loads(res2.text)
        data1 = request.data
        APi_User = 'http://14.98.78.69:2233/api/resource/User/'+data1['docname']+''
        data2 = {'background_image':image_res['message']['file_url']}
        data3 = json.dumps(data2)
        res21 = requests.put(url=APi_User, verify=False, data =data3)
        
        

        return Response({"rating":res2.text})

class Testimonial(APIView):
    def get(self,request,format=None):
        API_URL = 'http://14.98.78.69:2233/api/resource/Testimonials?fields=["*"]'
        res2 = requests.get(url=API_URL, verify=False)
        testimonial_res = json.loads(res2.text)
        return Response({'testimonial':testimonial_res})


@api_view(['GET', 'POST','OPTIONS'])
def get_cart_item(request):
    email = request.GET['email']
    customer_name = 'http://14.98.78.69:2233/api/resource/Customer?fields=["name"]&filters=[["Customer", "owner", "=", "'+email+'"]]'
    res = requests.get(url = customer_name,verify=False)
    data_cust = json.loads(res.text)

    sid = get_sid()
    API_ENDPOINT2 = 'http://14.98.78.69:2233/api/resource/Quotation?fields=["name"]&filters=[["Quotation","customer","=","'+data_cust['data'][0]['name']+'"],["Quotation","docstatus","=","0"]]'
    
    r2 = requests.get(API_ENDPOINT2,verify=False)
    resp = json.loads(r2.text)
    
    
    if len(resp['data'])>0:
        API_ENDPOINT = "http://14.98.78.69:2233/api/resource/Quotation/"+resp['data'][0]['name']+"?sid="+sid+""
        res2 = requests.get(url=API_ENDPOINT, verify=False)
        print(res2.text)
        return Response({"items":json.loads(res2.text)})
    
    return Response({"items":""})
        





@api_view(['GET', 'POST','OPTIONS'])
def add_to_quotation(request):
    email = request.POST['email']
    customer_address = request.POST['customer_address']
    customer_name = 'http://14.98.78.69:2233/api/resource/Customer?fields=["name"]&filters=[["Customer", "owner", "=", "'+email+'"]]'
    res = requests.get(url = customer_name,verify=False)
    data_cust = json.loads(res.text)
    API_ENDPOINT = "http://14.98.78.69:2233/api/resource/Quotation"
    
    items = request.POST['items']
    items = json.loads(items)
    #[{"item_code":"Black Shirt","qty":"1"}]
    data = {"email":email,"customer_address":customer_address,"company":"KIneticx","customer":data_cust['data'][0]['name'],"items":items,"docstatus":0,"api":1}
    data = json.dumps(data)
    res2 = requests.post(url=API_ENDPOINT, verify=False, data =data)
    print(res2.text)
    return Response({"items":json.loads(res2.text)})

@api_view(['GET', 'POST','OPTIONS'])
def update_quotation(request):
    email = request.POST['email']
    customer_address = request.POST['customer_address']
    customer_name = 'http://14.98.78.69:2233/api/resource/Customer?fields=["name"]&filters=[["Customer", "owner", "=", "'+email+'"]]'
    res = requests.get(url = customer_name,verify=False)
    data_cust = json.loads(res.text)
    print(data_cust)
    sid = get_sid()
    
    API_ENDPOINT2 = 'http://14.98.78.69:2233/api/resource/Quotation?fields=["name"]&filters=[["Quotation","customer","=","'+data_cust['data'][0]['name']+'"]]'
    r2 = requests.get(API_ENDPOINT2,verify=False)
    resp = json.loads(r2.text)
    print(resp)
    
    # if len(resp['data'])>0:
    #     API_ENDPOINT22 = "http://14.98.78.69:2233/api/resource/Quotation/"+resp['data'][0]['name']+"?sid="+sid+""
    #     r = requests.delete(API_ENDPOINT22)
    API_ENDPOINT = "http://14.98.78.69:2233/api/resource/Quotation/"+resp['data'][0]['name']+"?sid="+sid+""
    items = request.POST['items']
    items = json.loads(items)
    if len(items)==0:
        API_ENDPOINT22 = "http://14.98.78.69:2233/api/resource/Quotation/"+resp['data'][0]['name']+"?sid="+sid+""
        r = requests.delete(API_ENDPOINT22)
        return Response({"items":json.loads(r.text)})

    #[{"item_code":"Black Shirt","qty":"1"}]
    else:

        data = {"email":email,"customer_address":customer_address,"company":"KIneticx","customer":data_cust['data'][0]['name'],"items":items,"docstatus":0,"api":1}
        data = json.dumps(data)
        res2 = requests.put(url=API_ENDPOINT, verify=False, data =data)
        print(res2.text)

        return Response({"items":json.loads(res2.text)})

class WishList(APIView):
    def get(self,request,format=None):
        customer_name = get_customer_name( request.GET.get('email'))
        API_URL = 'http://14.98.78.69:2233/api/resource/Wishlist?fields=["*"]&filters=[["Wishlist","customer","=","'+customer_name+'"]]'
        res2 = requests.get(url=API_URL, verify=False)
        testimonial_res = json.loads(res2.text)
        return Response({'wishlist':testimonial_res})

    def post(self,request,format=None):
        data = request.data
        data = json.dumps(data)
        API_URL = 'http://14.98.78.69:2233/api/resource/Wishlist'
        res2 = requests.post(url=API_URL, verify=False, data =data)
        print(res2.text)
        return Response({"wishlist":json.loads(res2.text)})

    

class Update_Review(APIView):
    def post(self,request,format=None):
        
        data = request.data
        sid = get_sid()
        name = request.data['name']
        
        data = json.dumps(data)
        API_URL = 'http://14.98.78.69:2233/api/resource/Ratings/'+name+'?sid='+sid+''
        res2 = requests.put(url=API_URL, verify=False, data =data)
        return Response({"review":res2.text})


def get_customer_name(email):
    customer_name = 'http://14.98.78.69:2233/api/resource/Customer?fields=["name"]&filters=[["Customer", "owner", "=", "'+email+'"]]'
    res = requests.get(url = customer_name,verify=False)
    data_cust = json.loads(res.text)
    return data_cust['data'][0]['name']


class Get_SalesOrder(APIView):
    def get(self,request,format=None):
        customer_name = get_customer_name( request.GET.get('email'))
        sid = get_sid()
        lis = []
        res_Data = {}
        API_URL = 'http://14.98.78.69:2233/api/resource/Sales Order?fields=["name"]&filters=[["Sales Order","customer","=","'+customer_name+'"]]'
        res2 = requests.get(url=API_URL, verify=False)
        testimonial_res = json.loads(res2.text)
        for data in testimonial_res['data']:
            APU_URL1 = 'http://14.98.78.69:2233/api/resource/Sales Order/'+data['name']+'?sid='+sid+''
            
            res22 = requests.get(url=APU_URL1, verify=False)
            testimonial_res1 = json.loads(res22.text)
            for dat in testimonial_res1['data']['items']:
                lis.append(dat['item_code'])


        return Response({"items":lis})

class Insert_Lead_(APIView):
    def post(self,request,format=None):
        data = request.data
        data = json.dumps(data)
        API_URL = 'http://14.98.78.69:2233/api/resource/Lead'
        res2 = requests.post(url=API_URL, verify=False, data =data)
        print(res2.text)
        return Response({"lead":res2.text})

class Get_Cateogary(APIView):
    def get(self,request,format=None):
        API_URL = 'http://14.98.78.69:2233/api/resource/Benefits?fields=["*"]&filters=[["Benefits","item_code","=","'+request.GET.get('item_code')+'"],["Benefits","category","=","'+request.GET.get('category')+'"]]'
        res22 = requests.get(url=API_URL, verify=False)
        testimonial_res1 = json.loads(res22.text)
        return Response({"data":testimonial_res1})

class DeleteWishlist(APIView):
    def post(self,request,format=None):
        name =  request.data['name']
        list_of_brand = name.split(',')
        sid = get_sid()
        for l in list_of_brand:
            API_URL = 'http://14.98.78.69:2233/api/resource/Wishlist/'+name+'?sid='+sid+''
            res2 = requests.get(url=API_URL, verify=False)
            response = json.loads(res2.text)
            if len(response['data']) >0:
                r = requests.delete(API_URL)
            
        
                return Response({"wishlist":json.loads(r.text)})
            else:
                return Response({"wishlist":"Does not exist"})



def get_profile_pic(email):
    
    API_URL = 'http://14.98.78.69:2233/api/resource/User?fields=["user_image"]&filters=[["User","email","=","'+email+'"]]'
    res22 = requests.get(url=API_URL, verify=False)
    testimonial_res1 = json.loads(res22.text)
    print(len(testimonial_res1['data']))
    if len(testimonial_res1['data'])>0:
        return testimonial_res1['data'][0]['user_image']
    else:
        return ""


class DoctypeCRUD(APIView):
    
    def get(self, request, format=None):
        doctype = request.GET.get('module')
        sid = get_sid()
        if request.GET.get('docname'):
            docname = request.GET.get('docname')
            API_URL = 'http://14.98.78.69:2233/api/resource/'+doctype+'/'+docname+'?sid='+sid+''
            res22 = requests.get(url=API_URL, verify=False)
            testimonial_res1 = json.loads(res22.text)
            res = testimonial_res1['data']
            return Response({"data":res})
        else:
            API_URL167 = 'http://14.98.78.69:2233/api/resource/'+doctype+'?fields=["name"]&limit_page_length=all'
            res167 = requests.get(url=API_URL167, verify=False)
            testimonial_res1167 = json.loads(res167.text)
            post_length = len(testimonial_res1167['data'])
            start_page_length = request.GET.get('start_page_length')
            page_limit_length = request.GET.get('limit_page_length')
            testimonial_res1 = []
            API_URL1 = 'http://14.98.78.69:2233/api/resource/'+doctype+'?fields=["*"]&limit_page_length='+page_limit_length+''
            res1 = requests.get(url=API_URL1, verify=False)
            testimonial_res11 = json.loads(res1.text)
            for response in testimonial_res11['data']:
                len1 = 0
                len2=0
                if doctype =='Posts Manager':
                    API_URL1 = 'http://14.98.78.69:2233/api/resource/Posts Likes?fields=["person_name"]&filters=[["Posts Likes","post_id","=","'+response['name']+'"]]'
                    res2 = requests.get(url=API_URL1, verify=False)
                    testimonial_res13 = json.loads(res2.text)
                    len1 = len(testimonial_res13['data'])
                
                if doctype =='Posts Manager':
                    API_URL1tt = 'http://14.98.78.69:2233/api/resource/Comments?fields=["posts_manager"]&filters=[["Comments","posts_manager","=","'+response['name']+'"]]'
                    res222 = requests.get(url=API_URL1tt, verify=False)
                    testimonial_res131 = json.loads(res222.text)
                    len2 = len(testimonial_res131['data'])
                    
                
                
                
                API_URL = 'http://14.98.78.69:2233/api/resource/Media Table?fields=["media_data"]&filters=[["Media Table","post_id","=","'+response['name']+'"]]'

                res22 = requests.get(url=API_URL, verify=False)
                testimonial_res13 = json.loads(res22.text)
                user_image = get_profile_pic(response['owner'])
                image = testimonial_res13['data']

                API_URL_SHARED = 'http://14.98.78.69:2233/api/resource/Shared Users?fields=["*"]&filters=[["Shared Users","post_id","=","'+response['name']+'"]]'

                resshared = requests.get(url=API_URL_SHARED, verify=False)
                testimonial_res13shared = json.loads(resshared.text)
                shared_user = testimonial_res13shared['data']
                #shared_user = testimonial_res11['data']['shared_users']
                testimonial_res12 = response
                testimonial_res12.update({"user_image":user_image,"likes":len1,"comment_count":len2,"post_media":image,"shared_users":shared_user})
                
                testimonial_res1.append(testimonial_res12)
            dict_ = {"data":testimonial_res1[int(start_page_length):int(page_limit_length)],"length":post_length}

            
            return Response(dict_)
                
        
        
    def post(self, request, format=None):
        data = request.data
        data = json.dumps(data)
        module = request.data['module']
        data2 = {}
        owner = request.data['owner']
        person_name = get_customer_name(owner)
        data = json.loads(data)
        data.update({"person_name":person_name})
        try:
            b = data.pop('post_media')
        except:
            pass
        try:
            pop_shared = data.pop('shared_users')
            
        except:
            pass
        
        data = json.dumps(data)
        API_URL = 'http://14.98.78.69:2233/api/resource/'+module+''
        res2 = requests.post(url=API_URL, verify=False, data =data)
        response_data = json.loads(res2.text)
        
        
        name = response_data['data']['name']
        
    
        try:
            if b:
                b = json.loads(b)
                for z in b:
                    
                    z.update({'post_id':name,'customer_name':person_name})
                    z = json.dumps(z)
                    API_URL2 = 'http://14.98.78.69:2233/api/resource/Media Table'
                    res22 = requests.post(url=API_URL2, verify=False, data = z)
                    #response_data2 = json.loads(res22.text)

            
                    #response_shared = json.loads(resshared.text)
        except:
            pass
        
        try:
            pop_shared = json.loads(pop_shared)
            if pop_shared:
                for y in pop_shared:
                    customer_name = get_customer_name(y['email'])
                    y.update({'post_id':name,'customer_name':customer_name})
                    y = json.dumps(y)
                    API_URL_SHARED = 'http://14.98.78.69:2233/api/resource/Shared Users'
                    resshared = requests.post(url=API_URL_SHARED, verify=False, data = y)
        except:
            pass
            

        return Response({"data":response_data['data']})

    def put(self, request, format=None):
        data = request.data
        module = request.data['module']
        data = json.dumps(data)
        API_URL = 'http://14.98.78.69:2233/api/resource/'+module+''
        res2 = requests.put(url=API_URL, verify=False, data =data)
        print(res2.text)
        return Response({"data":res2.text})

class CommentSection(APIView):
    def get(self, request, format=None):
        post_id = request.GET.get('post_id')
        start_page_length = request.GET.get('start_page_length')
        page_limit_length = request.GET.get('limit_page_length')
        l=[]
        API_URL1 = 'http://14.98.78.69:2233/api/resource/Comments?fields=["*"]&filters=[["Comments","posts_manager","=","'+post_id+'"]]&limit_page_length='+page_limit_length+''
        res2 = requests.get(url=API_URL1, verify=False)
        testimonial_res11 = json.loads(res2.text)
        resp = testimonial_res11['data']
        for r in resp:
            print("--------------------------------")
            profile_image = get_profile_pic(r['owner'])
            customer_name = get_customer_name(r['owner'])
            API_REPLY = 'http://14.98.78.69:2233/api/resource/Reply Table?fields=["*"]&filters=[["Reply Table","parent1","=","'+r['name']+'"]]&limit_page_length=all'
            resreply = requests.get(url=API_REPLY, verify=False)
            replyjson = json.loads(resreply.text)
            replycount = len(replyjson['data'])
            r.update({"profile_pic":profile_image,"customer_name":customer_name,"replycount":replycount})
            l.append(r)

        
        API_URL = 'http://14.98.78.69:2233/api/resource/Comments?fields=["*"]&filters=[["Comments","posts_manager","=","'+post_id+'"]]&limit_page_length=all'
        res2 = requests.get(url=API_URL, verify=False)
        testimonial_res11 = json.loads(res2.text)
        resp = testimonial_res11['data']
        length1 = len(resp)
        r ={"data":l[int(start_page_length):int(page_limit_length)],"length":length1}
        return Response(r)

    def post(self, request, format=None):
        data = request.data
        data = json.dumps(data)
        
        API_URL = 'http://14.98.78.69:2233/api/resource/Comments'
        res2 = requests.post(url=API_URL, verify=False, data =data)
        response_data = json.loads(res2.text)
        resp_ = response_data['data']
        customer_name = get_customer_name(resp_['owner'])
        resp_.update({"customer_name":customer_name})
        

        return Response({"data":resp_})

    def put(self, request, format=None):
        data = json.dumps(request.data)
        data = json.loads(data)
        like_ = request.data['like_increment']
        name = request.data['name']
        owner = request.data['owner']
        
        check_ = check_like_getter(owner,name,like_)
        


        
        if int(check_)==1:

            #dislike_ = request.data['dislike_increment']
            Api_url = 'http://14.98.78.69:2233/api/resource/Comments?fields=["likes"]&filters=[["Comments","name","=","'+name+'"]]'
            ress = requests.get(Api_url)
            json_data = json.loads(ress.text)
            if int(like_)==1:
                like = int(json_data['data'][0]['likes'])
                like = int(like)
                like+=1
                data.update({"likes":like})
            elif int(like_)==-1:
                
                like = int(json_data['data'][0]['likes'])
                like = int(like)
                like-=1
                data.update({"likes":like})
            
            # if int(dislike_)==0:
            #     dislikes = data.pop('dislikes')
            #     dislikes = int(like)
            #     dislikes-=1
            #     data.update({"dislikes":dislikes})
            # elif int(dislike_)==-1:
            #     dislikes = data.pop('dislikes')
            #     dislikes = int(like)
            #     dislikes+=1
            #     data.update({"dislikes":dislikes})
            
            
            sid = get_sid()
            data = json.dumps(data)
            API_URL = 'http://14.98.78.69:2233/api/resource/Comments/'+name+'?sid='+sid+''
            res2 = requests.put(url=API_URL, verify=False, data =data)
            response_data = json.loads(res2.text)
            resp_ = response_data['data']
            customer_name = get_customer_name(resp_['owner'])
            resp_.update({"customer_name":customer_name})
            if int(like_) == -1:
                resp_.update({"status":"disliked"})
            else:
                resp_.update({"status":"liked"})

            print(resp_)
            return Response({"data":resp_})
        else:
            return Response({"status":"Already Liked"})


class ReplySection(APIView):
    def get(self, request, format=None):
        post_id = request.GET.get('post_id')
        l = []
        sid = get_sid()
        start_page_length = request.GET.get('start_page_length')
        page_limit_length = request.GET.get('limit_page_length')
        API_URL = 'http://14.98.78.69:2233/api/resource/Reply Table?fields=["*"]&filters=[["Reply Table","parent1","=","'+post_id+'"],["Reply Table","child","=",""]]&limit_page_length='+page_limit_length+''
        res22 = requests.get(url=API_URL, verify=False)
        testimonial_res1 = json.loads(res22.text)
        res = testimonial_res1['data']
        
        if len(res)>0:
            for r in res:

                profile_image = get_profile_pic(r['owner'])
                customer_name = get_customer_name(r['owner'])
                r.update({"profile_pic":profile_image,"customer_name":customer_name})
                
                l.append(r)
        API_URL1 = 'http://14.98.78.69:2233/api/resource/Reply Table?fields=["*"]&filters=[["Reply Table","parent1","=","'+post_id+'"],["Reply Table","child","=",""]]&limit_page_length=all'
        res2 = requests.get(url=API_URL1, verify=False)
        testimonial_res11 = json.loads(res2.text)
        resp = testimonial_res11['data']
        length1 = len(resp)
        r ={"data":l[int(start_page_length):int(page_limit_length)],"length":length1}
        return Response(r)


    def post(self, request, format=None):
        data = request.data
        data = json.dumps(data)
        API_URL = 'http://14.98.78.69:2233/api/resource/Reply Table'
        res2 = requests.post(url=API_URL, verify=False, data =data)
        response_data = json.loads(res2.text)
        
        resp_ = response_data['data']
        customer_name = get_customer_name(resp_['owner'])
        resp_.update({"customer_name":customer_name})
        return Response({"data":resp_})

    def put(self, request, format=None):
        data = json.dumps(request.data)
        data = json.loads(data)
        like_ = request.data['like_increment']
        dislike_ = request.data['dislike_increment']
        if int(like_)==0:
            like = data.pop('likes')
            like = int(like)
            like+=1
            data.update({"likes":like})
        elif int(like_)==-1:
            like = data.pop('likes')
            like = int(like)
            like-=1
            data.update({"likes":like})
        
        if int(dislike_)==0:
            dislikes = data.pop('dislikes')
            dislikes = int(like)
            dislikes-=1
            data.update({"dislikes":dislikes})
        elif int(dislike_)==-1:
            dislikes = data.pop('dislikes')
            dislikes = int(like)
            dislikes+=1
            data.update({"dislikes":dislikes})
        

        name = request.data['name']
        sid = get_sid()
        data = json.dumps(data)
        
        API_URL = 'http://14.98.78.69:2233/api/resource/Reply Table/'+name+'?sid='+sid+''
        res2 = requests.put(url=API_URL, verify=False, data =data)
        response_data = json.loads(res2.text)
        resp_ = response_data['data']
        customer_name = get_customer_name(resp_['owner'])
        resp_.update({"customer_name":customer_name})
        return Response({"data":resp_})


class Like_Getter(APIView):
    def get(self, request, format=None):
        post_id = request.GET.get('post_id')
        customer_name_list = []
        API_URL = 'http://14.98.78.69:2233/api/resource/Posts Likes?fields=["person_name"]&filters=[["Posts Likes","post_id","=","'+post_id+'"]]'
        res = requests.get(url=API_URL, verify=False)
        testimonial_res1 = json.loads(res.text)
        resp = testimonial_res1['data']
        if len(resp)>0:
            for r in resp:
                customer_name = get_customer_name(r['person_name'])
                profile_pic = get_profile_pic(r['person_name'])
                re_ = {"customer_name":customer_name,"profile_pic":profile_pic,"email":r['person_name']}
                customer_name_list.append(re_)
        
        res_list = [] 
        for i in range(len(customer_name_list)): 
            if customer_name_list[i] not in customer_name_list[i + 1:]: 
                res_list.append(customer_name_list[i]) 
        
        
        return Response(res_list)

    def post(self, request, format=None):
        data = request.data
        user_email = request.data['person_name']
        post_id = request.data['post_id']
        API_URL1 =  'http://14.98.78.69:2233/api/resource/Posts Likes?fields=["name"]&filters=[["Posts Likes","post_id","=","'+post_id+'"],["Posts Likes","person_name","=","'+user_email+'"]]'
        res = requests.get(url=API_URL1, verify=False)
        testimonial_res1 = json.loads(res.text)
        if len(testimonial_res1['data'])<=0:
            
            data = json.dumps(data)
            API_URL = 'http://14.98.78.69:2233/api/resource/Posts Likes'
            res2 = requests.post(url=API_URL, verify=False, data =data)
            response_data = json.loads(res2.text)
            return Response(response_data)
        else:
            return Response({'status':'already liked'})

    def put(self, request, format=None):
        user_email = request.data['person_name']

        post_id = request.data['post_id']
        API_URL = 'http://14.98.78.69:2233/api/resource/Posts Likes?fields=["name"]&filters=[["Posts Likes","post_id","=","'+post_id+'"],["Posts Likes","person_name","=","'+user_email+'"]]'
        res = requests.get(url=API_URL, verify=False)
        print(res.text)

        testimonial_res1 = json.loads(res.text)
        name = testimonial_res1['data'][0]['name']
        sid = get_sid()
        API_URL1 = 'http://14.98.78.69:2233/api/resource/Posts Likes/'+name+'?sid='+sid+''
        res2 = requests.delete(API_URL1)
        return Response(json.loads(res2.text))

                


def check_like_getter(user_email,post_id,like):
    
    if int(like) == 1:
        API_URL1 =  'http://14.98.78.69:2233/api/resource/Posts Likes?fields=["name"]&filters=[["Posts Likes","post_id","=","'+post_id+'"],["Posts Likes","person_name","=","'+user_email+'"]]'
        res = requests.get(url=API_URL1, verify=False)
        testimonial_res1 = json.loads(res.text)
        print(testimonial_res1)
        if len(testimonial_res1['data'])<=0:
            
            data = {'person_name':user_email,'post_id':post_id}
            data = json.dumps(data)
            API_URL = 'http://14.98.78.69:2233/api/resource/Posts Likes'
            res2 = requests.post(url=API_URL, verify=False, data =data)
            response_data = json.loads(res2.text)
            return 1
        else:
            return 0
    else:
        delete_unlike(post_id,user_email)
        return 1


def delete_unlike(post_id,user_email):

    API_URL = 'http://14.98.78.69:2233/api/resource/Posts Likes?fields=["name"]&filters=[["Posts Likes","post_id","=","'+post_id+'"],["Posts Likes","person_name","=","'+user_email+'"]]'
    res = requests.get(url=API_URL, verify=False)
    testimonial_res1 = json.loads(res.text)
    name = testimonial_res1['data'][0]['name']
    sid = get_sid()
    API_URL1 = 'http://14.98.78.69:2233/api/resource/Posts Likes/'+name+'?sid='+sid+''
    res2 = requests.delete(API_URL1)
    print(res2.text)

class User_Like_Getter(APIView):
    def get(self, request, format=None):
        email = request.GET.get('email')
        post_list = []
        API_URL = 'http://14.98.78.69:2233/api/resource/Posts Likes?fields=["post_id"]&filters=[["Posts Likes","person_name","=","'+email+'"]]'
        res = requests.get(url=API_URL, verify=False)
        testimonial_res1 = json.loads(res.text)
        resp = testimonial_res1['data']
        for r in resp:
            post_list.append(r['post_id'])
        return Response(post_list)

class Get_User_Uploaded_Images(APIView):
    def get(self, request, format=None):
        sid = get_sid()
        images_list = []
        images_list1 = 0
        start_page_length = request.GET.get('start_page_length')
        page_limit_length = request.GET.get('limit_page_length')
        customer_name = get_customer_name( request.GET.get('email'))
        API_URL_IMAGE = 'http://14.98.78.69:2233/api/resource/Media Table?fields=["media_data"]&filters=[["Media Table","customer_name","=","'+customer_name+'"]]&limit_page_length='+page_limit_length+''
        res = requests.get(url=API_URL_IMAGE, verify=False)
        json_data = json.loads(res.text)
        for r in json_data['data']:
            images_list.append(r['media_data'])
        API_URL_IMAGE_LENGTH = 'http://14.98.78.69:2233/api/resource/Media Table?fields=["media_data"]&filters=[["Media Table","customer_name","=","'+customer_name+'"]]&limit_page_length=all'
        res_length = requests.get(url=API_URL_IMAGE_LENGTH, verify=False)
        json_data_length = json.loads(res_length.text)
        images_list1 = len(json_data_length['data'])
        # API_URL = 'http://14.98.78.69:2233/api/resource/Posts Manager?fields=["name"]&filters=[["Posts Manager","person_name","=","'+customer_name+'"]]&limit_page_length='+page_limit_length+''
        # res = requests.get(url=API_URL, verify=False)
        # json_data = json.loads(res.text)
        # for r in json_data['data']:
        #     API_URL1 = 'http://14.98.78.69:2233/api/resource/Posts Manager/'+r['name']+'?sid='+sid+''
        #     res1 = requests.get(url=API_URL1, verify=False)
        #     json_data1 = json.loads(res1.text)
        #     if len(json_data1['data']['post_media'])>0:
        #         images_list.append(json_data1['data']['post_media'])
        
        
        # API_URL11 = 'http://14.98.78.69:2233/api/resource/Posts Manager?fields=["name"]&filters=[["Posts Manager","person_name","=","'+customer_name+'"]]&limit_page_length=all'
        # res11 = requests.get(url=API_URL11, verify=False)
        # json_data11 = json.loads(res11.text)
        # for r11 in json_data11['data']:
            
        #     API_URL111 = 'http://14.98.78.69:2233/api/resource/Posts Manager/'+r11['name']+'?sid='+sid+''
        #     res111 = requests.get(url=API_URL111, verify=False)
        #     json_data111 = json.loads(res111.text)
        #     if len(json_data111['data']['post_media'])>0:
        #         images_list1+=1
        
        #total_length = len(images_list1)
        print(images_list)
        dict_ = {"length":images_list1,"data":images_list[int(start_page_length):int(page_limit_length)]}

        return Response(dict_)

class Follower_Module(APIView):
    def get(self, request, format=None):
        email = request.GET.get('email')
        type = request.GET.get('type')
        
        l = []
        start_page_length = request.GET.get('start_page_length')
        page_limit_length = request.GET.get('limit_page_length')
        if type == "Follower":
            API_URL = 'http://14.98.78.69:2233/api/resource/Followers?fields=["*"]&filters=[["Followers","email","=","'+email+'"]]&limit_page_length='+page_limit_length+''
        elif type == "Following":
            customer_name = get_customer_name(email)
            API_URL = 'http://14.98.78.69:2233/api/resource/Followers?fields=["*"]&filters=[["Followers","customer_name","=","'+customer_name+'"]]&limit_page_length='+page_limit_length+''
        res = requests.get(url=API_URL, verify=False)
        json_data = json.loads(res.text)

        for r in json_data['data']:
            if type == "Following":
                customer_name = get_customer_name(r['email'])
                profile_image = get_profile_pic(r['email'])
                r.update({"profile_pic":profile_image,"customer_name":customer_name})
            else:
                try:
                    customer_email = get_customer_email(r['customer_name'])
                except:
                    customer_email = ""

                try:
                    profile_image = get_profile_pic(customer_email)
                except:
                    profile_image = ""
                r.update({"profile_pic":profile_image,"email":customer_email})
            
            
            
            l.append(r)
        return Response(l[int(start_page_length):int(page_limit_length)])
        

    def post(self, request, format=None):
        data = request.data
        user_email = request.data['email']
        type = request.data['type']
        customer_name = request.data['customer_name']
        API_URL = 'http://14.98.78.69:2233/api/resource/Followers?fields=["name"]&filters=[["Followers","email","=","'+user_email+'"],["Followers","customer_name","=","'+customer_name+'"]]'
        res = requests.get(url=API_URL, verify=False)
        json_data = json.loads(res.text)
        if json_data['data']:
            return Response({"status":"already following"})
        data = json.dumps(data)
        API_URL = 'http://14.98.78.69:2233/api/resource/Followers'
        res2 = requests.post(url=API_URL, verify=False, data =data)
        response_data = json.loads(res2.text)
        print(response_data)

        return Response({"data":response_data['data']})

    def put(self, request, format=None):
        user_email = request.data['email']
        type = request.data['type']
        customer_name = request.data['customer_name']
        API_URL = 'http://14.98.78.69:2233/api/resource/Followers?fields=["name"]&filters=[["Followers","email","=","'+user_email+'"],["Followers","customer_name","=","'+customer_name+'"]]'
        res = requests.get(url=API_URL, verify=False)
        testimonial_res1 = json.loads(res.text)
        name = testimonial_res1['data'][0]['name']
        sid = get_sid()
        API_URL1 = 'http://14.98.78.69:2233/api/resource/Followers/'+name+'?sid='+sid+''
        res2 = requests.delete(API_URL1)
        return Response(json.loads(res2.text))


class Following_list(APIView):
    def get(self, request, format=None):
        email = request.GET.get('email')
        type = request.GET.get('type')
        list_ = []
        if type == "Follower":
            API_URL = 'http://14.98.78.69:2233/api/resource/Followers?fields=["customer_name"]&filters=[["Followers","email","=","'+email+'"]]&limit_page_length=all'
        elif type == "Following":
            customer_name = get_customer_name(email)

            API_URL = 'http://14.98.78.69:2233/api/resource/Followers?fields=["email"]&filters=[["Followers","customer_name","=","'+customer_name+'"]]&limit_page_length=all'
            

        res = requests.get(url=API_URL, verify=False)
        testimonial_res1 = json.loads(res.text)
        for r in testimonial_res1['data']:
            if type == "Follower":
                list_.append(r['customer_name'])
            elif type == "Following":
                list_.append(get_customer_name(r['email']))
        return Response(list_)




class Search_User(APIView):
    def get(self,request,format=None):
        customer_name = request.GET.get('customer_name')
        list_ = []
        if len(customer_name) <3:
            return Response({"error":"length should be greater than 2"})
        API_URL = 'http://14.98.78.69:2233/api/resource/Customer?fields=["name","customer_name","email_id"]&filters=[["Customer","name","LIKE","%'+customer_name+'%"]]'
        res = requests.get(url=API_URL, verify=False)
        json_data = json.loads(res.text)
        for r in json_data['data']:
            if r['email_id']:
                r.update({"image":get_profile_pic(r['email_id'])})
            list_.append(r)
        return Response(list_)


class GetFollowList(APIView):
    def get(self,request,format=None):
        email = request.GET.get('email')
        list_ = []
        API_URL = 'http://14.98.78.69:2233/api/resource/Followers?fields=["customer_name"]&filters=[["Followers","email","=","'+email+'"]]&limit_page_length=all'
        res = requests.get(url=API_URL, verify=False)
        json_data = json.loads(res.text)
        for r in json_data['data']:
            list_.append(get_customer_email(r['customer_name']))
        return Response(list_)



def get_customer_email(email):
    customer_name = 'http://14.98.78.69:2233/api/resource/Customer?fields=["email_id"]&filters=[["Customer", "name", "=", "'+email+'"]]&limit_page_length=all'
    res = requests.get(url = customer_name,verify=False)
    data_cust = json.loads(res.text)
    return data_cust['data'][0]['email_id']

class At_TheRate(APIView):
    def get(self,request,format=None):
        email = request.GET.get('email')
        q = request.GET.get('q')
        list_ = []
        
        API_URL = API_URL = 'http://14.98.78.69:2233/api/resource/Followers?fields=["customer_name","email"]&filters=[["Followers","email","=","'+email+'"],["Followers","customer_name","LIKE","%'+q+'%"]]&limit_page_length=all'
        res = requests.get(url=API_URL, verify=False)
        json_data = json.loads(res.text)
        for r in json_data['data']:
            if r['email']:
                email_id = get_customer_email(r['customer_name'])
                
                dict_ = {"email_id":email_id,"image":get_profile_pic(r['email']),"customer_name":r['customer_name']}
                list_.append(dict_)
        return Response(list_)

class User_POST(APIView):
    def get(self,request,format=None):
        email = request.GET.get('email')
        sid = get_sid()
        post_list = []
        start_page_length = request.GET.get('start_page_length')
        page_limit_length = request.GET.get('limit_page_length')
        customer_name = get_customer_name(email)
        API_URL_LENGTH = 'http://14.98.78.69:2233/api/resource/Posts Manager?fields=["name"]&filters=[["Posts Manager","person_name","=","'+customer_name+'"]]&limit_page_length=all'
        res_LENGTH = requests.get(url=API_URL_LENGTH, verify=False)
        json_data_LENGTH = json.loads(res_LENGTH.text)
        total_length = len(json_data_LENGTH['data'])
        API_URL = 'http://14.98.78.69:2233/api/resource/Posts Manager?fields=["*"]&filters=[["Posts Manager","person_name","=","'+customer_name+'"]]&limit_page_length='+page_limit_length+''
        res = requests.get(url=API_URL, verify=False)
        json_data = json.loads(res.text)
        
        for r in json_data['data']:
            API_URL_MEDIA = 'http://14.98.78.69:2233/api/resource/Media Table?fields=["media_data"]&filters=[["Media Table","post_id","=","'+r['name']+'"]]'

            res22 = requests.get(url=API_URL_MEDIA, verify=False)
            testimonial_res13 = json.loads(res22.text)
            user_image = get_profile_pic(r['owner'])
            image = testimonial_res13['data']

            API_URL_SHARED = 'http://14.98.78.69:2233/api/resource/Shared Users?fields=["*"]&filters=[["Shared Users","post_id","=","'+r['name']+'"]]'

            resshared = requests.get(url=API_URL_SHARED, verify=False)
            testimonial_res13shared = json.loads(resshared.text)
            shared_user = testimonial_res13shared['data']
            r.update({'post_media':image,'shared_users':shared_user})
            post_list.append(r)
        resp_ = {"data":post_list[int(start_page_length):int(page_limit_length)],"count":total_length}
        return Response(resp_)

class Coupon_List(APIView):
    def get(self,request,format=None):
        email = request.GET.get('email')
        sid = get_sid()
        coupon_list = []
        customer_name = get_customer_name(email)
        API_URL = 'http://14.98.78.69:2233/api/resource/Coupon Code?fields=["name"]&filters=[["Coupon Code","customer","=","'+customer_name+'"]]'
        res = requests.get(url=API_URL, verify=False)
        json_data = json.loads(res.text)
        
        for r in json_data['data']:
            API_URL1 = 'http://14.98.78.69:2233/api/resource/Coupon Code/'+r['name']+'?sid='+sid+''
            res2 = requests.get(url=API_URL1, verify=False)
            json_data1 = json.loads(res2.text)
            coupon_list.append(json_data1['data'])
        return Response(coupon_list)


class YouTubeVid(APIView):
    def get(self,request,format=None):
        email = request.GET.get('email')
        q = request.GET.get('video_id')
        api_key = "AIzaSyCp3f_DHoCrsyE9SFMaOVF-C8nhs5NDHg8"
        youtube = build('youtube','v3',developerKey=api_key)
        req = youtube.search().list(q=q,part='snippet')
        res = req.execute()
        return Response(res)

class Follow_Count(APIView):
    def get(self, request, format=None):
        email = request.GET.get('email')
        type = request.GET.get('type')
        if type == "Follower":
            API_URL = 'http://14.98.78.69:2233/api/resource/Followers?fields=["name"]&filters=[["Followers","email","=","'+email+'"]]&limit_page_length=all'
        elif type == "Following":
            customer_name = get_customer_name(email)
            API_URL = 'http://14.98.78.69:2233/api/resource/Followers?fields=["name"]&filters=[["Followers","customer_name","=","'+customer_name+'"]]&limit_page_length=all'
        res = requests.get(url=API_URL, verify=False)
        json_data = json.loads(res.text)
        return Response({"count":len(json_data['data'])})

