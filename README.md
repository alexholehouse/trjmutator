trjmutator
===========

trjmutator is an attempt to provide a tool which can dynamically mutate a residue from a .xtc trajectory file to glycine. For all amino acids bar proline, the steric space occupied by a sidechain is equal to or greater than glycine, such that by removing the sidechain and projecting a C-H bond along the previously C(A)-C(B) bond, we can be sure of no steric clashes.

Installation
-------------

Installation uses

    sudo bash install.sh
    
You can edit the install.sh script to define the destination of both the install files and the link which should be in your PATH


Usage 
--------------

Run on an XTC file with a PDB file equal to the system topology (i.e. the PDB file should have the same number of atoms as each of the the xtc frames) and a residue to mutate

    trjmutator <xtc file> <pdb file> <residue to mutate>
    
    
Run on an XTC file with some kind of structure+mass which  should have the same number of atoms as each of the the xtc frames) and a residue to mutate. Note while more flexible, the -f means no santiy checks are performed, so errors may be harder to debug.

    trjmutator <xtc file> <tpr tpb tpa gro g96 pdb> <residue to mutate> -f
    
The same two basic modes can be run with additional start and end times for examining a particular trajectory, where start and end are in picoseconds

    trjmutator <xtc file> <pdb file> <residue to mutate> <start> <end> <-f>
    
    
After initiating the command you'll be created with a GROMACS group selection - for now just pick protein (1) as the group of interest.
    

    
