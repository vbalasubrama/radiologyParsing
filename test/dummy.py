# from ast import literal_eval as make_tuple
# str = "(109, 7, 35, -1)"
# print make_tuple(str)#str.rfind('X')

import fileinput
for line in fileinput.FileInput("file",inplace=1):
    if line.rstrip():
        print line