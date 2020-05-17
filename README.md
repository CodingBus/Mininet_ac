# README #

Currently, we have a basic script to generate a single switch topology with 4
hosts using 'sudo python ./auto.py'

Learning switches using POX are looked for in the pox or ext directories.
These are run with ~/pox/pox.py <modulename>
Example (if l2_pairs_copy.py is in the ext directory):

~/pox/pox.py l2_pairs_copy

Then one can run the auto script and the connection will be made between the 
mininet network looking for a remote controller and the pox module we just
launched.

Since the module cannot be directly run from the repo folder, one needs to move the module (currently l2_copy) into the ext folder before testing or running.
Will also need to be moved back into the repo directory to get committed when
done working on it (obviously). 

### Description ###

This repo will contain code to enforce an access control policy on an emulated
Mininet network using an OpenFlow controller.

We will be pulling some source code from the Mininet documentation and using
their Python API.

### How do I get set up? ###


### Contribution guidelines ###


### Who do I talk to? ###

Authors:
Devin Perez (devindperez@uoregon.edu)
Zeke Petersen (ezekielp@uoregon.edu)
