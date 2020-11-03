#!/bin/bash
module load singularity
sing_img=/ihome/dlambrecht/aed63/private_codes/singularity_images/qp2_05_03_20.simg

mkdir pt2_1e-1
cd pt2_1e-1
cp -r ../../${SLURM_JOB_NAME}.ezfio .
echo 'T' ${SLURM_JOB_NAME}.ezfio/determinants/read_wf
echo '1e-1' > ${SLURM_JOB_NAME}.ezfio/perturbation/pt2_max
echo 1000000  > ${SLURM_JOB_NAME}.ezfio/detrminants/n_det_max
qp_run fci ${SLURM_JOB_NAME}.ezfio > fci.out
