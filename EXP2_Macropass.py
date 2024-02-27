Main.py:
# input file
input_file = 'input2.txt'

# Attempt to open the input file
try:
    fp = open(input_file, 'r')
except FileNotFoundError:
    print(f"Error: File '{input_file}' not found.")
    exit(1)

mntc = 1
mdtc = 1

# Macro Name Table
mnt = {}

# Macro Definition Table
mdt = {}

# Flag to indicate if currently inside a macro definition
inside_macro = False

# Open files for MNT and MDT
fp_mnt = open('mnt_table.txt', 'w')
fp_mdt = open('mdt_table.txt', 'w')
fp_out = open('output_file.txt', 'w')

# Read each line from the input file
for line in fp:
    # Strip leading and trailing whitespace from the line
    line = line.strip()
    print("Current line:", line)

    # Split the line into elements
    elements = line.split()

    # Check if the line indicates the start of a macro definition
    if elements and elements[0] == 'MACRO':
        if len(elements) > 1:
            macro_name = elements[1]
            mnt[macro_name] = (mntc, mdtc)
            fp_mnt.write(f"{mntc}\t{macro_name}\t{mdtc}\n")
            mntc += 1
            mdt[macro_name] = []
            inside_macro = True
    elif inside_macro:
        # Check if the line indicates the end of a macro definition
        if elements and elements[0] == 'MEND':
            inside_macro = False
            # Write macro definition to MDT file
            for macro_line in mdt[macro_name]:
                fp_mdt.write(f"{mdtc}\t{macro_name}\t{macro_line}\n")
                mdtc += 1
        else:
            # Append the line to the MDT for the current macro
            mdt[macro_name].append(line)
    else:
        # Write non-macro lines to the output file
        fp_out.write(f"{line}\n")
        # Write non-macro lines to MDT file
        fp_mdt.write(f"{mdtc}\t\t{line}\n")
        mdtc += 1

# Close the input file
fp.close()

# Close MNT, MDT, and output files
fp_mnt.close()
fp_mdt.close()
fp_out.close()

Input:
Input.txt-
MACRO	-
M1	&ARG1,&SYSTEM
L	1,&ARG1
A	1,Y
ST	1,&SYSTEM
MEND	
START	
M1	DATA1,COMPUTER
L	2,K
M1	SYSTEM,PROGRAMMING
S	1,PROGRAM
M1	Y,D
M	1,J
END	

Output:
mdt.txt-
1	-	M1	&ARG1,&SYSTEM
2	-	L	1,&ARG1
3	-	A	1,Y
4	-	ST	1,&SYSTEM
5		START
6		M1	DATA1,COMPUTER
7		L	2,K
8		M1	SYSTEM,PROGRAMMING
9		S	1,PROGRAM
10		M1	Y,D
11		M	1,J
12		END

mdt.txt-
1	M1 1

Output.txt-
START
M1	DATA1,COMPUTER
L	2,K
M1	SYSTEM,PROGRAMMING
S	1,PROGRAM
M1	Y,D
M	1,J
END
