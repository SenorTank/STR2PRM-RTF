"""
This script will separate the RTF and PRM Components of a STR file and generate inputs matching the 
CHARMM-GUI input requirements. It is incomplete, but hopefully a good starting point.
"""

#Imports
import pickle   # Pickle was used to allow for fast input/output of any information, like the masses
import re       # This was a lot easier to use than trying to tease out nuances for finding lines
import argparse # This allows it to be used as a CLI rather than having to modify inputs

def Read_STR(file_path):
    """
        This function takes in a file path ("file_path") to read out the RTF and PRM sections 
        of the original script. From there, we can then return them a single dictionary object. 
        One consideration for furthering this tool and development is to consider building a full class
        with all the sections that could be included. This was problematic because I still couldn't
        completely separate the difference between an amino acid and a small molecule.
    """
    topology = []
    parameters = []
    with open(file_path, 'r') as f:
        topo = False
        for line in f:
            line = line.strip()
            if not line or line.startswith('!') or "END" in line:
                continue
            if 'read rtf card' in line:
                topo = True
                continue
            if 'read param card' in line:
                topo = False
                continue
            if topo:
                topology.append(line)
            else:
                parameters.append(line)

    return {'rtf':topology, 'prm':parameters }

def Add_Newline(stringy_boi):
    """
        Does exactly what it says. I just like naming some variables silly.
    """
    return stringy_boi + '\n'

def Import_Data(file_path):
    """
        Takes in the file path of a pickle file, and then just reads the data in, I hate
        writing open() statements in Python more than I have to.
    """
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data

# The Main Function here (I prefer the dunder approach over a full main function)
if __name__ == "__main__":

    # STR File path from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--File", help = "STR file you are splitting")
    args = parser.parse_args()

    # Checks the file, throws error accordingly
    if args.File:
        input_file = args.File
        file_name = input_file.split('.')[0]
    else:
        raise FileNotFoundError("Imaginary file not found.")

    # Loads up the information we need
    out = Read_STR(f'{input_file}')
    mass_data = Import_Data('mass.pkl')

    """
    This is where the end product is made. What should happen is that we get our RTF and PRM files, and
    they can be put straight into CHARMM for defining the parameters, but frankly, that doesn't
    work. Errors vary depending on what was input, and fixing them with different things starts
    turning into just writing it by hand, which is not the point of this program.
    """
    #Writing Topology File stuff
    with open(f'{file_name}.rtf', 'w') as f:
        for line in out['rtf']:
            f.writelines(Add_Newline(line))
        f.writelines(Add_Newline("END"))

    #Writing Parameter File stuff
    with open(f'{file_name}.prm', 'w') as f:
        for line in out['prm']:
            f.writelines(Add_Newline(line))
        f.writelines(Add_Newline("END"))
