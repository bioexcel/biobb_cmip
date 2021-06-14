from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.titration import titration

class TestTitrationSingularity():
    def setUp(self):
        fx.test_setup(self, 'titration_singularity')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_titration_singularity(self):
        titration(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
