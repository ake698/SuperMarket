from django.db import models


# Create your models here.


class Users(models.Model):
    stateChoice = (
        ('T', '同意登陆'),
        ('F', '拒绝登陆'),
    )
    identityChoice = (
        ('0', "财务"),
        ('1', "入库员"),
        ('2', "收银员")
    )
    id = models.AutoField(primary_key=True, max_length=100, verbose_name="ID")
    username = models.CharField(max_length=50, unique=True, verbose_name="账户")
    password = models.CharField(max_length=16, verbose_name="密码")
    nickname = models.CharField(max_length=30, verbose_name="昵称")
    phone = models.CharField(max_length=11, verbose_name="联系电话")
    state = models.CharField(verbose_name="是否允许登陆", choices=stateChoice, max_length=1, default="T")
    identity = models.CharField(verbose_name="身份", choices=identityChoice, max_length=1, default="2")
    createTime = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "员工管理"
        verbose_name_plural = "员工管理"

#会员管理
class VIP(models.Model):
    id = models.AutoField(primary_key=True, max_length=100, verbose_name="ID")
    nickname = models.CharField(max_length=30, verbose_name="昵称")
    phone = models.CharField(max_length=11, verbose_name="联系电话")
    account = models.FloatField(verbose_name="积分")
    createTime = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "会员管理"
        verbose_name_plural = "会员管理"

#供货商
class Supplier(models.Model):
    id = models.AutoField(primary_key=True, max_length=100, verbose_name="ID")
    name = models.CharField(max_length=20, verbose_name="供应商名称")
    phone = models.CharField(max_length=11, verbose_name="联系电话")
    address = models.CharField(max_length=20, verbose_name="供应商地址")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "供应商管理"
        verbose_name_plural = "供应商管理"


# 商品表
class Goods(models.Model):
    stateChoice = (
        ('T', '上架'),
        ('F', '下架'),
    )
    id = models.AutoField(primary_key=True, max_length=100, verbose_name="ID")
    name = models.CharField(max_length=20, verbose_name="商品名称")
    # img = models.ImageField(upload_to='goods/',default="author/default.jpg",blank=True,verbose_name="商品图片")
    sale_price = models.FloatField(verbose_name="出售价格")  # 出售价格
    left_num = models.IntegerField(default=0, verbose_name="商品数量")  # 剩余数量
    cost_price = models.FloatField(default=0, verbose_name="进货单价")  # 进货价格
    # sale_num = models.IntegerField(default=0,null=True,verbose_name="商品已卖出数量")        # 出售数量
    unit = models.CharField(max_length=5, default="个", verbose_name="单位")
    flag = models.CharField(verbose_name="是否上架", choices=stateChoice, max_length=1, default="F")
    margin = models.FloatField(verbose_name="利润率%",default=20,max_length=4)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None,ignore=True):
        if ignore:
            goods_price = round(self.cost_price * (1 + self.margin / 100),2)
            self.sale_price = goods_price
        # self.save()
        super(Goods,self).save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商品管理"
        verbose_name_plural = "商品管理"


# 商品进货记录 Record
class Purchase(models.Model):
    id = models.AutoField(primary_key=True, max_length=100, verbose_name="ID")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    goods_price = models.FloatField(default=0, verbose_name="进货单价")  # 进货价格
    purchase_num = models.IntegerField(default=0, verbose_name="进货数量")  # 进货数量
    sum_price = models.FloatField(verbose_name="总价格")

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = "商品管理"
        verbose_name_plural = "商品管理"



# 进货单
class Purchase_Record(models.Model):
    stateChoice = (
        ('1', '已通过审核'),
        ('2', '暂未审核'),
        ('3', '拒绝'),
    )
    id = models.AutoField(primary_key=True, max_length=100, verbose_name="ID")
    purchases = models.ManyToManyField(Purchase, verbose_name="进货记录", null=True, blank=True)
    sum_price = models.FloatField(verbose_name="总价格", default=0)
    purchaser = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="purchaser", verbose_name="进货人")
    Auditor = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="审核人", null=True, blank=True)
    state = models.CharField(verbose_name="状态", choices=stateChoice, max_length=1, default="2")
    isSubmit = models.BooleanField(verbose_name="是否提交", default=False)
    createTime = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE,verbose_name="进货厂商",default="1")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "进货管理"
        verbose_name_plural = "进货管理"
        ordering = ["-id"]

#退货记录
class Return_Record(models.Model):
    id = models.AutoField(primary_key=True, max_length=100, verbose_name="ID")
    returner = models.ForeignKey(Users, on_delete=models.CASCADE,related_name="returner",verbose_name="退货人")
    Auditor = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="审核人", null=True, blank=True)
    sum_price = models.FloatField(verbose_name="总价格")
    goods = models.CharField(max_length=200,verbose_name="退货商品")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "退货管理"
        verbose_name_plural = "退货管理"
        ordering = ["-id"]


# 商品出售记录 Record
class Sale(models.Model):
    id = models.AutoField(primary_key=True, max_length=100, verbose_name="ID")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    sale_num = models.IntegerField(default=0, verbose_name="销售数量")  # 出售数量
    profile = models.FloatField(default=0, verbose_name="销售利润")  # 利润
    sum_price = models.FloatField(verbose_name="总价格")

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = "销售记录管理"
        verbose_name_plural = "销售记录管理"


# 出售单
class Order(models.Model):
    id = models.AutoField(primary_key=True, max_length=100, verbose_name="ID")
    sales = models.ManyToManyField(Sale, verbose_name="销售记录", null=True)
    sum_price = models.FloatField(verbose_name="总价格", default=0)
    in_money = models.FloatField(verbose_name="收钱", default=0)
    out_money = models.FloatField(verbose_name="找零", default=0)
    good_count = models.IntegerField(verbose_name="订单商品数量", default=0)
    profile = models.FloatField(verbose_name="利润", default=0)
    saler = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="售货员")
    createTime = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "订单管理"
        verbose_name_plural = "订单管理"
        ordering = ["-id"]


#操作历史
class History(models.Model):
    id = models.AutoField(primary_key=True, max_length=100, verbose_name="ID")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="操作人", null=True, blank=True)
    action = models.CharField(verbose_name="操作记录", max_length=200, default="-")
    createTime = models.DateTimeField(auto_now=True, verbose_name="操作时间")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "操作日志"
        verbose_name_plural = "操作日志"
        ordering = ["-id"]