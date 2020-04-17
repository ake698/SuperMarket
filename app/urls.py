"""SuperMarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import app.views as v
urlpatterns = [
    path("goods/",v.goods),
    path("history/",v.history_page),
    path("get_vip/",v.get_VIP),
    #########销售相关
    path("sale/",v.sale),
    path("goodinfo/",v.goodinfo),
    path("order/",v.order),
    ################库存管理相关
    path("purchase/",v.addGoodCount),
    path("existpurchase/",v.exist_purchase),
    path("purchaselist/",v.purchaseList),
    path("purchase_submit/",v.purchase_submit),
    path("addpurchase/",v.addPurchase),
    path("purchase_delete/",v.deletePurchaseGood),
    path("add_return/",v.addreturn),
    path("return_page/",v.return_page),
    #####################财务相关
    path("purchase_record_action/",v.purchase_record_action),
    path("return_record_action/",v.return_record_action),
    path("dashboard/",v.dashboard),
    path("dashboardym/",v.dashboard_ym),
    path("pr_dashboard/",v.pr_dashboard),
    path("dashboardym/",v.dashboard_ym),
    path("supplier/",v.supplier),
    path("",v.goods),
]
