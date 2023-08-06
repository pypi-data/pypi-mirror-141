import re
import sys
def say_hello():
    print("Hello!")

def say_goodbye():
    print("Goodbye!")

def ReadTxt(path):
    with open(path, 'r') as file:
        file_contents = file.read()
    return file_contents

def CountSentences(file_contents):
    delimiters=[".","?","!"]
    regexPattern = '|'.join(map(re.escape, delimiters))
    sentences=re.split(regexPattern, file_contents)
    for i in sentences:
        i.strip(" ")
    sentences = [i for i in sentences if len(i)>0]
    return len(sentences)

def CountWords(file_contents):
    delimiters = [";", ",", ".", "!","?",":"]
    regexPattern = '|'.join(map(re.escape, delimiters))
    words=re.split(regexPattern, file_contents)
    for i in words:
        i.strip("\n")
    words = [i for i in words if len(i)>0]
    return len(words)

def Frequency(file_contents):
    delimiters = [";", ",", ".", "!","?",":"," "]
    regexPattern = '|'.join(map(re.escape, delimiters))
    words=re.split(regexPattern, file_contents)
    for i in words:
        i.strip("\n")
    l = [i for i in words if len(i)>0]
    
    d = dict()
    for i in l:
        if i != '':
            if i.lower() in d.keys():
                d[i.lower()] += 1
            else:
                d[i.lower()] = 1

    #print(d)
    return d

def FrequencyEquals1(file_contents):
    d = Frequency(file_contents)
    #print(d)
    d1 = dict()
    for i in d:
        if d[i]==1:
            #print(i)
            d1[i]=1
    return d1



