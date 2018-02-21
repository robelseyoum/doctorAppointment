from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings

# app_name="lifehub"

urlpatterns = [
    url(r'^home/$', views.home, name="home"),
    url(r'^gallery/$', views.gallery, name="gallery"),
    url(r'^our_staff/$', views.our_staff, name="our_staff"),
    url(r'^about_us/$', views.about_us, name="about_us"),
    url(r'^contact_us/$', views.contact_us, name="contact_us"),
    url(r'^registration/$', views.registration, name="registration"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^profile/(?P<user_id>.*)/$', views.profile, name="profile"),
    url(r'^appointment_book/$', views.appointment_book, name="appointment_book"),
    url(r'^appointment_me/$', views.appointment_me, name="appointment_me"),
    url(r'^appointment_update/$', views.appointment_update, name="appointment_update"),
    url(r'^feedback/$', views.feedback, name="feedback"),
    url(r'^patients/$', views.patients, name="patients"),
    url(r'^treatment/(?P<appointment_id>.*)/$', views.treatment, name="treatment"),
    url(r'^view_doctor/$', views.view_doctor, name="view_doctor"),
    url(r'^view_customer/$', views.view_customer, name="view_customer"),
    url(r'^view_appointment/$', views.view_appointment, name="view_appointment"),
    # url(r'^reschedule_delete_booking/(?P<call_type>.*)/$', views.reschedule_delete_booking, name="reschedule_delete_booking"),
    url(r'^view_feedback/$', views.view_feedback, name="view_feedback"),
    url(r'^delete_doctor/$', views.delete_doctor, name="delete_doctor"),
    url(r'^treatment_details/$', views.treatment_details, name="treatment_details"),
    url(r'^send_notification/$', views.send_notification, name="send_notification"),
    url(r'^delete_appointment/$', views.delete_appointment, name="delete_appointment"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
