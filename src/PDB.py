from math import sqrt

class PDB_papputools:

    """ The PDB_papputools accepts a PDB file for initialization
        and lets you do all kinds of weird and wonderfull things 
        to it. 

        As a class, it will be built out and extended upon as additional
        operations are required. 

        The underlying structures within the class must remain consistent
     """
        


    def __init__(self, filename, forcefield=None):
        """ init function to load the PDB contents into the 
            PDB data structure
        """
        
        filecontent = self.read_file(filename)

        self.stuff = filecontent
        
        self.residues = self.read_residues(filecontent)         


        
    def read_file(self, pdbfilename):
        """ Reads a file into a content list line by line
            and returns that list
         """
        with open(pdbfilename) as f:
            content = f.readlines()

        return content

    def read_residues(self, content):
        
        """ Function to read the content list and extract residues into
            a residue list. Note this uses lists and not dictionaries
            so if a PDB has multiple residues with the same number (but
            , for example, different chains) we don't overwrite residues.

            This the get_residue function is a search operation instead of
            a dictionary lookup, but builds in robustness and redunancy which
            is good! 
         """

        
        
        residues = []

        # scan through the content and pull residues
        # into a list
        allres = []
        current_res=0
        temp_res =[]

        header=True
        self.header=[]
        self.footer=[]
        
        for line in content:
            
            # if the current line is an atom...
            if filter(None, line.split(" "))[0].upper() == "ATOM":
                header=False

                # if the current atom comes a residue equal to the
                # current_res then append this atom to the temp_res
                # list (think of the temp_res list as a list which holds
                # each residue as it's built                                

                if current_res == int(filter(None, line.split(" "))[4]):
                    temp_res.append(filter(None, line.split(" ")))

                # If the current_res+1 is equal to the residue of the
                # line's atom we've 
                elif current_res+1 == int(filter(None, line.split(" "))[4]):
                    current_res=current_res+1                    
                    if len(temp_res) > 0: 
                        allres.append(temp_res)
                    temp_res = []
                    temp_res.append(filter(None, line.split(" ")))
                else:
                    print "ERROR!!!"
            else:
                # if we're in the header and the current line is not an atom
                # then append that line to the header list
                if header:
                    self.header.append(line)
                # if we're not in the header than must be in the footer yo!
                else:
                    self.footer.append(line)                
        return allres
            


    def get_atoms(self, atomid):
        
        """ Returns a list of atoms which match the atomid.
            Note you would probably expect this to be a list of 
            1. I've created a list because you could imagine two
            chains, where each atom has the same atomid, so
            in this case having a list avoids atoms being
            overwrittenx
        """
    
        atomslist = []
        
        for res in self.residues:
            for at in res:
                if at[i] == str(atomid):
                    atomslist.append(i)
        return atomslist

    #--------------------------------------------------------------
    #
    def get_residues(self, resid):
        """ Returns a list of residues which match the resid.
        Note you would probably expect this to be a list of 
        1. I've created a list because you could imagine two
        chains, where in each chain there is a residue with 
        the same residue. In this case having a list avoids 
        atoms being overwritten
        """ 
        residuelist = []

        for res in self.residues:
            if res[0][4] == resid:
                residuelist.append(res)

        return residuelist
        
    #--------------------------------------------------------------
    #
    def calculate_distance(self, pointA, pointB):
        """ Calculte the euclidian distance between
            two points
        """ 
        # calculate the deltas
        dx = pointA[0] - pointB[0]
        dy = pointA[1] - pointB[1]
        dz = pointA[2] - pointB[2]
        
        # euclidian geometry yo!
        return sqrt((dx*dx + dy*dy + dz*dz))
    

    #--------------------------------------------------------------
    #
    def get_distance(self, resid, atom1, atom2):
        """ Calculate the distance between two (named) atoms
            on a specific residue. Useful for examining
            bond deviations.
        """
            
        reslist = self.get_residues(str(resid))

        if len(reslist) != 1:
            print "ERROR"
            return

        res = reslist[0]

        point1 = []
        point2 = []

        for atom in res:
            if atom[2] == atom1:
                point1.append(float(atom[5]))
                point1.append(float(atom[6]))
                point1.append(float(atom[7]))

            if atom[2] == atom2:
                point2.append(float(atom[5]))
                point2.append(float(atom[6]))
                point2.append(float(atom[7]))


        return self.calculate_distance(point1, point2)

    #--------------------------------------------------------------
    #
    def convert_to_glycine(self, resid):
        """ Function which converts a residue defined by its
            resid to a Glycine residue. Note this corrects the bond
            length from a C-C to a C-H bond through an analytical
            optimization function.
            
            As of now Proline correction is not supported...
        """

        count=0        
        for res in self.residues:            
            
            # res[0][4] gets the id of the 0th atom

            if res[0][4] == str(resid):
                residue_to_switch = res

                # some edge cases
                if res[0][3] == "PRO":
                    print "ERROR: Cannot switch out proline for glycine... skipping"
                    return
                if res[0][3] == "GLY":
                    print "Switching GLY for GLY is non-sensical... skipping"
                    return

                print "Switching residue " + str(resid) + " (" + res[0][3] + ") for GLY"
                break

            count=count+1


        newgly = [self.glycine_alchemy(residue_to_switch[0]),
                  self.glycine_alchemy(residue_to_switch[1]),
                  self.glycine_alchemy(residue_to_switch[2]),
                  self.glycine_alchemy(residue_to_switch[3]),
                  self.glycine_alchemy(residue_to_switch[4], residue_to_switch[2]),
                  self.glycine_alchemy(residue_to_switch[-2]),
                  self.glycine_alchemy(residue_to_switch[-1])]

        self.residues[count] = newgly

        self.reset_atomnumbers()

    #--------------------------------------------------------------
    #
    def glycine_alchemy(self, atom, CA=None):
        """ Function which carries out the atomic switch on a residue 
        
        """

        # Convert CB_coordinates into HA2 coordinates

        if CA:
            
            # if CA is an atom the "atom" must be the alpha
            # carbon
            CB = atom
            
            # first lets define CA as (0,0,0) and CB as extending
            # from CA in 3D space
            # global coordinates (original)
            CA_cood_g = [float(CA[5]), float(CA[6]), float(CA[7])]
            CB_cood_g = [float(CB[5]), float(CB[6]), float(CB[7])]

            # local coordinates with CA as (0,0,0)
            CA_cood_l = [0,0,0]
            CB_cood_l = [CB_cood_g[0] - CA_cood_g[0],
                         CB_cood_g[1] - CA_cood_g[1],
                         CB_cood_g[2] - CA_cood_g[2]]

            # now solve the quadratic to calculate the 
            # 3D scale factor to scale each coordinate
            # to give the optimal C-H bond length
            SF = self.solveSF_quadratic(CB_cood_l)
            
            # now redfined the local coordinate
            CB_new_cood_l = [CB_cood_l[0] - CB_cood_l[0]*SF,
                             CB_cood_l[1] - CB_cood_l[1]*SF,
                             CB_cood_l[2] - CB_cood_l[2]*SF]

            CB_new_cood_g = [CB_new_cood_l[0] + CA_cood_g[0],
                             CB_new_cood_l[1] + CA_cood_g[1],
                             CB_new_cood_l[2] + CA_cood_g[2]]

            # sanity check
            print "Old bond length: " + str(self.calculate_distance(CA_cood_g, CB_cood_g))
            print "New bond length: " + str(self.calculate_distance(CA_cood_g, CB_new_cood_g))
            
            return(["ATOM", 
                    str(CB[1]), 
                    "HA2", 
                    "GLY", 
                    CB[4], 
                    self.coordinateString(CB_new_cood_g[0]),
                    self.coordinateString(CB_new_cood_g[1]), 
                    self.coordinateString(CB_new_cood_g[2]), 
                    "1.00", 
                    "0.00"])
        else:
            if str(atom[2]) == "HA":
                return(["ATOM", 
                        str(atom[1]), 
                        "HA1",
                        "GLY", 
                        atom[4], 
                        atom[5], 
                        atom[6], 
                        atom[7], 
                        "1.00", 
                        "0.00"])
            
            else:            
                return(["ATOM", 
                        str(atom[1]), 
                        str(atom[2]), 
                        "GLY", 
                    atom[4], 
                        atom[5], 
                        atom[6], 
                        atom[7], 
                        "1.00", 
                        "0.00"])                

    def coordinateString(self, floatval):
        strval = str(floatval)
        if len(strval) < 6:
            while len(strval) < 6:
                strval = strval + str(0)

        if len(strval) > 6:
            strval=strval[0:6]

            if strval.find(".") > 2:
                print "ERROR - coordinates are more than 5 significant figures!"
                raise Exception

        return strval

    def reset_atomnumbers(self):

        atomstart = int(self.residues[0][0][1])

        atnum=atomstart
        for res in self.residues:
            for atom in res:
                atom[1] = atnum
                atnum=atnum+1


    def write_file(self, filename):
        with open(filename, 'w') as f:
            for line in self.header:
                f.write(line)

            for res in self.residues:
                for atom in res:
                    
                    
                    
                    outline=str(atom[0]) + self.stringPadder(str(atom[1]), 7, reverse=True) + self.PDB_atom_stringPadder(atom[2]) + atom[3] + (6-len(str(atom[4])))*" " + str(atom[4]) + 6*" "+ self.stringPadder(str(atom[5]), 8)+ self.stringPadder(str(atom[6]), 8)+ self.stringPadder(str(atom[7]), 8) + self.stringPadder(str(atom[8]), 6) + self.stringPadder(str(atom[8]), 16) + "\n"
                    f.write(outline)                   
            for line in self.footer:
                f.write(line)
            
        print "File written (" + filename + ")"
                    

    def stringPadder(self, stringVar, totalLength, reverse=False):
        if reverse:
            return " "*(totalLength-len(stringVar))+stringVar
        else:
            return stringVar+" "*(totalLength-len(stringVar))

    def PDB_atom_stringPadder(self, atom):
        """ The "atom" column from PDB files is a pain in 
            the arse. 

            There are only a max of four characters in an
            atom identifier, but as you the number of characters
            in the identifier increases the distribution across
            the column goes
            
             C  
             CD
             HD1
            1HG2

        """

        if len(atom) == 1:
            return "  " + atom + "   "
        if len(atom) == 2:
            return "  " + atom + "  "
        if len(atom) == 3:
            return "  " + atom + " "
        if len(atom) == 4:
          return " " + atom + " "
        else:
            print "ERROR WRITING ATOM IN PDB!"
            raise Exception


    def solveSF_quadratic(self, coordinates):

        # optimal C-H bond distance from CHARMM27
        # force field (in A)
        optimal = 1.083

        ### For completeness, below is the LaTex
        ### derivation/origin of this polynomial
        ###
        ### Basically, there is some scaling factor
        ### which when each of the three coordinates is 
        ### multiplied by it scales the resulting vector
        ### to a specific distance.
        ### The polynomial allows you to define that
        ### distance based on a vector from (0,0,0)
        ### to some x,y,z coordinate and the ideal
        ### distance - say (0,0,0) to (x,y,z) is 10 - 
        ### using this info + the fact you want a vector
        ### along the same path to be 5 you can derive
        ### an SF such that now the vector (0,0,0) to
        ### (SF*x, SF*y, SF*z) is of length 5

        #-------------------------------------------------------------
        # \begin{align*}
        # D &= \sqrt{(x_a - Fx_a)^2 + (y_a - Fy_a)^2 + (z_a - Fz_a)^2 } \\
        # \end{align*}
        #
        # \begin{align*}
        # D^2 &= x_a^2 - 2Fx_a^2 + F^2x_a^2 + y_a^2 - 2Fy_a^2 + F^2y_a^2  + z_a^2 - 2Fz_a^2 + F^2z_a^2 \\
        # &= F^2\bigg(x_a^2 + y_a^2  + z_a^2\bigg) - 2F\bigg(x_a^2 + y_a^2 + z_a^2\bigg) + x_a^2 + y_a^2  + z_a^2  \\
        # &= F^2\bigg(SS\bigg) - 2F\bigg(SS\bigg) + SS  \\           
        # \end{align*}
        #
        # \begin{equation}
        # \dfrac{D^2 -  SS}{SS} = F^2 - 2F \\            
        # \end{equation}
        #
        # \begin{equation}
        # 0 = F^2 - 2F -   \dfrac{D^2 -  SS}{SS}\\            
        # \end{equation}
        #
        # \begin{equation}
        # 0 = -F^2 + 2F +   \dfrac{D^2 -  SS}{SS}\\            
        # \end{equation}
        #
        # \begin{align*}
        # F &= \dfrac{2\pm\sqrt{4-4\times(1)\times -\bigg(\dfrac{D^2 - SS}{SS}}\bigg)}{2}\\
        # &= \dfrac{2\pm\sqrt{4+4\bigg(\dfrac{D^2 - SS}{SS}}\bigg)}{2}
        # \end{align*}
        #-------------------------------------------------------------

        def sum_of_squares(x,y,z):
            return (x*x + y*y + z*z)
        def squared(x):
            return x*x

        x = coordinates[0]
        y = coordinates[1]
        z = coordinates[2]

        try:
            SF1 = (2 + sqrt(4+4*((optimal*optimal - sum_of_squares(x,y,z))/sum_of_squares(x,y,z))))/2
            SF2 = (2 - sqrt(4+4*((optimal*optimal - sum_of_squares(x,y,z))/sum_of_squares(x,y,z))))/2
        except ValueError, e:
            print "ERROR: Trying to get square root of " + c
            raise e

        if SF1 > 0 and SF1 < 1:
            return SF1
        if SF2 > 0 and SF2 < 1:
            return SF2

        print "WARNING: negative solutions to quadratic being used: could be indicative of some error..."
        if SF1 < 0 and SF1 > -1:
            return SF1
        if SF2 < 0 and SF2 > -1:
            return SF2

        print "ERROR: UNABLE TO FIND SUITABLE SOLUTION"
        raise Exception

        
        
        
                                                             
                


                            
                        
                        
            
        

                


        
        

        


                  
                
            
            
            

        
        

        


                

                
    


        

        

        
