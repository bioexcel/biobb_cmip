from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.cmip import cmip


class TestCmipMipDocker():
    def setUp(self):
        fx.test_setup(self, 'cmip_mip_docker')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_cmip_mip_docker(self):
        cmip(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_cube_path'])
        assert fx.not_empty(self.paths['output_grd_path'])
        assert fx.equal(self.paths['output_grd_path'], self.paths['ref_output_cmip_mip_grd_path'])
        assert fx.equal(self.paths['output_cube_path'], self.paths['ref_output_cmip_mip_cube_path'])


class TestCmipDockingDocker():
    def setUp(self):
        fx.test_setup(self, 'cmip_docking_docker')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_cmip_docking_docker(self):
        cmip(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.not_empty(self.paths['output_grd_path'])
        assert fx.not_empty(self.paths['output_rst_path'])
        # Can not compare PDB files formed excluvely by HETATM
        #assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_cmip_docking_pdb_path'])
        # GRD differs between executions
        #assert fx.equal(self.paths['output_grd_path'], self.paths['ref_output_cmip_docking_grd_path'])
        # RST differs between executions
        #assert fx.equal(self.paths['output_rst_path'], self.paths['ref_output_cmip_docking_rst_path'])

class TestCmipEnergyDocker():
    def setUp(self):
        fx.test_setup(self, 'cmip_energy_docker')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_cmip_mip_docker(self):
        cmip(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_cube_path'])
        assert fx.not_empty(self.paths['output_grd_path'])
        assert fx.equal(self.paths['output_grd_path'], self.paths['ref_output_cmip_mip_grd_path'])
        assert fx.equal(self.paths['output_cube_path'], self.paths['ref_output_cmip_mip_cube_path'])

class TestCmipSolvationDocker():
    def setUp(self):
        fx.test_setup(self, 'cmip_solvation_docker')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_cmip_mip_docker(self):
        cmip(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_cube_path'])
        assert fx.not_empty(self.paths['output_grd_path'])
        assert fx.equal(self.paths['output_grd_path'], self.paths['ref_output_cmip_mip_grd_path'])
        assert fx.equal(self.paths['output_cube_path'], self.paths['ref_output_cmip_mip_cube_path'])