#!/usr/bin/env python3

"""Module containing the CmipIgnoreResidues class and the command line interface."""
from typing import Optional
import shutil
from biobb_cmip.cmip.common import mark_residues
from biobb_common.generic.biobb_object import BiobbObject, launcher
import biobb_common.tools.file_utils as fu


class CmipIgnoreResidues(BiobbObject):
    """
    | biobb_cmip CmipIgnoreResidues
    | Class to ignore residues in CMIP potential calculations.
    | Mark residues which will be ignored in the CMIP potential calculations except for dielectric definition.

    Args:
        input_cmip_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/data/cmip/input_ignore_res.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_cmip_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/reference/cmip/ignore_res_gln3.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **residue_list** (*str*) - (None) Residue list in the format "Chain:Resnum" (no spaces between the elements) separated by commas. A residue without chain ("3") is marked in every chain, a chain without residue number ("A:") marks the whole chain. ie: "A:3".
            * **ignore_all** (*bool*) - (False) Mark all the residues in the PDB file.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.


    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_cmip.cmip.cmip_ignore_residues import cmip_ignore_residues
            prop = { 'residue_list': "A:3" }
            cmip_ignore_residues(input_cmip_pdb_path='/path/to/myStructure.pdb',
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

    def __init__(self, input_cmip_pdb_path: str, output_cmip_pdb_path: str, properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def stage_files(self) -> None:
        """The block does not use the sandbox: there are no files to stage."""

    def run(self) -> None:
        """Execute the :class:`CmipIgnoreResidues <cmip.cmip_ignore_residues.CmipIgnoreResidues>` object."""

        if not self.ignore_all and not self.residue_list:
            fu.log("Residue_list is empty and ignore_all is false nothing will be done.", self.out_log, self.global_log)
            shutil.copyfile(self.io_dict["in"]["input_cmip_pdb_path"], self.io_dict["out"]["output_cmip_pdb_path"])
            return

        if self.ignore_all:
            self.residue_list = None

        if self.residue_list:
            if not isinstance(self.residue_list, list):
                self.residue_list = str(self.residue_list).split(",")
            for i in range(len(self.residue_list)):
                residue_code_list = str(self.residue_list[i]).split(":")
                if len(residue_code_list) < 2:
                    resnum = residue_code_list[0]
                    chain = ''
                else:
                    chain, resnum = residue_code_list
                self.residue_list[i] = chain.strip().upper()+":"+str(resnum).strip()

        mark_residues(residue_list=self.residue_list or [], input_cmip_pdb_path=self.io_dict["in"]["input_cmip_pdb_path"], output_cmip_pdb_path=self.io_dict["out"]["output_cmip_pdb_path"], out_log=self.out_log, global_log=self.global_log)


cmip_ignore_residues = launcher(CmipIgnoreResidues)

if __name__ == '__main__':
    CmipIgnoreResidues.main()
