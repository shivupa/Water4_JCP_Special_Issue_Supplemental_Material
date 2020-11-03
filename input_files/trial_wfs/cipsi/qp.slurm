#!/bin/bash
qp_convert_output_to_ezfio -o ${SLURM_JOB_NAME}.ezfio ${SLURM_SUBMIT_DIR}/../../../b3lyp/RO/${SLURM_JOB_NAME}.gamess
echo '100000' > ${SLURM_JOB_NAME}.ezfio/determinants/n_det_max
qp_run save_ortho_mos ${SLURM_JOB_NAME}.ezfio
for i in {0..5}; do
  qp_run fci ${SLURM_JOB_NAME}.ezfio > fci_${i}.out
  #save_natorb
  qp_run save_natorb ${SLURM_JOB_NAME}.ezfio > no_${i}.out
done
