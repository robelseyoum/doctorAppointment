from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from base.models import *
from django.core.files.storage import FileSystemStorage
import uuid
from django.db import IntegrityError
import smtplib
from email.mime.text import MIMEText
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
import json
from base.models import *
from django.shortcuts import render_to_response

from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

import requests
from urllib.parse import urlparse

import datetime
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    if not request.user.is_authenticated():
        # return HttpResponseRedirect('/base/login/')
        return render(request, 'home.html' )
    else:
        user=request.user
        User_role=user.profile.role
        return render(request, 'home.html',{'User_role':User_role} )

def gallery(request):
    if not request.user.is_authenticated():
        # return HttpResponseRedirect('/base/login/')
        return render(request, 'gallery.html' )
    else:
        user=request.user
        User_role=user.profile.role
        return render(request, 'gallery.html',{'User_role':User_role} )

def our_staff(request):
    if not request.user.is_authenticated():
        # return HttpResponseRedirect('/base/login/')
        return render(request, 'our_staff.html' )
    else:
        user=request.user
        User_role=user.profile.role
        return render(request, 'our_staff.html',{'User_role':User_role} )
def about_us(request):
    if not request.user.is_authenticated():
        # return HttpResponseRedirect('/base/login/')
        return render(request, 'about_us.html' )
    else:
        user=request.user
        User_role=user.profile.role
        return render(request, 'about_us.html',{'User_role':User_role} )

def contact_us(request):
    if not request.user.is_authenticated():
        # return HttpResponseRedirect('/base/login/')
        return render(request, 'contact_us.html' )
    else:
        user=request.user
        User_role=user.profile.role
        return render(request, 'contact_us.html',{'User_role':User_role} )


def registration(request):
    # registration module
    if request.user.is_authenticated():
        return HttpResponseRedirect('/base/home/')

    elif request.method == "POST":
        username = request.POST.get('username',"")
        first_name = request.POST.get('first_name',"")
        email = request.POST.get('email',"")
        password = request.POST['password1']
        dob = request.POST['dob']
        sex = request.POST.get('sex',None)
        last_name = request.POST.get('last_name',"")
        phone = request.POST.get('phone',"")
        address = request.POST.get('address',"")
        role = request.POST.get('role',"")
        category = request.POST.get('category',"")


        date_object = datetime.datetime.strptime(dob, '%Y/%m/%d')

        IsUsernameExists=User.objects.filter(username=username).first()
        if IsUsernameExists is not None:
            message = '"' + username + '" already exist. Please try with a different username.'

            return render(request, 'signup.html',
                          {'error_message': message})



        # checking existing email.
        existing_email = User.objects.filter(email=email).first()
        if existing_email is not None:
            message = '"' + email + '" already exist. Please try with a different email.'

            return render(request, 'signup.html',
                          {'error_message': message})

        try:
            user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            email=email, last_name=last_name)
            user.set_password(raw_password=password)

            user.is_staff = True
            user.is_superuser = False
            user.is_active = True
            user.save()

            # role=3
            # user.is_superuser = True

            profile=Profile(user_id=user.pk,
                            is_admin=False,
                            phone=phone,
                            address=address,
                            sex=sex,
                            role=role,
                            dob=date_object

                            )
            profile.save()

            if role=='1':
                patient=Patient(user_id=user.pk)
                patient.save()
            if role=='2':
                doctor=Doctor(user_id=user.pk,category_id=category)
                doctor.save()


        except IntegrityError as e:

            e.message = 'Please fillup all fields correctly.Bad request.'

            return render(request, 'signup.html',
                          {'error_message': e.message})


        return render(request, 'login.html',
                      {'success_message': 'Registration Completed. Please login.'})
    else:
        return render(request, 'signup.html')

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/base/home/')

    else:

        from django.contrib.auth import login
        loginStatus = request.user.is_authenticated

        user = None
        # print(loginStatus)

        if request.method == 'POST':
            uname = request.POST['username']
            # uemail = request.POST['email']
            pword = request.POST['password']
            user = authenticate(username=uname, password=pword)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return HttpResponseRedirect('/base/begin/')
                    return HttpResponseRedirect('/base/home/')
                else:
                    return render(request, 'login.html', {'message': "It's not active user"})
            else:
                return render(request, 'login.html',
                              {'message': "Invalid login or your account is inactive"})

        elif request.method == 'GET':
            if (loginStatus == True):
                return HttpResponseRedirect('/base/home/')
            else:
                return render(request, 'login.html', {'message':''})
    return render(request, 'base/login.html', {'message': "Invalid User name Or Password"})
