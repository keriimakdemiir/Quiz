from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import *
from django.http import HttpResponse
from .models import UserProfile

def home(request):
    if request.method == 'POST':
        # Skor hesaplama kısmı
        score = 0
        total = 0
        for q in QuesModel.objects.all():
            total += 1
            if q.ans == request.POST.get(q.question):
                score += 10
        percent = score / (total * 10) * 100

        # Kullanıcının en iyi skorunu güncelle
        if request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            if percent > user_profile.best_score:
                user_profile.best_score = percent
                user_profile.save()

        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'percent': percent,
            'total': total
        }
        return render(request, 'Quiz/result.html', context)
    else:
        questions = QuesModel.objects.all()
        context = {
            'questions': questions
        }
        return render(request, 'Quiz/home.html', context)

def addQuestion(request):    
    if request.user.is_staff:
        form=addQuestionform()
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'Quiz/addQuestion.html',context)
    else: 
        return redirect('home') 

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home') 
    else: 
        form=createuserform()
        if request.method=='POST':
            form=createuserform(request.POST)
            if form.is_valid() :
                user=form.save()
                return redirect('login')
        context={
            'form':form,
        }
        return render(request,'Quiz/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'Quiz/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('/')

