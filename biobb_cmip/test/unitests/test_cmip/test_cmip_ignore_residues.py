# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.cmip_ignore_residues import cmip_ignore_residues


class TestCmipIgnoreResidues():
    def setup_class(self):
        fx.test_setup(self, 'cmip_ignore_residues')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_cmip_ignore_residues(self):
        cmip_ignore_residues(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_cmip_pdb_path'])
        assert fx.equal(self.paths['output_cmip_pdb_path'], self.paths['ref_output_ignore_residues_pdb_path'])
