from random import randint, uniform
from .models import Basket, BasketProduct, Customer
from django.db import connection
import json
from decimal import Decimal

cities = ["Ankara", "Istanbul", "Izmir", "Bursa", "Edirne", "Konya", "Antalya", "Diyarbakir", "Van", "Rize"]
cityCount = len(cities)
names = ["Ali", "Ahmet", "Ayse", "Fatma", "Cem"]
nameCount = len(names)
surnames = ["Demir", "Kilic", "Yilmaz", "Can", "Bulut"]
surnameCount = len(surnames)
descriptions = ["Toothpaste", "Shampoo", "Bread", "Apple", "Pear"]
descriptionCount = len(descriptions)

def createTestData(customerCount, basketCount):
    newAddedCustomerIDList = []
    for i in range(customerCount):
        randNameIdx = randint(0, nameCount - 1)
        randSurnameIdx = randint(0, surnameCount - 1)
        randCityIdx = randint(0, cityCount - 1)
        randName = names[randNameIdx]
        randSurname = surnames[randSurnameIdx]
        randCity = cities[randCityIdx]
        newCustomer = Customer(name = randName, surname = randSurname, city = randCity)
        newCustomer.save()
        newAddedCustomerIDList.append(newCustomer.id)
    for i in range(basketCount):
        randCustomerIDIdx = randint(0, customerCount - 1)
        randCustomerID = newAddedCustomerIDList[randCustomerIDIdx]
        newBasket = Basket(customer_id = randCustomerID)
        newBasket.save()
        randProductCount = randint(1, 5)
        for j in range(randProductCount):
            randCost = round(uniform(100, 1000), 2) # 2 decimal costs. Ex. 39.90 TL
            randDescriptionIdx = randint(0, descriptionCount - 1)
            randDescription = descriptions[randDescriptionIdx]
            newBasketProduct = BasketProduct(basket_id = newBasket.id, cost = randCost, description = randDescription)
            newBasketProduct.save()

class DtoCityAnalysis:
    def __init__(self, cityName, basketCount, totalCost):
        self.cityName = cityName
        self.basketCount = basketCount
        self.totalCost = totalCost
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return obj.__dict__

def getBasketAndCostByCity():
    sqlQuery = "select city, count(distinct adapp_basket.id) as basketCount, sum(adapp_basketproduct.cost) as totalCost" \
    " from ((adapp_customer inner join adapp_basket on adapp_customer.id = adapp_basket.customer_id)" \
    " inner join adapp_basketproduct on adapp_basket.id = adapp_basketproduct.basket_id) group by city" \
    " order by basketCount desc, cost desc, city asc"
    cursor = connection.cursor()
    cursor.execute(sqlQuery)
    queryResList = cursor.fetchall()
    dtoList = []
    for row in queryResList:
        curDtoObj = DtoCityAnalysis(row[0], row[1], row[2])
        dtoList.append(curDtoObj)
    jsonFilePath = "adapp/jsonFiles/dtoCityAnalysisList.json"
    with open(jsonFilePath, 'w', encoding='utf-8') as f:
        json.dump(dtoList, f, ensure_ascii=False, indent=4, cls=JsonEncoder)

def truncateTablesAndResetAutoIncrement():
    cursor = connection.cursor()
    cursor.execute("delete from adapp_basketproduct")
    cursor.execute("delete from adapp_basket")
    cursor.execute("delete from adapp_customer")
    cursor.execute("alter table adapp_basketproduct auto_increment = 1")
    cursor.execute("alter table adapp_basket auto_increment = 1")
    cursor.execute("alter table adapp_customer auto_increment = 1")
