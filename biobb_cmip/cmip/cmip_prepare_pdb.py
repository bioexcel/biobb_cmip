#!/usr/bin/env python3

"""Module containing the CmipPreparePDB class and the command line interface."""
from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject, launcher


class CmipPreparePDB(BiobbObject):
    """
    | biobb_cmip CmipPreparePDB
    | Class to add CMIP charges and atom types.
    | Add CMIP charges and atom types to a PDB structure using `biobb_structure_checking <https://anaconda.org/bioconda/biobb_structure_checking>`_.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/data/cmip/1aki.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_cmip_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/reference/cmip/egfr_cmip.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **remove_water** (*bool*) - (True) Remove Water molecules.
            * **keep_hydrogen** (*bool*) - (False) All hydrogen atoms will be removed before adding the new ones unless this option is set True.
            * **fix_sidechains** (*bool*) - (True) Complete side chains (heavy atoms, protein only).
            * **fix_backbone_atoms** (*bool*) - (True) Add missing O, OXT backbone atoms.
            * **check_structure_path** (*str*) - ("check_structure") Path to the check_structure executable binary of biobb_structure_checking.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.


    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_cmip.cmip.cmip_prepare_pdb import cmip_prepare_pdb
            prop = { 'restart': False }
            cmip_prepare_pdb(input_pdb_path='/path/to/myStructure.pdb',
                        output_cmip_pdb_path='/path/to/newStructure.pdb',
                        properties=prop)

    Info:
        * wrapped_software:
            * name: CMIP cmip
            * version: 2.7.0
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_pdb_path: str, output_cmip_pdb_path: str, properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def run(self) -> None:
        """Execute the :class:`CmipPreparePDB <cmip.cmip_prepare_pdb.CmipPreparePDB>` object."""

        command_list = ""
        if self.remove_water:
            command_list += 'water --remove yes; '

        if self.fix_backbone_atoms:
            command_list += 'backbone --add_caps none; '

        if self.fix_sidechains:
            command_list += 'fixside --fix All; '

        command_list += 'add_hydrogen --add_mode auto '
        if self.keep_hydrogen:
            command_list += ' --keep_h '
        command_list += '--add_charges CMIP'

        self.cmd = [self.check_structure_path,
                    '-v',
                    '-i', self.stage_io_dict["in"]["input_pdb_path"],
                    '-o', self.stage_io_dict["out"]["output_cmip_pdb_path"],
                    '--output_format', 'cmip',
                    '--non_interactive',
                    'command_list',
                    '--list', "'"+command_list+"'"]

        # Run Biobb block
        self.run_biobb()


cmip_prepare_pdb = launcher(CmipPreparePDB)

if __name__ == '__main__':
    CmipPreparePDB.main()
