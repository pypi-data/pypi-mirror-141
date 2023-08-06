
## Write srcipt Plain text
def lines(fileName,C):
    """ Tool to write lines into text file
    * Compulsory Inputs:
        - file_name      : the input file of PLUMED,...
        - C: list-of-lines
    * Outputs:
        - file   
    """
    with open(fileName,'w') as f:
        for item in C:
            f.write(item +'\n')
##====

