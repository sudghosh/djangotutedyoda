from django.shortcuts import render
import pandas as pd
from .models import Product, Purchase
# Create your views here.

def chart_select_view(request):
    products_df = pd.DataFrame(Product.objects.all().values())
    purchase_df = pd.DataFrame(Purchase.objects.all().values())
    products_df['name_id'] = products_df['id']
    merge_df = pd.merge(purchase_df,products_df,how='left',on='name_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)
    context = {
        'products': products_df.to_html(),
        'purchase': purchase_df.to_html(),
        'df': merge_df.to_html(),

    }

    return render(request,'products/main.html',context)