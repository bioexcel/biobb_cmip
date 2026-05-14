# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.cmip_run import cmip_run
import pytest
import sys


class TestCmipRunDocker():
    def setup_class(self):
        fx.test_setup(self, 'cmip_run_docker')

    def teardown_class(self):
        # pass
        fx.test_teardown(self)

    def test_cmip_run_docker(self):
        cmip_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_byat_path'])
        # assert fx.equal(self.paths['output_byat_path'], self.paths['ref_output_byat_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestCmipRunSingularity():
    def setup_class(self):
        fx.test_setup(self, 'cmip_run_singularity')

    def teardown_class(self):
        # pass
        fx.test_teardown(self)

    def test_cmip_run_singularity(self):
        cmip_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_byat_path'])
        # assert fx.equal(self.paths['output_byat_path'], self.paths['ref_output_byat_path'])
