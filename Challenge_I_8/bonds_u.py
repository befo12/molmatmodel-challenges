# extract U=O, U-I, U-O(water) distances from the last geometry of an NWChem output
import sys
from ase.io import read
a = read(sys.argv[1], format='nwchem-out', index=-1)
d = a.get_distance
print(f"U=O  {(d(0,1)+d(0,2))/2:.4f}   U-I  {(d(0,3)+d(0,4))/2:.4f}   U-O(water)  {(d(0,5)+d(0,6))/2:.4f}   O=U=O {a.get_angle(1,0,2):.1f}   E = {a.get_potential_energy():.4f} eV")
