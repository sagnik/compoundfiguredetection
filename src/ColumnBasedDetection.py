import os,sys
import json
import re
from subprocess import call

pdffigures="../libraries/pdffigures-coldetect/pdffigures"
T=5

def detectCompoundColumn(jl,pl):
    #jl=sys.argv[1]
    if not os.path.exists(pl) or not os.path.exists(jl): print "input files not found, exiting"; system.exit(1)
    if not os.path.exists(pdffigures): print "pdffigures not found, exiting"; system.exit(1)

    result=call([pdffigures, pl])
    if result==1: print "pdffigures coluldn't process the document, exiting"; system.exit(1)
    if result==2: return False; # we don't know what to do if the document is single column.
    if result==3: # we will check if the figure spans multi column
        PAGEWIDTH=json.load(open(jl)).get('Width',850)
        fBB=json.load(open(jl)).get('ImageBB',[0,0,0,0])
        fx1=fBB[0]
        fx2=fBB[2]
        #print fBB
        if fx1<(PAGEWIDTH/2-T) and fx2>(PAGEWIDTH/2+T): #figure spans multi column
            return True
        else:
            return False 
     

def main():
    jl=sys.argv[1]
    pl="../pdfs/"+os.path.split(jl)[-1].split("-")[0]+".pdf"
    #print jl,pl
    result=detectCompoundColumn(jl,pl)
    print sys.argv[1], "is compound?",result


if __name__=="__main__":
    main()      
     
