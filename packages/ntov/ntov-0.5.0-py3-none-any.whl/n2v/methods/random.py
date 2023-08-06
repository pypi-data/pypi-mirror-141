"""
zmp.py

Functions associated with zmp inversion
"""

import psi4
import numpy as np
from functools import reduce
rng = np.random.default_rng(12345)

psi4.core.be_quiet()
eps = np.finfo(float).eps

class Random():
    def random(self, 
            max_iter=100, 
            density_tol= psi4.core.get_option("SCF", "D_CONVERGENCE"), 
            mixing    = 1e-4,
            print_scf = False, 
            ):

        """
        Performs random inversion according to:
        
        Using random numbers to obtain Kohn-Sham potential for a given density

        Additional DIIS algorithms obtained from:
        2) 'Psi4NumPy: An interactive quantum chemistry programming environment 
        for reference implementations and rapid development.' by 
        Daniel G.A. Smith and others. 
        https://doi.org/10.1021/acs.jctc.8b00286

        Functionals that drive the SCF procedure are obtained from:
        https://doi.org/10.1002/qua.26400

        """

        self.shift      = 0.001
        self.diis_space = 100
        self.mixing     = mixing

        print("\nRunning Random Inversion:")
        self.random_scf(max_iter, print_scf=print_scf, D_conv=density_tol)

    def random_scf(self, maxiter, print_scf,D_conv):
        """
        Performs scf cycle
        Parameters
        ----------
        maxiter: integer, opt
            Maximum number of iterations for SCF calculation
        D_conv: float
            Convergence parameter for density and DIIS error. 
            Default is Psi4's Density convergence parameter: 1e-06
        """

        #Checks if there is dft grid available. 
        if hasattr(self.wfn, 'V_potential()') == False:
            ref = "RV" if self.ref == 1 else "UV"
            functional = psi4.driver.dft.build_superfunctional("SVWN", restricted=True if self.ref==1 else False)[0]
            Vpot = psi4.core.VBase.build(self.basis, functional, ref)
            Vpot.initialize()
            self.vpot = Vpot
        else:
            self.vpot = self.wfn.V_potential()

        D0 = self.on_grid_density(grid=None, Da=self.nt[0], Db=self.nt[1],  vpot=self.vpot)

        self.vxc_additive = np.zeros_like(D0)
        vc_old = np.zeros((self.nbf, self.nbf))
        vc     = np.zeros((self.nbf, self.nbf))
        Da = np.zeros((self.nbf, self.nbf))
        Db = np.zeros((self.nbf, self.nbf))
        D_old  = np.zeros_like(Da)


        #------------->  Iterating over lambdas:

        # Trial & Residual Vector Lists
        state_vectors_a, state_vectors_b = [], []
        error_vectors_a, error_vectors_b = [], []

        for SCF_ITER in range(1,maxiter):

        #------------->  Generate Fock Matrix:
            vc = self.generate_random_functional(Da, Db)

            #Potential mixing
            vc_fock =  (1-self.mixing) * vc_old + (self.mixing) * (vc)

            #Equation 10 of Reference (1). Level shift. 
            Fa = self.T + self.V + self.va + vc_fock
            # Fa += (self.S2 - reduce(np.dot, (self.S2, Da, self.S2))) * self.shift

            # if self.ref == 2:
            #     Fb = self.T + self.V + self.vb + vc_fock
            #     Fb += (self.S2 - reduce(np.dot, (self.S2, Db, self.S2))) * self.shift
            

        #------------->  DIIS:
            if SCF_ITER > 1: 
                #Construct the AO gradient
                # r = (A(FDS - SDF)A)_mu_nu
                grad_a = self.A.dot(Fa.dot(Da).dot(self.S2) - self.S2.dot(Da).dot(Fa)).dot(self.A)
                grad_a[np.abs(grad_a) < eps] = 0.0

                if SCF_ITER < self.diis_space:
                    state_vectors_a.append(Fa.copy())
                    error_vectors_a.append(grad_a.copy())
                else:
                    state_vectors_a.append(Fa.copy())
                    error_vectors_a.append(grad_a.copy())
                    del state_vectors_a[-1]
                    del error_vectors_a[-1]

                #Build inner product of error vectors
                Bdim = len(state_vectors_a)
                Ba = np.empty((Bdim + 1, Bdim + 1))
                Ba[-1, :] = -1
                Ba[:, -1] = -1
                Ba[-1, -1] = 0
                Bb = Ba.copy()

                for i in range(len(state_vectors_a)):
                    for j in range(len(state_vectors_a)):
                        Ba[i,j] = np.einsum('ij,ij->', error_vectors_a[i], error_vectors_a[j])

                #Build almost zeros matrix to generate inverse. 
                RHS = np.zeros(Bdim + 1)
                RHS[-1] = -1

                #Find coefficient matrix:
                Ca = np.linalg.solve(Ba, RHS.copy())
                Ca[np.abs(Ca) < eps] = 0.0 

                #Generate new fock Matrix:
                Fa = np.zeros_like(Fa)
                for i in range(Ca.shape[0] - 1):
                    Fa += Ca[i] * state_vectors_a[i]

                diis_error_a = np.max(np.abs(error_vectors_a[-1]))
                if self.ref ==  1:
                    Fb = Fa.copy()
                    diis_error = 2 * diis_error_a

                else:
                    grad_b = self.A.dot(Fb.dot(Db).dot(self.S2) - self.S2.dot(Db).dot(Fb)).dot(self.A)
                    grad_b[np.abs(grad_b) < eps] = 0.0
                    
                    if SCF_ITER < self.diis_space:
                        state_vectors_b.append(Fb.copy())
                        error_vectors_b.append(grad_b.copy())
                    else:
                        state_vectors_b.append(Fb.copy())
                        error_vectors_b.append(grad_b.copy())
                        del state_vectors_b[-1]
                        del error_vectors_b[-1]

                    for i in range(len(state_vectors_b)):
                        for j in range(len(state_vectors_b)):
                            Bb[i,j] = np.einsum('ij,ij->', error_vectors_b[i], error_vectors_b[j])

                    diis_error_b = np.max(np.abs(error_vectors_b[-1]))
                    diis_error = diis_error_a + diis_error_b

                    Cb = np.linalg.solve(Bb, RHS.copy())
                    Cb[np.abs(Cb) < eps] = 0.0 

                    Fb = np.zeros_like(Fb)
                    for i in range(Cb.shape[0] - 1):
                        Fb += Cb[i] * state_vectors_b[i]

            else:
                diis_error = 1.0
            
        #------------->  Diagonalization | Check convergence:

            Ca, Cocca, Da, eigs_a = self.diagonalize(Fa, self.nalpha)
            if self.ref == 2:
                Cb, Coccb, Db, eigs_b = self.diagonalize(Fb, self.nbeta)
            else: 
                Cb, Coccb, Db, eigs_b = Ca.copy(), Cocca.copy(), Da.copy(), eigs_a.copy()

            ddm = D_old - Da
            vc_old = vc 
            D_old = Da
            derror = np.max(np.abs(ddm))

            density_current = self.on_grid_density(grid=None, Da=Da, Db=Db, vpot=self.vpot)
            grid_diff = np.max(np.abs(D0 - density_current))

            #Uncomment to debug internal SCF
            if print_scf:
                if np.mod(SCF_ITER, 1) == 0:  
                    print(f"Iteration: {SCF_ITER:3d} | Conv Error: {derror:10.10e} | DIIS Error:  | DD: {np.max(grid_diff)}")
            
            # if abs(derror) < D_conv: #and abs(diis_error) < D_conv:
            #     self.vc = vc
            #     break
            if SCF_ITER == maxiter - 1:
                raise ValueError("Maximum Number of SCF cycles reached. Try different settings.")

            density_current = self.on_grid_density(grid=None, Da=Da, Db=Db, vpot=self.vpot)
            grid_diff = np.max(np.abs(D0 - density_current))


    def generate_random_functional(self, Da, Db):
        """
        Generates S_n Functional as described by:
        Using random numbers to obtain Kohn-Sham potential for a given density
        Kumar + Harbola
        """

        # Obtain target density on dft_grid 
        D0 = self.on_grid_density(grid=None, Da=self.nt[0], Db=self.nt[1],  vpot=self.vpot)
        D_current = self.on_grid_density(grid=None, Da=Da, Db=Db,  vpot=self.vpot)
        target_density = D0
        current_density = D_current
        diff = current_density - target_density
        max_diff = np.max(diff)

        # Components for equation 12
        vc = np.empty_like(target_density)
        for i in range(diff.shape[0]):
                if current_density[i] < target_density[i]:
                    vc[i] =   max_diff * rng.random()
                else:
                    vc[i] = - max_diff * rng.random()

        self.vxc_additive += vc
        vc_nm = self.dft_grid_to_fock(vc, self.vpot)

        return vc_nm
        
