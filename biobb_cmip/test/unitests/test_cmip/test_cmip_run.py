# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.cmip_run import cmip_run


class TestCmipRun():
    def setup_class(self):
        fx.test_setup(self, 'cmip_run')

    def teardown_class(self):
        # pass
        fx.test_teardown(self)

    def test_cmip_run(self):
        cmip_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_byat_path'])
        # assert fx.equal(self.paths['output_byat_path'], self.paths['ref_output_byat_path'])
