import sys
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

DB = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="northwind"
)
##NOTE
#Der er ingen "orderdetails" som bruger "discount" feltet, så det bliver der ikke taget højde for
ordersCountryDetails_query = """select O.OrderID, ShipCountry, OrderDate, UnitPrice, Quantity from (select OrderID, ShipCountry, OrderDate from northwind.orders) as O
join (select OrderID, UnitPrice, Quantity from northwind.orderdetails) as OD on OD.orderId = O.orderId
order by O.OrderId, OD.OrderId;"""



ordersCountryDetails_df = pd.read_sql(ordersCountryDetails_query,DB)

countries = {}
countriesByYear = {}
#(pandas index,) O.OrderID, ShipCountry, OrderDate, UnitPrice, Quantity
for x in ordersCountryDetails_df.itertuples():
    country = x[2]
    year = f"{x[3].month_name()} - {x[3].year}"
    value = x[4]*x[5]
    countries[country] = countries.get(country, 0) + value
    
    year_countries = countriesByYear.get(year,{})
    year_countries[country] = year_countries.get(country,0) + value
    countriesByYear[year] = year_countries

ordersProductSum_query = """select CategoryName, sum(Quantity) as Quantity from
(select CategoryId, Quantity from northwind.orderdetails
join northwind.products on products.ProductId = orderdetails.ProductId) as pd
join northwind.categories on categories.CategoryId = pd.CategoryId
group by CategoryName;"""
ordersProductSum_df = pd.read_sql(ordersProductSum_query,DB)



##plotting
#sales by country
items = sorted(countries.items(),key=lambda x:x[1],reverse=True)
x = [x for x,_ in items]
y = [y for _,y in items]
plt.bar(x,y)
plt.xticks(rotation=80)
plt.title("Sales by country")
plt.savefig("Sales by country",bbox_inches="tight")
plt.clf()
#sales by country by year
for c in countries:
    years = [year for year in countriesByYear]
    salesYear = [countriesByYear[year].get(c,0) for year in years]
    plt.bar(years, salesYear,label=c)
    plt.legend(loc='center left',bbox_to_anchor=(1, 0.5))
plt.xticks(list(countriesByYear),rotation=90)
plt.title("country purcase by year")
plt.savefig("country purcase by year",bbox_inches="tight")
plt.clf()

labels = [f"{x[1]}({x[2]})" for x in ordersProductSum_df.itertuples()]
values = [x[2] for x in ordersProductSum_df.itertuples()]
plt.pie(values,labels=labels)
plt.title("Products sold by category")
plt.savefig("Products sold by category")
plt.clf()