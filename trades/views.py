import nltk
import numpy as np
from bs4 import BeautifulSoup
from django.db.models.functions import Lower
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.db.models import Max, Sum, Count

import pandas as pd
import trades.models as models
import json
import datetime


# request.GET["name"]
def index(request):
    file_path = 'templates/trades/index.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()
    return HttpResponse(txt)
    # return render(request, 'trades/index.html')


def add_center(request):
    name = request.GET['name']
    if name is None or len(name) > 100:
        s = 'failed insertion!'
    else:
        center_add_fast(name)
        s = 'successful insertion!'
    return HttpResponse(ans(True, False, s, {}).answer)


def center_add_fast(name):
    models.Center(name=name, profit=0).save()


def delete_center(request):
    name = request.GET['name']
    if name is None:
        s = 'failed deletion!'
    else:
        center = models.Center.objects.filter(name=name)
        if center.exists():
            center.delete()
            s = 'successful deletion!'
        else:
            s = 'no such center!'
    return HttpResponse(ans(True, False, s, {}).answer)


def center_delete_fast(name):
    center = models.Center.objects.filter(name=name)
    if center.exists():
        center.delete()


def add_enterprise(request):
    name = request.GET['name']
    country = request.GET['country']
    city = request.GET['city']
    supply_center = request.GET['supply_center']
    industry = request.GET['industry']
    if name is None or country is None or supply_center is None or industry is None or len(name) > 100 or len(
            country) > 100 or len(city) > 100 or len(industry) > 100 or not models.Center.objects.filter(
        name=supply_center).exists():
        s = 'failed insertion!'
    else:
        enterprise_add_fast(name, country, city, supply_center, industry)
        s = 'successful insertion!'
    return HttpResponse(ans(True, False, s, {}).answer)


def enterprise_add_fast(name, country, city, center, industry):
    center = models.Center.objects.get(name=center)
    models.Enterprise(name=name, country=country, city=city, supply_center=center, industry=industry).save()


def delete_enterprise(request):
    name = request.GET['name']
    if name is None:
        s = 'failed deletion!'
    else:
        enterprise = models.Enterprise.objects.filter(name=name)
        if enterprise.exists():
            enterprise.delete()
            s = 'successful deletion!'
        else:
            s = 'no such enterprise!'
    return HttpResponse(ans(True, False, s, {}).answer)


def enterprise_delete_fast(name):
    enterprise = models.Enterprise.objects.filter(name=name)
    if enterprise.exists():
        enterprise.delete()


def add_models(request):
    number = request.GET['number']
    model = request.GET['model']
    name = request.GET['name']
    unit_price = request.GET['unit_price']
    if name is None or model is None or number is None or unit_price is None or len(name) > 100 or len(
            model) > 100 or len(number) > 10 or int(unit_price) < 0:
        s = 'failed insertion!'
    else:
        models_add_fast(number, model, name, unit_price)
        s = 'successful insertion!'
    return HttpResponse(ans(True, False, s, {}).answer)


def models_add_fast(number, model, name, unit_price):
    models.Models(number=number, model=model, name=name, unit_price=int(unit_price)).save()


def delete_models(request):
    model = request.GET['number']
    if model is None:
        s = 'failed deletion!'
    else:
        model = models.Models.objects.filter(model=model)
        if model.exists():
            model.delete()
            s = 'successful deletion!'
        else:
            s = 'no such model!'
    return HttpResponse(ans(True, False, s, {}).answer)


def models_delete_fast(model):
    model = models.Models.objects.filter(model=model)
    if model.exists():
        model.delete()


