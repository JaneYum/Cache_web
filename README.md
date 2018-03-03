
web cache and json write


# json write
test_dict = {'bigberg': [7600, {1: [['iPhone', 6300], ['Bike', 800], ['shirt', 300]]}]}
print(test_dict)
print(type(test_dict))

# dumps - string
json_str = json.dumps(test_dict)
print(json_str)
print(type(json_str))

# load - string changed to dict
new_dict = json.loads(json_str)


# load:把文件打开，并把字符串变换为数据类型
with open("../config/record.json",'r') as load_f:
    load_dict = json.load(load_f)

# dump: dict write into Json file
with open("../config/record.json","w") as f:
    json.dump(new_dict,f)
    
    
# Cache
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
