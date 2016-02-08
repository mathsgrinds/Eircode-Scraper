#!/usr/bin/env python
import mechanize
import os
import threading
import csv
import random
import time
from bs4 import BeautifulSoup
import unicodedata

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

def random_eircode():
    routing_key = random.sample(pool_of_routing_keys, 1)[0]
    unique_identifier = random.sample(pool_of_unique_identifiers, 1)[0]
    return str(routing_key+" "+unique_identifier)

def get_address_from_eircode(eircode):
    browser = mechanize.Browser(factory=mechanize.RobustFactory())
    url = "http://correctaddress.anpost.ie/pages/Search.aspx"
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
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
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
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
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
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

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def test_address_starts_with_int(address):
    x = address.split(" ")[0]
    if RepresentsInt(x):
        return True
    else:
        return False

def test_address_starts_with(address, start):
    address = address.strip(" ")
    leader = address.split(", ")[0]
    x = leader.split(" ")[0]
    y = leader.split(" ")[-1]
    if(x == start):
        if RepresentsInt(y):
            return True
        else:
            return False

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

def fix_csv_file():
    with open("eircode.csv", 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            print str('"'+row[0]+'","'+row[1]+'"'+"\n")
            if row[1] != "":
                with open("eircode_fixed.csv", 'a') as g:
                    g.write(str('"'+row[0]+'","'+row[1]+'"'+"\n"))

def add_to_csv(eircode):
    if eircode in exclude:
        return False
    else:
        address = get_address_from_eircode(eircode)
        if address != "":
            address = address+", IRELAND"
            row= '"'+eircode+'","'+address+'"'+"\n"
            with open(filename,'a') as f: f.write(row)
            print "ADDED TO CSV FILE: "+row
            exclude.add(eircode)
            return True

def search_street(address):
    blocks = ["APARTMENT", "UNIT", "FLAT", "SUITE"]
    if test_address_starts_with_int(address):
        last_eircode = ""
        n=0
        x = address.split(" ")[0]
        base_address = address.replace(x, "", 1)
        while True:
            n=n+1
            address = str(n) + base_address
            eircode = get_eircode_from_address(address)
            address = address.replace(", "+eircode,"")
            if(eircode == "" or eircode == last_eircode):
                break
            else:
                last_eircode = eircode
            add_to_csv(eircode)
    else:
        for start in blocks:
            if test_address_starts_with(address, start):
                last_eircode = ""
                n=0
                x = address.split(",")[0]
                base_address = address.replace(x, "", 1)
                while True:
                    n=n+1
                    address = start+" "+str(n)+base_address
                    eircode = get_eircode_from_address(address)
                    address = address.replace(", "+eircode,"")
                    if(eircode == "" or eircode == last_eircode):
                        break
                    else:
                        last_eircode = eircode
                    add_to_csv(eircode)
    addresses = get_addresses_from_address(address)
    if addresses != "" and test_address_starts_with_int(address) == False and start == blocks[-1]:
        for address in addresses:
            eircode = get_eircode_from_address(address)
            if eircode != "":
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

def generate_database(n=15):
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
generate_database()
#-------------------------------------------------------------
