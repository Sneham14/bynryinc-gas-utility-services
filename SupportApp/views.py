from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import  Feedback
from GasUtilityConsumerServicesApp.models import *
# Create your views here.

def post_feedback(request): 
    if request.method == "POST":
        feedback = request.POST.get('feedback', None)
        if feedback != '':  
            f = Feedback(sender=request.user, feedback=feedback)
            f.save()        
            print(feedback)   

        try:
            if (request.user.patient.is_patient == True) :
                return HttpResponse("Feedback successfully sent.")
        except:
            pass
        
        if (request.user.doctor.is_doctor == True) :
            return HttpResponse("Feedback successfully sent.")
        else :
            return HttpResponse("Feedback field is empty   .")


def get_feedback(request):
    if request.method == "GET":
        obj = Feedback.objects.all()
        return redirect(request, 'chatbody.html',{"obj":obj})




