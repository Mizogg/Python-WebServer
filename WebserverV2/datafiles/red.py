import sys

def add_to_bf(file_txt, file_txt2):
    with open(file_txt, 'r') as source, open(file_txt2, 'w') as dest:
        dest.writelines(source.readlines()[1:])

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