def add_staff(request):
    name = request.GET['name']
    age = request.GET['age']
    gender = request.GET['gender']
    number = request.GET['number']
    supply_center = request.GET['supply_center']
    mobile_phone = request.GET['mobile_phone']
    type = request.GET['type']
    if name is None or age is None or gender is None or number is None or supply_center is None or mobile_phone is None or type is None or len(
            name) > 50 or len(
        gender) > 10 or len(number) > 10 or int(age) < 0 or len(mobile_phone) > 20 or len(
        type) > 20 or not models.Center.objects.filter(
        name=supply_center).exists():
        s = 'failed insertion!'
    else:
        staff_add_fast(supply_center, name, age, gender, number, mobile_phone, type)
        s = 'successful insertion!'
    return HttpResponse(ans(True, False, s, {}).answer)


def staff_add_fast(supply_center, name, age, gender, number, mobile_phone, type):
    center = models.Center.objects.get(name=supply_center)
    models.Staff(name=name, age=int(age), gender=gender, number=number, supply_center=center,
                 mobile_number=mobile_phone, type=type).save()


def alter_enterprise_info(request):
    name = request.GET['name']
    country = request.GET['country']
    city = request.GET['city']
    industry = request.GET['industry']
    enterprise = models.Enterprise.objects.filter(name=name)
    if not enterprise.exists():
        s = 'no such enterprise!'
    else:
        enterprise.update(country=country, city=city, industry=industry)
        s = 'successful change!'
    return HttpResponse(ans(True, False, s, {}).answer)


def alter_models_info(request):
    name = request.GET['name']
    number = request.GET['number']
    model = request.GET['model']
    unit_price = request.GET['unit_price']
    Model = models.Models.objects.filter(model=model)
    if not Model.exists():
        s = 'no such model!'
    else:
        Model.update(number=number, name=name, unit_price=int(unit_price))
        s = 'successful change!'
    return HttpResponse(ans(True, False, s, {}).answer)


def delete_staff(request):
    number = request.GET['number']
    if number is None:
        s = 'failed deletion!'
    else:
        staff = models.Staff.objects.filter(number=number)
        if staff.exists():
            staff.delete()
            s = 'successful deletion!'
        else:
            s = 'no such staff!'
    return HttpResponse(ans(True, False, s, {}).answer)


def alter_staff_info(request):
    name = request.GET['name']
    age = request.GET['age']
    gender = request.GET['gender']
    number = request.GET['number']
    supply_center = request.GET['supply_center']
    mobile_phone = request.GET['mobile_phone']
    type = request.GET['type']
    staff = models.Staff.objects.filter(number=number)
    if not staff.exists():
        s = 'no such staff!'
    else:
        center = models.Center.objects.get(name=supply_center)
        staff.update(name=name, age=int(age), gender=gender,
                     supply_center=center, mobile_number=mobile_phone,
                     type=type)
        s = 'successful change!'
    return HttpResponse(ans(True, False, s, {}).answer)


def select_center_info(request):
    name = request.GET['name']
    table = {}
    if name is None:
        s = 'wrong input!'
    else:
        center = models.Center.objects.filter(name=name)
        if not center.exists():
            s = 'no such center!'
        else:
            s = "let's show them below!"
            table['col_names'] = ['name', 'profit']
            table['rows'] = []
            for cen in center:
                temp = []
                temp.append(cen.name)
                temp.append(str(cen.profit))
                table['rows'].append(temp)
    return HttpResponse(ans(True, True, s, table).answer)


def select_enterprise_info(request):
    name = request.GET['name']
    country = request.GET['country']
    city = request.GET['city']
    supply_center = request.GET['supply_center']
    industry = request.GET['industry']
    table = {}
    enterprise = models.Enterprise.objects.all()
    if supply_center != '':
        center = models.Center.objects.filter(name=supply_center)
        if center.exists():
            enterprise = enterprise.filter(supply_center=center)
    if name != '':
        enterprise = enterprise.filter(name=name)
    if country != '':
        enterprise = enterprise.filter(country=country)
    if city != '':
        enterprise = enterprise.filter(city=city)
    if industry != '':
        enterprise = enterprise.filter(industry=industry)

    s = "let's show them below!"
    table['col_names'] = ['name', 'country', 'city', 'supply_center', 'industry']
    table['rows'] = []
    for cen in enterprise:
        temp = []
        temp.append(cen.name)
        temp.append(cen.country)
        temp.append(cen.city)
        temp.append(cen.supply_center.name)
        temp.append(cen.industry)
        table['rows'].append(temp)
    return HttpResponse(ans(True, True, s, table).answer)


