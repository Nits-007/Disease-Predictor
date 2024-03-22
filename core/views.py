from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
import sqlite3
from .predict import *
from django.utils import timezone
from datetime import datetime
from .doctor import *
from .helper import *
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
import time
import json
from .doctor import *
# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required(login_url='users:login')
def check(request):       
    return render(request, 'patient.html')


@login_required(login_url='users:login')
def patient_details(request):
    if request.method=="POST":
        name=request.POST.get('name')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        weight=request.POST.get('weight')
        height=request.POST.get('height')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        city=request.POST.get('city')
        blood_group=request.POST.get('bg')
        blood_pressure=request.POST.get('bp')
        user=request.user
        print(user,name,age,gender,weight,height,address,phone,email,blood_group,blood_pressure,city)

        patient=Patient.objects.filter(user=user,name=name,phone=phone,email=email).first()
        if patient is None:
            patient=Patient.objects.create(user=user, name=name, age=age, gender=gender, weight=weight, height=height, address=address, phone=phone, email=email, blood_group=blood_group,blood_pressure=blood_pressure,city=city)
        else:
            patient.age = age
            patient.gender = gender
            patient.weight = weight
            patient.height = height
            patient.address = address
            patient.blood_group = blood_group
            patient.blood_pressure = blood_pressure
            patient.city = city
            patient.save()
        conn=sqlite3.connect('disease.db')
        cursor=conn.cursor()
        symptoms=set()
        for i in range(1,18):
            column_name=f'Symptom_{i}'
            query=f"SELECT {column_name} from Disease WHERE {column_name} is NOT NULL"
            cursor.execute(query)
            for row in cursor.fetchall():
                symptoms.add(row[0])
        cursor.close()
        conn.close()
        all_symptoms=list(symptoms)
        all_symptoms.sort()
        context={
            'patient':patient,
            'all_symptoms':all_symptoms,
        }
        return render(request,'symptom.html',context) 





@login_required(login_url='users:login')
def disease(request):
    if request.method=="POST":
        user=request.user
        patient_id=request.POST.get('patient_id')
        print(patient_id)
        symptoms=request.POST.getlist('additional_data')
        print(symptoms)
        for s in symptoms:
            symptom=s
        print(symptom)
        symptom=json.loads(symptom)
        print(type(symptom))
        patient=Patient.objects.filter(user=user,pk=patient_id).first()
        d,p=pred(symptom)
        result=list(zip(d,p))
        current=timezone.now()
        current = current.strftime('%Y-%m-%d %H:%M')
        current=str(current)
        ans=[]
        ans.append(symptoms)
        ans.append(result)
        print(ans)
        patient.disease[current]=ans
        patient.save()
        context={
            'result':result,
            'patient_id':patient_id,
        }
        return render(request,'disease.html',context)
    

def detail(request):
    disease=request.POST.get('disease')
    patient_id=request.POST.get('patient')
    user=request.user
    patient=Patient.objects.filter(user=user,pk=patient_id).first()
    disease=disease.strip()
    doctor=scrape_doctors(patient.city)
    
    description=description_db(disease)

    precaution=precaution_db(disease)

    remedy=remedy_db(disease)
    
    test=test_db(disease)
    

    context={
        'doctors':doctor,
        'precautions':precaution,
        'remedies':remedy,
        'descriptions':description,
        'tests':test,
    }

    return render(request, 'detail.html',context)



def record(request):
    user=request.user
    search=request.GET.get('search')
    date_search = request.GET.get('date_search')
    patients=Patient.objects.filter(user=user)
    if search:
        patients=patients.filter(name__icontains=search)
    if date_search:
        try:
            date_search = datetime.strptime(date_search, '%Y-%m-%d').date()
        except ValueError:
            date_search = None

        if date_search:
            patients = patients.filter(date_updated=date_search)
    context={
        'patients':patients,
        'search':search,
        'date_search':date_search,
    }
    patients = patients.order_by('-date_updated')
    return render(request, 'record.html', context)

def record_detail(request,id):
    user=request.user
    patient=Patient.objects.filter(user=user, pk=id).first()
    return render(request, 'record_detail.html', {'patient':patient})



def report(request):
    if request.method=="POST":
        user=request.user
        patient_id=request.POST.get('patient')
        print(patient_id)
        patient=Patient.objects.filter(user=user, pk=patient_id).first()
        patient_detail=dict()
        patient_detail['name']=patient.name
        patient_detail['age']=patient.age
        patient_detail['gender']=patient.gender
        patient_detail['weight']=patient.weight
        patient_detail['height']=patient.height
        patient_detail['bmi']=patient.weight/((patient.height/100)**2)
        patient_detail['bg']=patient.blood_group
        patient_detail['bp']=patient.blood_pressure
        disease=request.POST.get('disease')
        current=timezone.now()
        current = current.strftime('%Y-%m-%d %H:%M')
        current=str(current)
        disease=disease.strip()
        description=description_db(disease)
        precaution=precaution_db(disease)
        remedy=remedy_db(disease)
        test=test_db(disease)
        doctor=scrape_doctors(patient.city)
        current_date = datetime.now()
        formatted_date = current_date.strftime("%dth %B %Y")
        context={
            'patient':patient_detail,
            'current':current,
            'user':user,
            'disease':disease,
            'precautions':precaution,
            'remedies':remedy,
            'descriptions':description,
            'tests':test,
            'patient_id':patient_id,
            'doctors':doctor,
            'formatted_date':formatted_date,
        }
        return render(request, 'report.html', context)


