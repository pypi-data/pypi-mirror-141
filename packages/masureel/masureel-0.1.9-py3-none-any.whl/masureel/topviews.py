topviewlist= []
from math import prod
import os
from pathlib import Path
import zipfile
from airtable import Airtable


base = "appVz0Sb0OZ0Cwng7"
path = "/Volumes/DOWNLOAD/1082"

def get_products(product_set):
    counter = 0
    tb = Airtable(table_name="Collectie", base_id=base, api_key=os.getenv("AIRTABLE_API_KEY"))
    table_list = tb.get_all()
    for t in table_list:
        #print(t)
        n = t["fields"]["code"] 
        if n in product_set:
          print(f"hey i recognize {n}")
          counter += 1

    print(f'script found {counter} topviews on F drive out of total {len(table_list)}')



def get_topviews():
  product_set = set()
  for t in Path(path).rglob("*.tif"):
    product_set.add(t.stem.upper())

  for x in Path(path).rglob("*.zip"):
    #print(x)
    if "Topview" in x.name:
      zip = zipfile.ZipFile(x.resolve())
      for file in zip.namelist():
        if "jpg" in file and '(g)' not in file:
          product= file.split('/')[-1].split('.')[0]
          
          if product not in product_set:
            product_set.add(product)

  return product_set

# tifs = glob.glob('**/*.txt', recursive=True)

# with os.scandir(dir) as it:
#     for entry in it:
#         if entry.name.endswith(".tif") and entry.is_file():
#             print(entry.name, entry.path)
#         if entry.name.endswith(".zip") and entry.is_file():
#             print(entry.name, entry.path)
#         if entry.is_dir:
#             print(entry.path)


# for p in os.listdir(dir):
#     sub = os.path.join(dir, p)
#     if os.path.isdir(sub):
#         print(f"{p} is dir so...")
#         for s in os.listdir(sub):
#             print(s)
#             if os.path.isdir(os.path.join(sub,s)):
#                 probe = os.path.join(sub, s)
#                 if os.path.isdir(probe):
#                     for file in os.listdir(probe):
#                         if "tif" in file:
#                             topviewlist.append(file.upper().split('.')[0])
#     if os.path.isfile:
#         print(f"{p} is a file, but is it zip?")



# with open('data/topviews.json', 'w') as f:
#     json.dump(topviewlist, f)


# tb = Airtable('appVz0Sb0OZ0Cwng7', 'Collectie', api_key=os.environ["AIRTABLE_API_KEY"])

# for x in tb.get_all():
#     if x["fields"]["code"] in topviewlist:
#         tb.update(x['id'], fields={'Topview found':'true'}, typecast=True)  