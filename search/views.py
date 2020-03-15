import json

from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

def index(request):
    products = []
    query = request.POST.get("search",False)
    if not query:
        return render(request, 'search/index.html')

    products += search_daraz_json(query)
    products += search_ishopping(query)
    products += search_saverspk(query)
    products += search_telemart(query)
    products = sorted(products, key=lambda k: k['price'])
    return render(request,'search/index.html',{"products":products})

def search_daraz(query):
    try:
        products = []
        url = "https://www.daraz.pk/catalog/?q=" + query
        resource = requests.get(url).text
        soup = BeautifulSoup(resource, "html.parser")
        list = soup.find_all(attrs = {"type": "application/ld+json"})[1].string
        list = json.loads(list)
        list = list["itemListElement"]
        for item in list:
            try:
                products.append(({"name": item["name"], "href": item["url"], "price": float(item["offers"]["price"]),
                                  "image": item["image"],"site":"Daraz.com"}))
            except:
                continue
        return products
    except Exception as e:
        return []

def search_daraz_json(query):
    try:
        products = []
        url = "https://www.daraz.pk/catalog/?_keyori=ssd&ajax=true&from=suggest_normal&q=" + query
        resource = requests.get(url).text
        list = json.loads(resource)
        list = list["mods"]["listItems"]
        for item in list:
            try:
                products.append(
                    ({"name": item["name"], "href": item["productUrl"], "price": float(item["price"]),
                      "image": item["image"], "site": "Daraz.com"}))
            except:
                continue
        return products
    except Exception as e:
        return []

def search_ishopping(query):
    try:
        products = []
        url = "https://eucs4.klevu.com/cloud-search/n-search/search?ticket=klevu-14920772243175751&paginationStartsFrom=0&sortPrice=false&ipAddress=undefined&analyticsApiKey=klevu-14920772243175751&showOutOfStockProducts=false&klevuFetchPopularTerms=false&klevu_priceInterval=500&fetchMinMaxPrice=true&klevu_multiSelectFilters=true&noOfResults=20&klevuSort=rel&enableFilters=true&filterResults=&visibility=search&category=KLEVU_PRODUCT&klevu_filterLimit=50&sv=1212&lsqt=&responseType=json&resultForZero=1&term=" + query
        resource = requests.get(url).text
        list = json.loads(resource)
        list = list["result"]
        for item in list:
            try:
                products.append(
                    ({"name": item["name"], "href": item["url"], "price": float(item["price"]),
                      "image": item["image"], "site": "Ishopping.com"}))
            except:
                continue
        return products
    except Exception as e:
        return []

def search_saverspk(query):
    try:
        products = []
        url = "https://www.searchanise.com/getwidgets?api_key=4S6h9h8k9i&restrictBy%5Bstatus%5D=A&restrictBy%5Bempty_categories%5D=N&restrictBy%5Busergroup_ids%5D=0%7C1&restrictBy%5Bcategory_usergroup_ids%5D=0%7C1&restrictBy%5Bapproved%5D=Y&restrictBy%5Bactive_company%5D=Y&startIndex=0&items=true&pages=true&facets=false&categories=true&suggestions=true&vendors=false&tags=false&pageStartIndex=0&pagesMaxResults=3&categoryStartIndex=0&categoriesMaxResults=3&suggestionsMaxResults=4&union%5Bprice%5D%5Bmin%5D=price_0%7Cprice_1&vendorsMaxResults=3&output=jsonp&callback=jQuery22404147613927260918_1584256529242&_=1584256529250&tagsMaxResults=3&maxResults=33&q=" + query
        resource = requests.get(url).text.split('"items":')[1].replace('});','')
        list = json.loads(resource)
        for item in list:
            try:
                products.append(
                    ({"name": item["title"], "href": item["link"], "price": float(item["price"]),
                      "image": item["image_link"], "site": "Savers.pk"}))
            except:
                continue
        return products
    except Exception as e:
        return []

def search_telemart(query):
    try:
        products = []
        url = "https://iw6vhpl077-3.algolianet.com/1/indexes/New_Telemart/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.32.1&x-algolia-application-id=IW6VHPL077&x-algolia-api-key=ee7d5abead68d64b082fe5d93d02ae78"
        data = {"params":"query={}&hitsPerPage=30".format(query)}
        resource = requests.post(url=url,json=data).text
        list = json.loads(resource)
        list = list["hits"]
        for item in list:
            try:
                if float(item["special_price"]) > 0:
                    products.append(
                        ({"name": item["name"], "href": item["url"], "price": float(item["special_price"]),
                          "image": item["image_url"], "site": "Telemart.pk"}))
            except:
                continue
        return products
    except Exception as e:
        return []