from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Basket, BasketProduct, Customer
from .viewsHelper import createTestData, getBasketAndCostByCity, truncateTablesAndResetAutoIncrement

class IndexView(generic.TemplateView):
    template_name = 'adapp/index.html'

class SqlDatabaseView(generic.TemplateView):
    template_name = 'adapp/sqldatabase.html'

    def get_context_data(self, **kwargs):
         context = super(SqlDatabaseView, self).get_context_data(**kwargs)
         context['customerTable'] = Customer.objects.all().order_by("id")
         context['basketTable'] = Basket.objects.all().order_by("id")
         context['basketProductTable'] = BasketProduct.objects.all().order_by("id")
         return context

def addSqlData(request):
    customerCount = int(request.POST["customerCount"])
    basketCount = int(request.POST["basketCount"])
    createTestData(customerCount, basketCount)
    return HttpResponseRedirect(reverse('adapp:sqldatabase'))

def analyseByCity(request):
    getBasketAndCostByCity()
    return HttpResponseRedirect(reverse('adapp:index'))

def clearTables(request):
    truncateTablesAndResetAutoIncrement()
    return HttpResponseRedirect(reverse('adapp:sqldatabase'))