def logout(request):
    if request.user.is_authenticated():
        from django.contrib.auth import logout
        logout(request)
        return HttpResponseRedirect('/base/login')
    else:
        return HttpResponseRedirect('/base/login')


def profile(request,user_id):
    if request.method == "GET":
        user=User.objects.filter(id=user_id).first()
        profile=Profile.objects.filter(user_id=user_id).first()
        User_role = user.profile.role



        return render(request, 'profile.html', {'user':user,'profile':profile,'User_role':User_role})
    if request.method == "POST":

        username = request.POST.get('username', "")
        first_name = request.POST.get('first_name', "")
        email = request.POST.get('email', "")
        dob = request.POST['dob']
        sex = request.POST.get('sex', None)
        last_name = request.POST.get('last_name', "")
        phone = request.POST.get('phone', "")
        address = request.POST.get('address', "")
        # role = request.POST.get('role', "")
        # date_object = datetime.datetime.strptime(dob, '%Y/%m/%d').strftime('%m/%d/%y')

        # profile = Profile.objects.filter(user_id=user_id).first()
        #
        # print(profile.dob)
        # print(datetime.datetime.strptime(dob, '%b. %d, %Y').strftime('%Y-%m-%d'))
        #
        # if profile.dob != datetime.datetime.strptime(dob, '%b. %d, %Y').strftime('%Y-%m-%d'):
        #     dob =datetime.datetime.strptime(dob, '%b. %d, %Y').strftime('%Y-%m-%d')
        #     print("date changed")
        #     print(dob)



        user_updated=User.objects.filter(id=user_id).update(username=username,first_name=first_name,
                                                    email=email,
                                                    last_name=last_name
                                                    )

        profile_updated=Profile.objects.filter(user_id=user_id).update(dob=dob,sex=sex,phone=phone,address=address)

        user = User.objects.filter(id=user_id).first()
        profile = Profile.objects.filter(user_id=user_id).first()
        User_role = user.profile.role

        return render(request, 'profile.html', {'user':user,'profile':profile,'User_role':User_role})

def appointment_book(request):
    if request.user.is_authenticated():
        if request.method=='GET':
            doctors_id = Profile.objects.filter(role=2).values_list('user_id', flat=True)


            doctor_info = []
            for id in doctors_id:
                userinfo=User.objects.filter(id=id).first()
                doctor_obj=Doctor.objects.filter(user_id=id).first()


                category=Category.objects.filter(id=doctor_obj.category_id).first()
                temp = {}
                temp["id"] = userinfo.id
                temp["username"] = userinfo.username
                temp["category_name"] = category.category_name

                doctor_info.append(temp)

            user = request.user
            User_role = user.profile.role
            return render(request, 'appointment_book.html', {'doctorList': doctor_info,'User_role':User_role})

        if request.method == 'POST':
            doctor_id = request.POST['doctor_id']
            appointment_booking_date = request.POST['appointment_booking_date']

            # print(request.user.id)1418
            # print(doctor_id)
            patient=Patient.objects.filter(user_id=request.user.id).first()
            doctor=Doctor.objects.filter(user_id=doctor_id).first()
            appoinment=Appointment(patient_id=patient.id,doctor_id=doctor.id,
                                   last_change=datetime.datetime.now(),
                                   appointment=appointment_booking_date,
                                   )
            appoinment.save()

            return HttpResponseRedirect('/base/appointment_me/')

    else:
        return HttpResponseRedirect('/base/login/')



def appointment_update(request):
    if request.user.is_authenticated():
        requested_user=request.user
        if request.method=='GET':
            doctors_id = Profile.objects.filter(role=2).values_list('user_id', flat=True)
            doctor_info = []
            for id in doctors_id:
                userinfo=User.objects.filter(id=id).first()
                doctor_obj=Doctor.objects.filter(user_id=id).first()
                category=Category.objects.filter(id=doctor_obj.category_id).first()
                temp = {}
                temp["id"] = userinfo.id
                temp["username"] = userinfo.username
                temp["category_name"] = category.category_name
                temp["doctor_id"]=doctor_obj.id

                doctor_info.append(temp)

            patient=Patient.objects.filter(user_id=requested_user.id).order_by('-creation_date').first()

            # print(patient.id)

            previous_appoinment_data=Appointment.objects.filter(patient_id=patient.id).order_by('-creation_date').first()

            user = request.user
            User_role = user.profile.role
            return render(request, 'appointment_update.html', {'previous_appoinment_data':previous_appoinment_data,'doctorList': doctor_info,'User_role':User_role})
        if request.method == 'POST':
            doctor_user_id = request.POST['doctor_user_id']
            appointment_update_date = request.POST['appointment_update_date']

            # print(doctor_user_id)19

            doctor = Doctor.objects.filter(user_id=doctor_user_id).first()
            patient = Patient.objects.filter(user_id=requested_user.id).order_by('-creation_date').first()

            update=Appointment.objects.filter(patient_id=patient.id).order_by('-creation_date').update(doctor_id=doctor.id,appointment=appointment_update_date,last_change=datetime.datetime.now())
            return HttpResponseRedirect('/base/appointment_update/')

    else:
        return HttpResponseRedirect('/base/login/')