def select_model_info(request):
    number = request.GET['number']
    model = request.GET["model"]
    name = request.GET['name']
    unit_price = request.GET['unit_price']
    table = {}
    modelss = models.Models.objects.all()
    if name != '':
        modelss = modelss.filter(name=name)
    if model != '':
        modelss = modelss.filter(model=model)
    if number != '':
        modelss = modelss.filter(number=number)
    if unit_price != '':
        modelss = modelss.filter(unit_price=int(unit_price))

    s = "let's show them below!"
    table['col_names'] = ['number', 'model', 'name', 'unit_price', 'sales_volume']
    table['rows'] = []
    for cen in modelss:
        temp = []
        temp.append(cen.number)
        temp.append(cen.model)
        temp.append(cen.name)
        temp.append(str(cen.unit_price))
        temp.append(str(cen.sales_volume))
        table['rows'].append(temp)
    return HttpResponse(ans(True, True, s, table).answer)


def select_staff_info(request):
    name = request.GET['name']
    age = request.GET['age']
    gender = request.GET['gender']
    number = request.GET['number']
    supply_center = request.GET['supply_center']
    mobile_number = request.GET['mobile_number']
    type = request.GET['type']
    table = {}
    staff = models.Staff.objects.all()
    if supply_center != '':
        center = models.Center.objects.filter(name=supply_center)
        if center.exists():
            staff = staff.filter(supply_center=center)
    if name != '':
        staff = staff.filter(name=name)
    if age != '':
        staff = staff.filter(age=int(age))
    if gender != '':
        staff = staff.filter(gender=gender)
    if number != '':
        staff = staff.filter(number=number)
    if mobile_number != '':
        staff = staff.filter(mobile_number=mobile_number)
    if type != '':
        staff = staff.filter(type=type)

    s = "let's show them below!"
    table['col_names'] = ['name', 'age', 'gender', 'number', 'supply_center', 'mobile_number', 'type']
    table['rows'] = []
    for cen in staff:
        temp = []
        temp.append(cen.name)
        temp.append(int(cen.age))
        temp.append(cen.gender)
        temp.append(cen.number)
        temp.append(cen.supply_center.name)
        temp.append(cen.mobile_number)
        temp.append(cen.type)
        table['rows'].append(temp)
    return HttpResponse(ans(True, True, s, table).answer)


def stockIn(request):
    supply_center = request.GET['supply_center']
    product_model = request.GET['product_model']
    supply_staff = request.GET['supply_staff']
    date = request.GET['date']
    purchase_price = request.GET['purchase_prise']
    quantity = request.GET['quantity']
    staff = models.Staff.objects.filter(number=supply_staff)
    model = models.Models.objects.filter(
        model=product_model)
    if staff.exists() and model.exists():
        s = 'failure!'
        staff = staff[0]
        if staff.supply_center.name == supply_center and staff.type == 'Supply Staff':
            s = 'success!'
            mc = models.Model_center.objects.get(model=model[0], center=staff.supply_center)
            quantity = int(quantity) + mc.quantity
            mc.update(quantity=quantity)
            purchase_price = -int(purchase_price) + staff.supply_center.profit
            staff.supply_center.update(profit=purchase_price)
    else:
        s = 'failure!'
    return HttpResponse(ans(True, False, s, {}).answer)


