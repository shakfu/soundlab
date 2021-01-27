#!/usr/bin/python
import os
import sys



def main():
    NbSpace=0
    NbTab=0
    NbSpaceNext=0
    Space=" "
    # Will add 2 spaces for next line
    Add2List  = ["instr", "opcode", "groupbox"]
    # Will remove 2  spaces for itself and following lines 
    Remove2List = ["endin", "endop" ,"}" ]
    # Will add 4 spaces for next line
    Add4NextList = ["if"]
    # Will remove 4  spaces for itself but let following lines unchanged
    Remove4List = ["elseif", "else"]
    # Will remove 4 spaces for following line and itself
    Remove4NextList = ["loop_lt", "loop_gt" , "loop_le","loop_ge" , "endif", "rireturn"]

    if len(sys.argv) <>3 :
        print "Usage :\n python beautifier.py infile.csd outfile.csd"
        sys.exit(2)
    with open(sys.argv[1]) as f:
        for line in f:          
            if line.isspace() ==False :
                s = line.strip()
                firstword = s.split(None, 1)[0]
                
                if firstword in Add2List:
                   NbSpaceNext= NbSpace+2
                   
                if firstword in Add4NextList :
                    NbSpaceNext= NbSpace+4
                    
                if firstword in Remove4List  :
                    NbSpace= NbSpace-4
                    
                if firstword in Remove4NextList  :
                    NbSpaceNext= NbSpace-4
                    NbSpace= NbSpace-4
                    
                if firstword in Remove2List :
                    NbSpaceNext= NbSpace-2
                    NbSpace= NbSpace-2                
                    
                if firstword.endswith(':') :
                    NbSpaceNext= NbSpace+4
                    
                SpaceLine = NbSpace*Space
                Sout = SpaceLine + s+"\n"
            else:
                Sout = line
            with open(sys.argv[2], 'a') as f1:
                f1.write(Sout)
            NbSpace=NbSpaceNext
		
			
if __name__ == "__main__":
    main()		
	
		