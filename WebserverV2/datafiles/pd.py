import pandas as pd
import sys

cols2drop = [1]
   
cols = [i for i in range(2) if i not in cols2drop]

def add_to_bf(file_txt, file_txt2):

    (pd.read_csv(file_txt, usecols=cols, delim_whitespace=True)
       .to_csv(file_txt2, index=False, sep=' '))
   
   

if __name__ == "__main__":

    if len (sys.argv) < 3:
        print ("Mistake. Too few options.")
        sys.exit (1)

    if len (sys.argv) > 3:
        print ("Mistake. Too few options.")
        sys.exit (1)

    file_txt = sys.argv[1]
    file_txt2 = sys.argv[2]

    print ("Please wait")
    add_to_bf(file_txt, file_txt2)