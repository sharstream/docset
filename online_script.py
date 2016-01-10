    ##################################
    # ONLINE SOURCE        ########### 
    # TO DO                ###########
    # DocBrowser Class API ###########
    # Python 2,3.x         ###########
    ##################################

# define a variable to hold the source URL
# In this case we'll try to use the free data feed 
# This feed lists all index from ochera url

import re
#import requests
import urllib, urllib2 
import os, sqlite3
from bs4 import BeautifulSoup  as bs, NavigableString#, SoupStrainer
from urllib import urlretrieve
from io import StringIO#, BytesIO
from lxml.html import parse, fromstring, tostring#, etree
from json import loads

    #####################
    ### Configuration ###            
    #####################

metacount = 0
docset_name = 'Osehra.docset'
root_url = 'http://code.osehra.org/dox/'
root_new = 'http://code.osehra.org/OSEHRA_dox/'

global root_index

if root_url is not None:
    root_index = root_url
else:
    root_index = root_new

output = docset_name + '/Contents/Resources/Documents/'

    ### create directory ### 

if not os.path.exists(output): 
    os.makedirs(output)

icon = 'http://www.osehra.org/profiles/drupal_commons/themes/commons_osehra_earth/logo.png'
cc_icon = 'http://i.creativecommons.org/l/by/3.0/88x31.png'

    ### Add icons ### 

urllib.urlretrieve(icon, docset_name + "/icon.png")
urllib.urlretrieve(cc_icon, docset_name + "/cc_icon.png")

def save_shapes(path):
    urlretrieve(root_url + path, output + urllib.unquote(path).encode('utf8'))
    
    #####################
    ### Anchor/Content ##            
    #####################
    
# def insert_anchor():
#     modules = {}
# #     for fname in os.listdir(output):
#     file_ = open(os.path.join(output,'routines.html')).read()#fname loop
#     soup = bs(file_,"lxml")
#     img_ = {}
#     href = {}
#     print soup
# #     any_ = re.compile('.*')
#     for tag in soup.findAll('el', href=True):
#         print tag
#         print tag.string
#     save_images(os.path.join(output,'routines.html'))
# 
#     untypes = set()
#     for fname, tree in soup.iteritems():
#         with open(os.path.join(output, fname), 'w') as htmlfile:
#             htmlfile.write("""<!doctype html>
#                             <html>
#                             <head>
#                                 <link rel="stylesheet" href="../css/DoxygenStyle.css" type="text/css" />
#                                 <link rel="stylesheet" href="../css/code_pretty_scripts/prettify.css" type="text/css" />
#                                 <link rel="stylesheet" href="../css/footer.html" type="text/css" />
#                                 <link rel="stylesheet" href="../css/header.html" type="text/css" />
#                                 <link rel="stylesheet" href="../css/index.html" type="text/css" />
#                                 <link rel="stylesheet" href="../css/source_header.html" type="text/css" />
#                                 <style>
#                                     body {
#                                         margin: 2em;
#                                     }
#                                     .members .member .short {
#                                         display: none;
#                                     }
#                                     .members .member .long {
#                                         display: block;
#                                     }
#                                 </style>
#                             </head>
#                             <body>
#                             <span style="font-size:2em; font-weight:bold">%s</span>
#                             <div id="center-container" class="class-overview"><div class="x-panel-body">"""%fname[:-len('.html')]) 
#             
#             for a in tree.find_all('//a'):
#                 if 'href' not in a.attrib: continue
#                 if a.attrib['href'].startswith('source/'):
#                     a.attrib['href'] = '../' + a.attrib['href']
#                 else:
#                     if not a.attrib['href'].startswith('#'): continue
#                     ignore = ['/guide/', '/example/', '/guides/', '/video/']
#                     if any(i in a.attrib['href'] for i in ignore): continue
#                     
#                     fragment = a.attrib['href'].replace('#!/api/', '')
#                     def cfg():
#                         return fragment.replace('property-', 'cfg-')
#                     
#                     if fragment in ids:
#                         a.attrib['href'] = ids[fragment][0] + '#' + ids[fragment][1]
#                     elif cfg() in ids:
#                         a.attrib['href'] = ids[cfg()][0] + '#' + ids[cfg()][1]
#                     elif fragment == '#':
#                         # remove JS elements
#                         a.getparent().remove(a)
#                     else:
#                         if os.path.isfile(os.path.join(output, fragment+'.js')):
#                             a.attrib['href'] = fragment+'.html'
#                         else:
#                             print fragment, 'missing.'
#                                         
#             for pre in tree.find_all('//pre'):
#                 if not pre.attrib.get('class'):
#                     # enables CSS
#                     pre.attrib['class'] = 'notpretty'
#                                       
#             for section in tree.getroot().find_class('members-section'):
#                 stype = section.find('h3').text
#                 try:
#                     idxtype = {'Methods': 'clm',
#                                'Properties': 'Property',
#                                'Config options': 'Option',
#                                'Events': 'event',
#                                'CSS Mixins': 'Mixin',
#                                'CSS Variables': 'var'}[stype]
#                 except KeyError:
#                     untypes.add(stype)
#                     idxtype = 'unknown'
#                 for member in section.find_class('member'):
#                     membername = member.xpath('div[@class="title"]/a/text()')
#                     if not len(membername): continue
#                     membername = membername[0]
#                     member.insert(0, fromstring("<a name='//apple_ref/cpp/%s/%s' class='dashAnchor' />" % (idxtype, membername)))
#                     if member.find_class('defined-in')[0].text and \
#                             member.find_class('defined-in')[0].text != fname[:-len('.html')]:
#                         assert member.find_class('defined-in')[0].text + '.html' in trees, member.find_class('defined-in')[0].text
#                         continue
#                     cur.execute('INSERT INTO searchIndex(type, name, path) values(?, ?, ?)',
#                         (idxtype, fname[:-len('html')]+membername,
#                          os.path.join('html', fname)+'#'+member.attrib['id']))
#                     
#             cur.execute('INSERT INTO searchIndex(type, name, path) values("cl", ?, ?)',
#                     (fname[:-len('.html')], os.path.join('html', fname)))
#             htmlfile.write(tostring(tree))
#             
#             print(htmlfile)
#             
#             htmlfile.write("""</body></div></div></html>""")
#             
#     #####################
    ####### XPath #######            
    #####################
        
    #####################
    ####### Saving ######            
    #####################
    
