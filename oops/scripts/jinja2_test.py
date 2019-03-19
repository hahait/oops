#!/usr/bin/env python

from jinja2 import PackageLoader,Environment,FileSystemLoader
import os

env = Environment(loader=FileSystemLoader("./"))
templ = env.get_template("index.html")
templ_result = templ.render(aa='123',bb='234')

def render(tpl_path, **kwargs) :
    path, filename = os.path.split(tpl_path)
    return Environment(loader=FileSystemLoader(path)).get_template(filename).render(**kwargs)