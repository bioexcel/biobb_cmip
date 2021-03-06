from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.ignore_residues import ignore_residues


class TestIgnoreResidues():
    def setUp(self):
        fx.test_setup(self, 'ignore_residues')

    def tearDown(self):
        pass
        #fx.test_teardown(self)

    def test_ignore_residues(self):
        ignore_residues(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_cmip_pdb_path'])
        assert fx.equal(self.paths['output_cmip_pdb_path'], self.paths['ref_output_ignore_residues_pdb_path'])


