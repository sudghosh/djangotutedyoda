from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
import pandas as pd
from .models import Product, Purchase
from .utils import get_simple_plot, get_salesman_by_id, sales_view_plot
from .forms import PurchaseForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def sales_dist_view(request):
    df = pd.DataFrame(Purchase.objects.all().values())
    df['salesman_id']=df['salesman_id'].apply(get_salesman_by_id)
    df.rename({'salesman_id':'salesman'}, axis=1, inplace=True)
    df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
    graph = sales_view_plot(x='date',y='total_price',hue='salesman',df=df)
    context = {
        'graph':graph
    }
    return render(request,'products/sales.html',context)


@login_required
def chart_select_view(request):
    error_message = None
    df=None
    graph = None
    price = None
    try:
        products_df = pd.DataFrame(Product.objects.all().values())
        purchase_df = pd.DataFrame(Purchase.objects.all().values())
        products_df['name_id'] = products_df['id']
    except:
        products_df = None
        purchase_df = None

    if purchase_df is not None:
        if purchase_df.shape[0] > 0:
            df = pd.merge(purchase_df,products_df,how='left',on='name_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)
            price = df['price']
            if request.method == 'POST':
                chart_type = request.POST.get('chart_type')
                date_from = request.POST['date_from']
                date_to = request.POST['date_to']
                
                df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
                df2 = df.groupby('date',as_index=False)['total_price'].agg('sum')
                
                if chart_type != None:
                    if date_from != "" and date_to != "":
                        date_from = datetime.strptime(date_from,"%Y-%m-%d").date().strftime('%d-%m-%Y')
                        date_to = datetime.strptime(date_to,"%Y-%m-%d").date().strftime('%d-%m-%Y')
                        if date_to > date_from:
                            df = df[(df['date']>date_from) & (df['date']<date_to)]
                            df2 = df.groupby('date',as_index=False)['total_price'].agg('sum')
                        else:
                            error_message = "From Date should not be greater than To date"
                    # function to create chart
                    graph = get_simple_plot(chart_type,x=df2['date'], y=df2['total_price'], data=df)
                else:
                    error_message = 'Please select a chart type to continue.'
    else:
        error_message = "No Records in the Database."


    context = {
        # 'products': products_df.to_html(),
        # 'purchase': purchase_df.to_html(),
        'error_message': error_message,
        'graph': graph,
        'price': price,

    }

    return render(request,'products/main.html',context)

# https://djangokatya.wordpress.com/2019/07/05/how-to-clear-post-data/
# How to clear POST data in Django – ‘Confirm Form Resubmission’ // 1-minute guide

@login_required
def add_purchase_view(request):
    
    record_added_message=None
    
    form = PurchaseForm(request.POST or None)
    
    if form.is_valid():
            obj = form.save(commit=False)
            obj.salesman = request.user
            obj.save()
            form = PurchaseForm()
            messages.success(request,'Record Added Successfully')
            return HttpResponseRedirect(request.path)
    else:
        
        form=PurchaseForm()
        record_added_message=None
    context = {
        'form':form,
    }
    return render(request,'products/add.html',context)