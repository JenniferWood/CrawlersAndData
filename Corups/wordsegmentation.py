# -*- coding: utf-8 -*-
import sys
 
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import jieba
import jieba.posseg

jieba.load_userdict('mydictFM.txt')
stopkey=[line.strip() for line in file('stopwords.txt')]
splitkey = ['，','。','！','？',' ',' ','~','～','、',':',"："]

resourcedir = "/Users/apple/Documents/GITHUB/基于评论的推荐/Corups/jdata/BK/"
resultdir = "/Users/apple/Documents/GITHUB/基于评论的推荐/Corups/jd-jieba/BK/"


def eachFile(shop):
    filepath = resourcedir+shop+"/"
    print filepath
    pathDir = os.listdir(filepath)
    for file in pathDir:
        if os.path.exists(resultdir+shop+"/") is False:
            os.makedirs(resultdir+shop+"/")

        #if os.path.exists(resultdir+shop+"/"+file) is False:
            #print "Word Segmenting :",shop+"/"+file
        splitSentence(filepath+file,resultdir+shop+"/"+file)

def splitSentence(inputFile, outputFile):
    fin = open(inputFile, 'r')
    fout = open(outputFile, 'w')
    outstr = []

    for line in fin:
        line = line.strip()

        #wl = jieba.cut(line)
        line = jieba.posseg.cut(line)

        for w in line:
            #if w.flag == 'x':
            ww = w.word.encode('utf-8')
            if ww in splitkey or ww.strip()=='':
                if len(outstr)==0:continue
                fout.write(" ".join(outstr)+'\n')
                outstr = []
            elif ww not in stopkey:
            #else:
                outstr.append("/".join([w.word,w.flag]))

        if len(outstr)>0:
            fout.write(" ".join(outstr)+'\n')
            outstr = []
        
    fin.close()
    fout.close()

#splitSentence(resourcedir,resultdir)

shops = os.listdir(resourcedir)
for shop in shops:
    if shop=='.DS_Store' : continue
    shop = shop.encode('utf-8')
    eachFile(shop)