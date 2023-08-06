import os
import re
import shutil
import datetime
from typing import Callable, Dict
import jinja2
import cyrtranslit
from pathlib import Path

_BUILD_PATH  = "_build"
_EXPORT_PATH = "export"
_BUILD_YAML_PATH = "_build/index.yaml"
_BUILD_STATIC_PATH = "_build/_static"
_BUILD_IMAGE_PATH = "_build/_image"

_FILTER = {"doctrees", "_sources", ".buildinfo", "search.html",
                        "searchindex.js", "objects.inv", "pavement.py","course-errors.js","genindex.html","index.yaml"}                       
_EXTENSION_LIST = ['md', 'rst', 'ipynb', 'txt', 'html'] 

_TEMPLATE_PATTERN = re.compile(r"^.*(\.t)\.[^\.]+$")

def filter_name(item :str) -> bool:
        if item not in _FILTER:
            return True
        else:
            return False

def copy_dir(src_dir :str, dest_dir: str, filter_name:Callable[[str], bool] = None) -> None:
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for item in os.listdir(src_dir):
        if filter_name and not filter_name(item):
            continue
        s = os.path.join(src_dir, item)
        if os.path.isdir(s):
            d = os.path.join(dest_dir, item)
            copy_dir(s, d, filter_name)
        else:
            d = os.path.join(dest_dir, item)
            try:
                shutil.copyfile(s, d)
            except FileNotFoundError:
                pass

def default_template_arguments() -> Dict[str, datetime.date]:
    return {"now":datetime.datetime.now()}

def apply_template_dir(src_dir, dest_dir, template_params, filter_name=None) -> None:
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for item in os.listdir(src_dir):
        if filter_name and not filter_name(src_dir, item):
            continue
        s = os.path.join(src_dir, item)     
        if os.path.isdir(s):
            d = os.path.join(dest_dir, item)
            apply_template_dir(s, d, template_params, filter_name)
        else:
            match = _TEMPLATE_PATTERN.match(item)
            if match:
                i,j = match.span(1)
                d = os.path.join(dest_dir, item[:i] + item[j:])
                with open(s, "r", encoding='utf8') as sf:
                    t = jinja2.Template(sf.read())
                dtext = t.render(template_params)
                with open(d, "w", encoding='utf8') as df:
                    df.write(dtext)
            else:
                d = os.path.join(dest_dir, item)
                shutil.copyfile(s,d)

def title_fix(srt_content: str) -> str:
    new_content_rows = srt_content.split('\n')
    top_title = re.search(r"^([=|\~]|\-|\'|\:)\1*$",new_content_rows[0])    
    if(top_title is not None and ((new_content_rows[0])!= len(new_content_rows[1]))):
        new_content_rows[0] = new_content_rows[0][0]*len(new_content_rows[1]) 
    for i in range (1,len(new_content_rows)):
        title = re.search(r"^([=|\~]|\-|\'|\:)\1*$",new_content_rows[i-1])
        underline = re.search(r"^([=|\~]|\-|\'|\:)\1*$",new_content_rows[i])
        if((underline is not None) and (new_content_rows[i-1])!= len(new_content_rows[i]) and (title is None)):
            new_content_rows[i]=new_content_rows[i][0]*len(new_content_rows[i-1])
    srt_content=""
    for row in new_content_rows:
        srt_content+= row+"\n"
    return srt_content.rstrip()+"\n"

def cyrl_to_latin(src_dir: str, dest_dir: str) -> None:
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for item in os.listdir(src_dir):
        extension = os.path.splitext(item)[1][1:]
        s = os.path.join(src_dir, item) 
        if os.path.isdir(s):
            d = os.path.join(dest_dir, item)
            cyrl_to_latin(s, d)
        else:
            d = os.path.join(dest_dir, item)
            shutil.copyfile(s,d)
            f = open(s, encoding="utf8")
            content = f.read()
            newF = open(d, "w", encoding="utf8")
            newF.truncate(0)          
            if extension in _EXTENSION_LIST:
                new_content = cyrtranslit.to_latin(content, 'sr')
                if(extension == "rst"):
                    new_content = title_fix(new_content)
                newF.write(new_content)
            else:
                newF.write(content)
            newF.close()
            
def delete_dir(dir: Path) -> None:
    if os.path.exists(dir):
        try:
            shutil.rmtree(dir)
        except:
            print("Unable to delete directory {} and or files in the directory. Check if the directory is open in another program.".format(dir))

def delete_file(file: str) -> None:
    if os.path.exists(file):
        try:
            os.remove(file)
        except:
            print("Unable to delete the file {}. Check if they are open in another program.".format(file))