def appointment_me(request):
    if request.user.is_authenticated():
        requested_user=request.user
        User_role = requested_user.profile.role
        if User_role=='1':
            patient = Patient.objects.filter(user_id=requested_user.id).order_by('-creation_date').first()
            appointment=Appointment.objects.filter(patient_id=patient.id).order_by('-creation_date').first()

            if appointment is not None:
                doctor = Doctor.objects.filter(id=appointment.doctor_id).first()
                doctor_user_info=User.objects.filter(id=doctor.user_id).first()

                appointment_data = []

                temp = {}
                temp["appointment_id"] = appointment.id
                temp["creation_date"] = appointment.creation_date
                temp["last_change"] = appointment.last_change
                temp["doctor_name"] = doctor_user_info.username
                temp["appointment_date"] = appointment.appointment

                appointment_data.append(temp)
                alert_message=""
                today=datetime.datetime.now()
                if appointment.appointment.replace(tzinfo=None) - today < timedelta(days=1) and appointment.appointment.replace(tzinfo=None) - today > timedelta(days=0):
                    alert_message="Notice: You have an Appoinmet in less than 1 day."
                    # print("HAHAHAHA")
                print(appointment.appointment.replace(tzinfo=None)-today+datetime.timedelta(days=1))
                # print(appointment.appointment.replace(tzinfo=None) - today )



                return render(request, 'appointment_list.html', {'appointment_data':appointment_data,'User_role':User_role,'alert_message':alert_message })

            else:
                return render(request, 'appointment_list.html',
                              {'appointment_data': None, 'User_role': User_role})



        if User_role == '2':
            doctor = Doctor.objects.filter(user_id=requested_user.id).first()
            appointments=Appointment.objects.filter(doctor_id=doctor.id).order_by('-creation_date').all()

            appointment_data = []
            for appointment in appointments:
                patient=Patient.objects.filter(id=appointment.patient_id).order_by('-creation_date').first()
                patient_user_info=User.objects.filter(id=patient.user_id).first()

                temp = {}
                temp["appointment_id"] = appointment.id
                temp["creation_date"] = appointment.creation_date
                temp["last_change"] = appointment.last_change
                temp["patient_name"] = patient_user_info.username
                temp["appointment_date"] = appointment.appointment

                appointment_data.append(temp)
            return render(request, 'Doctor_appointment.html',
                          {'appointment_data': appointment_data, 'User_role': User_role})





    else:
        return HttpResponseRedirect('/base/login/')


def feedback(request):
    if request.user.is_authenticated():
        requested_user = request.user
        User_role = requested_user.profile.role
        if request.method=='GET':

            return render(request, 'feedback.html', {'User_role':User_role})
        if request.method=='POST':
            feedback = request.POST['feedback']
            patient = Patient.objects.filter(user_id=requested_user.id).order_by('-creation_date').first()

            feedback=Feedback(patient_id=patient.id,feedback=feedback)
            feedback.save()

            return render(request, 'feedback.html', {'User_role':User_role})
    else:
        return HttpResponseRedirect('/base/login/')


def treatment(request,appointment_id):

    if request.user.is_authenticated():
        appointment = Appointment.objects.filter(id=appointment_id).first()
        patient = Patient.objects.filter(id=appointment.patient_id).order_by('-creation_date').first()
        doctor = Doctor.objects.filter(id=appointment.doctor_id).order_by('-creation_date').first()
        requested_user = request.user
        User_role = requested_user.profile.role
        if request.method == 'GET':

            return render(request, 'treatment_single_patient.html', {'User_role': User_role,
                                                                     'appointment':appointment,
                                                                     'patient':patient})
        if request.method == 'POST':
            treatment_for = request.POST.get('treatment_for','')
            treatment_txt = request.POST.get('treatment','')
            notes = request.POST.get('notes','')
            appointment_id = request.POST.get('appointment_id','')
            treatment=Treatment(patient_id=patient.id,
                                doctor_id=doctor.id,
                                last_change=datetime.datetime.now(),
                                treatment=treatment_txt,
                                treatment_for=treatment_for,
                                dnote=notes,
                                appointment_id=appointment_id
                                )
            treatment.save()
            return HttpResponseRedirect('/base/treatment_details/')
            # return render(request, 'treatment_single_patient.html', {'User_role': User_role,
            #                                                          'appointment': appointment,
            #                                                          'patient': patient})

    else:
        return HttpResponseRedirect('/base/login/')



