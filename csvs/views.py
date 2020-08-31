from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import upload_form
from .models import Csvs
import pandas as pd
import csv
from django.contrib.auth.models import User
from products.models import Product, Purchase
from datetime import datetime
# Create your views here.

def data_upload_view(request):
    print('first line')
    try:
        form = upload_form(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            form=upload_form()

            obj = Csvs.objects.get(activate=False)
            print('file_run')

            with open(obj.file_name.path,'r') as csv_file1:
                reader = pd.read_csv(csv_file1)
                data = reader.values.tolist()
                reader = None
                for row in data:
                    user = User.objects.get(id=int(row[4]))
                    prod, _ = Product.objects.get_or_create(name=row[0])
                    
                    purhcase = Purchase.objects.create(
                        name = prod,
                        price = int(row[1]),
                        quantity = int(row[2]),
                        salesman = user,
                        date = datetime.strptime(row[5],'%d-%m-%Y')
                        
                        )
            messages.success(request,'File Uploaded Successfully')
            obj.activate = True
            obj.save()
            
            return HttpResponseRedirect(request.path)
    except Exception as e:
        messages.error(request,'Oops Something not done correctly try again!')
        print(e)
        form=upload_form()
        return HttpResponseRedirect(request.path)

    context = {
        'form':form
    }
    return render(request,'csvs/upload.html',context)