from django.shortcuts import render, redirect
from django.http import request
from blog.myPython_package import utils, scraype, my_lstm
from .models import TopImage, BlogModel, StockExist, StockData
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView
import pandas as pd
import numpy as np
import logging

# Create your views here.
def loginfunc(request):
    num = [1, 2, 3, 4, 5]
    TopImages=TopImage.objects.all()
    object=TopImages[0]
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password= password)
        if user is not None:
            login(request, user)
            return redirect('top')
        else:
            return redirect('login')
    return render(request, 'login.html',{'object': object})

def signupfunc(request):
    user2 = User.objects.all()
    print(user2)
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']
        try:
            User.objects.get(username=user_name)
            return render(request, 'signup.html',{'error':'This username is already resistered !'})
        except:
            user = User.objects.create_user(user_name, ' ', password)
        
        return redirect('login') 
    ##return data conbined template 
    return render(request, 'signup.html', {'some' : 100})

def topfunc(request):
    object_list = BlogModel.objects.all()
    close=0
    error0=""

    ##Login request
    if request.method == 'POST' and request.POST['redirect_to'] == 'top':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password= password)
        if user is not None:
            login(request, user)
            return redirect('top')
        else:
            return redirect('top')

    ##Scrayping And AI request
    elif request.method == 'POST' and request.POST['redirect_to'] == 'scraype':
        num = request.POST['num']

        if StockExist.objects.filter(stock_id =num).count() == 0:
            logging.info('Scraype New data from web')
            stock = scraype.ScrapeStock(num)
            req=stock.scraypeDate()
            achive="model0"
            if req:
                # close_array=stock.getData().iloc[0].loc[:'Close'].values
                try:
                    model0=StockExist.objects.create(stock_id=num)
                    # model0=StockExist
                    achive="model1"
                    for i in range(stock.get_length()):
                        logging.info("ROOP: {}".format(i))
                        logging.critical("date data == {}".format(type(stock.get_date(i))))
                        StockData.objects.create(stock_id=StockExist.objects.filter(stock_id=num)[0],
                         date_data=stock.get_date(i), open_data= stock.get_open(i), 
                         high = stock.get_high(i), low = stock.get_low(i), 
                         close_data=stock.get_close(i),volume= stock.get_volume(i))
                except Exception as e:
                    logging.critical("CRITICAL at DB create {}".format(e))
                    logging.critical("Error at {}".format(achive))
                    close=0
                    error0 = e
                else:
                    # StockExist.save()
                    # StockData.save()
                    # close=StockData.objects.filter(stock_id=model0.pk)[-1].open_data
                    logging.warning('get data from DB')
                    succsecc_db, data_set = StockData.get_stock_array(num)
                    print('success to get data from DB ')
                    close=data_set[1,1]

            else:
                close=10
                error0='No stock data at web'
                return render(request, 'top.html', {'objects': object_list, 'close': close, 'error':error0}) 
        
        logging.debug('get data from DB')
        succsecc_db, data_set = StockData.get_stock_array(num)
        logging.debug('success to get data from DB ')
        logging.debug('Call AI System ')
        model = my_lstm.LSTM_model()
        boo, history = model.train_model(data_set[0,:])
        success_ai, predicted = model.predict(data_set[0,:])
        close=predicted


    return render(request, 'top.html', {'objects': object_list, 'close': close, 'error':error0})    

def logoutfunc(request):
    logout(request)
    return redirect('top')

class BlogCreate(CreateView):
    template_name = 'create.html'
    model = BlogModel
    fields = ['title', 'auther', 'content', 'images', 'tag']
    success_url = reverse_lazy('top')
    # def get_success_url(self):
    #     print("SUCCESS TO SUBMIT")
    #     return super().get_success_url('top')

class BlogDelete(DeleteView):
    model= BlogModel
    template_name = 'delete.html'
    success_url = reverse_lazy('top')
