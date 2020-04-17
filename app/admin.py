from django.contrib import admin
from app.models import *
# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = ("id","username","password","nickname","state","createTime",)
    list_editable = ("state",)

class GoodsAdmin(admin.ModelAdmin):
    list_display = ("id","name","sale_price","left_num","cost_price","margin","unit","flag")
    list_editable = ("flag",)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id","sum_price","purchaser","Auditor","state","createTime","supplier")

    def get_queryset(self, request):
        qs = super(PurchaseAdmin,self).get_queryset(request)
        return qs.filter(isSubmit=True)

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","sum_price","in_money","out_money","good_count","profile","saler","createTime")

class HistoryAdmin(admin.ModelAdmin):
    list_display = ("id","user","action","createTime")

class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id","name","phone","address")

class VIPAdmin(admin.ModelAdmin):
    list_display = ("id","nickname","phone","account","createTime")

admin.site.register(Users,UsersAdmin)
admin.site.register(Goods,GoodsAdmin)
admin.site.register(Purchase_Record,PurchaseAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(History,HistoryAdmin)
admin.site.register(Supplier,SupplierAdmin)
admin.site.register(VIP,VIPAdmin)
admin.site.site_title = "超市系统管理后台"
admin.site.site_header = "超市系统管理后台"