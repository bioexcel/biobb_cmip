from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.titration import titration


class TestTitration():
    def setup_class(self):
        fx.test_setup(self, 'titration')

    def teardown_class(self):
        pass
        #fx.test_teardown(self)

    def test_titration(self):
        titration(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
