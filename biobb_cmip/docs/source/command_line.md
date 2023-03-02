# BioBB CMIP Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Prepare_structure
Generate a CMIP suitable PDB input.
### Get help
Command:
```python
prepare_structure -h
```
    /bin/sh: /Users/pau/anaconda3/envs/dev/bin/prepare_structure: Permission denied
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Path to the input PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/data/cmip/egfr.pdb). Accepted formats: PDB
* **input_topology_path** (*string*): Path to the input topology path. File type: input. [Sample file](https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/data/cmip/egfr_topology.zip). Accepted formats: ZIP, TOP, PSF, PRMTOP
* **output_cmip_pdb_path** (*string*): Path to the output PDB file. File type: output. [Sample file](https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/reference/cmip/egfr_cmip.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (cmip/cmip:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_prepare_structure.yml)
```python
properties:
  remove_tmp: true

```
#### Command line
```python
prepare_structure --config config_prepare_structure.yml --input_pdb_path egfr.pdb --input_topology_path egfr_topology.zip --output_cmip_pdb_path egfr_cmip.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_prepare_structure.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### Command line
```python
prepare_structure --config config_prepare_structure.json --input_pdb_path egfr.pdb --input_topology_path egfr_topology.zip --output_cmip_pdb_path egfr_cmip.pdb
```

## Prepare_pdb
Class to add CMIP charges and atom types.
### Get help
Command:
```python
prepare_pdb -h
```
    usage: prepare_pdb [-h] [-c CONFIG] -i INPUT_PDB_PATH -o OUTPUT_CMIP_PDB_PATH
    
    Model the missing atoms in the backbone of a PDB structure.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_PDB_PATH, --input_pdb_path INPUT_PDB_PATH
                            Input PDB file name
      -o OUTPUT_CMIP_PDB_PATH, --output_cmip_pdb_path OUTPUT_CMIP_PDB_PATH
                            Output PDB file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/data/cmip/1aki.pdb). Accepted formats: PDB
* **output_cmip_pdb_path** (*string*): Output PDB file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/reference/cmip/egfr_cmip.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **remove_water** (*boolean*): (True) Remove Water molecules..
* **add_hydrogen** (*boolean*): (True) Add Hydrogen atoms to the structure..
* **keep_hydrogen** (*boolean*): (False) If **add_hydrogen** is True. All hydrogen atoms will be removed before adding the new ones unless this option is set True..
* **fix_sidechains** (*boolean*): (True) Complete side chains (heavy atoms, protein only)..
* **fix_backbone_atoms** (*boolean*): (True) Add missing O, OXT backbone atoms..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_prepare_pdb.yml)
```python
properties:
  remove_tmp: true

```
#### Command line
```python
prepare_pdb --config config_prepare_pdb.yml --input_pdb_path 1aki.pdb --output_cmip_pdb_path egfr_cmip.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_prepare_pdb.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### Command line
```python
prepare_pdb --config config_prepare_pdb.json --input_pdb_path 1aki.pdb --output_cmip_pdb_path egfr_cmip.pdb
```

## Titration
Wrapper class for the CMIP titration module.
### Get help
Command:
```python
titration -h
```
    usage: titration [-h] [-c CONFIG] --input_pdb_path INPUT_PDB_PATH --output_pdb_path OUTPUT_PDB_PATH [--input_vdw_params_path INPUT_VDW_PARAMS_PATH] [--input_params_path INPUT_PARAMS_PATH]
    
    Wrapper of the CMIP Titration module.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
      --input_vdw_params_path INPUT_VDW_PARAMS_PATH
      --input_params_path INPUT_PARAMS_PATH
    
    required arguments:
      --input_pdb_path INPUT_PDB_PATH
      --output_pdb_path OUTPUT_PDB_PATH
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Path to the input PDB file. File type: input. [Sample file](https://raw.githubusercontent.com/bioexcel/biobb_cmip/master/biobb_cmip/test/data/cmip/1kim_h.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Path to the output PDB file. File type: output. [Sample file](https://raw.githubusercontent.com/bioexcel/biobb_cmip/master/biobb_cmip/test/reference/cmip/1kim_neutral.pdb). Accepted formats: PDB
* **input_vdw_params_path** (*string*): Path to the CMIP input Van der Waals force parameters, if not provided the CMIP conda installation one is used ("$CONDA_PREFIX/share/cmip/dat/vdwprm"). File type: input. [Sample file](None). Accepted formats: TXT
* **input_params_path** (*string*): Path to the CMIP input parameters file. File type: input. [Sample file](None). Accepted formats: TXT
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **params** (*object*): ({}) CMIP options specification..
* **energy_cutoff** (*number*): (9999.9) Energy cutoff, extremely hight value to enable the addition of all the ions and waters before reaching the cutoff..
* **num_wats** (*integer*): (10) Number of water molecules to be added..
* **neutral** (*boolean*): (False) Neutralize the charge of the system. If selected *num_positive_ions* and *num_negative_ions* values will not be taken into account..
* **num_positive_ions** (*integer*): (10) Number of positive ions to be added (Tipatom IP=Na+)..
* **num_negative_ions** (*integer*): (10) Number of negative ions to be added (Tipatom IM=Cl-)..
* **binary_path** (*string*): (titration) Path to the CMIP Titration executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (cmip/cmip:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_titration.yml)
```python
properties:
  neutral: true
  remove_tmp: false

```
#### [Docker config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_titration_docker.yml)
```python
properties:
  container_image: quay.io/biocontainers/cmip:2.7.0--h8c3ec31_0
  container_path: docker
  container_volume_path: /inout
  neutral: true

```
#### [Singularity config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_titration_singularity.yml)
```python
properties:
  container_image: cmip.simg
  container_path: singularity
  container_volume_path: /inout
  neutral: true

```
#### Command line
```python
titration --config config_titration.yml --input_pdb_path 1kim_h.pdb --output_pdb_path 1kim_neutral.pdb --input_vdw_params_path input.txt --input_params_path input.txt
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_titration.json)
```python
{
  "properties": {
    "remove_tmp": false,
    "neutral": true
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_titration_docker.json)
```python
{
  "properties": {
    "neutral": true,
    "container_path": "docker",
    "container_image": "quay.io/biocontainers/cmip:2.7.0--h8c3ec31_0",
    "container_volume_path": "/inout"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_titration_singularity.json)
```python
{
  "properties": {
    "neutral": true,
    "container_path": "singularity",
    "container_image": "cmip.simg",
    "container_volume_path": "/inout"
  }
}
```
#### Command line
```python
titration --config config_titration.json --input_pdb_path 1kim_h.pdb --output_pdb_path 1kim_neutral.pdb --input_vdw_params_path input.txt --input_params_path input.txt
```

## Cmip
Wrapper class for the CMIP cmip module.
### Get help
Command:
```python
cmip -h
```
    usage: cmip [-h] [-c CONFIG] --input_pdb_path INPUT_PDB_PATH [--input_probe_pdb_path INPUT_PROBE_PDB_PATH] [--output_pdb_path OUTPUT_PDB_PATH] [--output_grd_path OUTPUT_GRD_PATH] [--output_cube_path OUTPUT_CUBE_PATH] [--output_rst_path OUTPUT_RST_PATH] [--output_byat_path OUTPUT_BYAT_PATH] [--output_log_path OUTPUT_LOG_PATH] [--input_vdw_params_path INPUT_VDW_PARAMS_PATH] [--input_params_path INPUT_PARAMS_PATH] [--output_json_box_path OUTPUT_JSON_BOX_PATH] [--output_json_external_box_path OUTPUT_JSON_EXTERNAL_BOX_PATH] [--input_json_box_path INPUT_JSON_BOX_PATH] [--input_json_external_box_path INPUT_JSON_EXTERNAL_BOX_PATH]
    
    Wrapper of the CMIP cmip module.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
      --input_probe_pdb_path INPUT_PROBE_PDB_PATH
      --output_pdb_path OUTPUT_PDB_PATH
      --output_grd_path OUTPUT_GRD_PATH
      --output_cube_path OUTPUT_CUBE_PATH
      --output_rst_path OUTPUT_RST_PATH
      --output_byat_path OUTPUT_BYAT_PATH
      --output_log_path OUTPUT_LOG_PATH
      --input_vdw_params_path INPUT_VDW_PARAMS_PATH
      --input_params_path INPUT_PARAMS_PATH
      --output_json_box_path OUTPUT_JSON_BOX_PATH
      --output_json_external_box_path OUTPUT_JSON_EXTERNAL_BOX_PATH
      --input_json_box_path INPUT_JSON_BOX_PATH
      --input_json_external_box_path INPUT_JSON_EXTERNAL_BOX_PATH
    
    required arguments:
      --input_pdb_path INPUT_PDB_PATH
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Path to the input PDB file. File type: input. [Sample file](https://raw.githubusercontent.com/bioexcel/biobb_cmip/master/biobb_cmip/test/data/cmip/1kim_h.pdb). Accepted formats: PDB
* **input_probe_pdb_path** (*string*): Path to the input probe file in PDB format. File type: input. [Sample file](None). Accepted formats: PDB
* **output_pdb_path** (*string*): Path to the output PDB file. File type: output. [Sample file](https://raw.githubusercontent.com/bioexcel/biobb_cmip/master/biobb_cmip/test/reference/cmip/1kim_neutral.pdb). Accepted formats: PDB
* **output_grd_path** (*string*): Path to the output grid file in GRD format. File type: output. [Sample file](None). Accepted formats: GRD
* **output_cube_path** (*string*): Path to the output grid file in cube format. File type: output. [Sample file](None). Accepted formats: CUBE
* **output_rst_path** (*string*): Path to the output restart file. File type: output. [Sample file](None). Accepted formats: TXT
* **input_rst_path** (*string*): Path to the input restart file. File type: output. [Sample file](None). Accepted formats: TXT
* **output_byat_path** (*string*): Path to the output atom by atom energy file. File type: output. [Sample file](None). Accepted formats: TXT, OUT
* **output_log_path** (*string*): Path to the output CMIP log file LOG. File type: output. [Sample file](https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/reference/cmip/ref_cmip.log). Accepted formats: LOG
* **input_vdw_params_path** (*string*): Path to the CMIP input Van der Waals force parameters, if not provided the CMIP conda installation one is used ("$CONDA_PREFIX/share/cmip/dat/vdwprm"). File type: input. [Sample file](None). Accepted formats: TXT
* **input_params_path** (*string*): Path to the CMIP input parameters file. File type: input. [Sample file](None). Accepted formats: TXT
* **output_json_box_path** (*string*): Path to the output CMIP box in JSON format. File type: output. [Sample file](https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/reference/cmip/ref_box.json). Accepted formats: JSON
* **output_json_external_box_path** (*string*): Path to the output external CMIP box in JSON format. File type: output. [Sample file](https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/reference/cmip/ref_box.json). Accepted formats: JSON
* **input_json_box_path** (*string*): Path to the input CMIP box in JSON format. File type: input. [Sample file](https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/reference/cmip/ref_box.json). Accepted formats: JSON
* **input_json_external_box_path** (*string*): Path to the input CMIP box in JSON format. File type: input. [Sample file](https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/reference/cmip/ref_box.json). Accepted formats: JSON
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **execution_type** (*string*): (mip_pos) Default options for the params file, each one creates a different params file. .
* **params** (*object*): ({}) CMIP options specification..
* **binary_path** (*string*): (cmip) Path to the CMIP cmip executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (cmip/cmip:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_cmip.yml)
```python
properties:
  execution_type: pb_interaction_energy

```
#### [Docker config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_cmip_docker.yml)
```python
properties:
  container_image: quay.io/biocontainers/cmip:2.7.0--h8c3ec31_0
  container_path: docker
  container_volume_path: /inout
  execution_type: pb_interaction_energy
  remove_tmp: true

```
#### [Singularity config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_cmip_singularity.yml)
```python
properties:
  container_image: cmip.simg
  container_path: singularity
  container_volume_path: /inout
  execution_type: mip_pos
  remove_tmp: true

```
#### Command line
```python
cmip --config config_cmip.yml --input_pdb_path 1kim_h.pdb --input_probe_pdb_path input.pdb --output_pdb_path 1kim_neutral.pdb --output_grd_path output.grd --output_cube_path output.cube --output_rst_path output.txt --input_rst_path output.txt --output_byat_path output.txt --output_log_path ref_cmip.log --input_vdw_params_path input.txt --input_params_path input.txt --output_json_box_path ref_box.json --output_json_external_box_path ref_box.json --input_json_box_path ref_box.json --input_json_external_box_path ref_box.json
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_cmip.json)
```python
{
  "properties": {
    "execution_type": "pb_interaction_energy"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_cmip_docker.json)
```python
{
  "properties": {
    "remove_tmp": true,
    "execution_type": "pb_interaction_energy",
    "container_path": "docker",
    "container_image": "quay.io/biocontainers/cmip:2.7.0--h8c3ec31_0",
    "container_volume_path": "/inout"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_cmip_singularity.json)
```python
{
  "properties": {
    "remove_tmp": true,
    "execution_type": "mip_pos",
    "container_path": "singularity",
    "container_image": "cmip.simg",
    "container_volume_path": "/inout"
  }
}
```
#### Command line
```python
cmip --config config_cmip.json --input_pdb_path 1kim_h.pdb --input_probe_pdb_path input.pdb --output_pdb_path 1kim_neutral.pdb --output_grd_path output.grd --output_cube_path output.cube --output_rst_path output.txt --input_rst_path output.txt --output_byat_path output.txt --output_log_path ref_cmip.log --input_vdw_params_path input.txt --input_params_path input.txt --output_json_box_path ref_box.json --output_json_external_box_path ref_box.json --input_json_box_path ref_box.json --input_json_external_box_path ref_box.json
```

## Ignore_residues
Class to ignore residues in CMIP potential calculations.
### Get help
Command:
```python
ignore_residues -h
```
    /bin/sh: /Users/pau/anaconda3/envs/dev/bin/ignore_residues: Permission denied
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_cmip_pdb_path** (*string*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/data/cmip/input_ignore_res.pdb). Accepted formats: PDB
* **output_cmip_pdb_path** (*string*): Output PDB file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_cmip/raw/master/biobb_cmip/test/reference/cmip/ignore_res_gln3.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **residue_list** (*string*): (None) Residue list in the format "Chain:Resnum" (no spaces between the elements) separated by commas. If no chain is provided all the residues in the pdb file will be market. ie: "A:3"..
* **ignore_all** (*boolean*): (False) Mark all the residues in the PDB file..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_ignore_residues.yml)
```python
properties:
  remove_tmp: true
  residue_list: 3

```
#### Command line
```python
ignore_residues --config config_ignore_residues.yml --input_cmip_pdb_path input_ignore_res.pdb --output_cmip_pdb_path ignore_res_gln3.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_cmip/blob/master/biobb_cmip/test/data/config/config_ignore_residues.json)
```python
{
  "properties": {
    "residue_list": 3,
    "remove_tmp": true
  }
}
```
#### Command line
```python
ignore_residues --config config_ignore_residues.json --input_cmip_pdb_path input_ignore_res.pdb --output_cmip_pdb_path ignore_res_gln3.pdb
```
