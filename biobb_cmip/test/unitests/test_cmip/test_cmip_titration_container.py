# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.cmip_titration import cmip_titration
import pytest
import sys


class TestCmipTitrationDocker():
    def setup_class(self):
        fx.test_setup(self, 'cmip_titration_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_cmip_titration_docker(self):
        cmip_titration(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestCmipTitrationSingularity():
    def setup_class(self):
        fx.test_setup(self, 'cmip_titration_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_cmip_titration_singularity(self):
        cmip_titration(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
