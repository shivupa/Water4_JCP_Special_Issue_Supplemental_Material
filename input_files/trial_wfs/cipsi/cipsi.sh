#!/bin/bash
#convert the gamess output file
qp_convert_output_to_ezfio -o water4.ezfio water4.gamess
#set the target number of determinants.
echo '100000' > water4.ezfio/determinants/n_det_max
# orhogonalize the imported molecular orbitals
qp_run save_ortho_mos water4.ezfio
#Do five rounds of natural orbital generation from CIPSI wave functions
for i in {0..5}; do
  qp_run fci water4.ezfio > fci_${i}.out
  #save_natorb
  qp_run save_natorb water4.ezfio > no_${i}.out
done
# Run a final CIPSI calculation to obtain the QMC trial wave function
qp_run fci water4.ezfio > fci.out
