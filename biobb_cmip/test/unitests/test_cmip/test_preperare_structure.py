from biobb_common.tools import test_fixtures as fx
from biobb_cmip.cmip.prepare_structure import prepare_structure


# class TestPrepareStructure():
#     def setUp(self):
#         fx.test_setup(self, 'prepare_structure')
#
#     def tearDown(self):
#         pass
#         #fx.test_teardown(self)
#
#     def test_prepare_structure(self):
#         prepare_structure(properties=self.properties, **self.paths)
#         assert fx.not_empty(self.paths['output_pdb_path'])
#         assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_prepare_structure_pdb_path'], remove_hetatm=False)


class TestPrepareStructureTopology():
    def setUp(self):
        fx.test_setup(self, 'prepare_structure_topology')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_prepare_structureTopology(self):
        prepare_structure(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_prepare_structure_topology_path'], remove_hetatm=False)
