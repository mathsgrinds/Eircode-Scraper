#!/usr/bin/env python
import mechanize
import os
import threading
import csv
import random
import time
from bs4 import BeautifulSoup
import unicodedata
import re

def generate_pool(keys=("A41", "A42", "A45", "A63", "A67", "A75", "A81", "A82", "A83", "A84", "A85", "A86", "A91", "A92", "A94", "A96", "A98", "C15", "D01", "D02", "D03", "D04", "D05", "D06", "D6W", "D07", "D08", "D09", "D10", "D11", "D12", "D13", "D14", "D15", "D16", "D17", "D18", "D20", "D22", "D24", "E21", "E25", "E32", "E34", "E41", "E45", "E53", "E91", "F12", "F23", "F26", "F28", "F31", "F35", "F42", "F45", "F52", "F56", "F91", "F92", "F93", "F94", "H12", "H14", "H16", "H18", "H23", "H53", "H54", "H62", "H65", "H71", "H91", "K32", "K34", "K36", "K45", "K56", "K67", "K78", "N37", "N39", "N41", "N91", "P12", "P14", "P17", "P24", "P25", "P31", "P32", "P36", "P43", "P47", "P51", "P56", "P61", "P67", "P72", "P75", "P81", "P85", "R14", "R21", "R32", "R35", "R42", "R45", "R51", "R56", "R93", "R95", "T12", "T23", "T34", "T45", "T56", "V14", "V15", "V23", "V31", "V35", "V42", "V92", "V93", "V94", "V95", "W12", "W23", "W34", "W91", "X35", "X42", "X91", "Y14", "Y21", "Y25", "Y34", "Y35")):
    global pool_of_routing_keys
    global pool_of_unique_identifiers
    global exclude
    exclude = set()
    pool_of_routing_keys = set()
    pool_of_unique_identifiers = set()
    for r in keys:
        pool_of_routing_keys.add(r)
    for u1 in "0 1 2 3 4 5 6 7 8 9 A C D E F H K N P R T V W X Y".split(" "):
        for u2 in "0 1 2 3 4 5 6 7 8 9 A C D E F H K N P R T V W X Y".split(" "):
            for u3 in "0 1 2 3 4 5 6 7 8 9 A C D E F H K N P R T V W X Y".split(" "):
                for u4 in "0 1 2 3 4 5 6 7 8 9 A C D E F H K N P R T V W X Y".split(" "):
                    pool_of_unique_identifiers.add(u1+u2+u3+u4)

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def random_user_agent():
    from random import choice
    user_agents = ['Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36']
    random_user_agent = choice(user_agents)
    return random_user_agent

def RepresentsLetter(s):
    if s in "A C D E F H K N P R T V W X Y".split(" "):
        return True
    else:
        return False

def check_eircode(eircode):
    try:
        routing_key = eircode.split(" ")[0]
        unique_identifiers = eircode.split(" ")[1]
        keys=("A41", "A42", "A45", "A63", "A67", "A75", "A81", "A82", "A83", "A84", "A85", "A86", "A91", "A92", "A94", "A96", "A98", "C15", "D01", "D02", "D03", "D04", "D05", "D06", "D6W", "D07", "D08", "D09", "D10", "D11", "D12", "D13", "D14", "D15", "D16", "D17", "D18", "D20", "D22", "D24", "E21", "E25", "E32", "E34", "E41", "E45", "E53", "E91", "F12", "F23", "F26", "F28", "F31", "F35", "F42", "F45", "F52", "F56", "F91", "F92", "F93", "F94", "H12", "H14", "H16", "H18", "H23", "H53", "H54", "H62", "H65", "H71", "H91", "K32", "K34", "K36", "K45", "K56", "K67", "K78", "N37", "N39", "N41", "N91", "P12", "P14", "P17", "P24", "P25", "P31", "P32", "P36", "P43", "P47", "P51", "P56", "P61", "P67", "P72", "P75", "P81", "P85", "R14", "R21", "R32", "R35", "R42", "R45", "R51", "R56", "R93", "R95", "T12", "T23", "T34", "T45", "T56", "V14", "V15", "V23", "V31", "V35", "V42", "V92", "V93", "V94", "V95", "W12", "W23", "W34", "W91", "X35", "X42", "X91", "Y14", "Y21", "Y25", "Y34", "Y35")
        u1 = unique_identifiers[0]
        u2 = unique_identifiers[1]
        u3 = unique_identifiers[2]
        u4 = unique_identifiers[3]
        if routing_key not in keys:
            return False
        if RepresentsInt(u1) and RepresentsInt(u2) and RepresentsInt(u3) and RepresentsInt(u4):
            return False
        if RepresentsLetter(u1) and RepresentsLetter(u2) and RepresentsLetter(u3) and RepresentsLetter(u4):
            return False
        return True	
    except:
        return False

def random_eircode():
    eircode = ""
    while check_eircode(eircode) == False:
        routing_key = random.sample(pool_of_routing_keys, 1)[0]
        unique_identifier = random.sample(pool_of_unique_identifiers, 1)[0]
        eircode = routing_key+" "+unique_identifier
    return eircode

