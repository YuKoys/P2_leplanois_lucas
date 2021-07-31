import requests
from bs4 import BeautifulSoup
import csv
import urllib.request

def find_all_url(beginning_url):
  reques = requests.get(beginning_url)
  res = []

  if reques.ok:
    bool_out = True
    soup = BeautifulSoup(reques.text, 'html.parser')
    ul = soup.findAll('li',  class_ = "next")
    
    while bool_out or ul != []:
      
      h3 = soup.findAll('h3')
      for h in h3: 
        a = h.find('a')
        url_livres = beginning_url[0:36] + a['href'][9:]
        res.append(url_livres)

      if ul != []:
        a2 = ul[0].find('a')
        url = beginning_url[:-10] + a2['href']
        reques = requests.get(url)
        soup = BeautifulSoup(reques.text, 'html.parser')
        ul = soup.findAll('li', class_ = "next")
      else: 
        bool_out = False

      
      
  return res

#res = find_all_url('http://books.toscrape.com/catalogue/category/books/travel_2/index.html')
#print(res)
#print(len(res))




def info_book(url):
  res = requests.get(url)
  if res.ok:
    soup = BeautifulSoup(res.text, 'html.parser')
    
    title = soup.find('h1').text
    
    tdlist = soup.findAll('td')
    tdlist.pop(4)
    tdlist.pop(5)
    td = []


    for i in range(len(tdlist)):
      if i == 2 or i == 3:
        td.append(tdlist[i].text[1:])
      else:
        td.append(tdlist[i].text)

    image = soup.find('img')
    img = image['src']
    img = img[5:]
    img = "http://books.toscrape.com" + img
    p = soup.findAll('p')
    description = p[3].text
    numb_stars = p[2]['class'][1]

    retres = ( url, td[0], title, td[3], td[2], td[4], description, td[1], numb_stars, img )
    return retres




#res = info_book("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")

#print(res)
def url_categorie(beginning_url):
  reque = requests.get(beginning_url)
  res = []
  if reque.ok:
    soup = BeautifulSoup(reque.text, "html.parser")

    ul = soup.findAll('ul')
    a = ul[2].findAll('a')
    for ihref in a:
      url = beginning_url + "/" + ihref['href']
      res.append(url)
  return res

#def function_that_return_csv_file_name(url,numb_page):
  #print(url)
#  res = url[:(-13 - numb_page)]
#  res = res[51:]
#  return res

#res = function_that_return_csv_file_name("http://books.toscrape.com/catalogue/category/books/travel_2/index.html", 0)
#print(res)


def call_all_function(beginning_url):
  list_url_categorie = url_categorie(beginning_url)
  name_csv_file = ""
  first_line = ("product_page_url","universal_ product_code (upc)", "title", "price_including_tax", 
  "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url")
  for i in range(len(list_url_categorie)):
  #for i in range(1):
    list_url_books_in_categorie = find_all_url(list_url_categorie[i])
    if i > 7: 
      name_csv_file = list_url_categorie[i][:(-13 -1)]
      name_csv_file = name_csv_file[51:]
      name2 = "csv/" + str(name_csv_file) + ".csv"
    else:
      name_csv_file = list_url_categorie[i][:-13]
      name_csv_file = name_csv_file[51:]
      name2 = "csv/" + str(name_csv_file) + ".csv"
    
    #f = open(name_csv_file + ".csv", "w", newline = "")
    #f = open("travel.csv", "w", newline = "")
    f = open(name2, "w", encoding = "utf-8", newline = "")
    writer = csv.writer(f)
    writer.writerow(first_line)
    for j in list_url_books_in_categorie:
      info_book_variable = info_book(j)  
      img = "image/" + info_book_variable[9][44:]
      urllib.request.urlretrieve(info_book_variable[9], img)
      writer.writerow(info_book_variable)
    f.close()


call_all_function('http://books.toscrape.com')
    



#f = open("crashtest.csv", "w", newline="")


#tup1 = ("tezjiojio",15)
#writer = csv.writer(f)
#writer.writerow(tup1)


#f.close()