def patients(request):
    if request.user.is_authenticated():
        requested_user = request.user
        User_role = requested_user.profile.role
        doctor = Doctor.objects.filter(user_id=requested_user.id).first()
        appointments = Appointment.objects.filter(doctor_id=doctor.id).all()

        patient_list = []
        for appointment in appointments:
            patient = Patient.objects.filter(id=appointment.patient_id).first()
            profile = Profile.objects.filter(user_id=patient.user_id).first()

            temp = {}
            temp["first_name"] = patient.user.first_name
            temp["last_name"] = patient.user.last_name
            # temp["last_change"] = appointment.last_change
            # temp["sex"] = profile.sex
            if profile.sex=='0':
                temp["sex"] = "Female"
            elif profile.sex=='1':
                temp["sex"] = "Male"
            if profile.sex=='2':
                temp["sex"] = "Both"




            temp["dob"] = profile.dob
            temp["patient_address"] = profile.address
            temp["patient_phone_number"] = profile.phone

            patient_list.append(temp)


        # patient_list=Patient.objects.filter(id__in=patients_id).all()

        return render(request, 'patients.html', {'patient_list': patient_list,'User_role':User_role })



    else:
        return HttpResponseRedirect('/base/login/')


def view_doctor(request):
    if request.user.is_authenticated():
        requested_user = request.user
        User_role = requested_user.profile.role
        doctors = Doctor.objects.all()


        doctor_list = []
        for doctor in doctors:
            doctor_profile = Profile.objects.filter(user_id=doctor.user_id).first()

            temp = {}
            temp["doctor_id"] = doctor.id
            temp["first_name"] = doctor.user.first_name
            temp["last_name"] = doctor.user.last_name
            # temp["last_change"] = appointment.last_change
            if doctor_profile.sex=='0':
                temp["sex"] = "Female"
            elif doctor_profile.sex=='1':
                temp["sex"] = "Male"
            if doctor_profile.sex=='2':
                temp["sex"] = "Both"

            temp["doctor_address"] = doctor_profile.address
            temp["doctor_phone_number"] = doctor_profile.phone

            doctor_list.append(temp)

        return render(request, 'doctor_list.html', {'doctor_list': doctor_list, 'User_role': User_role})

    else:
        return HttpResponseRedirect('/base/login/')



def delete_doctor(request):
    if request.user.is_authenticated():
        doctor_id = request.POST['doctor_id']
        appointment=Appointment.objects.filter(doctor_id=doctor_id).delete()
        treatment=Treatment.objects.filter(doctor_id=doctor_id).delete()

        doctor_info=Doctor.objects.filter(id=doctor_id).first()


        isDoctorProfileDeleted = Profile.objects.filter(user_id=doctor_info.user_id).delete()
        isDoctorUserDeleted = User.objects.filter(id=doctor_info.user_id).delete()
        isDoctorDeleted = Doctor.objects.filter(id=doctor_id).delete()

        return HttpResponse("1")


    else:
        return HttpResponseRedirect('/base/login/')






def view_customer(request):
    if request.user.is_authenticated():
        requested_user = request.user
        User_role = requested_user.profile.role
        patients = Patient.objects.all()

        patient_list = []
        for patient in patients:

            profile = Profile.objects.filter(user_id=patient.user_id).first()

            temp = {}
            temp["first_name"] = patient.user.first_name
            temp["last_name"] = patient.user.last_name
            # temp["last_change"] = appointment.last_change
            # temp["sex"] = profile.sex
            if profile.sex=='0':
                temp["sex"] = "Female"
            elif profile.sex=='1':
                temp["sex"] = "Male"
            if profile.sex=='2':
                temp["sex"] = "Both"




            temp["dob"] = profile.dob
            temp["patient_address"] = profile.address
            temp["patient_phone_number"] = profile.phone

            patient_list.append(temp)


        # patient_list=Patient.objects.filter(id__in=patients_id).all()

        return render(request, 'patients.html', {'patient_list': patient_list,'User_role':User_role })



    else:
        return HttpResponseRedirect('/base/login/')

