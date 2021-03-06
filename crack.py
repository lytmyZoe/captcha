#\u7528python\u7C7B\u5B9E\u73B0\u5411\u91CF\u7A7A\u95F4
#\u5B83\u4F1A\u6BD4\u8F83\u4E24\u4E2Apython\u5B57\u5178\u7C7B\u578B\u5E76\u8F93\u51FA\u4ED6\u4EEC\u7684\u76F8\u4F3C\u5EA6?\u75280~1\u7684\u6570\u5B57\u8868\u793A?
from PIL import Image
import hashlib
import time
import os
import math

class VectorCompare:
    #\u8BA1\u7B97\u77E2\u91CF\u5927\u5C0F
    def magnitude(self, concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    #\u8BA1\u7B97\u77E2\u91CF\u4E4B\u95F4\u7684cos\u503C
    def relation(self,concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

def buildvector(im):
    d1 = {}

    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

v = VectorCompare()

iconset =['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

#加载训练集
imageset = []
for letter in iconset:
    for img in os.listdir('./iconset/%s/'%(letter)):
        temp = []
        if img != "Thumbs.db" and img != ".DS_Store":
            temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
        imageset.append({letter:temp})



"""
#-*- coding:utf-8 -*-
from PIL import Image
im = Image.open("captcha.gif")
#?\u5C06\u56FE\u7247\u8F6C\u6362\u4E3A8\u4F4D\u50CF\u7D20\u6A21\u5F0F?
im.convert("P")
#\u6253\u5370\u989C\u8272\u76F4\u65B9\u56FE
#\u989C\u8272\u76F4\u65B9\u56FE\u7684\u6BCF\u4E00\u4F4D\u6570\u5B57\u90FD\u4EE3\u8868\u4E86\u56FE\u7247\u4E2D\u542B\u6709\u5BF9\u5E94\u4F4D\u7684\u989C\u8272\u7684\u50CF\u7D20\u7684\u6570\u91CF
print(im.histogram())
his = im.histogram()
values = {}
for i in range(256):
    values[i] = his[i]
for j,k in sorted(values.items(),key=lambda x:x[1],reverse = True)[:10]:
    print(j,k)
"""

#\u524D\u9762\u5F97\u5230\u4E86\u56FE\u7247\u4E2D\u6700\u591A\u768410\u79CD\u989C\u8272
#220?227\u662F\u6211\u4EEC\u9700\u8981\u7684\u7EA2\u8272\u548C\u7070\u8272?\u53EF\u4EE5\u901A\u8FC7\u8FD9\u4E00\u8BAF\u606F\u6784\u9020\u4E00\u79CD\u9ED1\u767D\u4E8C\u503C\u56FE\u7247
#-*- coding:utf-8 -*-
#from PIL import Image

im = Image.open("0q1d10.gif")
im2 = Image.new("P",im.size,255)
im.convert("P")
temp = {}


for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y,x))
        temp[pix] = pix
        if pix == 220 or pix == 227: #these are the numbers to get
            im2.putpixel((y,x),0)
#im2.save('new.gif')


#\u5F97\u5230\u5355\u4E2A\u5B57\u7B26\u7684\u50CF\u7D20\u96C6\u5408?\u8FDB\u884C\u7EB5\u5411\u5207\u5272
inletter = False
foundletter = False
start = 0
end = 0

letters = []

for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y,x))
        if pix != 255:
            inletter = True

    if foundletter == False and inletter == True:
        foundletter = True
        start = y
    
    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start,end))

    inletter = False
#print(letters)
#\u5F97\u5230\u6BCF\u4E2A\u5B57\u7B26\u5F00\u59CB\u548C\u7ED3\u675F\u7684\u5217\u5E8F\u53F7


#\u5BF9\u56FE\u7247\u8FDB\u884C\u5207\u5272?\u5F97\u5230\u6BCF\u4E2A\u5B57\u7B26\u6240\u5728\u7684\u90A3\u90E8\u5206\u56FE\u7247
#import hashlib
#import time

count = 0
for letter in letters:
    #\u524D\u4E24\u4E2A\u503C\u4E3A\u5DE6\u4E0A\u89D2\u5750\u6807
    #\u540E\u4E24\u4E2A\u503C\u4E3A\u53F3\u4E0B\u89D2\u5750\u6807
    #im3 = im2.crop((letter[0], 0, letter[1],im2.size[1]))
    #im3.save("./%s.gif"%(count))
    #count += 1
    m = hashlib.md5()
    im3 = im2.crop(( letter[0], 0, letter[1], im2.size[1]))

    guess = []
    
    for image in imageset:
        for x,y in image.items():
            if len(y) != 0:
                guess.append((v.relation(y[0],buildvector(im3)),x))

    guess.sort(reverse=True)
    print(guess[0])

    count +=1





















