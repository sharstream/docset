# Doc Browser

This is the VistaJS Documentation Guide

## Overview

**Getting DocBrowserAPI with python Apps Development Ready**

> Stages:
> 
> 1. Development
> 
> 2. Test
> 
> 3. Stage
> 
> 4. Production
> 
> 5. Integration

**IDE & version control**

- liclipse (Eclipse plug-in to python)
- Git 

**Library**

- Python 2.7/3.3 ... (version compatibility)
- BeautifulSoup 4.4 ... (web scrap library)
- html5lib ... (html.parser)
- requests ... (url spider scarp)
- urllib ... (url file retriever)
- json ... (decoder)
- lxml, libxslt, lxmllib2 ... (xml parsers)
type the following command prompt: `python -m pip install lxml-3.4.4-cp27-none-win_amd64.whl` in cmd or batch

**Databases**

- SQLite3 

**Viewer**

- Zeal to Window
- Dash.app to iOS and Linux

Steps:

1. Create the SQLite Index:
 
							<docset name>.docset/Contents/Resources/docSet.dsidx
							CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);
							CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);
2. Populate the SQLite Index. You need to create a script (or application or whatever) that will go through your HTML documentation and add appropriate rows into the SQLite database. Rows can be added using this query:

							INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES ('name', 'type', 'path');
3. Calling through sqlite3 from python:

							db = sqlite3.connect('osehra/Contents/Resources/docSet.dsidx')

The values are:

- `name` is the name of the entry. For example, if you are adding a class, it would be the name of the class. This is the column that Dash searches.
- `type` is the type of the entry. For example, if you are adding a class, it would be "Class". For a list of types that Dash recognises, see below.
- `path` is the relative path towards the documentation file you want Dash to display for this entry. It can contain an anchor (#). Alternatively, Dash also supports http:// URL entries.


**Considerations:**

1. Create a project structure
2. Copy the documentation into the structure
3. Scan the documentation for the information you wish to index
4. Update the sqlite database in the structure with the index information

**Structure src:**

`online_osehra.py`: script file that manages the download source of Osehra repository dynamically from a server. 

`offline_osehra.py`: script file that manages the download source of Osehra repository physically from a computer.

**Making a soup:**

BeautifulSoup lib version 4.0 is a python lib for pulling data out of HTML and XML files. It works with some parser to navigate, search and modify the parse tree. In osehra’s code guide there are some reference tags that contain source attributes to move on to other html files. Create a BeautifulSoup Object from string can perform the searching into html document:

    import urllib2
    from bs4 import BeautifulSoup
    url = "http://code.osehra.org/dox/index.html"
    html_page = urllib2.urlopen(url)
    soup_object = BeautifulSoup(html_page)

Also the BeautifulSoup lib has methods like find_all that  look through osehra tags and return a list of references as following:

    ...
    <a href = 'index.html'>Home</a>
	<a href = 'packages.html'>Package List</a>
	<a href = 'routines.html'>Routine Alphabetical List</a>
	<a href = 'globals.html'>Global Alphabetical List</a>
	<a href = 'filemanfiles.html'>FileMan Files List</a>
	<a href = 'filemansubfiles.html'>FileMan Sub-Files List</a>
	<a href = 'Packages_Namespace_Mapping.html'>
	Package-Namespace Mapping</a>
	<a href = 'https://github.com/OSEHRA-Sandbox/VistA-M/tree/FOIA_May_2015/'>
	repository</a>
    ...

**Installation packages:**

to install the BeautifulSoup, html5 and requests libs type in shell:

	$ python setup.py install

in each lib folders.

**Saving list of index in osehra API docset**

Type `Ctrl + B` in *python shell* over `scrap_osehra.py` file  to show the following result:

    DB add >> name: , path: http://code.osehra.org/dox/http://www.osehra.org
    DB add >> name: Home, path: http://code.osehra.org/dox/index.html
    DB add >> name: Package List, path: http://code.osehra.org/dox/packages.html
    DB add >> name: Routine Alphabetical List, path: http://code.osehra.org/dox/routines.html
    DB add >> name: Global Alphabetical List, path: http://code.osehra.org/dox/globals.html
    DB add >> name: FileMan Files List, path: http://code.osehra.org/dox/filemanfiles.html
    DB add >> name: FileMan Sub-Files List, path: http://code.osehra.org/dox/filemansubfiles.html
    DB add >> name: Package-Namespace Mapping, path: http://code.osehra.org/dox/Packages_Namespace_Mapping.html
    DB add >> name: repository, path: http://code.osehra.org/dox/https://github.com/OSEHRA-Sandbox/VistA-M/tree/FOIA_May_2015/

**Scrapping list of index**

    ...
    <a href = 'Package_Web_Services_Client.html'>Web Services Client</a>
    <a href = 'Package_Wireless_Medication_Administration.html'>Wireless Medication Administration</a>
    <a href = 'Package_Womens_Health.html'>Womens Health</a>
    <a href = 'Package_Wounded_Injured_and_Ill_Warriors.html'>Wounded Injured and Ill Warriors</a>
    <a href = 'http://creativecommons.org/licenses/by/3.0/'>Creative Commons Attribution 3.0 Unported License</a>
    Namespaces: 150
    ...