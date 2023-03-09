# configuration mod utility
#
# usage: config <file> <section> <Key> <Value> <instance#> - Change a configuration key to the value in the section of the file
#               
#       Modifies the instance number of the key in section(optional) of the configuration file file to be value.  If the key is preceded
#       by a #, then the # is removed in the file.  Do not place the # in the command line.

import sys
import getopt

configlinehelptext = 'config.py -f <file> -s <section - optional> -k <key> -v <value>\nconfig.py -h for more information'

def lout(item:str):
    # prints out a line, but strips off trailing newline if it is there
    if '\n' in item:
        print(item[0:-1])
    else:
        print(item)

def config(argv) -> int:
    fname = ''
    section = ''
    key=''
    value=''
    Break=' '

    try:
       opts, args = getopt.getopt(argv,"f:s:k:v:B:",["file=","section=","key=","value=","Break="])
    except getopt.GetoptError:
            print('\nCONFIG.PY\n==============================================================================================\n')
            print('This script modifies configuration text files.  You must specify the file, key, and value.')
            print('The section parameter is optional.\n\n')
            print('Command Format:')
            print('\tconfig.py -f <file> -s <section - optional> -k <key> -v <value> -B <Break>\n\tconfig.py -h for more information\n\n\tparameters:')
            print('\t\tfile - the configuration file to modify')
            print('\t\tsection - the section to modify denoted in the file by the name being enclosed')
            print('\t\t\tin square brackets.  If not specied then all occurances otf the key')
            print('\t\t\twill have their value set to the specified value')
            print('\t\tkey - the key name to be modified')
            print('\t\tvalue - the new value for the key')
            print('\t\tBreak - the character used to separate key value pairs.  Default is a space')
            print()
            sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h',"--help"):
            print (configlinehelptext)
            sys.exit()
        elif opt in ("-f", "--file"):
            fname = arg
        elif opt in ("-s", "--section"):
            section = arg
        elif opt in ("-k","--key"):
            key = arg
        elif opt in ("-v","--value"):
            value=arg
        elif opt in ("-B","--Break"):
            Break = arg 
    
    if fname=='' or key=='' or value=='':
        print (configlinehelptext)
        sys.exit()
    
    insection = section == ''  #  are we in our section - if section is not specified then we are always in our section
    sectionfound=insection  # did we find our section - if no section specified then we have always found our section
    keyset = False

    with open(fname,'r') as f:
        for line in f.readlines():
            working = line.strip()
            iscomment = working[0:1] == '#'
            if iscomment: # print out commented lines
                lout(line)
                working = ' '+working[1:]
            else:
                if working[0:1] == '[' and working[-1:] == ']':  # section found
                    if insection and not keyset:   # we are in the section, have found the start of a new section, and have not set the key yet, so it is a new key value pair
                        lout(key+Break+value)
                        keyset = True
                    lout(line)
                    insection=False
                    if working[1:len(working)-1].upper() == section.upper():
                        insection=True
                        sectionfound = True
                else:
                    if working.find(Break) == 0: # not a key value pair
                       lout(line)
                       pass
                    else:  # kvp, not a section
                        if not insection:  # we are processing sections, and we are not in the right section
                            lout(line)
                            pass
                        else:  # process the key value pair line
                            if working[0:working.find(Break)].upper() == key.upper():  # key found, set value
                                lout(line[0:line.find(Break)+1]+value)
                                keyset = True
                            else:
                                lout(line)
        if section != '' and not sectionfound:   # we never found the section we are processing so, make it
            lout('['+section+']')
        if not keyset:  # we will get here if we have not set the key
            lout(key+Break+value)
            keyset = True
    if keyset:
        return 1
    else:
        return 0

if __name__ == "__main__":
    config(sys.argv[1:])
else:
    pass