def quick_stock_in(supply_center, product_model, supply_staff, date, purchase_price, quantity):
    staff = models.Staff.objects.filter(number=supply_staff)
    model = models.Models.objects.filter(
        model=product_model)

    if staff.exists() and model.exists():
        staff = staff[0]
        if staff.supply_center.name == supply_center and staff.type == 'Supply Staff':
            mc = models.Model_center.objects.get(model=model[0], center=staff.supply_center)
            quantity = int(quantity) + mc.quantity
            mc.update(quantity=quantity)
            purchase_price = -int(purchase_price) + staff.supply_center.profit
            staff.supply_center.update(profit=purchase_price)


def placeOrder(request):
    contract_num = request.GET['contract_num']
    enterprise = request.GET['enterprise']
    product_model = request.GET['product_model']
    quantity = request.GET['quantity']
    contract_manager = request.GET['contract_manager']
    contract_date = request.GET['contract_date']
    estimated_delivery_date = request.GET['estimated_delivery_date']
    lodgement_date = request.GET['lodgement_date']
    salesman_num = request.GET['salesman_num']
    contract_type = request.GET['contract_type']
    staff = models.Staff.objects.get(number=salesman_num)
    manager = models.Staff.objects.get(number=contract_manager)
    model = models.Models.objects.get(model=product_model)
    enterprise = models.Enterprise.objects.get(name=enterprise)
    center = enterprise.supply_center
    mc = models.Model_center.objects.get(model=model, center=center)
    if mc.quantity < int(quantity) or staff.type != 'Salesman':
        s = 'failure!'
    else:
        s = 'success!'
        center.profit += model.unit_price * int(quantity)
        center.save()
        mc.quantity -= int(quantity)
        mc.save()
        model.sales_volume += int(quantity)
        model.save()
        if not models.Contract.objects.filter(contract_num=contract_num).exists():
            models.Contract(contract_num=contract_num, enterprise=enterprise, contract_manager=manager,
                            contract_date=parse_date(contract_date), contract_type=contract_type).save()
        contract = models.Contract.objects.get(contract_num=contract_num)
        models.Order(contract=contract, product_model=model, quantity=int(quantity),
                     estimate_delivery_date=parse_date(estimated_delivery_date),
                     lodgement_delivery_date=parse_date(lodgement_date), salesman_num=staff).save()
    return HttpResponse(ans(True, False, s, {}).answer)


def quick_place_order(contract_num, enterprise, product_model, quantity, contract_manager, contract_date,
                      estimated_delivery_date, lodgement_date, salesman_num, contract_type):
    staff = models.Staff.objects.get(number=salesman_num)
    manager = models.Staff.objects.get(number=contract_manager)
    model = models.Models.objects.get(model=product_model)
    enterprise = models.Enterprise.objects.get(name=enterprise)
    center = enterprise.supply_center
    mc = models.Model_center.objects.get(model=model, center=center)
    if mc.quantity < int(quantity) or staff.type != 'Salesman':
        a = 1
    else:
        center.profit += model.unit_price * int(quantity)
        center.save()
        mc.quantity -= int(quantity)
        mc.save()
        model.sales_volume += int(quantity)
        model.save()
        if not models.Contract.objects.filter(contract_num=contract_num).exists():
            models.Contract(contract_num=contract_num, enterprise=enterprise, contract_manager=manager,
                            contract_date=parse_date(contract_date), contract_type=contract_type).save()
        contract = models.Contract.objects.get(contract_num=contract_num)
        models.Order(contract=contract, product_model=model, quantity=int(quantity),
                     estimate_delivery_date=parse_date(estimated_delivery_date),
                     lodgement_delivery_date=parse_date(lodgement_date), salesman_num=staff).save()


