#!/usr/bin/env python3

"""Module containing the CmipRun class and the command line interface."""
import os
from typing import Optional
from typing import Any
import shutil
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu
from biobb_cmip.cmip.common import create_params_file
from biobb_cmip.cmip.common import params_preset
from biobb_cmip.cmip.common import params_from_box
from biobb_cmip.cmip.common import write_json_box

# CMIP flag of each optional input and output file, in the order of the command
_FILE_FLAGS = {'input_probe_pdb_path': '-pr', 'output_pdb_path': '-outpdb', 'output_grd_path': '-grdout',
               'output_cube_path': '-cube', 'output_rst_path': '-rst', 'output_byat_path': '-byat',
               'output_log_path': '-o'}


class CmipRun(BiobbObject):
    """
    | biobb_cmip CmipRun
    | Wrapper class for the CMIP cmip module.
    | Compute classical molecular interaction potentials with the CMIP cmip module.

    Args:
        input_pdb_path (str): Path to the input PDB file. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_cmip/master/biobb_cmip/test/data/cmip/RBD-hACE2.hACE2.cmip.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_probe_pdb_path (str) (Optional): Path to the input probe file in PDB format. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_cmip/master/biobb_cmip/test/data/cmip/RBD-hACE2.RBD.cmip.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str) (Optional): Path to the output PDB file, its name must end in .pdb and not contain underscores. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_cmip/master/biobb_cmip/test/reference/cmip/cmip_docking.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_grd_path (str) (Optional): Path to the output grid file in GRD format. File type: output. Accepted formats: grd (edam:format_2330).
        output_cube_path (str) (Optional): Path to the output grid file in cube format. File type: output. Accepted formats: cube (edam:format_2330).
        output_rst_path (str) (Optional): Path to the output restart file. File type: output. Accepted formats: txt (edam:format_2330).
        input_rst_path (str) (Optional): Path to the input restart file. File type: input. Accepted formats: txt (edam:format_2330).
        output_byat_path (str) (Optional): Path to the output atom by atom energy file. File type: output. Accepted formats: txt (edam:format_2330), out (edam:format_2330).
        output_log_path (str) (Optional): Path to the output CMIP log file LOG. File type: output. Accepted formats: log (edam:format_2330).
        input_vdw_params_path (str) (Optional): Path to the CMIP input Van der Waals force parameters, if not provided the CMIP conda installation one is used ("$CONDA_PREFIX/share/cmip/dat/vdwprm"). File type: input. Accepted formats: txt (edam:format_2330).
        input_params_path (str) (Optional): Path to the CMIP input parameters file. File type: input. Accepted formats: txt (edam:format_2330).
        output_json_box_path (str) (Optional): Path to the output CMIP box in JSON format. File type: output. Accepted formats: json (edam:format_3464).
        output_json_external_box_path (str) (Optional): Path to the output external CMIP box in JSON format. File type: output. Accepted formats: json (edam:format_3464).
        input_json_box_path (str) (Optional): Path to the input CMIP box in JSON format. File type: input. Accepted formats: json (edam:format_3464).
        input_json_external_box_path (str) (Optional): Path to the input external CMIP box in JSON format. File type: input. Accepted formats: json (edam:format_3464).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **execution_type** (*str*) - ("mip_pos") Default options for the params file, each one creates a different params file. Values: check_only (Dry Run of CMIP), mip_pos (MIP O+  Mehler Solmajer dielectric), mip_neg (MIP O-  Mehler Solmajer dielectric), mip_neu (MIP Oxygen Mehler Solmajer dielectric), solvation (Solvation & MEP), pb_interaction_energy (Docking Interaction energy calculation. PB electrostatics), docking (Docking Mehler Solmajer dielectric), docking_rst (Docking from restart file).
            * **params** (*dict*) - ({}) CMIP options specification.
            * **binary_path** (*str*) - ("cmip") Path to the CMIP cmip executable binary.
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

            from biobb_cmip.cmip.cmip_run import cmip_run
            prop = { 'execution_type': 'mip_pos' }
            cmip_run(input_pdb_path='/path/to/myStructure.pdb',
                     output_cube_path='/path/to/myGrid.cube',
                     output_log_path='/path/to/myLog.log',
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

    def __init__(self, input_pdb_path: str, input_probe_pdb_path: Optional[str] = None, output_pdb_path: Optional[str] = None,
                 output_grd_path: Optional[str] = None, output_cube_path: Optional[str] = None, output_rst_path: Optional[str] = None,
                 input_rst_path: Optional[str] = None, output_byat_path: Optional[str] = None, output_log_path: Optional[str] = None,
                 input_vdw_params_path: Optional[str] = None, input_params_path: Optional[str] = None, output_json_box_path: Optional[str] = None,
                 output_json_external_box_path: Optional[str] = None, input_json_box_path: Optional[str] = None,
                 input_json_external_box_path: Optional[str] = None, properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

        # Properties specific for BB
        self.params = {k: str(v) for k, v in self.params.items()}

        if not self.io_dict['in'].get('input_vdw_params_path'):
            self.io_dict['in']['input_vdw_params_path'] = f"{os.environ.get('CONDA_PREFIX')}/share/cmip/dat/vdwprm"

    def prepare(self) -> None:
        """Create the CMIP parameters file."""
        output_pdb_path = self.io_dict['out']['output_pdb_path']
        if output_pdb_path and (not output_pdb_path.endswith('.pdb') or "_" in Path(output_pdb_path).name):
            message = f"ERROR: output_pdb_path ({output_pdb_path}) name must end in .pdb and not contain underscores"
            fu.log(message, self.out_log, self.global_log)
            raise ValueError(message)

        params_preset_dict: dict[str, Any] = params_preset(execution_type=self.execution_type)
        # Grids of the input boxes, the outer one first
        for box_key, grid_id in (('input_json_external_box_path', '0'), ('input_json_box_path', '')):
            if self.io_dict['in'][box_key]:
                params_preset_dict.update(params_from_box(self.io_dict['in'][box_key], grid_id))

        # The output boxes are read from the CMIP log
        if self.io_dict['out']['output_json_box_path'] or self.io_dict['out']['output_json_external_box_path']:
            if not self.io_dict['out']['output_log_path']:
                self.io_dict['out']['output_log_path'] = self.create_tmp_file('.log')

        # Restart OUT
        if self.io_dict['out']['output_rst_path']:
            params_preset_dict['FULLRST'] = 1
            params_preset_dict['OREST'] = 1

        # Restart IN
        if self.io_dict['in']['input_rst_path']:
            params_preset_dict['IREST'] = 2
            if not self.io_dict['out']['output_rst_path']:
                self.io_dict['out']['output_rst_path'] = self.create_tmp_file('')
        else:
            params_preset_dict['IREST'] = 0

        self.io_dict['in']['combined_params_path'] = create_params_file(
            output_params_path=str(Path(self.create_tmp_dir()).joinpath('params')),
            input_params_path=self.io_dict['in']['input_params_path'],
            params_preset_dict=params_preset_dict,
            params_properties_dict=self.params)

    def run(self) -> None:
        """Execute the :class:`CmipRun <cmip.cmip_run.CmipRun>` object."""

        self.cmd = [self.binary_path,
                    '-i', self.stage_io_dict['in']['combined_params_path'],
                    '-vdw', self.stage_io_dict['in']['input_vdw_params_path'],
                    '-hs', self.stage_io_dict['in']['input_pdb_path']]
        staged_files = {**self.stage_io_dict['in'], **self.stage_io_dict['out']}
        for file_key, flag in _FILE_FLAGS.items():
            if staged_files.get(file_key):
                self.cmd += [flag, staged_files[file_key]]

        # CMIP reads the input restart from the -rst file (written in the sandbox)
        if self.io_dict['in']['input_rst_path']:
            shutil.copy2(self.io_dict['in']['input_rst_path'], self.sandbox_file('output_rst_path'))

        # Run Biobb block
        self.run_biobb()

        # CMIP removes or adds the .pdb extension of the output PDB and writes "ATOMTM" for "ATOM  "
        output_pdb_path = self.sandbox_file('output_pdb_path')
        if output_pdb_path:
            for cmip_pdb_path in (output_pdb_path[:-4], output_pdb_path + '.pdb'):
                if Path(cmip_pdb_path).exists():
                    shutil.move(cmip_pdb_path, output_pdb_path)
                    break
            if Path(output_pdb_path).exists():
                pdb_text = Path(output_pdb_path).read_text()
                Path(output_pdb_path).write_text(pdb_text.replace('ATOMTM', 'ATOM  '))
            else:
                fu.log(f"WARNING: File not found output_pdb_path: {output_pdb_path}", self.out_log, self.global_log)

        # JSON boxes from the CMIP log
        for box_key, external in (('output_json_box_path', False), ('output_json_external_box_path', True)):
            if self.io_dict['out'][box_key]:
                write_json_box(self.sandbox_file('output_log_path'), self.sandbox_file(box_key), external)


cmip_run = launcher(CmipRun)

if __name__ == '__main__':
    CmipRun.main()
