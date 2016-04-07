import sys
import json
import re

patterns=[
re.compile("a\)(.*?)b\)"), # <a) b)>, <a)., b).> 
re.compile("lower(.*?)upper"), # <lower, upper> 
re.compile("i\)(.*?)ii\)"), # <i) ii)>, <i)., ii).> 
re.compile("1\)(.*?)1\)"), # <1) 2)>, <1)., 2).> 
re.compile("left(.*?)right"), # <left, right>
re.compile("top(.*?)bottom") # <left, right>
 
]

def detectCompound(jl):
    #jl=sys.argv[1]
    caption=re.sub('[^0-9a-zA-Z)(.]+', '', json.load(open(jl)).get('Caption',"")).lower()
    imtext=re.sub('[^0-9a-zA-Z)(.]+', '',''.join([x.get('Text',"") for x in json.load(open(jl)).get('ImageText',[])])).lower()
    if not caption and not imtext: print "caption and image text empty, can't detect compound figure or not",jl; sys.exit(1)
    else:
        captionmatches=[len(re.findall(p,caption)) for p in patterns]
        imtextmatches=[len(re.findall(p,imtext)) for p in patterns]
        ''' 
        print caption
        print imtext
        print captionmatches  
        print imtextmatches
        '''
        if (sum(captionmatches)!=1 and sum(imtextmatches)!=1) or sum(captionmatches)+sum(imtextmatches)==0:
            #print captionmatches,imtextmatches
            return False
        else: 
            return True

def main():
    result=detectCompound(sys.argv[1])
    print sys.argv[1], "is compound?",result


if __name__=="__main__":
    main()      
     
