from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.cmip import cmip


# class TestCmipMip():
#     def setup_class(self):
#         fx.test_setup(self, 'cmip_mip')
#
#     def teardown_class(self):
#         #pass
#         fx.test_teardown(self)
#
#     def test_cmip_mip(self):
#         cmip(properties=self.properties, **self.paths)
#         assert fx.not_empty(self.paths['output_cube_path'])
#         assert fx.not_empty(self.paths['output_grd_path'])
#         assert fx.equal(self.paths['output_grd_path'], self.paths['ref_output_cmip_mip_grd_path'])
#         assert fx.equal(self.paths['output_cube_path'], self.paths['ref_output_cmip_mip_cube_path'])


# class TestCmipDocking():

#     def setup_class(self):
#         fx.test_setup(self, 'cmip_docking')
#
#     def teardown_class(self):
#         #pass
#         fx.test_teardown(self)
#
#     def test_cmip_docking(self):
#         cmip(properties=self.properties, **self.paths)
#         assert fx.not_empty(self.paths['output_pdb_path'])
#         assert fx.not_empty(self.paths['output_grd_path'])
#         assert fx.not_empty(self.paths['output_rst_path'])
#         assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_cmip_docking_pdb_path'], remove_hetatm=False)
#         #assert fx.equal(self.paths['output_grd_path'], self.paths['ref_output_cmip_docking_grd_path'])
#         #assert fx.equal(self.paths['output_rst_path'], self.paths['ref_output_cmip_docking_rst_path'])


class TestCmipEnergy():
    def setup_class(self):
        fx.test_setup(self, 'cmip')

    def teardown_class(self):
        #pass
        fx.test_teardown(self)

    def test_cmip_energy(self):
        cmip(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_byat_path'])
        #assert fx.equal(self.paths['output_byat_path'], self.paths['ref_output_byat_path'])

# class TestCmipSolvation():

#     def setup_class(self):
#         fx.test_setup(self, 'cmip_solvation')
#
#     def teardown_class(self):
#         #pass
#         fx.test_teardown(self)
#
#     def test_cmip_mip(self):
#         cmip(properties=self.properties, **self.paths)
#         assert fx.not_empty(self.paths['output_cube_path'])
#         assert fx.not_empty(self.paths['output_grd_path'])
#         assert fx.equal(self.paths['output_grd_path'], self.paths['ref_output_cmip_mip_grd_path'])
#         assert fx.equal(self.paths['output_cube_path'], self.paths['ref_output_cmip_mip_cube_path'])