######################################
##### OFFLINE SOURCE       ########### 
##### TO DO                ###########
##### DocBrowser API       ###########
##### Python 2,3.x         ###########
##########################################################
# A python script to generate the VistA cross reference ##
# web page and make sure that all the VistA files under ##
# web directory are copied to VistA Directory           ##
##########################################################

import urllib
import os, sqlite3 
from bs4 import BeautifulSoup as bs
import plistlib
from collections import OrderedDict
import json
import html5lib
from lxml.html import fromstring
import sys, bs4
sys.modules['BeautifulSoup'] = bs4

    #####################
    ### Configuration ###            
    #####################

metacount = 0
docset_name = 'VistA.docset'
input_ = 'VistA/code.osehra.org/dox/'
output = os.path.join(docset_name, 'Contents', 'Resources', 'Documents')
indexpath = 'VistA/code.osehra.org/dox/index.html'
    ### create directory ### 

if not os.path.exists(output): 
    os.makedirs(output)
    
icon = 'http://www.osehra.org/profiles/drupal_commons/themes/commons_osehra_earth/logo.png'
cc_icon = 'http://i.creativecommons.org/l/by/3.0/88x31.png'

    ### Add icons ### 

urllib.urlretrieve(icon, docset_name + "/icon.png")
urllib.urlretrieve(cc_icon, docset_name + "/88x31.png")

    #####################
    ###  Entry Types  ###            
    #####################
    
