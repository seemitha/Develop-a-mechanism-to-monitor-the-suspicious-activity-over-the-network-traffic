from dataclasses import dataclass
from django.shortcuts import redirect, render
# from grpc import Status
from django.http import HttpResponse
import pandas as pd

from sklearn.preprocessing import LabelEncoder

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from django.http import JsonResponse
from django.core.mail import send_mail
import smtplib


# Create your views here.


def indexView(request):
    return render(request,'index.html')

def adminView(request):
    return render(request,'login.html')

    
def loginView(request):
    print('Login Process')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if username == 'admin' and password == '123':
            return render(request,'home.html')
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})

def analysisView(request):
    print('reached')
    train_dataset=pd.read_csv('Train_data.csv')

    encoded_protocolType=LabelEncoder().fit_transform(y=train_dataset.protocol_type)
    protocol_type=train_dataset.protocol_type
    train_dataset.protocol_type=encoded_protocolType

    encoded_flag=LabelEncoder().fit_transform(y=train_dataset.flag)
    original_flag=train_dataset.flag
    train_dataset.flag=encoded_flag

    encoded_service=LabelEncoder().fit_transform(y=train_dataset.service)
    original_service=train_dataset.service
    train_dataset.service=encoded_service

    train_dataset.rename(columns={'class':'target'},inplace=True)
    train_dataset.target=LabelEncoder().fit_transform(y=train_dataset.target)

    train_dataset

    X=train_dataset.iloc[:,:-1]
    Y=train_dataset.target

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.10, random_state=42)
    model=RandomForestClassifier(n_estimators=100,criterion='entropy')

    model.fit(X_train,y_train)
    model.predict(X_test)
    
    test_dataset_row=pd.read_csv('Test_data.csv').sample()
    row=test_dataset_row

# encoded_protocolType[list(protocol_type).index('icmp')]
    p=list(test_dataset_row['protocol_type'])
    test_dataset_row.protocol_type=encoded_protocolType[list(protocol_type).index(p[0])]

    s=list(test_dataset_row['service'])
    test_dataset_row.service=encoded_service[list(original_service).index(s[0])]

    s=list(test_dataset_row['flag'])
    test_dataset_row.flag=encoded_flag[list(original_flag).index(s[0])]

   
   
    print(test_dataset_row.transpose())

    y_predicted=model.predict(test_dataset_row)
    if y_predicted[0] == 0:
        result='Normal Taffic'
    else:
        result='Abnormal Traffic'
    

    return render(request,'divData.html',{'analysisData': result,'row':row.transpose().to_html()});

def contactView(request):
    return render(request,'contact.html')

def send_email(request):

    name = request.POST['name']
    query = request.POST['query']
    # creates SMTP session

    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication

    s.login("19f25@sdmit.in", "sdmit.in")
    
    # message to be sent

    message = "Query is "+query+" from "+name
    
    # sending the mail

    s.sendmail("19f25@sdmit.in", "sharalshiny062001@gmail.com", message)
    
    # terminating the session
    s.quit()
    return render(request,'contact.html')