def download(request):
    if request.method=="POST":
        user=request.user
        print(user)
        patient_id=request.POST.get('patient')
        print(patient_id)
        patient_id=int(patient_id)
        patient=Patient.objects.filter(user=user, pk=patient_id).first()
        patient_detail=dict()
        patient_detail['id']=patient.id
        patient_detail['name']=patient.name
        patient_detail['age']=patient.age
        patient_detail['gender']=patient.gender
        patient_detail['weight']=patient.weight
        patient_detail['height']=patient.height
        patient_detail['bmi']=patient.weight/((patient.height/100)**2)
        patient_detail['bg']=patient.blood_group
        patient_detail['bp']=patient.blood_pressure
        print(patient_detail)
        disease=request.POST.get('disease')
        current=timezone.now()
        current = current.strftime('%Y-%m-%d %H:%M')
        current=str(current)
        disease=disease.strip()
        description=description_db(disease)
        precaution=precaution_db(disease)
        remedy=remedy_db(disease)
        test=test_db(disease)
        print(description, precaution, remedy, test)
        context={
            'patient':patient_detail,
            'current':current,
            'user':user,
            'disease':disease,
            'precautions':precaution,
            'remedies':remedy,
            'descriptions':description,
            'tests':test,
        }
        template=loader.get_template('download_report.html')
        html=template.render(context)
        options={
        'page-size':'Letter',
        'encoding':'UTF-8'
        }
        pdf_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdf=pdfkit.from_string(html, False, options, configuration=pdf_config)
        response=HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition']='attachment'
        filename='report.pdf'
        return response
    




def add(request):
    if request.method=="POST":
        disease=request.POST.get('disease')
        print(disease)

        symptoms=request.POST.getlist('symptoms')
        symptoms=symptoms[0]
        symptom=symptoms.split(',')
        print(symptom)
        if len(symptom)>17:
            symptom=symptom[:17] 
        symptom += [''] * (17 - len(symptom))
   

        descriptions=request.POST.get('description')
        description=[descriptions]
        print(description)
        if len(description)>1:
            description=description[:1]
        description=description[0]
        print(description)
        print(type(description))

        precautions=request.POST.getlist('precautions')
        precautions=precautions[0]
        precaution=precautions.split(',')
        print(precaution)
        if len(precaution)>4:  
            precaution=precaution[:4]
        precaution += [''] * (4 - len(precaution))



        remedys = request.POST.getlist('remedy')
        remedys = remedys[0] 
        remedy = remedys.split(',')
        print(remedy) 
        if len(remedy)>3:
            remedy=remedy[:3]
        remedy += [''] * (3 - len(remedy))

        tests = request.POST.getlist('test')
        
        connection = sqlite3.connect('disease.db')
        cursor = connection.cursor()
        query = "INSERT INTO Disease (Disease, "
        query += ", ".join([f"Symptom_{i}" for i in range(1, 18)])
        query += ") VALUES (?, "
        query += ", ".join(["?" for _ in range(17)])
        query += ")"
        cursor.execute(query, tuple([disease] + symptom))
        connection.commit()
        connection.close()

        connection=sqlite3.connect('description.db')
        cursor=connection.cursor()
        cursor.execute("INSERT INTO Description (disease, description) VALUES (?, ?)", (disease, description))
        connection.commit()
        connection.close()

        connection = sqlite3.connect('precaution.db')
        cursor = connection.cursor()
        query = "INSERT INTO Disease (Disease, "
        query += ", ".join([f'"Precaution {i}"' for i in range(1, 5)])
        query += ") VALUES (?, "
        query += ", ".join(["?" for _ in range(4)])
        query += ")"
        cursor.execute(query, [disease] + precaution)
        connection.commit()
        connection.close()

        connection = sqlite3.connect('remedy.db')
        cursor = connection.cursor()
        query = f"INSERT INTO Remedy (Disease, Remedies1, Remedies2, Remedies3) VALUES (?, ?, ?, ?)"
        cursor.execute(query, [disease] + remedy)
        connection.commit()
        connection.close()

        connection = sqlite3.connect('test.db')
        cursor = connection.cursor()
        query = f"INSERT INTO Test (Disease, Test) VALUES (?, ?)"
        cursor.execute(query, [disease] + tests)
        connection.commit()
        connection.close()
        return redirect('core:index')


    return render(request, 'add.html')