def insert_anchor():
    
    paths = ["globals.html", "filemanfiles.html", "Packages_Namespace_Mapping.html", "filemansubfiles.html", "routines.html", "packages.html"] 
    i =0
    while i < len(paths):    
        stype = ''
        name = ''
        path_ = ''
        entry = OrderedDict()
        entries = OrderedDict()
        jsonEntries = []
        validate = True
        header = {"name":"Methods","isHeader":validate}  
        jsonEntries.append(header) 
        page = open(os.path.join(output,paths[i]),'r').read() 
        from bs4 import SoupStrainer
        if paths[i] in 'packages.html': 
            stype = 'Package'  
        elif paths[i] in 'routines.html': 
            stype = 'Method'
        elif paths[i] in 'globals.html': 
            stype = 'Global'            
        elif paths[i] in 'filemanfiles.html': 
            stype = 'File' 
            list_fileman = []
            bsFile = bs(page, parse_only=SoupStrainer('td'))
            for a in bsFile.find_all('a'):
                text_ = ''
                entry = OrderedDict()
                add_path = '//apple_ref/cpp/Method/' 
                print('Running filemanfiles')
                name = urllib.unquote(a.get('href')).encode('utf-8')
                text_ = text_ + a.text
                text = text_
                path_ = urllib.unquote(name).encode('utf-8')
                if path_ in list_fileman: continue
                add_path += text
                list_fileman.append(path_) 
                entry['name'] = text_
                entry['path'] = add_path
                entry['entryType'] = stype
                jsonEntries.append(entry)
                entries['entries'] = jsonEntries
                with open(os.path.join(output,paths[i]) + ".dashtoc","w") as json_file:
                    json.dump(entries, json_file)
                json_file.close()
                try:
                    if name is not '':
                        cur.execute('INSERT INTO searchIndex(type, name, path) values(?, ?, ?)',(stype, text_,name+'#'+add_path))
                        print 'index already uploaded'
                except sqlite3.IntegrityError as err:
                    print(err)    
                    # sqlite3.IntegrityError: column bar is not unique          
        elif paths[i] in 'filemansubfiles.html': 
            stype = 'File' 
            list_fileman = []
            bsFile = bs(page, parse_only=SoupStrainer('td'))
            for a in bsFile.find_all('a'):
                entry = OrderedDict()
                add_path = '//apple_ref/cpp/Method/' 
                print('Running filemansubfiles')
                name = urllib.unquote(a.get('href')).encode('utf-8')
                path_ = urllib.unquote(name).encode('utf-8')
                if path_ in list_fileman: continue
                add_path += path_[:-len('.html')]
                list_fileman.append(path_) 
                entry['name'] = name[:-len('.html')]
                entry['path'] = add_path
                entry['entryType'] = stype
                jsonEntries.append(entry)
                entries['entries'] = jsonEntries
                with open(os.path.join(output,paths[i]) + ".dashtoc","w") as json_file:
                    json.dump(entries, json_file)
                json_file.close()
                try:
                    if name is not '':
                        cur.execute('INSERT INTO searchIndex(type, name, path) values(?, ?, ?)',(stype, name[:-len('.html')],name+'#'+add_path))
                        print 'index already uploaded'
                except sqlite3.IntegrityError as err:
                    print(err)            
        else:
            stype = 'Namespace' 
            list_fileman = []
            bsFile = bs(page, parse_only=SoupStrainer('td'))
            for a in bsFile.find_all('a'):
                entry = OrderedDict()
                add_path = '//apple_ref/cpp/Method/' 
                print('Running Namespaces_Packages_Mapping')
                name = urllib.unquote(a.get('href')).encode('utf-8')
                path_ = urllib.unquote(name).encode('utf-8')
                if path_ in list_fileman: continue
                add_path += path_[:-len('.html')]
                list_fileman.append(path_)
                entry['name'] = name[:-len('.html')] 
                entry['path'] = add_path
                entry['entryType'] = stype
                jsonEntries.append(entry)
                entries['entries'] = jsonEntries
                with open(os.path.join(output,paths[i]) + ".dashtoc","w") as json_file:
                    json.dump(entries, json_file)
                json_file.close()
                try:
                    if name is not '':
                        cur.execute('INSERT INTO searchIndex(type, name, path) values(?, ?, ?)',(stype, name[:-len('.html')],name+'#'+add_path))
                        print 'index already uploaded'
                except sqlite3.IntegrityError as err:
                    print(err)  
        bsFile = bs(page, 'html5lib')     
        for a in bsFile.find_all('a',attrs={'class':'el'}):
            entry = OrderedDict()
            add_path_global = ''
            name = urllib.unquote(a.get('href')).encode('utf-8') 
            text = a.text
            add_path = '//apple_ref/cpp/Method/'  
            without_html = name[:-len('.html')]    
            add_path_global += add_path + text  
            add_path += urllib.unquote(without_html).encode('utf-8')                 
            entry["name"] = name[:-len('.html')]
            entry["path"] = add_path
            if stype is 'Global':
                entry['name'] = text
                entry['path'] = add_path_global
            entry["entryType"] = stype
            jsonEntries.append(entry)
            entries["entries"]= jsonEntries  
            with open(os.path.join(output,paths[i]) + ".dashtoc","w") as json_file:
                json.dump(entries, json_file)
            json_file.close()
            jsonEntries_index = []
            entry = OrderedDict()
            entries_index = {}#each entry type node of main sub-html file
            header_index = {"name":stype,"isHeader":validate} 
            jsonEntries_index.append(header_index)
            raw_data = open(os.path.join(output,name),'r')
            dom =  fromstring(raw_data.read())
            indexmumps = dom.xpath('//p//span//a/@href')
            if not indexmumps: pass
            else:
                item = indexmumps[0]
                entry["path"] = indexmumps[0]
                entry["name"] = item[:-len('.html')]
                entry["entryType"] = stype
                entries_index["entries"] = entry
