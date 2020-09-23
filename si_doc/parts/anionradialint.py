import numpy
import quadpy
import pyscf
import pyscf.tools

filename = "anion_allelec_res_4.0_homoshivhf_norev.molden"
r_max = 100
num_radial_pts = 1000
mo_idx = 20

mol, mo_energy, mo_coeff, mo_occ, irrep_labels, spins = pyscf.tools.molden.load(
    filename
)
singly_occ_orb = mo_coeff[:, mo_idx]

lebedev_laikov = quadpy.u3.schemes["lebedev_131"]()
angular_pts = lebedev_laikov.theta_phi
angular_weights = lebedev_laikov.weights
num_angular_pts = len(angular_pts[0])

radial_pts = numpy.linspace(r_max, 0, num_radial_pts, endpoint=False)[::-1]


def sph2cart(r, theta_phi):
    theta = theta_phi[0]
    phi = theta_phi[1]
    x = r * numpy.cos(theta) * numpy.sin(phi)
    y = r * numpy.sin(theta) * numpy.sin(phi)
    z = r * numpy.cos(phi)
    return numpy.vstack((x, y, z)).T


values = []
for r in radial_pts:
    r_pts = r * numpy.ones(num_angular_pts)
    coords = sph2cart(r_pts, angular_pts)
    ao = mol.eval_gto("GTOval_cart", coords)
    value = angular_weights @ ao @ singly_occ_orb
    values.append(4 * numpy.pi * r * r * value ** 2)

values = numpy.array(values)

numpy.savetxt("{}_values.txt".format(filename), values)
numpy.savetxt("{}_r.txt".format(filename), radial)