def mump_examples(path):
    url_to = os.path.join(root_url, path)
    routine = bs(urllib2.urlopen(url_to))
    span_tags = routine.find_all('span')
    for mump in span_tags:
        href = mump.get('href')
        path_enc = urllib.unquote(href).encode('utf8')
        urlretrieve(root_url + path, output + path_enc)

def save_index(path):                
    url_retrieve = urllib.unquote(os.path.join(root_index, path)).encode('utf8')
    output_ = urllib.unquote(os.path.join(output, path)).encode('utf8')
    urlretrieve(url_retrieve, output_)   
        
def update_db(name, path):
    typ = 'func'
    cur.execute("SELECT rowid FROM searchIndex WHERE path = ?", (path,))
    fetched = cur.fetchone()                
    if fetched is None:
        cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, typ, path))
        urlretrieve(root_url + path, output + urllib.unquote(path).encode('utf8'))
        print('DB add >> name: %s, path: %s' % (name, path))  
    else:
        print("record exists")

def save_images(path):
    
    ### Files download ###
    
    url = urllib.urlopen(root_index + path).read()
    soup = bs(url)
    images = soup.find_all('img')                 
    for image in images:
        url_retrieve = os.path.join(input, image['src'])
        input_ = urllib.unquote(url_retrieve).encode('utf8')
        out = os.path.join(output, image['src'])
        output_ = urllib.unquote(out).encode('utf8')
        urlretrieve(input_, output_)
    