def get_address_from_eircode(eircode):
    browser = mechanize.Browser(factory=mechanize.RobustFactory())
    url = "http://correctaddress.anpost.ie/pages/Search.aspx"
    browser.addheaders = [('User-agent', random_user_agent() )]
    browser.open(url)
    html = browser.response().read()
    browser.select_form(nr=0)
    browser.form.set_all_readonly(False)
    browser["ctl00$body$txtEircode"] = str(eircode)
    request = browser.form.click()
    response = browser.submit()
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find(id="ctl00_body_hfTextToCopy")
    try:
        value = tag['value']
        address = value.replace("\n",", ")
        return str(unicodedata.normalize('NFKD', address).encode('ascii','ignore'))
    except:
        return ""

def get_addresses_from_address(address):
    browser = mechanize.Browser(factory=mechanize.RobustFactory())
    leading = address.split(",")[0]
    eircode = get_eircode_from_address(address)
    address = address.replace(leading, "*")
    address = address.replace(eircode, "*")
    url = "http://correctaddress.anpost.ie/pages/Search.aspx"
    browser.addheaders = [('User-agent',random_user_agent())]
    browser.open(url)
    html = browser.response().read()
    browser.select_form(nr=0)
    browser.form.set_all_readonly(False)
    browser["ctl00$body$txtAutoComplete"] = str(address)
    request = browser.form.click()
    response = browser.submit()
    html = response.read()
    try:
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.find(id="ctl00_body_hfTextToCopy")
        results = set()
        for table in soup.findAll("table"):
            for row in table.findAll("tr"):
                for a in row.findAll("a"):
                    if a.text.replace(" , ", ",") is not None:
                        results.add(a.text.replace(" , ", ", "))
        return unicodedata.normalize('NFKD', results).encode('ascii','ignore')
    except:
        return ""

def get_eircode_from_address(address):
    browser = mechanize.Browser(factory=mechanize.RobustFactory())
    url = "http://correctaddress.anpost.ie/pages/Search.aspx"
    browser.addheaders = [('User-agent', random_user_agent())]
    browser.open(url)
    html = browser.response().read()
    browser.select_form(nr=0)
    browser.form.set_all_readonly(False)
    browser["ctl00$body$txtAutoComplete"] = str(address)
    request = browser.form.click()
    response = browser.submit()
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find(id="ctl00_body_hfTextToCopy")
    try:
        value = tag['value']
        address = value.replace("\n",", ")
        return str(address.split(",")[-1].strip(" "))
    except:
        try:
         return (soup.findAll("table")[0].findAll("tr")[1:][0]).find("a").text.split(",")[-1].strip(" ")
        except:
            return ""

def generate_valid_eircode():
    result = ""
    while(result == ""):
        eircode = random_eircode()
        result = get_address_from_eircode(eircode)
    return eircode

def test_address_contains_int(address):
    try:
        return int(re.search(r'\d+',address.replace(get_eircode_from_address(address),"")).group())
    except:
        return 0

def load_csv_file(name="eircode"):
    global filename
    filename = name+".csv"
    if not os.path.exists(filename):
        print "File does not exist. Creating file now."
        header = '"Eircode","Address"'+"\n"
        print header
        with open(filename, 'a') as f:
            f.write(header)
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            exclude.add(row[0])
    exclude.remove("Eircode")
    return str(len(exclude))

def sort_table(table, cols):
    for col in reversed(cols):
        table = sorted(table, key=operator.itemgetter(col))
    return table

def add_to_csv(eircode):
    if eircode in exclude:
        return False
    else:
        try:
            address = get_address_from_eircode(eircode)
            if address != "":
                address = address+", IRELAND"
                row= '"'+eircode+'","'+address+'"'+"\n"
                with open(filename,'a') as f: f.write(row)
                print "ADDED TO CSV FILE: "+row
                exclude.add(eircode)
                return True
        except:
            return False

def search_street(address):
    x = test_address_contains_int(address)
    if x != 0:
        last_eircode = ""
        n=0
        base_address = address.replace(str(x), "***", 1)
        while True:
            n=n+1
            address = base_address.replace("***",str(n))
            eircode = get_eircode_from_address(address)
            address = address.replace(", "+eircode,"")
            if(eircode == "" or eircode == last_eircode):
                break
            else:
                last_eircode = eircode
            add_to_csv(eircode)
       
def search_unique_identifier(eircode):
    routing_key = eircode.split(" ")[0]
    unique_identifer = eircode.split(" ")[1]
    for key in pool_of_routing_keys:
        eircode = key + " " + unique_identifer
        address = get_address_from_eircode(eircode)
        address = address.replace(", "+eircode,"")
        if address != "":
            add_to_csv(eircode)
            search_street(address)

def init():    
    generate_pool()
    print "Loading CSV file and removing previously found Eircodes."
    previous = load_csv_file()
    print "The CSV file contains "+previous+" Eircodes. These have been removed from the search."

def search():
    while True:
        eircode = generate_valid_eircode()
        add_to_csv(eircode)
        search_unique_identifier(eircode)

def generate_csv(n=15):
    init()
    threads = []
    for x in range(n):
        print "Loading "+str(x+1)+"/"+str(n)+"."
        t = threading.Thread(target=search)
        threads.append(t)
        t.start()
    print "Searching... please wait."

#-------------------------------------------------------------
#------------------------# MAIN #----------------------------#
#-------------------------------------------------------------
print "Run? (YES/no)"
yes = set(['yes','y', 'ye', ''])
choice = raw_input().lower()
if choice in yes:
   generate_csv()
else:
   quit()
#-------------------------------------------------------------
