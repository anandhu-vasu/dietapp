from django.shortcuts import render,redirect
from django.contrib import messages

from dietapp.models import Form,Profile
from dietapp.form import SignUpForm

from plotly.offline import plot
from plotly.graph_objects import Scatter

from dietapp.bmi import BMI

import joblib
import re

from sklearn import preprocessing
import pandas as pd
from pandas import DataFrame
from pandas import read_csv
from pandas.io.json import json_normalize
from io import StringIO

from datetime import datetime
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def form(request):
    return render(request, 'form.html', {})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account created successfully")
            return redirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form':form})


def mom(request):
    return render(request, 'mom.html')


def dashboard(request,nav=None):
    if request.user.is_authenticated:
        if nav=='weight-tracker':
            if request.user.profile.all():
                x_data = list(request.user.profile.values_list('date',flat=True))
                y_data = list(request.user.profile.values_list('weight',flat=True))
                weight_plot = plot(
                    [Scatter(
                        x=x_data,
                        y=y_data,
                        mode='lines+markers',
                        name='Weight',
                        opacity=0.8,
                        marker_color=y_data,
                        line_color='grey',
                        hovertemplate="%{y} Kg on  %{x}",
                    )],
                    output_type='div',
                    include_plotlyjs=False,
                    show_link=False,
                    link_text="",
                )
            else:
                weight_plot = "<div class='no-data' >No Records Available for Weight Tracking</div>"
            return render(request, 'weight-tracker.html', {'weight_plot': weight_plot})
        elif nav == 'dietplans':
            if request.user.profile.all():
                breakfast = request.user.profile.values_list('breakfast',flat=True)
                lunch = request.user.profile.values_list('breakfast',flat=True)
                dinner = request.user.profile.values_list('breakfast',flat=True)
                date = request.user.profile.values_list('date',flat=True)
                foodlist = []
                for i in range(0,len(breakfast)):
                    foodlist.append(
                        {
                            'breakfast':breakfast[i].split("_"),
                            'lunch':lunch[i].split("_"),
                            'dinner':dinner[i].split("_"),
                            'date':date[i]
                        }
                    )
                foodlist.reverse()
                return render(request, 'dietplans.html', {'foodlist':foodlist})
            else:
                return render(request, 'dietplans.html')
        elif nav == "dietform":
            last = request.user.profile.last()
            return render(request,'dietform.html',{'last':last})
        elif nav == "currentdiet":
            if request.user.profile.all():
                latest = request.user.profile.last()
                fooddiet = {
                    'breakfast': latest.breakfast.split("_"),
                    'lunch': latest.lunch.split("_"),
                    'dinner': latest.dinner.split("_"),
                    'date': latest.date,
                }
                diet_status = "Current Personalised Diet Plan"
                return render(request, 'mydiet.html', {'fooddiet': fooddiet,'diet_status':diet_status})
            else:
                return render(request,'mydiet.html')
        elif nav == 'mydiet':
            return diet(request)
        elif nav == 'details':
            if request.user.profile.all():
                last = request.user.profile.last();
                weight_diff=0
                height_diff=0
                if request.user.profile.count() > 1:
                    pre = request.user.profile.get(id=last.id-1)
                    if pre:
                        weight_diff = last.weight - pre.weight
                        height_diff = last.height - pre.height
                return render(request,'details.html',{**BMI(last.weight,last.height),'last':last,'diff':{'height':height_diff,'weight':weight_diff}})
            else:
                return render(request,'details.html')
        else:
            if request.user.profile.all():
                lastdate = request.user.profile.last().date
                diff_date = timezone.now() - lastdate
                return render(request,'home.html',{'diff_date':diff_date.days})
            else:
                return render(request, 'home.html')
    else:
        return redirect('/')


def diet(request):
    if request.method == 'POST':
        data=request.POST
        form = Form(
            gender=data['gender'],
            age=data['age'],
            occupation=data['occupation'],
            height=data['height'],
            weight=data['weight'],
            diet_plan=data['plan'],
            veg=data['veg'],
            disease=data['disease'],
            allergy=data['allergy'],
        )
        form.save()
        user= request.user
        f=open("dietapp/csv/data.csv","w")
        f.write(data['gender']+',')
        f.write(data['age']+',')
        f.write(data['occupation']+',')
        f.write(data['height']+',')
        f.write(data['weight']+',')
        f.write(data['plan']+',')
        f.write(data['veg']+',')
        f.write(data['disease']+',')
        f.write(data['allergy'])
        f.close()

        names = ['gender', 'age', 'occupation', 'height', 'weight', 'plan', 'veg', 'disease', 'allergy']
        transet = read_csv('dietapp/csv/food.csv', names=names)
        dataset=read_csv('dietapp/csv/data.csv',names=names)

        le = preprocessing.LabelEncoder()
        for column_name in transet.columns:
            if transet[column_name].dtype == object:
                le.fit(transet[column_name].astype(str))
            else:
                pass
        le = preprocessing.LabelEncoder()
        for column_name in dataset.columns:
            if dataset[column_name].dtype == object:
                le.fit(transet[column_name].astype(str))
                dataset[column_name] = le.transform(dataset[column_name].astype(str))
            else:
                pass

        breakfast_model = joblib.load("staticfiles/ml_models/breakfast_model.sav")
        [breakfast]=breakfast_model.predict(dataset.values)
        lunch_model = joblib.load("staticfiles/ml_models/lunch_model.sav")
        [lunch] = lunch_model.predict(dataset.values)
        dinner_model = joblib.load("staticfiles/ml_models/dinner_model.sav")
        [dinner] = dinner_model.predict(dataset.values)

        breakfast=re.sub(r'[*]\d+', '',breakfast)
        lunch = re.sub(r'[*]\d+', '', lunch)
        dinner = re.sub(r'[*]\d+', '', dinner)
        fooddiet = {'breakfast': breakfast.split('_'), 'lunch': lunch.split('_'), 'dinner': dinner.split('_'), }
        if user.is_authenticated:
            last = request.user.profile.last();
            diet_status = "Your New Personalised Diet Plan"
            Profile.objects.create(
                user=user,
                gender=data['gender'],
                age=data['age'],
                occupation=data['occupation'],
                height=data['height'],
                weight=data['weight'],
                diet_plan=data['plan'],
                veg=data['veg'],
                disease=data['disease'],
                allergy=data['allergy'],
                breakfast=breakfast,
                lunch=lunch,
                dinner=dinner,
            )
            if last:
                if (last.breakfast == breakfast or last.lunch == lunch or last.dinner == dinner):
                    diet_status = "No need to Change the diet plan."
            return render(request,"mydiet.html",{'diet_status':diet_status,'fooddiet':fooddiet,**BMI(data['weight'],data['height'])})
        return render(request, "diet.html",{'fooddiet':fooddiet})
    return redirect('/form/')

def error404(request,exception):
    return render(request, "404.html")
def error500(request):
    return render(request,"500.html")