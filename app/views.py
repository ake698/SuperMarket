from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app.libs.identity_check import check
from app.libs.initJson import initJson
from app.models import *
import json, time
from datetime import datetime, timedelta
# Create your views here.



# 返回验证码
from app.models import Users


# 获取当前用户
def get_user(request):
    id = request.session.get("id")
    user = Users.objects.get(id=int(id))
    return user


def get_code(request):
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random, os
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
            20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    # 构造字体对象
    ttrFile = os.path.join(os.path.dirname(__file__), 'kt.ttf')
    font = ImageFont.truetype(ttrFile, 40)
    # 构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# 登陆
def user_login(request):
    if request.method == 'POST':
        username = request.POST['userName']
        passwd = request.POST['passWord']
        j_captcha = request.POST['j_captcha'].upper()
        code = request.session.get('verifycode').upper()
        errJson = initJson(success=False)
        if code != j_captcha:
            errJson['detail'] = "验证码错误"
            return HttpResponse(json.dumps(errJson), content_type="application/json")

        user = Users.objects.filter(username=username, password=passwd)
        if user:
            if user.first().state != "T":
                errJson['detail'] = "禁止登陆！"
                return HttpResponse(json.dumps(errJson), content_type="application/json")
            request.session["id"] = user.first().id
            request.session["userName"] = username
            request.session["nickName"] = user.first().nickname
            request.session['identity'] = user.first().identity
            response = HttpResponse(json.dumps(initJson()), content_type="application/json")
            #########添加操作历史
            add_history(user.first(), "登陆操作")
            return response
        else:
            errJson['detail'] = "账号或者密码错误"
            return HttpResponse(json.dumps(errJson), content_type="application/json")

    return render(request, 'login.html')


# 用户注销
@check([0, 1, 2])
def logout(request):
    #########添加操作历史
    add_history(get_user(request), "退出登陆")
    request.session.flush()
    response = HttpResponse("注销成功")
    response.delete_cookie("username")
    response['Refresh'] = "2;/"
    return response


@check([0, 1, 2])
# 操作历史展示
def history_page(request):
    id = request.GET.get("Search")
    user = get_user(request)
    history = History.objects.filter(user=user)
    if id:
        history = history.filter(id=int(id))
    return render(request, 'manage/hisotry.html', {"history": history})


@check([0, 1, 2])
# 商品列表
def goods(request):
    goods = Goods.objects.filter(flag="T")
    key = request.GET.get("Search")
    if key:
        goods = goods.filter(id=int(key))
    # 商品提醒
    flag = goods.filter(left_num__lt=5)
    msg = ""
    if flag:
        goods_tip = ""
        for i in flag:
            goods_tip = i.name + " "
        msg = "商品:%s,不足，请及时补充！" % goods_tip
        flag = True
    return render(request, 'manage/goods.html', {"goods": goods, "msg": msg, "flag": flag})


#获取单个VIP信息
def get_VIP(request):
    if request.method == "POST":
        phone = request.POST['phone']
        Vip = VIP.objects.filter(phone=phone)
        if Vip:
            vip = Vip.first()
            result = initJson()
            result['detail'] = {
                "id":vip.id,
                "phone": vip.phone,
                "name": vip.nickname,
                "account": vip.account,
            }
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            return HttpResponse(json.dumps(initJson(success=False)), content_type="application/json")

@check([0,1])
#供货商列表
def supplier(request):
    supplier = Supplier.objects.all()
    key = request.GET.get("Search")
    if key:
        supplier = supplier.filter(id=int(key))
    return render(request, 'manage/supplier.html', {"supplier": supplier,})

@check([0,1])
#所有退货单
def return_page(request):
    user = get_user(request)
    returns = Return_Record.objects.all()
    if user.identity == "1":
        returns = returns.filter(returner=user)
    key = request.GET.get("Search")
    if key:
        returns = returns.filter(id=int(key))
    return render(request,'manage/return_page.html',{"returns":returns})


########################销售相关#########################

