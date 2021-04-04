import requests
from bs4 import BeautifulSoup
import pandas as pd

reload = True
files = ['annotated_wd_data_train_answerable.txt'] #'annotated_wd_data_valid_answerable.txt', 'annotated_wd_data_test_answerable.txt']

for file_name in files:

   print(f"### Working on {file_name}")
   save_file = file_name.split(".txt")[0]
   save_file = f"n_{save_file}.csv"
   print(f"### Saving on {save_file}")

   e_base_url = "https://www.wikidata.org/wiki/"
   p_base_url = "https://www.wikidata.org/wiki/Property:"
   t_list = {'e1': [], 'p': [], 'e2': [], 'q': []} 

   f = open(file_name)
   lines = f.readlines()
   if reload: 
      _df = pd.read_csv(save_file)
      p_linenum = len(list(_df['e1'])) 
      lines = lines[p_linenum:]
   for line_num, line in enumerate(lines):
      
      if line_num % 100 == 0:
         debug = True
         print(f"---Working in {line_num}/{len(lines)}")
         _df = pd.read_csv(save_file)
         t_list['e1'] += list(_df['e1'])
         t_list['p'] += list(_df['p'])
         t_list['e2'] += list(_df['e2'])
         t_list['q'] += list(_df['q'])
         df = pd.DataFrame(t_list)
         df.to_csv(save_file)
         print(f"Saving .. {save_file}, # of lines: {len(t_list['e1'])}")
         t_list = {'e1': [], 'p': [], 'e2': [], 'q': []} 

      else:
         debug = False
      
      reverse = False
      if debug: print(line)
      e1, p, e2, q = line.split("\t")
      if debug: print(f"e1: {e1}, p: {p}, e2: {e2}, q: {q}")
      extract = [e1, p, e2, q]
      ret = []
      for i, elem in enumerate(extract):
         if i == 1:
            if 'P' in p:
               url = p_base_url+elem
            elif 'R' in p:
               elem = "P"+elem.split("R")[1]
               url = p_base_url + elem
            else:
               print("*** Should be P or R!")
         elif i == 3:
            print(f"question: {q}")
            continue
         else:
            url = e_base_url+elem
   
         try:
            if debug: print(f"url: {url}")
            req = requests.get(url)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.select_one("#firstHeading > span > span.wikibase-title-label")
            text = text.get_text()
            if debug: print(f"text: {text}")
            ret.append(text)
         except:
            continue
      
      if len(ret) == 3:
         if reverse:
            t_list['e1'].append(ret[2])
            t_list['p'].append(ret[1])
            t_list['e2'].append(ret[0])
            t_list['q'].append(q)
         else: 
            t_list['e1'].append(ret[0])
            t_list['p'].append(ret[1])
            t_list['e2'].append(ret[2])
            t_list['q'].append(q)
      else:
         print(f"**!!*!*!*!*!*!*! ERROR|| ret: {ret}, extract: {extract}")

   debug = True
   print(f"---Working in {line_num}/{len(lines)}")
   _df = pd.read_csv(save_file)
   t_list['e1'] += list(_df['e1'])
   t_list['p'] += list(_df['p'])
   t_list['e2'] += list(_df['e2'])
   t_list['q'] += list(_df['q'])
   df = pd.DataFrame(t_list)
   df.to_csv(save_file)
   print(f"Saving .. {save_file}, # of lines: {len(t_list['e1'])}")
   
   """
   df = pd.DataFrame(t_list)
   df.to_csv(f"{save_file}")
   print(f"Saving .. n_{file_name.split('.txt')[0]}.csv")
   print(f"total number: {len(lines)} to {len(t_list['e1'])}")
   """