def updateOrder(request):
    contract = request.GET['contract']
    product_model = request.GET['product_model']
    salesman = request.GET['salesman']
    quantity = request.GET['quantity']
    estimate_delivery_date = request.GET['estimate_delivery_date']
    lodgement_date = request.GET['lodgement_date']
    staff = models.Staff.objects.get(number=salesman)
    center = staff.supply_center
    model = models.Models.objects.get(model=product_model)
    mc = models.Model_center.objects.get(model=model, center=center)
    contract = models.Contract.objects.get(contract_num=contract)
    order = models.Order.objects.filter(contract=contract, salesman_num=staff.number, product_model=model)
    center = models.Center.objects.get(name=center)
    if order.exists():
        s = 'success!'
        order = order[0]
        center.profit = center.profit + (quantity - order.quantity) * model.unit_price
        center.save()
        mc.quantity = mc.quantity + order.quantity - int(quantity)
        mc.save()
        order.quantity = int(quantity)
        order.save()
        if order.quantity == 0:
            order.delete()
        else:
            order.estimate_delivery_date = parse_date(estimate_delivery_date)
            order.lodgement_delivery_date = parse_date(lodgement_date)
            order.save()
        model.sales_volume = model.sales_volume + int(quantity) - order.quantity
        model.save()
    else:
        s = 'failure!'
    return HttpResponse(ans(True, False, s, {}).answer)


def quick_update_order(contract, product_model, salesman, quantity, estimate_delivery_date, lodgement_date):
    staff = models.Staff.objects.get(number=salesman)
    center = staff.supply_center
    model = models.Models.objects.get(model=product_model)
    mc = models.Model_center.objects.get(model=model, center=center)
    contract = models.Contract.objects.get(contract_num=contract)
    order = models.Order.objects.filter(contract=contract, salesman_num=staff.number, product_model=model)
    center = models.Center.objects.get(name=center)
    if order.exists():
        order = order[0]
        center.profit = center.profit + (quantity - order.quantity) * model.unit_price
        center.save()
        mc.quantity = mc.quantity + order.quantity - int(quantity)
        mc.save()
        order.quantity = int(quantity)
        order.save()
        if order.quantity == 0:
            order.delete()
        else:
            order.estimate_delivery_date = parse_date(estimate_delivery_date)
            order.lodgement_delivery_date = parse_date(lodgement_date)
            order.save()
        model.sales_volume = model.sales_volume + int(quantity) - order.quantity
        model.save()


def deleteOrder(request):
    contract = request.GET['contract']
    salesman = request.GET['salesman']
    seq = request.GET['seq']
    seq = int(seq) - 1
    contract = models.Contract.objects.get(contract_num=contract)
    salesman = models.Staff.objects.get(number=salesman)
    orders = models.Order.objects.filter(contract=contract, salesman_num=salesman).order_by('estimate_delivery_date',
                                                                                            Lower(
                                                                                                'product_model__model'))
    if orders.exists():
        s = 'success!'
        order = orders[seq]
        mc = models.Model_center.objects.get(model=order.product_model, center=salesman.supply_center)
        mc.center.profit -= order.quantity * order.product_model.unit_price
        mc.quantity += order.quantity
        mc.model.sales_volume -= order.quantity
        mc.model.save()
        mc.save()
        order.delete()
    else:
        s = 'failure!'
    return HttpResponse(ans(True, False, s, {}).answer)


def quick_delete_order(contract, salesman, seq):
    seq = int(seq) - 1
    contract = models.Contract.objects.get(contract_num=contract)
    salesman = models.Staff.objects.get(number=salesman)
    orders = models.Order.objects.filter(contract=contract, salesman_num=salesman).order_by('estimate_delivery_date',
                                                                                            Lower(
                                                                                                'product_model__model'))
    if orders.exists():
        order = orders[seq]
        mc = models.Model_center.objects.get(model=order.product_model, center=salesman.supply_center)
        mc.center.profit -= order.quantity * order.product_model.unit_price
        mc.quantity += order.quantity
        mc.model.sales_volume -= order.quantity
        mc.model.save()
        mc.save()
        order.delete()


def getAllStaffCount(request):
    count = models.Staff.objects.all().values('type').annotate(Count('number'))
    table = {}
    s = "let's show them below!"
    table['col_names'] = ['type', 'number']
    table['rows'] = []
    for cen in count:
        temp = []
        temp.append(cen['type'])
        temp.append(cen['number__count'])
        table['rows'].append(temp)
    return HttpResponse(ans(True, True, s, table).answer)