def save_package_folders(path):
    
    ### Directory download ###
    
    subdir = path
    folder_uni = os.path.join(output, subdir)
    folder = urllib.unquote(folder_uni).encode('utf8')
                            # read these folders ['$P($P(REC(_diagnosis_,I),U,3),_', '$P(URL,__', '$S(DATA=0__N', 'BMP', 'STRCAT(Data', 'DATA__Interest', 'DATA___COUNT____', 'DATA_$E(DATE,4,5)__', 'code_pretty_scripts' ]
                            # not exists:
                            # Z, Y, X Folders, 
                            # Wireless Medication Admin, 
                            # Pharmacy Product System National,
                            # Pharmacy Enterprise Customization System,
                            # Occupational Health Record-Keeping System,
                            # Medication Order Check Healthcare Application,
                            # N Folder,
                            # MCCR National Database - Field,     
                            # J Folder, 
                            # Integrated Home Telehealth,
                            # FileMan Delphi Components,
                            # CPRS Plugins
                            # Folders. 
    if not os.path.exists(folder):
        os.makedirs(folder)    
     
def add_urls(saved):

    ### Souping index_page ###

    paths = ["index.html", "packages.html", "routines.html", "globals.html", "filemanfiles.html", "filemansubfiles.html", "Packages_Namespace_Mapping.html"]

    i = 0   
    while i < len(paths):
        
    #####################
    ####### URL #########            
    ##################### 
         
        url = root_index + paths[i] 
        page = urllib2.urlopen(url)
        soup = bs(page)
        page.close()
        
        any_ = re.compile('.*')
        body = soup.find('body')
        centers = body.find_all('center')
     
    ####### Index download ######### 
              
        try:
            if centers is not None and saved is False:      
                for index in centers[0].find_all('a'):
                    save_index(index.get('href'))
                saved = True
        except:
            pass

        tbody = soup.find('tbody')
        if tbody is not None:
            hrefs = tbody.find_all('a', {'href':any_})
            for href in hrefs:             
                name = href.text.strip().replace('\n', '') 
                path = href.get('href')
                filtered = ('http://code.osehra.org', '/', 'dox') 
                try:
                    if path is not None and name is not None and not path.startswith(filtered):
                        update_db(name, path) 
                        if paths[i] in 'packages.html':                              
                            shapes = soup.find_all('area', {'href': any})
                            save_package_folders(href.text)   
                            path_pack = urllib.unquote(href.get('href')).encode('utf8') 
                            urlretrieve(root_url + path, output + urllib.unquote(path).encode('utf8'))
                            try:
                                save_images(path_pack)
                            except:
                                pass
                            for shape in shapes:
                                save_shapes(shape.et('href'))
                        elif paths[i] in 'routines.html':                            
#                             mump_examples(path)
                            save_images(path)                                          
                except:
                    pass
        i+=1

def surrounded_by_strings(tag):
    
    return (isinstance(tag.next_element, NavigableString)
        and isinstance(tag.previous_element, NavigableString))

def strip_tags(html, invalid_tags):
    
    soup = bs(html)

    for tag in soup.find_all(True):
        if tag.name in invalid_tags:
            s = ""

            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(unicode(c), invalid_tags)
                s += unicode(c)

            tag.replaceWith(s)

    return soup

def add_infoplist():
    CFBundleIdentifier = 'Osehra'
    CFBundleName = 'Vista API'
    DocSetPlatformFamily = 'code'
    index_path = os.path.join(output,'code.osehra.org','dox')
    info = " <?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
         "<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\"> " \
         "<plist version=\"1.0\"> " \
         "<dict> " \
         "    <key>CFBundleIdentifier</key> " \
         "    <string>Osehra</string> " \
         "    <key>CFBundleName</key> " \
         "    <string>ista API</string>" \
         "    <key>DocSetPlatformFamily</key>" \
         "    <string>code</string>" \
         "    <key>dashIndexFilePath</key>" \
         "    <string>Osehra.docset/Contents/Resources/Documents/</string>" \
         "    <key>DashDocSetFallbackURL</key>" \
         "    <string>http://code.osehra.org/dox/index.html</string>" \
         "</dict>" \
         "</plist>".format(CFBundleIdentifier, CFBundleName, DocSetPlatformFamily, index_path)
    open(docset_name + '/Contents/info.plist', 'wb').write(info)

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
    
saved = False

# add_urls(saved)
add_infoplist()
# insert_anchor()

    ###### Commit and close #######

db.commit()
db.close()
