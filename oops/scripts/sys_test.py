#!/usr/bin/env python

import fileinput

for line in fileinput.input():
    print(
        "文件名：",fileinput.filename(),
        "读的是第几行: ",fileinput.filelineno(),
        "读的行内容: ", line
    )