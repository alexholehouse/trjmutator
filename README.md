trjmutator
===========

trjmutator is an attempt to provide a tool which can dynamically mutate a residue from a .xtc trajectory file to glycine. For all amino acids bar proline, the steric space occupied by a sidechain is equal to or greater than glycine, such that by removing the sidechain and projecting a C-H bond along the previously C(A)-C(B) bond, we can be sure of no steric clashes.

Installation
-------------

Installation uses

    sudo bash install.sh
    
You can edit the install.sh script to define the destination of both the install files and the link which should be in your PATH

Notes
------

Right now the C-H bond length is optimized to CHARMM27 such the bond is 1.083 Angstroms long. If there is interested in dynamic selection of this bond length, this can easily be achieved, as optimization of the bond length is done through an analytical solution. That being said, 1.083 seems reasonable, although *ever* C-H bond is exactly 1.083 in length. One possible future update may be to add some kind of stochastic noise to the bond length (i.e. select from a distribution focussed around 1.083).

The Proline beta-carbon is not an appropriate projection from the alpha carbon for the C-H bond, so right now proline residues are simply skipped. Caclulating the optimized C-H bond for a proline is possible, but does not, categorically, ensure we don't create steric clashes. This may be considered in future versions.


Usage 
-----

Run on an XTC file with a PDB file equal to the system topology (i.e. the PDB file should have the same number of atoms as each of the the xtc frames) and a residue to mutate

    trjmutator <xtc file> <pdb file> <residue to mutate>
    
    
Run on an XTC file with some kind of structure+mass which  should have the same number of atoms as each of the the xtc frames) and a residue to mutate. Note while more flexible, the -f means no santiy checks are performed, so errors may be harder to debug.

    trjmutator <xtc file> <tpr tpb tpa gro g96 pdb> <residue to mutate> -f
    
The same two basic modes can be run with additional start and end times for examining a particular trajectory, where start and end are in picoseconds

    trjmutator <xtc file> <pdb file> <residue to mutate> <start> <end> <-f>
    
    
After initiating the command you'll be created with a GROMACS group selection - for now just pick protein (1) as the group of interest.

Output
--------

Generates 

* an xtc file (new_compiled.xtc) - this is the .xtc file with the replaced residue
* a pdb file (new\_compiled_start.pdb) - this is the PDB file associated with the first frame of the .xtc file


    

    