# #             
# #     ################################################################################## 
# #     ############# Validating the xpath to DOM by each href tag into each html ########
# #     ############# This should query DOM and validate stype for each Entry type #######
# #     ##################################################################################

            list_index = []  
            for link in dom.xpath('//td//a/@href'): # select the url in href for all a tags(links)
                print('Index from '+ name +' page: '+ link)
                entry = OrderedDict()            
                if link in list_index: continue
                entry["name"] = link[:-len('.html')]
                entry["path"] = link
                list_index.append(link)
                if '#' in link: continue
                entry["entryType"] = stype
                jsonEntries_index.append(entry)
                entries_index["entries"] = jsonEntries_index
                with open(os.path.join(output,path_) + ".dashtoc","w") as json_index:
                    json.dump(entries_index, json_index) 
                json_index.close()   
           
    # ################################################################################## 
    # ############# I want to parse and change the html with this anchor tag to ######## 
    # ############# identify query and Tree Explorer Interface from Zeal ###############
    # ############# Application how??????? #############################################  
    # ################################################################################## 

    ################################################################################## 
    ############# Also I want to complete the html with the rest anchor tag   ######## 
    ############# and also the rest of the html document including   ################# 
    ############# with the "name", "path", and "entryType" included    ###############
    ############# also save the databases ############################################  
    ##################################################################################
  
            try:
                if stype is 'Global':
                    cur.execute('INSERT INTO searchIndex(type, name, path) values(?, ?, ?)',(stype, text,name+'#'+add_path_global))
                 
                    continue
                cur.execute('INSERT INTO searchIndex(type, name, path) values(?, ?, ?)',(stype, name[:-len('.html')],name+'#'+add_path))
                print 'index already uploaded'
            except sqlite3.IntegrityError as err:
                    print(err)      
        i+=1
        
    ##########################
    ###  Table of Content  ###
    ###  TO DO             ###         
    ##########################
    
    ##########################################
    ####### Walking through Directories ######            
    ##########################################
  
    #####################
    ####### Saving ######            
    #####################
   
def create_meat_json():
    
    meta_json = {
     "name": "OSEHRA VistA Code Documentation",
     "revision": "2",
     "sourceId": "com.kapeli",
     "title": "vista api reference",
     "version": "1.1"
    }   
    with open(os.path.join(docset_name,"meta.json"), "w") as json_file:
        json.dump(meta_json, json_file)

def make_path(output):
     
    try:
        if not os.path.exists(output):
            os.makedirs(output) 
    except OSError:
        pass

def dest_path(p):
    '''Determines relative path of p to INPUT_DIR,
       and generates a matching path on OUTPUT_DIR.
    '''
    path = os.path.relpath(p,input_)
    return os.path.join(output,path)

keyword = "KEYWORD"
      
def add_docs():
    
    ### Souping index_page ###
    
    make_path(output)
    for path, dirs, files in os.walk(input_):
        for d in dirs:
            dir_path = os.path.join(path,d)
            # Handle case of OUTPUTDIR inside INPUTDIR
            if dir_path == output:
                dirs.remove(d)
                continue
            make_path(dest_path(dir_path))    
        for f in files:
            file_path = os.path.join(path, f)
            out_path = dest_path(file_path)
            with open(file_path, "rb") as fh, open(out_path, "wb") as fo:
                for line in fh:
                    if keyword not in line:
                        fo.write(line) 

    #####################
    ##### INFO_PLIST ####            
    ##################### 
   
def add_infoplist():
    
    try:
        with open(os.path.join(docset_name, 'Contents','Info.plist'),'w') as output_file:
            plistObj = {'CFBundleVersion':1.0,'CFBundleIdentifier':'VistA docset','DocSetPlatformFamily':'code','isDashDocset':True, 'DashDocSetFamily':'dashtoc','dashIndexFilePath':os.path.join(output,'index.html'),'DocSetFallbackURL':'http://code.osehra.org/dox/','NSHumanReadableCopyright':'Apex Data Solutions, LLC'}
            plistlib.writePlist(plistObj, output_file)
            output_file.seek(0)
    finally:
        output_file.close()

    #####################
    ###### SQLITE #######            
    ##################### 
    
db = sqlite3.connect(docset_name + '/Contents/Resources/docSet.dsidx')
db.text_factory = str

cur = db.cursor()

try:
    cur.execute('DROP TABLE searchIndex;')
except:pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

    ###### Start #######
    
add_docs() #DONE   
add_infoplist() #DONE
create_meat_json() #DONE
insert_anchor() #DONE

    ###### Commit and close #######

db.commit()
db.close()