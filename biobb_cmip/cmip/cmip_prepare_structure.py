#!/usr/bin/env python3

"""Module containing the CmipPrepareStructure class and the command line interface."""
from typing import Optional
import warnings
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu
from biobb_cmip.cmip.common import write_cmip_pdb
from biobb_cmip.cmip.common import get_topology_charges_and_elements
from biobb_cmip.cmip.common import get_pdb_charges_and_elements


class CmipPrepareStructure(BiobbObject):
    """
    | biobb_cmip PrepareStructure
    | Generate a CMIP suitable PDB input.
    | Generate a CMIP suitable PDB input from a common PDB file or a Topology + PDB file.

    Args:
        input_pdb_path (str): Path to the input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/data/cmip/egfr.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_topology_path (str) (Optional): Path to the input topology path. File type: input. `Sample file <https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/data/cmip/egfr_topology.zip>`_. Accepted formats: zip (edam:format_3987), top (edam:format_3880), psf (edam:format_3882), prmtop (edam:format_3881).
        output_cmip_pdb_path (str): Path to the output PDB file. File type: output. `Sample file <https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/reference/cmip/egfr_cmip.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - ("cmip/cmip:latest") Container Image identifier.
            * **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.


    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_cmip.cmip.prepare_structure import prepare_structure
            prop = { }
            prepare_structure(input_pdb_path='/path/to/myStructure.pdb',
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

    def __init__(self, input_pdb_path: str, output_cmip_pdb_path: str, input_topology_path: Optional[str] = None, properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def stage_files(self) -> None:
        """The block does not use the sandbox: there are no files to stage."""

    def run(self) -> None:
        """Execute the :class:`CmipPrepareStructure <cmip.cmip_prepare_structure.CmipPrepareStructure>` object."""
        # Charges and atom types from the topology
        if self.io_dict['in']['input_topology_path']:
            top_file = self.io_dict['in']['input_topology_path']
            if top_file.lower().endswith(".zip"):
                top_file = fu.unzip_top(zip_file=top_file, out_log=self.out_log)
                self.tmp_files.append(str(Path(top_file).parent))

            fu.log(f'Reading the charges and atom types of {top_file}', self.out_log, self.global_log)
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                charges_list, elements_list = get_topology_charges_and_elements(top_file)

        # Charges and atom types from the CMIP residue library
        else:
            charges_list, elements_list = get_pdb_charges_and_elements(
                self.io_dict['in']['input_pdb_path'], out_log=self.out_log, global_log=self.global_log)

        write_cmip_pdb(self.io_dict['in']['input_pdb_path'],
                       self.io_dict['out']['output_cmip_pdb_path'],
                       charges_list,
                       elements_list)


cmip_prepare_structure = launcher(CmipPrepareStructure)

if __name__ == '__main__':
    CmipPrepareStructure.main()
