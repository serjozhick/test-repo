from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

import urllib
import re
from bs4 import BeautifulSoup

def LoadSelary():
    f = open('selary.html', 'r')
    html = f.read()
    ##html = urllib.urlopen('http://belstat.gov.by/ofitsialnaya-statistika/otrasli-statistiki/naselenie/trud/operativnaya-informatsiya_8/zarabotnaya-plata/?cmd=print').read()
    parsed_html = BeautifulSoup(html, 'html.parser')
    result = list()
    for table in parsed_html.find_all('table'):
        year = 0
        for row in table.find_all('tr'):
            monthInd = 0
            if year == 0:
                year = 1
                continue
            for col in row.find_all('span'):
                if monthInd > 0:
                    result.append([year + '.' + str(monthInd), col.text])
                    #print year + '.' + str(monthInd), col.text
                else:
                    year = col.text[:4]
                monthInd+=1
        break
    f_out = open('data.csv', 'w')
    for line in result:
        f_out.write(line[0])
        f_out.write(',')
        f_out.write(line[1])
        f_out.write('\n')

def LoadPrice(year, month, day):
    url = 'http://www.nbrb.by/statistics/rates/ratesDaily.asp?fromdate=' + year + '-' + month + '-' + day
    html = urllib.urlopen(url).read()
    #f = open('priceTest.html', 'r')
    #html = f.read()
    parsed_html = BeautifulSoup(html, 'html.parser')
    result = list()
    for table in parsed_html.find_all('table', {'class' : "stexttbl"}):
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) > 0 and columns[0].text == 'USD':
                textResult = columns[2].text.strip()
                textResult = textResult.replace(",", ".")
                textResult = re.sub(r'\s+', '', textResult, flags=re.UNICODE)
                return float(textResult)
    return 'unknown'

def WritePrice():
    f_in = open('data.csv', 'r')
    f_out = open('data2.csv', 'w')
    for line in f_in.readlines():
        f_out.write(line.strip('\n'))
        f_out.write(',')
        date = line.split(',', 1)[0]
        dateArr = date.split('.')
        if dateArr[1] == '12':
            month = '1'
            year = str(int(dateArr[0]) + 1)
        else:
            month = str(int(dateArr[1]) + 1)
            year = dateArr[0]
        f_out.write(str(LoadPrice(year, month, '1')))
        f_out.write(',')
        f_out.write(year + '.' + month)
        f_out.write('\n')

def LoadOil(year):    
    url = 'http://www.calc.ru/dinamika-Brent.html?date=' + year
    html = urllib.urlopen(url).read()
    parsed_html = BeautifulSoup(html, 'html.parser')
    result = range(12)
    for table in parsed_html.find_all('table', {'class' : "result_table padt10"}):
        index = 11
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) > 0:
                textResult = columns[1].text.strip()
                textResult = textResult.replace(",", ".")
                textResult = re.sub(r'\s+', '', textResult, flags=re.UNICODE)
                result[index] = float(textResult)
                index -= 1
    return result

def WriteOil():
    f_in = open('data2.csv', 'r')
    f_out = open('data3.csv', 'w')
    loadedYear = '0'
    loadedOil = []
    for line in f_in.readlines():
        f_out.write(line.strip('\n'))
        f_out.write(',')
        date = line.split(',', 1)[0]
        dateArr = date.split('.')
        year = dateArr[0]
        month = int(dateArr[1])
        if loadedYear != year:
            loadedOil = LoadOil(year)
            loadedYear = year
        f_out.write(str(loadedOil[month - 1]))
        f_out.write(',')
        f_out.write(year + '.' + str(month))
        f_out.write('\n')

def Calc():
    f_in = open('data3.csv', 'r')
    f_out = open('data4.csv', 'w')
    for line in f_in.readlines():
        f_out.write(line.strip('\n'))
        f_out.write(',')
        data = line.split(',')
        superValue = float(data[1]) / float(data[2]) / float(data[4])
        print superValue
        f_out.write(str(superValue))
        f_out.write('\n')

Calc()

"""
class MyHTMLParser(HTMLParser):
    inTable = False
    def handle_starttag(self, tag, attrs):
        if (tag == 'table'):
            self.inTable = True
        if (self.inTable):
            print "Start tag:", tag
            for attr in attrs:
                print "     attr:", attr
    def handle_endtag(self, tag):
        if (tag == 'table'):
            self.inTable = False
        if (self.inTable):
            print "End tag  :", tag
    def handle_data(self, data):
        if (self.inTable):
           print "Data     :", data
    def feedUrl(self, url):
        print(url)
        page = urllib.urlopen(url).read()
	print(page)
        ##self.feed(page)
    def feedFile(self, path):
        f = open(path, 'r')
        page = f.read()
        self.feed(page)

parser = MyHTMLParser()
parser.feedFile('selary.html')
"""
