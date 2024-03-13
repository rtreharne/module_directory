from canvasapi import Canvas
import getpass
import datetime
import tqdm
import re
import os
from bs4 import BeautifulSoup

override_pages = False


def filter_files(regex, dirname="formatted_html"):
    for root, dirs, files in os.walk(dirname):
        for file in files:
            if not re.search(regex, file):
                os.remove(os.path.join(root, file))

def disable_anchor_tags(dirname="formatted_html"):
    for root, dirs, files in os.walk(dirname):
        for file in files:
            with open(os.path.join(root, file), "r", encoding='utf-8') as f:
                data = f.read()
                data = data.replace("<a", "<a disabled href")
            with open(os.path.join(root, file), "w", encoding='utf-8') as f:
                f.write(data)

def get_or_create_canvas_module(course, title="Module Directory 202324"):

    # Get all modules in course
    modules = [x for x in course.get_modules()]

    # If module already exists, return

    for module in modules:
        if module.name == title:
            print(f"Module '{title}' already exists.")
            return module
        
    # Create module
    print(f"Creating module '{title}'")
    module = course.create_module({"name": title}) 

    return module

def get_title_and_html(fpath):
    with open(fpath, "r", encoding='utf-8') as f:
        html = f.read()
        title = fpath.split("\\")[-1].split(".")[0]
    
    return title, html


def get_or_create_canvas_page(pages, course, title, html):
    items = pages

    html = html.split("<script")[0]

    global override_pages

    for item in items:
        
        if item.title == title:
            if override_pages:
                item = item.edit(wiki_page={"title": title, "body": html})
                return item
            else:
                override = input(f" '{title}' already exists. Override? (y/n/a): ")
                if override == "y":
                    item = item.edit(wiki_page={"title": title, "body": html})
                    return item
                elif override == "n":
                    return item
                elif override == "a":
                    item = item.edit(wiki_page={"title": title, "body": html})
                    override_pages = True
                    return item
        
    # Create Canvas page
    page = course.create_page(wiki_page={"title": title, "body": html})

    return page

def strip_attributes(html, attributes):
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup():
        for attribute in attributes:
            del tag[attribute]

    return str(soup)

def main():
    print(
"""
                      ░▓▓░   ░░                             
                       ░░    ▓▓                             
                   ░░       ░██░       ░░                   
                 ░░█▒░  ░██████████░  ░▒█░░                 
            ░▒░  ░░█▒░░     ░██░      ░▒█░░ ░░▒░            
             ▒     ░░        ▓▓        ░░    ░▒             
                    ░░░      ░░      ░░░                    
                 ▓███████▓░      ░▓███████▓                 
        ░▒▒░   ▒██▒░░░  ▒██▒░  ░▒██▒░░▒ ░▒██▒   ░▒▒░        
        ░███▓ ░██░░█▒    ░██░░░░██░░▓▓░▒█░░██░ ▓███░        
        ░▓░▓█▒▒█▒░▓░      ▒██████▒░█░░█░░  ▒█▒▒█▓░▓░        
         ░ ▒█▓░██░        ▓█▒░░▒█▓░░▓▓░   ░██░▓█▓ ░         
          ░▓██░▓█▓░     ░▒██░  ░▓█▓░     ░▓█▓░██▓░          
          ░████░░███▓▓▓███▒░    ░▒███▓▓▓███░░████░          
          ▒▒▒██░  ░▒▓▓▓▒░░        ░░▒▓▓▓▒░  ░██▒▒▒          
           ░███░       ░░░░      ░░░░       ░███░           
           ▒███░     ▒██████▒  ▒██████▒     ░███▒           
          ░██▒░    ▒████████████████████▒    ░▒██░          
         ░▓█████▓███████████▒░░▒███████████▓▓████▓░         
         ░███████████████▓░      ░▒███████████████░         
         ▓██▓███░░░░░░░     ░▓▓░     ░░░░░░░███▓██▓░        
        ░▓█░▓█████▓▓▓▓▓ ░  ▒████▒  ░ ▓▓▓▓▓█████▓░█▓░        
         ▒▓░███████████░▓░░██████░░█░███████████░▓▒         
          ░ █████████████▓▒██████▒▓█████████████ ░          
            ░██▒████████████████████████████▒██░            
             ▓█░████████████████████████████░█▓░            
             ░▓░▒██████████████████████████▒░▓░             
                 ▓██▒▓████████████████▓▒██▓                 
                 ░██▒░███▓▓███████▓███▒▒██░                 
                   ▒█░▒██▓▒██████▓▒██▒░█▒                   
                    ░░░░██░▓█████░▓█░ ░░                    
                         ▒▒░▓███░▒▒░                        
                             ▒▓                                             
""" )
    print("")
    print("www.canvaswizards.org.uk")
    print("")
    print("Welcome to the Canvas Module Directory Creator!")
    print("By Robert Treharne, University of Liverpool. 2024")
    print("")

    # if config.py exists, import it
    try:
        from config import CANVAS_URL, CANVAS_TOKEN
    except ImportError:
        CANVAS_URL = input('Enter your Canvas URL: ')
        print("")
        CANVAS_TOKEN = getpass.getpass('Enter your Canvas token: ')
        print("")

    # if course_id in config.py, use it
    try:
        from config import course_id
    except ImportError:
        course_id = int(input('Enter the course ID: '))
        print("")

    # create Canvas object
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)

    # get course
    course = canvas.get_course(course_id)

    # create regex to filter 'LIFEXXX'
    regex = re.compile(r"LIFE\d{3}")

    print("Filtering files ...")

    print("")

    filter_files(regex) # Ignores all html files that don't match the regex

    print("Disabling anchor tags ...")
    
    print("")
    disable_anchor_tags() # Disables all anchor tags in html files

    # get or create module
    module = get_or_create_canvas_module(course, title="Module Directory 202324")

    # get all pages in course
    pages = [x for x in course.get_pages()]

    # organise pages in alphabetical order by title
    pages = sorted(pages, key=lambda x: x.title)

    # create index page html

    index_html = """<table style="width:100%">"""

    for root, dirs, files in os.walk("formatted_html"):
        for file in tqdm.tqdm(files, desc="Creating module directory ..."):
            title, html = get_title_and_html(os.path.join(root, file))
            page = get_or_create_canvas_page(pages, course, title, html)
            index_html += f"<tr><td><a href='{page.url}'>{title}</a></td></tr>"
    
    index_html += "</table>"
    page = get_or_create_canvas_page(pages, course, "Module Directory 202324", index_html)
    module.create_module_item({"type": "Page", "content_id": page.page_id, "page_url": page.url, "title": page.title})

if __name__ == "__main__":

    main() # Creates module directory in Canvas
    