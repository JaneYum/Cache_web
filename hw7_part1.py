# 507/206 Homework 7 Part 1
import requests
import json
from bs4 import BeautifulSoup

#### Your Part 1 solution goes here ####
#Cache
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        header = {'User-Agent': 'SI_CLASS'}
        resp = requests.get(url, headers=header)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

#### Implement your function here ####

def get_umsi_data(page=0,number = 20):
    url = 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All&page='
    url_page = url + str(page)
    page_text = make_request_using_cache(url_page)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    # and create a dictionary named umsi_titles
    # whose keys are the names of each person in the UMSI directory
    # each of which is associated value is that person's title and their emails
    name_div = page_soup.find_all(class_='field-name-title')
    title_div = page_soup.find_all(class_='field field-name-field-person-titles field-type-text field-label-hidden')
    contact_url = page_soup.find_all(class_='field field-name-contact-details field-type-ds field-label-hidden')
    umsi_titles = {}
    for i in range(number):
        name = name_div[i].find('h2').string
        title = title_div[i].string

        personal_url = contact_url[i].find('a')['href']
        baseurl = 'https://www.si.umich.edu'+ personal_url
        contact_text = make_request_using_cache(baseurl)
        contact_page_soup = BeautifulSoup(contact_text, 'html.parser')

        email= contact_page_soup.find(class_= "field field-name-field-person-email field-type-email field-label-inline clearfix")
        email_address = email.find('a').string

        person = {}
        person = {"title":title,"email":email_address}
        umsi_titles[name]=person
    return umsi_titles
    # page = 0 to 12

def every_page_info():
    page = 0
    umsi_titles = {}
    while page <= 11:
        onepage_dict = get_umsi_data(page = page)
        umsi_titles = {**umsi_titles,**onepage_dict}
        page +=1
    onepage_dict = get_umsi_data(page = 12,number=12)
    umsi_titles = {**umsi_titles,**onepage_dict}
    return umsi_titles

#### Execute funciton, get_umsi_data, here ####
umsi_titles = every_page_info()
#### Write out file here #####
with open("directory_dict.json","w") as f:
    json.dump(umsi_titles,f)