def view_appointment(request):
    if request.user.is_authenticated():
        requested_user=request.user
        User_role = requested_user.profile.role
        if User_role=='3':
            # patient = Patient.objects.order_by('-creation_date').all()
            appointments=Appointment.objects.order_by('-creation_date').all()

            if appointments.count() !=0:

                appointment_data = []

                for appointment in appointments:

                    doctor = Doctor.objects.filter(id=appointment.doctor_id).first()
                    doctor_user_info=User.objects.filter(id=doctor.user_id).first()



                    temp = {}
                    temp["appointment_id"] = appointment.id
                    temp["creation_date"] = appointment.creation_date
                    temp["last_change"] = appointment.last_change
                    temp["doctor_name"] = doctor_user_info.username
                    temp["appointment_date"] = appointment.appointment
                    temp["is_notified"] = appointment.is_notified


                    alert_message=""
                    today=datetime.datetime.now()
                    if appointment.appointment.replace(tzinfo=None) - today < timedelta(days=1) and appointment.appointment.replace(tzinfo=None) - today >timedelta(days=0) :
                        alert_message="Notice: Appointment within 1 day.."

                    temp["alert_message"] = alert_message
                    appointment_data.append(temp)


                return render(request, 'all_appointment_list.html', {'appointment_data':appointment_data,'User_role':User_role })

            else:
                return render(request, 'all_appointment_list.html',
                              {'appointment_data': None, 'User_role': User_role})
    else:
        return HttpResponseRedirect('/base/login/')


from django.core.mail import send_mail
def send_notification(request):
    if request.user.is_authenticated():
        appointment_id = request.POST['appointment_id']
        appointment=Appointment.objects.filter(id=appointment_id).first()
        patient=Patient.objects.filter(id=appointment.patient_id).first()

        # print(patient.user.email)
        try:
            send_mail('Appoinment Notification', 'Dear '+patient.user.username+',You Have an Appointment Within 1 Day. Please Make sure You don\'t miss the appointment.Thanks.' , 'madiaddis3@gmail.com', [patient.user.email])
            Appointment.objects.filter(id=appointment_id).update(is_notified=True)
            return HttpResponse("1")
        except:
            return HttpResponse("0")


    else:
        return HttpResponseRedirect('/base/login/')


def delete_appointment(request):
    if request.user.is_authenticated():
        appointment_id = request.POST['appointment_id']


        try:
            appointment = Appointment.objects.filter(id=appointment_id).delete()
            return HttpResponse("1")
        except:
            return HttpResponse("0")


    else:
        return HttpResponseRedirect('/base/login/')







def view_feedback(request):
    if request.user.is_authenticated():
        requested_user=request.user
        User_role = requested_user.profile.role
        if User_role=='3':
            # patient = Patient.objects.order_by('-creation_date').all()
            feedbacks=Feedback.objects.order_by('-creation_date').all()

            if feedbacks.count() !=0:

                feedback_data = []

                for feedback in feedbacks:
                    patient = Patient.objects.filter(id=feedback.patient_id).first()



                    temp = {}
                    temp["patient_id"] = feedback.patient_id
                    temp["creation_date"] = feedback.creation_date
                    temp["patient_name"] = patient.user.username
                    temp["feedback"] = feedback.feedback


                    feedback_data.append(temp)


                return render(request, 'all_feedback.html', {'feedback_data':feedback_data,'User_role':User_role })

            else:
                return render(request, 'all_feedback.html',
                              {'feedback_data': None, 'User_role': User_role})
    else:
        return HttpResponseRedirect('/base/login/')






def treatment_details(request):
    if request.user.is_authenticated():
        requested_user = request.user
        User_role = requested_user.profile.role
        doctor = Doctor.objects.filter(user_id=requested_user.id).first()
        treatments = Treatment.objects.filter(doctor_id=doctor.id).order_by('-creation_date')

        treatment_data = []
        for treatment in treatments:
            patient = Patient.objects.filter(id=treatment.patient_id).first()


            temp = {}
            temp["appointment_id"] = treatment.appointment_id
            temp["patient_name"] = patient.user.username
            temp["treatment_date"] = treatment.creation_date
            temp["treatment"] = treatment.treatment
            temp["treatment_for"] = treatment.treatment_for
            temp["notes"] = treatment.dnote

            treatment_data.append(temp)



        return render(request, 'treatment_details.html', {'User_role': User_role,'treatment_data':treatment_data})
    else:
        return HttpResponseRedirect('/base/login/')