def quick_get_all_staff_count():
    count = models.Staff.objects.all().values('type').annotate(Count('number'))
    table = {}
    table['col_names'] = ['type', 'number']
    table['rows'] = []
    for cen in count:
        temp = []
        temp.append(cen['type'])
        temp.append(cen['number__count'])
        table['rows'].append(temp)
    return table


def getContractCount(request):
    count = models.Contract.objects.count()
    return HttpResponse(ans(True, False, str(count), {}).answer)


def quick_get_contract_count():
    count = models.Contract.objects.count()
    return str(count)


def getOrderCount(request):
    count = models.Order.objects.count()
    return HttpResponse(ans(True, False, str(count), {}).answer)


def quick_get_order_count():
    count = models.Order.objects.count()
    return str(count)


def getNeverSoldProductCount(request):
    count = models.Model_center.objects.filter(quantity__gt=0).filter(model__sales_volume=0).values('model').count()
    return HttpResponse(ans(True, False, str(count), {}).answer)


def quick_get_never_sold_product_count():
    count = models.Model_center.objects.filter(quantity__gt=0).filter(model__sales_volume=0).values('model').count()
    return str(count)


def getFavoriteProductModel(request):
    value = models.Models.objects.all().aggregate(Max('sales_volume'))
    model = models.Models.objects.filter(sales_volume=value['sales_volume__max'])
    table = {}
    s = "let's show them below!"
    table['col_names'] = ['model_name', 'quantity']
    table['rows'] = []
    for cen in model:
        temp = []
        temp.append(cen.model)
        temp.append(int(cen.sales_volume))
        table['rows'].append(temp)
    return HttpResponse(ans(True, True, s, table).answer)


def quick_get_favorite_product_model():
    value = models.Models.objects.all().aggregate(Max('sales_volume'))
    model = models.Models.objects.filter(sales_volume=value['sales_volume__max'])
    table = {}
    table['col_names'] = ['model_name', 'quantity']
    table['rows'] = []
    for cen in model:
        temp = []
        temp.append(cen.model)
        temp.append(int(cen.sales_volume))
        table['rows'].append(temp)
    return table


def getAvgStockByCenter(request):
    value = models.Model_center.objects.filter(quantity__gt=0).values('center').annotate(
        num=Sum('quantity') / Count('model'))
    table = {}
    s = "let's show them below!"
    table['col_names'] = ['center', 'num']
    table['rows'] = []
    for cen in value:
        temp = []
        temp.append(cen['center'])
        temp.append(cen['num'])
        table['rows'].append(temp)
    return HttpResponse(ans(True, True, s, table).answer)


def quick_get_avg_stock_by_center():
    value = models.Model_center.objects.filter(quantity__gt=0).values('center').annotate(
        num=Sum('quantity') / Count('model'))
    table = {}
    table['col_names'] = ['center', 'num']
    table['rows'] = []
    for cen in value:
        temp = []
        temp.append(cen['center'])
        temp.append(cen['num'])
        table['rows'].append(temp)
    return table


def getProductByNumber(request):
    number = request.GET['number']
    product = models.Model_center.objects.filter(model__number=number).filter(quantity__gt=0)
    table = {}
    s = "let's show them below!"
    table['col_names'] = ['center', 'model', 'quantity']
    table['rows'] = []
    for cen in product:
        temp = []
        temp.append(cen.center.name)
        temp.append(cen.model.model)
        temp.append(str(cen.quantity))
        table['rows'].append(temp)
    return HttpResponse(ans(True, True, s, table).answer)


