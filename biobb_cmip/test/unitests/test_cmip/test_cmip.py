from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.cmip import cmip


# class TestCmipMip():
#     def setUp(self):
#         fx.test_setup(self, 'cmip_mip')
#
#     def tearDown(self):
#         #pass
#         fx.test_teardown(self)
#
#     def test_cmip_mip(self):
#         cmip(properties=self.properties, **self.paths)
#         assert fx.not_empty(self.paths['output_cube_path'])
#         assert fx.not_empty(self.paths['output_grd_path'])
#         assert fx.equal(self.paths['output_grd_path'], self.paths['ref_output_cmip_mip_grd_path'])
#         assert fx.equal(self.paths['output_cube_path'], self.paths['ref_output_cmip_mip_cube_path'])


class TestCmipDocking():
    def setUp(self):
        fx.test_setup(self, 'cmip_docking')

    def tearDown(self):
        pass
        #fx.test_teardown(self)

    def test_cmip_docking(self):
        cmip(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.not_empty(self.paths['output_grd_path'])
        assert fx.not_empty(self.paths['output_rst_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_cmip_docking_pdb_path'], remove_hetatm=False)
        #assert fx.equal(self.paths['output_grd_path'], self.paths['ref_output_cmip_docking_grd_path'])
        #assert fx.equal(self.paths['output_rst_path'], self.paths['ref_output_cmip_docking_rst_path'])


# class TestCmipEnergy():
#     def setUp(self):
#         fx.test_setup(self, 'cmip_energy')
#
#     def tearDown(self):
#         #pass
#         fx.test_teardown(self)
#
#     def test_cmip_mip(self):
#         cmip(properties=self.properties, **self.paths)
#         assert fx.not_empty(self.paths['output_cube_path'])
#         assert fx.not_empty(self.paths['output_grd_path'])
#         assert fx.equal(self.paths['output_grd_path'], self.paths['ref_output_cmip_mip_grd_path'])
#         assert fx.equal(self.paths['output_cube_path'], self.paths['ref_output_cmip_mip_cube_path'])
#
# class TestCmipSolvation():
#     def setUp(self):
#         fx.test_setup(self, 'cmip_solvation')
#
#     def tearDown(self):
#         #pass
#         fx.test_teardown(self)
#
#     def test_cmip_mip(self):
#         cmip(properties=self.properties, **self.paths)
#         assert fx.not_empty(self.paths['output_cube_path'])
#         assert fx.not_empty(self.paths['output_grd_path'])
#         assert fx.equal(self.paths['output_grd_path'], self.paths['ref_output_cmip_mip_grd_path'])
#         assert fx.equal(self.paths['output_cube_path'], self.paths['ref_output_cmip_mip_cube_path'])