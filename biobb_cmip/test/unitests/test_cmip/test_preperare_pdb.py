from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.prepare_pdb import prepare_pdb


class TestPreparePDB():
    def setUp(self):
        fx.test_setup(self, 'prepare_pdb')

    def tearDown(self):
        # pass
        fx.test_teardown(self)

    def test_prepare_pdb(self):
        prepare_pdb(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_cmip_pdb_path'])
        assert fx.equal(self.paths['output_cmip_pdb_path'], self.paths['ref_output_prepare_structure_pdb_path'])


