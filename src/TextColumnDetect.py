import os,sys
from TextBasedDetection import detectCompound
from ColumnBasedDetection import detectCompoundColumn

def main():
    jl=sys.argv[1]
    pl="../pdfs/"+os.path.split(jl)[-1].split("-")[0]+".pdf"
    r1=detectCompound(jl)
    r2=detectCompoundColumn(jl,pl)
    result=True
    if not r1 and not r2: #we can classify some non compound images as compound ones 
    #but should rarely classify a compound image as a non compound one
        result=False 
    print sys.argv[1], "is compound?",result


if __name__=="__main__":
    main()
