import time
from selenium import webdriver
from datetime import date
from fake_useragent import UserAgent
from lxml import html, etree
import requests
import yfinance as yf

# ticker = 'FLR'
# current_date_y = str(date.today().year) + '-' + str(date.today().month) + '-' + str(date.today().day)
# from_date_y = str(date.today().year) + '-' + str(date.today().month - 1) + '-' + str(date.today().day)
#
# stock = yf.Ticker(ticker)
# # data = yf.download(ticker, from_date_y,current_date_y, interval='2m')
#
# # print(data)
# # show actions (dividends, splits)
# print(stock.actions)
#
# # show dividends
# print(stock.dividends)
#
# # show splits
# print(stock.splits)
from fake_useragent import UserAgent



op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)
driver.get(f'https://finance.yahoo.com/quote/MMM/analysis?p=MMM')
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(3)
# xpath_el = driver.find_element_by_class_name('B(8px) Pos(a) C(white) Py(2px) Px(0) Ta(c) Bdrs(3px) Trstf(eio) Trsde(0.5) Arrow South Bdtc(i)::a Fw(b) Bgc($buy) Bdtc($buy)')
# print(driver.page_source)
element = driver.find_element_by_xpath('//*[@id="Col2-4-QuoteModule-Proxy"]/div/section/div/div/div[1]')
# exit()


print(element.text)
driver.close()
exit()


ua = UserAgent()
time.sleep(1)
headers = {'User-Agent': str(ua.chrome)}
url_ticker = f'https://finance.yahoo.com/quote/ETRN/analysis?p=ETRN'
time.sleep(3)
r = requests.get(url_ticker, headers=headers, timeout=(3.05, 27))
tree = html.fromstring(r.content)
#
#
# tr = etree.HTML(r.text)
# el = tr.xpath('//*[@id="Col2-4-QuoteModule-Proxy"]/div/section/div/div/div[1]')
# print(el)
#
# for item in el:
#     print(etree.tostring(item))


print(r.content)
# print(tree[1])
for index, item in enumerate(tree[0]):
    print(index)
    print(etree.tostring(item))
# print(r.json())



# def get_rating_yh(stock):
#     time.sleep(1)
#     ua = UserAgent()
#     headers = {'User-Agent': str(ua.chrome)}
#     url_ticker = f'https://finance.yahoo.com/quote/{stock}/analysis?p={stock}'
#     time.sleep(3)
#     r = requests.get(url_ticker, headers=headers)
#     tree = html.fromstring(r.content)
#     name_stock_exchange = tree.xpath('//*[@id="Col2-4-QuoteModule-Proxy"]/div/section/div/div/div[1]')
#     print(name_stock_exchange)
#
#
# print(get_rating_yh('API'))
