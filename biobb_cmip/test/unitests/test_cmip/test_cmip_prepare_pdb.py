# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.cmip_prepare_pdb import cmip_prepare_pdb


class TestCmipPreparePDB():
    def setup_class(self):
        fx.test_setup(self, 'cmip_prepare_pdb')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_cmip_prepare_pdb(self):
        cmip_prepare_pdb(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_cmip_pdb_path'])
        assert fx.equal(self.paths['output_cmip_pdb_path'], self.paths['ref_output_prepare_structure_pdb_path'])
