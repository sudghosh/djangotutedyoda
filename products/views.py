from django.shortcuts import render
from datetime import datetime
import pandas as pd
from .models import Product, Purchase
from .utils import get_simple_plot
# Create your views here.

def chart_select_view(request):
    error_message = None
    df=None
    graph = None
    products_df = pd.DataFrame(Product.objects.all().values())
    purchase_df = pd.DataFrame(Purchase.objects.all().values())
    products_df['name_id'] = products_df['id']
    

    if purchase_df.shape[0] > 0:
        df = pd.merge(purchase_df,products_df,how='left',on='name_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)
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

    }

    return render(request,'products/main.html',context)