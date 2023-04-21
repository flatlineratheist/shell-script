from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from wapi.models import *


# Create your views here.
@login_required(login_url='/admin') #redirect when user is not logged in
def adminlogin(request):
    if request.method == 'POST':
        return HttpResponse("POST")
    lang = WAPILanguage.objects.all()
    role = WAPIRoleName.objects.all()
    qType = WAPIQuestionType.objects.all()
    validationType = WAPIValidationType.objects.all()
    
    
    return render(request,'login.html',{'lang':lang,'role':role,'qType':qType,'validationType':validationType})

