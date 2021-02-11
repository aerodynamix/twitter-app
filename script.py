#!/usr/bin/env python3

PATHX = "/usr/local/lib/python3.9/site-packages/rest_framework_swagger" \
        "/templates/rest_framework_swagger/index.html"

filex = open(PATHX, "r")
lines = filex.readlines()
lines[1] = "{% load static %}\n"

filex = open(PATHX, "w")
filex.writelines(lines)
filex.close()