def getContractInfo(request):
    contract_number = request.GET['contract_number']
    enterprise = request.GET['enterprise']
    contract_manager = request.GET['contract_manager']
    #contract = models.Contract.objects.get(contract_num=contract_number)
    if not contract_number == 'contract_num=contract_number':
        contract = models.Contract.objects.filter(contract_num=contract_number)
    if not enterprise == '':
        contract = models.Contract.objects.filter(enterprise__name=enterprise)
    if not contract_manager == '':
        contract = models.Contract.objects.filter(contract_manager__number=contract_manager)
    table = {}
    table['col_names'] = ['product_model', 'quantity', 'salesman_man', 'edate', 'ldate','up']
    contracts = contract
    for con in contracts:
        s = con.contract_num + " " + con.contract_manager.name + " " + con.enterprise.name + " " + con.enterprise.supply_center.name
        table['rows'] = []
        order = models.Order.objects.filter(contract=con)
        for cen in order:
            temp = []
            temp.append(cen.product_model.model)
            temp.append(cen.quantity)
            temp.append(cen.salesman_num.name)
            temp.append(str(cen.estimate_delivery_date))
            temp.append(str(cen.lodgement_delivery_date))
            temp.append(str(cen.product_model.unit_price))
            table['rows'].append(temp)
    return HttpResponse(ans(True, True, s, table).answer)


def test_input(request):
    data = pd.read_csv('trades/data/center.csv')
    data = np.array(data)
    for rows in data:
        center_add_fast(rows[1])
    data = pd.read_csv('trades/data/enterprise.csv')
    data = np.array(data)
    for rows in data:
        enterprise_add_fast(rows[1], rows[2], rows[3], rows[4], rows[5])
    data = pd.read_csv('trades/data/model.csv')
    data = np.array(data)
    for rows in data:
        models_add_fast(rows[1], rows[2], rows[3], rows[4])
    data = pd.read_csv('trades/data/staff.csv')
    data = np.array(data)
    for rows in data:
        staff_add_fast(rows[5], rows[1], rows[2], rows[3], rows[4], rows[6], rows[7])
    data = pd.read_csv('trades/test_cases/in_stoke_test.csv')
    data = np.array(data)
    for rows in data:
        quick_stock_in(rows[1], rows[2], rows[3], rows[4], rows[5], rows[6])
    data = pd.read_csv('trades/test_cases/task2_test_data_final_public.tsv', sep='\t')
    data = np.array(data)
    for rows in data:
        quick_place_order(rows[0], rows[1], rows[2], rows[3], rows[4], rows[5], rows[6], rows[7], rows[8], rows[9])
    data = pd.read_csv('trades/test_cases/update_final_test.tsv', sep='\t')
    data = np.array(data)
    for rows in data:
        quick_update_order(rows[0], rows[1], rows[2], rows[3], rows[4], rows[5])
    data = pd.read_csv('trades/test_cases/delete_final.tsv', sep='\t')
    data = np.array(data)
    for rows in data:
        part = rows[0].split(' ')
        quick_delete_order(part[0], part[6], part[14])

    return HttpResponse(ans(False, False, '', {}).answer)


def test_output(request):
    table = quick_get_all_staff_count()
    s = 'Q6\n'
    for rows in table['rows']:
        s += rows[0] + " " + str(rows[1]) + '\n'
    s += 'Q7\n'
    s += quick_get_contract_count() + '\n'
    s += 'Q8\n'
    s += quick_get_order_count() + '\n'
    s += 'Q9\n'
    s += quick_get_never_sold_product_count() + '\n'
    s += 'Q10\n'
    table = quick_get_favorite_product_model()
    for rows in table['rows']:
        s += rows[0] + " " + str(rows[1]) + '\n'
    s += 'Q11\n'
    table = quick_get_avg_stock_by_center()
    for rows in table['rows']:
        s += rows[0] + " " + str(rows[1]) + '\n'

    return HttpResponse(ans(True, True, s, {}).answer)


class ans(object):
    def __init__(self, b1, b2, rs, rt):
        self.answer = json.dumps({"show_str": b1, "show_table": b2, "result_str": rs, "result_table": rt})
