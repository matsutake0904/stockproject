from django.db import models
from django.contrib.auth.models import User
import logging
import pandas as pd
import numpy as np

# Create your models here.
# class TagModel(models.Model):
#     tag = models.CharField(max_length=100)
#     def __str__(self):
#         return self.tag

class TopImage(models.Model):
    title = models.CharField(max_length= 100)
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="")
    tag = models.TextField()
    good = models.IntegerField(default=0)


class BlogModel(models.Model):
    title = models.CharField(max_length=100)
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    images = models.ImageField(null=True, blank=True)
    tag = models.TextField(null=True, blank=True)
    pablish = models.BooleanField(default=False)

class StockExist(models.Model):
    stock_id=models.IntegerField(primary_key=True)
    stock_name=models.CharField(max_length=100, null=True, blank=True)

class StockData(models.Model):
    stock_id=models.ForeignKey(StockExist, on_delete= models.CASCADE)
    # stock_id=models.IntegerField(primary_key=True)
    date_data = models.CharField(max_length=50)
    open_data = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close_data = models.FloatField()
    volume = models.IntegerField()

    @staticmethod
    def get_stock_array(num):
        try:
            stock_model=StockExist.objects.get(stock_id=num)
        except Exception as e:
            logging.critical('Exception at Stockdata loading: {}'.format(e))
            return False, 0
        else:
            query_set = StockData.objects.filter(stock_id=stock_model).order_by('date_data')
            header=['date', 'open' ,'close', 'high', 'low', 'volume']
            logging.debug('Query size= 7* {}'.format(len(query_set)))
            data=np.empty((5, len(query_set)), dtype=None)
            counter=0
            for i in query_set:
                # data=np.append(data,[i.open_data, i.high, i.low, i.close_data, i.volume])
                # data[0,counter] = i.date_data
                data[0,counter] = i.open_data
                data[1,counter] = i.high
                data[2,counter] = i.low
                data[3,counter] = i.close_data
                data[4,counter] = i.volume
                counter += 1
            print(data)
            return True, data

    @staticmethod
    def get_stock_dictionary(num):
        try:
            stock_model=StockExist.objects.get(stock_id=num)
        except Exception as e:
            logging.critical('Exception at Stockdata loading: {}'.format(e))
            return False, 0
        else:
            query_set = StockData.objects.filter(stock_id=stock_model).order_by('date_data')
            header=['date', 'open' ,'close', 'high', 'low', 'volume']
            logging.debug('Query size= 7* {}'.format(len(query_set)))
            data=np.empty((5, len(query_set)), dtype=None)
            counter=0
            for i in query_set:
                # data=np.append(data,[i.open_data, i.high, i.low, i.close_data, i.volume])
                # data[0,counter] = i.date_data
                data[0,counter] = i.open_data
                data[1,counter] = i.high
                data[2,counter] = i.low
                data[3,counter] = i.close_data
                data[4,counter] = i.volume
                counter += 1
            print(data)
            return True, data