# 获取单个商品信息
def goodinfo(request):
    if request.method == "POST":
        goodid = request.POST['key']
        good = Goods.objects.filter(id=goodid)
        if good and good.first().flag == "T":
            good = good.first()
            result = initJson()
            result['detail'] = {
                "pk": good.id,
                "name": good.name,
                "left": good.left_num,
                "price": good.sale_price,
                "cost":good.cost_price
            }
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            return HttpResponse(json.dumps(initJson(success=False)), content_type="application/json")


# 销售台
@check([2])
def sale(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        # 获取商品信息
        goods = data["goods"]
        money = float(data["money"])
        vipid = int(data["vipid"])
        # 订单应收
        sum_price = 0.00
        # 订单总利润
        sum_profile = 0
        # 订单总商品数量
        good_count = 0
        user = get_user(request)
        order = Order.objects.create(saler=user, in_money=money)
        for i in goods:
            good_info = i.split("-")
            good = Goods.objects.get(id=int(good_info[0]))
            # 此商品的价钱
            price = good.sale_price * int(good_info[1])
            # print(price)
            # 此商品利润计算
            profile = price - good.cost_price * int(good_info[1])
            # print(profile)
            sale = Sale.objects.create(goods=good, sale_num=int(good_info[1])
                                       , sum_price=price, profile=profile)
            sum_price += price
            sum_profile += profile
            good_count += int(good_info[1])
            order.sales.add(sale)
            # 扣除商品数量
            good.left_num = good.left_num - int(good_info[1])
            good.save()
        ####################添加积分
        vip = VIP.objects.filter(id=int(vipid))
        if vip:
            vip = vip.first()
            vip.account += sum_price
            vip.save()
            order.vip = vip
        # 添加销售记录
        order.sum_price = sum_price
        order.out_money = money - sum_price
        order.profile = round(sum_profile,2)
        order.good_count = good_count
        order.save()

        #####################添加销售记录操作
        add_history(user, "新建销售订单，订单号为%s，金额为：%s" % (order.id, order.sum_price))
        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    return render(request, 'manage/sale.html')


# 只有财务和销售能看到历史订单
@check([0, 2])
def order(requset):
    user = get_user(requset)
    order = Order.objects.all()
    print(user.identity)
    if user.identity == "0":
        # 财务可看所有
        pass
    else:
        # 为销售  只能看自己销售的订单
        order = order.filter(saler=user)
    return render(requset, 'manage/order.html', {"order": order})


########################入库相关#################################

@check([1])
# 在没提交之前删除进货单中的商品
def deletePurchaseGood(request):
    id = request.GET.get("id")
    if id:
        Purchase.objects.get(id=int(id)).delete()

        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    return HttpResponse(json.dumps(initJson(success=False)), content_type="application/json")


@check([1])
# 进货新商品
def addGoodCount(request):
    if request.method == "POST":
        good_name = request.POST['good_name']
        good_cost_price = float(request.POST['good_cost_price'])
        #利润率
        good_margin = float(request.POST['good_sale_price'])
        good_num = request.POST['good_num']
        good_unit = request.POST['good_unit']
        # 新建商品
        good = Goods.objects.create(name=good_name, cost_price=good_cost_price,
                                    unit=good_unit,margin=good_margin)
        #########添加记录
        user = get_user(request)
        add_history(user, "添加新的商品%s" % good.name)
        # 新建单个商品进货记录
        price = int(good_num) * good_cost_price
        good_purchase = Purchase.objects.create(goods=good, purchase_num=good_num, sum_price=price,goods_price=good_cost_price)
        # 添加至进货记录表
        if not request.session.get("purchase"):
            user = get_user(request)
            PR = purchase = Purchase_Record.objects.create(purchaser=user)
            request.session["purchase"] = purchase.id
        else:
            PR = Purchase_Record.objects.get(id=int(request.session["purchase"]))
        PR.purchases.add(good_purchase)
        PR.save()
        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    # 为新获入库
    return render(request, 'manage/purchase.html')


@check([1])
# 为已存在的商品补货
def exist_purchase(request):
    if request.method == "POST":
        good_id = request.POST['good_id']
        good_num = request.POST['good_num']
        good_cost_price = float(request.POST['good_cost_price'])
        good = Goods.objects.get(id=int(good_id))
        # 新建单个商品进货记录
        sum_price = int(good_num) * float(good_cost_price)
        # print("此商品进价额度：%s"%sum_price)
        good_purchase = Purchase.objects.create(goods=good, purchase_num=good_num,goods_price = good_cost_price,
                                                sum_price=sum_price)
        if not request.session.get("purchase"):
            user = get_user(request)
            PR = purchase = Purchase_Record.objects.create(purchaser=user)
            request.session["purchase"] = purchase.id
        else:
            PR = Purchase_Record.objects.get(id=int(request.session["purchase"]))
        PR.purchases.add(good_purchase)
        # PR.sum_price = PR.sum_price + good_purchase.sum_price
        PR.save()
        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    try:
        type = request.GET["type"]
        goodId = request.GET['id']
    except:
        type = ""
    if type == "1":
        good = Goods.objects.get(id=int(goodId))
        # 为补货
        return render(request, 'manage/exitstpurchase.html', {"good": good})
    return redirect("/goods/")


@check([1])
# 提交订货单
def purchase_submit(request):

    id = request.session.get("purchase")
    PR = Purchase_Record.objects.get(id=int(id))
    if PR.purchases.count() < 1:
        result = initJson(success=False)
        result["detail"] = "无进货商品，不可提交"
        return HttpResponse(json.dumps(result), content_type="application/json")
    PR.isSubmit = True
    price = 0
    count = 0
    for i in PR.purchases.all():
        price += i.sum_price
        count += i.purchase_num
    # print("最终进货价：%s" % price)
    PR.sum_price = price
    PR.good_count = count
    #供应商
    supplier_id = request.GET.get("supplier")
    PR.supplier = Supplier.objects.get(id=int(supplier_id))
    PR.save()
    #######添加进货单
    add_history(get_user(request), "添加进货单(待审核),ID:%s，金额为：%s" % (PR.id, PR.sum_price))
    del request.session["purchase"]
    return HttpResponse(json.dumps(initJson()), content_type="application/json")


# 进货单子  权限 0，1 销售不可看
@check([0, 1])
def purchaseList(requset):
    user = get_user(requset)
    list = Purchase_Record.objects.filter(isSubmit=True)
    if user.identity == 1:
        list = list.filter(purchaser=user)
    return render(requset, 'manage/purchaseList.html', {"list": list})


@check([1])
# 新建进货单子  权限 1 只允许采购查看
def addPurchase(request):
    user = get_user(request)
    purchaseId = request.session.get("purchase")
    if purchaseId:
        purchase = Purchase_Record.objects.get(id=int(purchaseId))
    else:
        purchase = Purchase_Record.objects.create(purchaser=user)
        request.session["purchase"] = purchase.id
    supplier = Supplier.objects.all()
    return render(request, 'manage/addpurchase.html', {"purchase": purchase,"supplier":supplier})


@check([1])
#新加退货单
def addreturn(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        # 获取商品信息
        goods = data["goods"]
        # 订单价格
        sum_price = 0.00
        #商品id和数量
        goods_id_num = ""
        #商品所有信息
        goods_all = ""
        user = get_user(request)
        for i in goods:
            good_info = i.split("-")
            good = Goods.objects.get(id=int(good_info[0]))
            price = good.cost_price * int(good_info[1])
            #价钱
            sum_price += price
            #商品id和数量
            goods_id_num += "%s,"%i
            #商品所有信息
            goods_all += "%s*%s"%(good.name,good_info[1])
        #添加退货记录
        Return_Record.objects.create(returner=user, sum_price=sum_price, goods=goods_all, goods_id_num=goods_id_num)
        #####添加操作记录
        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    return render(request, "manage/addreturn.html")
################################################################################财务功能

@check([0])
# 对进货单的审核
def purchase_record_action(requset):
    try:
        id = requset.GET["id"]
        type = requset.GET["type"]
    except:
        return HttpResponse(json.dumps(initJson(success=False)), content_type="application/json")
    PR = Purchase_Record.objects.get(id=int(id))
    if type == "permit":
        PR.state = 1
    else:
        PR.state = 3
        PR.Auditor = get_user(requset)
        PR.save()
        #####################
        add_history(PR.Auditor, "拒绝进货单%s,金额为%s" % (PR.id, PR.sum_price))
        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    PR.Auditor = get_user(requset)
    PR.save()
    add_history(PR.Auditor, "通过进货单%s,金额为%s" % (PR.id, PR.sum_price))
    # 更新库存
    for i in PR.purchases.all():
        #重新估算进货价和售价
        cost = i.goods.left_num * i.goods.cost_price
        new_cost = i.purchase_num * i.goods_price
        last_cost = (cost + new_cost) * (1 + i.goods.margin / 100)
        sale_price = last_cost / (i.purchase_num + i.goods.left_num)
        i.goods.sale_price = round(sale_price,2)
        #商品入库上架
        i.goods.left_num = i.purchase_num + i.goods.left_num
        i.goods.flag = "T"
        # 商品审核通过
        add_history(PR.Auditor, "进货单%s审核通过，商品%s增加%s" % (PR.id, i.goods.name, i.purchase_num))
        i.goods.save(ignore=False)
    return HttpResponse(json.dumps(initJson()), content_type="application/json")

@check([0])
# 对退货单的审核
def return_record_action(requset):
    try:
        id = requset.GET["id"]
        type = requset.GET["type"]
    except:
        return HttpResponse(json.dumps(initJson(success=False)), content_type="application/json")
    RR = Return_Record.objects.get(id=int(id))
    if type == "permit":
        RR.state = 1
    else:
        RR.state = 3
        RR.Auditor = get_user(requset)
        RR.save()
        #####################
        add_history(RR.Auditor, "拒绝退货单%s,金额为%s" % (RR.id, RR.sum_price))
        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    RR.Auditor = get_user(requset)
    RR.state = "1"
    RR.save()
    add_history(RR.Auditor, "通过退货单%s,金额为%s" % (RR.id, RR.sum_price))
    # 更新库存
    goods_info = str(RR.goods_id_num).split(",")
    for i in goods_info:
        if i=="":
            continue
        id_num = i.split("-")
        id = int(id_num[0])
        num = int(id_num[1])
        #商品扣除
        good = Goods.objects.get(id=int(id))
        good.left_num -= num
        good.save(ignore=False)
    return HttpResponse(json.dumps(initJson()), content_type="application/json")

@check([0])
# 单天销售额
def dashboard(request):
    date = request.GET.get("date")
    return_date = date
    if date:
        # print(date)
        date = datetime.strptime(date, "%Y-%m-%d")
        order = Order.objects.filter(createTime__date=date)
    else:
        now = datetime.now()
        date = now.date()
        order = Order.objects.filter(createTime__date=date)
    # print(order)
    sum = get_Sum(order)
    sum_price = sum[0]
    sum_profile = round(sum[1], 2)
    good_count = sum[2]

    sale_list = []
    date_list = []
    for i in range(0, 7).__reversed__():
        d_date = date - timedelta(days=i)
        day_order = Order.objects.filter(createTime__date=d_date)
        d_sum = get_Sum(day_order)
        sale_list.append(d_sum[0])
        date_list.append(d_date.strftime("%Y-%m-%d"))

    return render(request, 'manage/dashboard.html', {"order": order,"date":return_date,
                                                     "sum_price": sum_price, "sum_profile": sum_profile,
                                                     "good_count": good_count,
                                                     "sale_list": sale_list, "date_list": date_list})

# 单天进货统计
def pr_dashboard(request):
    date = request.GET.get("date")
    return_date = date
    if date:
        # print(date)
        date = datetime.strptime(date, "%Y-%m-%d")
        PR = Purchase_Record.objects.filter(createTime__date=date).filter(state="1")
    else:
        now = datetime.now()
        date = now.date()
        PR = Purchase_Record.objects.filter(createTime__date=date).filter(state="1")
    # print(order)
    sum = get_Sum2(PR)
    sum_price = sum[0]
    good_count = sum[1]

    purchase_list = []
    date_list = []
    for i in range(0, 7).__reversed__():
        d_date = date - timedelta(days=i)
        day_PR = Purchase_Record.objects.filter(createTime__date=d_date).filter(state="1")
        d_sum = get_Sum2(day_PR)
        purchase_list.append(d_sum[0])
        date_list.append(d_date.strftime("%Y-%m-%d"))
    sc = Supplier.objects.count()

    return render(request, 'manage/PRdashboard.html', {"PR": PR,"date":return_date,
                                                     "sum_price": sum_price, "sc": sc,
                                                     "good_count": good_count,
                                                     "purchase_list": purchase_list, "date_list": date_list})


@check([0])
# 年月销售统计
def dashboard_ym(request):
    year = request.GET.get("year")
    month = request.GET.get("month")
    now = datetime.now()
    date_list, sale_list = [], []
    return_date = "%s" % year
    if not year or year == "":
        year = now.year
        return_date = "%s" % now.year
    order = Order.objects.filter(createTime__year=int(year))

    if month and month != "":
        return_date += "-" + str(month)
        order = order.filter(createTime__month=int(month))
        for i in range(int(month) - 3, int(month) + 1):
            date_list.append("%s-%s" % (year, i))
            temp_order = Order.objects.filter(createTime__month=i).filter(createTime__year=year)
            d_sum = get_Sum(temp_order)
            sale_list.append(d_sum[0])
    else:
        for i in range(int(year) - 3, int(year) + 1):
            date_list.append(i)
            temp_order = Order.objects.filter(createTime__year=i)
            d_sum = get_Sum(temp_order)
            sale_list.append(d_sum[0])
    sum = get_Sum(order)
    sum_price = sum[0]
    sum_profile = round(sum[1], 2)
    good_count = sum[2]
    return render(request, 'manage/dashboardym.html', {"order": order,
                                                       "sum_price": sum_price, "sum_profile": sum_profile,
                                                       "good_count": good_count, "date": return_date,
                                                       "sale_list": sale_list, "date_list": date_list})

@check([0])
# 年月进货统计
def pr_dashboard_ym(request):
    year = request.GET.get("year")
    month = request.GET.get("month")
    now = datetime.now()
    date_list, purchase_list = [], []
    return_date = "%s" % year
    if not year or year == "":
        year = now.year
        return_date = "%s" % now.year
    PR = Purchase_Record.objects.filter(createTime__year=int(year))

    if month and month != "":
        return_date += "-" + str(month)
        PR = PR.filter(createTime__month=int(month))
        for i in range(int(month) - 3, int(month) + 1):
            date_list.append("%s-%s" % (year, i))
            temp_PR = Purchase_Record.objects.filter(createTime__month=i).filter(createTime__year=year)
            d_sum = get_Sum2(temp_PR)
            purchase_list.append(d_sum[0])
    else:
        for i in range(int(year) - 3, int(year) + 1):
            date_list.append(i)
            temp_PR = Purchase_Record.objects.filter(createTime__year=i)
            d_sum = get_Sum2(temp_PR)
            purchase_list.append(d_sum[0])
    sum = get_Sum2(PR)
    sum_price = sum[0]
    # sum_profile = round(sum[1], 2)
    good_count = sum[1]
    sc = Supplier.objects.count()
    return render(request, 'manage/PRdashboardym.html', {"PR": PR,
                                                       "sum_price": sum_price, "sc": sc,
                                                       "good_count": good_count, "date": return_date,
                                                       "purchase_list": purchase_list, "date_list": date_list})



# 获取销售额度
def get_Sum(order):
    money = 0
    profile = 0
    count = 0
    for i in order:
        money += i.sum_price
        profile += i.profile
        count += i.good_count
    return [money, profile, count]

# 获取进货额度
def get_Sum2(PR):
    money = 0
    count = 0
    for i in PR:
        money += i.sum_price
        count += i.good_count
    return [money, count]

# 记录操作历史
def add_history(user, action):
    History.objects.create(user=user, action=action)
