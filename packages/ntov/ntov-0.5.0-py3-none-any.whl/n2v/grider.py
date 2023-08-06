"""
grider.py
"""

import numpy as np
import psi4

from opt_einsum import contract

class Psi4Grider():
    def __init__(self, mol, basis, ref):
        
        self.mol = mol
        self.ref = ref
        self.basis = basis
        self.basis_str = basis.name()
        self.nbf   = self.basis.nbf()

        wfn_base = psi4.core.Wavefunction.build(self.mol, self.basis_str)
        self.wfn = psi4.proc.scf_wavefunction_factory('svwn', wfn_base, "UKS")
        self.wfn.initialize()

        self.nalpha = self.wfn.nalpha()
        self.nbeta  = self.wfn.nbeta()

        # Clean Vpot
        restricted = True if ref == 1 else False
        reference  = "RV" if ref == 1 else "UV"
        functional = psi4.driver.dft.build_superfunctional("SVWN", restricted=restricted)[0]
        self.Vpot = psi4.core.VBase.build(self.basis, functional, reference)
        self.Vpot.initialize()

        self.npoints = self.Vpot.grid().npoints()   

    def compute_LDA(self):
        """
        Computres LDA Calculation on Molecule
        """
        wfn = psi4.energy("SVWN/" + self.basis_str, molecule=self.mol, return_wfn=True)[1]
        Da  = wfn.Da().np
        Db  = wfn.Db().np
        Ca  = wfn.Ca().np
        Cb  = wfn.Cb().np
        epsilon_a = wfn.epsilon_a().np
        epsilon_b = wfn.epsilon_b().np

        return Da, Db, Ca, Cb, epsilon_a, epsilon_b

    def generate_grid(self, x, y, z):
        """
        Genrates Mesh from 3 separate linear spaces and flatten,
        needed for cubic grid.

        Parameters
        ----------
        grid: tuple of three np.ndarray
            (x, y, z)

        Returns
        -------
        grid: np.ndarray
            shape (3, len(x)*len(y)*len(z)).
        """
        # x,y,z, = grid
        shape = (len(x), len(y), len(z))
        X,Y,Z = np.meshgrid(x, y, z, indexing='ij')
        X = X.reshape((X.shape[0] * X.shape[1] * X.shape[2], 1))
        Y = Y.reshape((Y.shape[0] * Y.shape[1] * Y.shape[2], 1))
        Z = Z.reshape((Z.shape[0] * Z.shape[1] * Z.shape[2], 1))
        grid = np.concatenate((X,Y,Z), axis=1).T

        return grid, shape

    def grid_to_blocks(self, grid, basis=None):
        """
        Generate list of blocks to allocate given grid

        Parameters
        ----------
        grid: np.ndarray
            Grid to be distributed into blocks
            Size: (3, npoints) for homogeneous grid
                  (4, npoints) for inhomogenous grid to account for weights
        basis: psi4.core.BasisSet; optional
            The basis set. If not given, it will use target wfn.basisset().

        Returns
        -------
        blocks: list    
            List with psi4.core.BlockOPoints
        npoints: int
            Total number of points (for one dimension)
        points: psi4.core.{RKS, UKS}
            Points function to set matrices.
        """
        assert (grid.shape[0] == 3) or (grid.shape[0] == 4), """Grid does not have the correct dimensions. \n
                                                              Array must be of size (3, npoints) or (4, npoints)"""
        if_w = grid.shape[0] == 4

        if basis is None:
            basis = self.basis

        epsilon    = psi4.core.get_global_option("CUBIC_BASIS_TOLERANCE")
        extens     = psi4.core.BasisExtents(basis, epsilon)
        max_points = psi4.core.get_global_option("DFT_BLOCK_MAX_POINTS")        
        npoints    = grid.shape[1]
        nblocks = int(np.floor(npoints/max_points))
        blocks = []

        max_functions = 0
        #Run through full blocks
        idx = 0
        for nb in range(nblocks):
            x = psi4.core.Vector.from_array(grid[0][idx : idx + max_points])
            y = psi4.core.Vector.from_array(grid[1][idx : idx + max_points])
            z = psi4.core.Vector.from_array(grid[2][idx : idx + max_points])
            if if_w:
                w = psi4.core.Vector.from_array(grid[3][idx : idx + max_points])
            else:
                w = psi4.core.Vector.from_array(np.zeros(max_points))  # When w is not necessary and not given

            blocks.append(psi4.core.BlockOPoints(x, y, z, w, extens))
            idx += max_points
            max_functions = max_functions if max_functions > len(blocks[-1].functions_local_to_global()) \
                                          else len(blocks[-1].functions_local_to_global())

        #Run through remaining points
        if idx < npoints:
            x = psi4.core.Vector.from_array(grid[0][idx:])
            y = psi4.core.Vector.from_array(grid[1][idx:])
            z = psi4.core.Vector.from_array(grid[2][idx:])
            if if_w:
                w = psi4.core.Vector.from_array(grid[3][idx:])
            else:
                w = psi4.core.Vector.from_array(np.zeros_like(grid[2][idx:]))  # When w is not necessary and not given
            blocks.append(psi4.core.BlockOPoints(x, y, z, w, extens))

            max_functions = max_functions if max_functions > len(blocks[-1].functions_local_to_global()) \
                                          else len(blocks[-1].functions_local_to_global())

        zero_matrix = psi4.core.Matrix(basis.nbf(), basis.nbf())
        if self.ref == 1:
            point_func = psi4.core.RKSFunctions(basis, max_points, max_functions)
            point_func.set_pointers(zero_matrix)
        else:
            point_func = psi4.core.UKSFunctions(basis, max_points, max_functions)
            point_func.set_pointers(zero_matrix, zero_matrix)

        return blocks, npoints, point_func

    def ao(self, coeff, grid=None, basis=None):
        """
        Generates a quantity on the grid given its ao representation.
        *This is the most general function for basis to grid transformation.

        Parameters
        ----------
        coeff: np.ndarray
            Vector/Matrix of quantity on ao basis. Shape: {(num_ao_basis, ), (num_ao_basis, num_ao_basis)}
        grid: np.ndarray Shape: (3, npoints) or (4, npoints) or tuple for block_handler (return of grid_to_blocks)
            grid where density will be computed.
        basis: psi4.core.BasisSet, optional
            The basis set. If not given it will use target wfn.basisset().
        Vpot: psi4.core.VBase
            Vpotential object with info about grid. 
            Provides DFT spherical grid. Only comes to play if no grid is given. 

        Returns
        -------
        coeff_r: np.ndarray Shape: (npoints, )
            Quantity expressed by the coefficient on the given grid 


        """


        if grid is not None:
            if type(grid) is np.ndarray:
                if grid.shape[0] != 3 and grid.shape[0] != 4:
                    raise ValueError("The shape of grid should be (3, npoints) "
                                     "or (4, npoints) but got (%i, %i)" % (grid.shape[0], grid.shape[1]))
                blocks, npoints, points_function = self.grid_to_blocks(grid, basis=basis)
            else:
                blocks, npoints, points_function = grid
        elif grid is None:
            Vpot = self.Vpot
            nblocks = Vpot.nblocks()
            blocks = [Vpot.get_block(i) for i in range(nblocks)]
            npoints = Vpot.grid().npoints()
            points_function = Vpot.properties()[0]
        else:
            raise ValueError("A grid or a V_potential (DFT grid) must be given.")

        coeff_r = np.zeros((npoints))

        offset = 0
        for i_block in blocks:
            points_function.compute_points(i_block)
            b_points = i_block.npoints()
            offset += b_points
            lpos = np.array(i_block.functions_local_to_global())
            if len(lpos)==0:
                continue
            phi = np.array(points_function.basis_values()["PHI"])[:b_points, :lpos.shape[0]]

            if coeff.ndim == 1:
                l_mat = coeff[(lpos[:])]
                coeff_r[offset - b_points : offset] = contract('pm,m->p', phi, l_mat)
            elif coeff.ndim == 2:
                l_mat = coeff[(lpos[:, None], lpos)]
                coeff_r[offset - b_points : offset] = contract('pm,mn,pn->p', phi, l_mat, phi)

        return coeff_r

    def density(self, Da, Db=None, grid=None):
        """
        Generates Density given grid

        Parameters
        ----------
        Da, Db: np.ndarray
            Alpha, Beta densities. Shape: (num_ao_basis, num_ao_basis)
        grid: np.ndarray Shape: (3, npoints) or (4, npoints) or tuple for block_handler (return of grid_to_blocks)
            grid where density will be computed.
        vpot: psi4.core.VBase
            Vpotential object with info about grid.
            Provides DFT spherical grid. Only comes to play if no grid is given. 

        Returns
        -------
        density: np.ndarray Shape: (ref, npoints)
            Density on the given grid. 
        """

        Da = psi4.core.Matrix.from_array(Da)
        if Db is not None:
            Db = psi4.core.Matrix.from_array(Db)

        if grid is not None:
            if type(grid) is np.ndarray:
                if grid.shape[0] != 3 and grid.shape[0] != 4:
                    raise ValueError("The shape of grid should be (3, npoints) "
                                     "or (4, npoints) but got (%i, %i)" % (grid.shape[0], grid.shape[1]))
                blocks, npoints, points_function = self.grid_to_blocks(grid)
            else:
                blocks, npoints, points_function = grid
        elif grid is None:
            nblocks = self.Vpot.nblocks()
            blocks = [self.Vpot.get_block(i) for i in range(nblocks)]
            npoints = self.Vpot.grid().npoints()
            points_function = self.Vpot.properties()[0]
        else:
            raise ValueError("A grid or a V_potential (DFT grid) must be given.")

        if Db is None:
            points_function.set_pointers(Da)
            rho_a = points_function.point_values()["RHO_A"]
            density   = np.zeros((npoints))
        else:
            points_function.set_pointers(Da, Db)
            rho_a = points_function.point_values()["RHO_A"]
            rho_b = points_function.point_values()["RHO_B"]
            density   = np.zeros((npoints, self.ref))

        offset = 0
        for i_block in blocks:
            points_function.compute_points(i_block)
            b_points = i_block.npoints()
            offset += b_points

            if self.ref == 1:
                density[offset - b_points : offset] = rho_a.np[ :b_points]
            else:
                density[offset - b_points : offset, 0] = rho_a.np[ :b_points]
                density[offset - b_points : offset, 1] = rho_b.np[ :b_points]

        return density

        pass

    def esp(self, Da=None, Db=None, vpot=None, grid=None, compute_hartree=True):
        """
        Generates EXTERNAL/ESP/HARTREE and Fermi Amaldi Potential on given grid
        Parameters
        ----------
        Da,Db: np.ndarray, opt, shape (nbf, nbf)
            The electron density in the denominator of Hartee potential. If None, the original density matrix
            will be used.
        grid: np.ndarray Shape: (3, npoints) or (4, npoints) or tuple for block_handler (return of grid_to_blocks)
            grid where density will be computed.
        vpot: psi4.core.VBase
            Vpotential object with info about grid.
            Provides DFT spherical grid. Only comes to play if no grid is given. 
        
        Returns
        -------
        vext, hartree, esp, v_fa: np.ndarray
            External, Hartree, ESP, and Fermi Amaldi potential on the given grid
            Shape: (npoints, )
        """
        wfn = self.wfn

        if Da is not None or Db is not None:
            Da_temp = np.copy(self.wfn.Da().np)
            Db_temp = np.copy(self.wfn.Db().np)
            if Da is not None:
                wfn.Da().np[:] = Da
            if Db is not None:
                wfn.Db().np[:] = Db

        nthreads = psi4.get_num_threads()
        psi4.set_num_threads(1)
        
        if grid is not None:
            if type(grid) is np.ndarray:
                blocks, npoints, points_function = self.grid_to_blocks(grid)
            else:
                blocks, npoints, points_function = grid
        elif vpot is not None:
            nblocks = vpot.nblocks()
            blocks = [vpot.get_block(i) for i in range(nblocks)]
            npoints = vpot.grid().npoints()
        elif vpot is not None and grid is not None:
            raise ValueError("Only one option can be given")

        #Initialize Arrays
        vext = np.zeros(npoints)
        esp  = np.zeros(npoints)

        #Get Atomic Information
        mol_dict = self.mol.to_schema(dtype='psi4')
        natoms = len(mol_dict["elem"])
        indx = [i for i in range(natoms) if self.mol.charge(i) != 0.0]
        natoms = len(indx)
        #Atomic numbers and Atomic positions
        zs = [mol_dict["elez"][i] for i in indx]
        rs = [self.mol.geometry().np[i] for i in indx]

        if compute_hartree:
            esp_wfn = psi4.core.ESPPropCalc(wfn)

        #Loop Through blocks
        offset = 0
        with np.errstate(divide='ignore'):
            for i_block in blocks:
                b_points = i_block.npoints()
                offset += b_points
                x = i_block.x().np
                y = i_block.y().np
                z = i_block.z().np

                #EXTERNAL
                for atom in range(natoms):
                    r =  np.sqrt((x-rs[atom][0])**2 + (y-rs[atom][1])**2 + (z-rs[atom][2])**2)
                    vext_temp = - 1.0 * zs[atom] / r
                    vext_temp[np.isinf(vext_temp)] = 0.0
                    vext[offset - b_points : offset] += vext_temp

                if compute_hartree:
                    #ESP
                    xyz = np.concatenate((x[:,None],y[:,None],z[:,None]), axis=1)
                    grid_block = psi4.core.Matrix.from_array(xyz)
                    esp[offset - b_points : offset] = esp_wfn.compute_esp_over_grid_in_memory(grid_block).np

        #Hartree
        if compute_hartree:
            hartree = - 1.0 * (vext + esp)

        if Da is not None:
            self.wfn.Da().np[:] = Da_temp
        if Db is not None:
            self.wfn.Db().np[:] = Db_temp
        psi4.set_num_threads(nthreads)

        if compute_hartree:
            return vext, hartree, esp
        else:
            return vext

    def vxc(self, func_id=1, Da=None, Db=None, grid=None):
        """
        Generates Vxc given grid
        Parameters
        ----------
        Da, Db: np.ndarray
            Alpha, Beta densities. Shape: (num_ao_basis, num_ao_basis)
        func_id: int
            Functional ID associated with Density Functional Approximationl.
            Full list of functionals: https://www.tddft.org/programs/libxc/functionals/
        grid: np.ndarray Shape: (3, npoints) or (4, npoints) or tuple for block_handler (return of grid_to_blocks)
            grid where density will be computed.
        Vpot: psi4.core.VBase
            Vpotential object with info about grid.
            Provides DFT spherical grid. Only comes to play if no grid is given. 
        Returns
        -------
        VXC: np.ndarray
            Exchange correlation potential on the given grid
            Shape: (npoints, )
        """

        if func_id != 1:
            raise ValueError("Only LDA fucntionals are supported on the grid")

        if Da is None:
            Da = self.Dt[0]
        if Db is None:
            Db = self.Dt[0]

        if grid is not None:
            if type(grid) is np.ndarray:
                blocks, npoints, points_function = self.grid_to_blocks(grid)
            else:
                blocks, npoints, points_function = grid
            density = self.density(Da=Da, Db=Db, grid=grid)
        elif grid is None and Vpot is not None:
            nblocks = self.Vpot.nblocks()
            blocks = [Vpot.get_block(i) for i in range(nblocks)]
            npoints = Vpot.grid().npoints()
            density = self.density(Da=Da, Db=Db, Vpot=self.Vpot)
        else:
            raise ValueError("A grid or a V_potential (DFT grid) must be given.")

        vxc = np.zeros((npoints, self.ref))
        ingredients = {}
        offset = 0
        for i_block in blocks:
            b_points = i_block.npoints()
            offset += b_points
            if self.ref == 1:
                ingredients["rho"] = density[offset - b_points : offset]
            else:
                ingredients["rho"] = density[offset - b_points : offset, :]

            if self.ref == 1:
                functional = Functional(1, 1)
            else:
                functional = Functional(1, 2) 
            xc_dictionary = functional.compute(ingredients)
            vxc[offset - b_points : offset, :] = xc_dictionary['vrho']

        return np.squeeze(vxc)

    def average_local_orbital_energy(self, D, C, eig, grid_info=None):
        """
        (4)(6) in mRKS.
        """

        # Nalpha = self.molecule.nalpha
        # Nbeta = self.molecule.nbeta

        if grid_info is None:
            e_bar = np.zeros(self.Vpot.grid().npoints())
            nblocks = self.Vpot.nblocks()

            points_func = self.Vpot.properties()[0]
            points_func.set_deriv(0)
            blocks = None
        else:
            blocks, npoints, points_func = grid_info
            e_bar = np.zeros(npoints)
            nblocks = len(blocks)
            points_func.set_deriv(0)

        if Db is None:
            points_func.set_pointers(Da)
        else:
            points_function.set_pointers(Da, Db)

        # For unrestricted
        iw = 0
        for l_block in range(nblocks):
            # Obtain general grid information
            if blocks is None:
                l_grid = self.Vpot.get_block(l_block)
            else:
                l_grid = blocks[l_block]
            l_npoints = l_grid.npoints()

            points_func.compute_points(l_grid)
            l_lpos = np.array(l_grid.functions_local_to_global())
            if len(l_lpos) == 0:
                iw += l_npoints
                continue
            l_phi = np.array(points_func.basis_values()["PHI"])[:l_npoints, :l_lpos.shape[0]]
            lD = D[(l_lpos[:, None], l_lpos)]
            lC = C[l_lpos, :]
            rho = contract('pm,mn,pn->p', l_phi, lD, l_phi)
            e_bar[iw:iw + l_npoints] = contract("pm,mi,ni,i,pn->p", l_phi, lC, lC, eig, l_phi) / rho

            iw += l_npoints
        assert iw == e_bar.shape[0], "Somehow the whole space is not fully integrated."
        return e_bar

    def optimized_external_potential(self, grid=None, average_alpha_beta=False):
        """
        $
        v^{~}{ext}(r) = \epsilon^{-LDA}(r)
        - \frac{\tau^{LDA}{L}}{n^{LDA}(r)}
        - v_{H}^{LDA}(r) - v_{xc}^{LDA}(r)
        $
        (22) in [1].
        """

        Nalpha = self.nalpha
        Nbeta = self.nbeta

        # LDA calculation
        Da_LDA, Db_DLA, Ca_LDA, Cb_LDA, epsilon_a_LDA, epsilon_b_LDA = self.eng.compute_LDA()
        vxc_LDA = self.on_grid_vxc(Da=Da_LDA, Db=Db_LDA, grid=grid)

        if self.ref != 1:
            assert vxc_LDA.shape[-1] == 2
            vxc_LDA_beta = vxc_LDA[:,1]
            vxc_LDA = vxc_LDA[:, 0]
            vxc_LDA_DFT_beta = vxc_LDA_DFT[:, 1]
            vxc_LDA_DFT = vxc_LDA_DFT[:, 0]

        # _average_local_orbital_energy() taken from mrks.py.
        #---> Compute average loca orbital energy
        e_bar = self.average_local_orbital_energy(Da_LDA, Ca_LDA[:, :Nalpha], epsilon_a_LDA[:Nalpha], grid=grid)
        tauLmP_rho = self._get_l_kinetic_energy_density_directly(Da_LDA, Ca_LDA[:,:Nalpha], grid=grid_info)
        tauP_rho = self._pauli_kinetic_energy_density(Da_LDA, Ca_LDA[:,:Nalpha], grid=grid)

        tauL_rho_DFT = tauLmP_rho_DFT + tauP_rho_DFT
        tauL_rho = tauLmP_rho + tauP_rho

        vext_opt_no_H_DFT = e_bar_DFT - tauL_rho_DFT - vxc_LDA_DFT
        vext_opt_no_H = e_bar - tauL_rho - vxc_LDA

        J = self.form_jk(Ca_LDA[:,:Nalpha],  Cb_LDA[:,:Nbeta])[0]
        vext_opt_no_H_DFT_Fock = self.dft_grid_to_fock(vext_opt_no_H_DFT, self.Vpot)
        vext_opt_DFT_Fock = vext_opt_no_H_DFT_Fock - J[0] - J[1]

        # # Does vext_opt need a shift?
        # Fock_LDA = self.T + vext_opt_DFT_Fock + J[0] + J[1] + self.dft_grid_to_fock(vxc_LDA_DFT, self.Vpot)
        # eigvecs_a = self.diagonalize(Fock_LDA, self.nalpha)[-1]
        # shift = eigvecs_a[Nalpha-1] - epsilon_a_LDA[Nalpha-1]
        # vext_opt_DFT_Fock -= shift * self.S2
        # print("LDA shift:", shift, eigvecs_a[Nalpha-1], epsilon_a_LDA[Nalpha-1])

        vH = self.on_grid_esp(grid=grid_info, wfn=wfn_LDA)[1]
        vext_opt = vext_opt_no_H - vH
        # vext_opt -= shift

        if self.ref != 1:
            e_bar_DFT_beta = self._average_local_orbital_energy(Db_LDA, Cb_LDA[:,:Nbeta], epsilon_b_LDA[:Nbeta])
            e_bar_beta = self._average_local_orbital_energy(Db_LDA, Cb_LDA[:, :Nbeta], epsilon_b_LDA[:Nbeta], grid_info=grid_info)


            tauLmP_rho_DFT_beta = self._get_l_kinetic_energy_density_directly(Db_LDA, Cb_LDA[:,:Nbeta])
            tauLmP_rho_beta = self._get_l_kinetic_energy_density_directly(Db_LDA, Cb_LDA[:,:Nalpha], grid_info=grid_info)

            tauP_rho_DFT_beta = self._pauli_kinetic_energy_density(Db_LDA, Cb_LDA[:,:Nbeta])
            tauP_rho_beta = self._pauli_kinetic_energy_density(Db_LDA, Cb_LDA[:,:Nbeta], grid_info=grid_info)

            tauL_rho_DFT_beta = tauLmP_rho_DFT_beta + tauP_rho_DFT_beta
            tauL_rho_beta = tauLmP_rho_beta + tauP_rho_beta

            vext_opt_no_H_DFT_beta = e_bar_DFT_beta - tauL_rho_DFT_beta - vxc_LDA_DFT_beta
            vext_opt_no_H_beta = e_bar_beta - tauL_rho_beta - vxc_LDA_beta

            vext_opt_no_H_DFT_Fock_beta = self.dft_grid_to_fock(vext_opt_no_H_DFT_beta, self.Vpot)
            vext_opt_DFT_Fock_beta = vext_opt_no_H_DFT_Fock_beta - J[0] - J[1]

            vext_opt_beta = vext_opt_no_H_beta - vH

            # vext_opt_DFT_Fock = (vext_opt_DFT_Fock + vext_opt_DFT_Fock_beta) * 0.5
            # vext_opt = (vext_opt + vext_opt_beta) * 0.5

            return (vext_opt_DFT_Fock, vext_opt_DFT_Fock_beta), (vext_opt, vext_opt_beta)
        return vext_opt_DFT_Fock, vext_opt

    def get_orbitals(self, basis, molecule):

        pass
