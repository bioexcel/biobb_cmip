""" Common functions for package biobb_cmip.cmip """
import os
import re
import json
from pathlib import Path
from typing import Union, Any, Optional
import MDAnalysis as mda  # type: ignore
from MDAnalysis.topology.guessers import guess_atom_element  # type: ignore
import logging
import biobb_common.tools.file_utils as fu

Grid = tuple[tuple[float, float, float], tuple[float, float, float], dict[str, tuple[float, float, float]]]

_NUMBER = r"([-+]?(?:\d*\.\d+|\d+))"
# Grid lines of the CMIP log: label -> key of the values
_GRID_LOG_LINES = {"Grid origin": "origin", "Grid Size": "size", "Grid units": "INT", "Grid center": "CEN", "Grid density": "DIM"}


def get_grid(cmip_log_path: Union[str, Path], external: bool = False) -> Grid:
    """Go from a CMIP log or a JSON box file to the origin, size and params (CEN, DIM, INT) of its grid,
    or of its outer grid with **external** (CMIP log only)."""
    with open(cmip_log_path) as log_file:
        first_line = log_file.readline().strip()
    if first_line.startswith("{"):
        return _get_grid_from_box_file(cmip_log_path)
    return _get_grid_from_text(cmip_log_path, external)


def _get_grid_from_box_file(cmip_box_path: Union[str, Path]) -> Grid:
    with open(cmip_box_path) as json_file:
        grid_dict = json.load(json_file)
    origin = grid_dict['origin']['x'], grid_dict['origin']['y'], grid_dict['origin']['z']
    size = grid_dict['size']['x'], grid_dict['size']['y'], grid_dict['size']['z']
    return origin, size, grid_dict['params']


def _get_grid_from_text(cmip_log_path: Union[str, Path], external: bool = False) -> Grid:
    grid_titles = ["AUTOMATIC OUTER GRID", "MANUAL OUTER GRID"] if external else ["AUTOMATIC GRID", "MANUAL GRID"]
    values: dict[str, Any] = {}
    with open(cmip_log_path) as log_file:
        inside_grid = False
        for line in log_file:
            line = line.strip()
            inside_grid = inside_grid or line in grid_titles
            if not inside_grid:
                continue
            for label, key in _GRID_LOG_LINES.items():
                match = re.match(rf"{label}:\s+{_NUMBER}\s+{_NUMBER}\s+{_NUMBER}", line)
                if match:
                    number_type = int if key == "DIM" else float
                    values[key] = tuple(number_type(group) for group in match.groups())
            if len(values) == len(_GRID_LOG_LINES):
                break
    return values.get("origin"), values.get("size"), {key: values.get(key) for key in ("CEN", "DIM", "INT")}  # type: ignore


def write_json_box(cmip_log_path: Union[str, Path], json_box_path: Union[str, Path], external: bool = False) -> None:
    """Go from a CMIP log to a JSON box file with the origin, size and params of its grid,
    or of its outer grid with **external**."""
    origin, size, grid_params = get_grid(cmip_log_path, external)
    with open(json_box_path, 'w') as json_file:
        json.dump({'origin': dict(zip('xyz', origin)), 'size': dict(zip('xyz', size)), 'params': grid_params},
                  json_file, indent=4)


def params_from_box(json_box_path: Union[str, Path], grid_id: str = '') -> dict[str, Any]:
    """Go from a JSON box file to the CMIP params of a grid read from the params file (readgrid 0) with its
    spacing, center and dimensions; **grid_id** "0" for the outer grid."""
    _, _, grid_params = get_grid(json_box_path)
    return {f'readgrid{grid_id}': 0,
            **{f'grid_{param.lower()}{grid_id}': _grid_line(param, grid_params[param], grid_id) for param in ('INT', 'CEN', 'DIM')}}


def _grid_line(param: str, values, grid_id: Union[int, str] = '') -> str:
    """Go from a grid param (INT, CEN or DIM) and its x, y, z values to its line of the params file,
    ie: INTX0=1.5,INTY0=1.5,INTZ0=1.5."""
    return ','.join(f"{param}{axis}{grid_id}={value}" for axis, value in zip('XYZ', values))


def write_cmip_pdb(input_pdb_path, output_cmip_pdb_path, charges_list, elements_list) -> None:
    """Go from a PDB file and the charge and CMIP atom type of each atom to a CMIP PDB file."""
    with open(input_pdb_path) as inPDB, open(output_cmip_pdb_path, 'w') as outPDB:
        index = 0
        for line in inPDB:
            line = line.rstrip()
            if not re.match('^ATOM', line) and not re.match('^HETATM', line):
                continue
            outPDB.write("{}{:8.4f}  {}\n".format(line[:54], charges_list[index], elements_list[index]))
            index += 1


def get_topology_charges_and_elements(input_topology_path: str) -> tuple[list[float], list[str]]:
    """Go from a topology (top, psf, prmtop) to the charge and CMIP atom type of each atom."""
    universe = _load_topology(input_topology_path)
    two_letter_elements = {"CL": "Cl", "NA": "Na", "ZN": "Zn", "MG": "Mg"}
    elements = []
    for atom in universe.atoms:  # type: ignore
        element = guess_atom_element(atom.name)
        if element == 'H':
            bonded_element = guess_atom_element(atom.bonded_atoms[0].name)
            if bonded_element == 'O':
                element = 'HO'
            elif bonded_element in ['N', 'S']:
                element = 'HN'
        elements.append(two_letter_elements.get(element, element))
    return [round(charge, 4) for charge in universe.atoms.charges], elements  # type: ignore


def _load_topology(topology_path: str) -> mda.Universe:
    """Go from a topology file to an MDAnalysis Universe; a GROMACS top file is read without its force
    field includes, which MDAnalysis cannot read."""
    if not topology_path.lower().endswith('.top'):
        return mda.Universe(topology_path)
    # Next to the top file, where its other includes are
    top_without_ff = fu.create_unique_file_path(Path(topology_path).parent, '.top')
    with open(topology_path) as top_file, open(top_without_ff, 'w') as out_file:
        out_file.writelines(line for line in top_file if not re.search(r"\.ff.*\.itp", line))
    try:
        return mda.Universe(top_without_ff, topology_format="ITP")
    finally:
        os.unlink(top_without_ff)


def get_pdb_charges_and_elements(input_pdb_path: str, residue_library_path: Optional[str] = None,
                                 out_log: Optional[logging.Logger] = None,
                                 global_log: Optional[logging.Logger] = None) -> tuple[list[float], list[str]]:
    """Go from a PDB file to the charge and CMIP atom type of each atom, from a CMIP residue library
    (default: aa.lib of the package). ValueError if an atom is not in the library."""
    if not residue_library_path:
        residue_library_path = str(Path(__file__).parent.joinpath("dat", "aa.lib").resolve())
    library = _read_residue_library(residue_library_path)
    fu.log(f"{len(library)} residue/atom pairs loaded from {residue_library_path}", out_log, global_log)

    charges_list: list[float] = []
    elements_list: list[str] = []
    missing_atoms: list[str] = []
    residue_num = None
    with open(input_pdb_path) as inPDB:
        for line in inPDB:
            if not re.match('^ATOM', line) and not re.match('^HETATM', line):
                continue
            nomat = line[12:16]
            if re.match('^[1-9]', nomat):
                nomat = nomat[1:4] + nomat[:1]
            nomat = nomat.replace(' ', '')
            nomr = line[17:21].replace(' ', '')
            # Assumption: every HIS is protonated as HID
            if nomr == "HIS":
                nomr = "HID"
                if residue_num != line[23:27]:
                    fu.log(f"WARNING replacing HIS:{line[23:27]} by HID", out_log, global_log)
                    residue_num = line[23:27]
            # Only the OXT atom gets the parameters of the C-terminal residue, not the other atoms of the residue
            if nomat == "OXT":
                nomr = nomr + "C"
                fu.log(f"WARNING replacing {nomr[:-1]}:{line[23:27]} by {nomr}", out_log, global_log)
            atom_params = library.get(f"{nomr}:{nomat}")
            if atom_params is None:
                missing_atoms.append(f"{nomr}:{nomat}")
                continue
            elements_list.append(atom_params[0])
            charges_list.append(atom_params[1])
    if missing_atoms:
        message = f"Atoms not found in the CMIP residue library {residue_library_path}: {', '.join(dict.fromkeys(missing_atoms))}"
        fu.log(f"ERROR: {message}", out_log, global_log)
        raise ValueError(message)
    return charges_list, elements_list


def _read_residue_library(residue_library_path: str) -> dict[str, tuple[str, float]]:
    """Go from a CMIP residue library to a dictionary "RES:ATOM" -> (atom type, charge)."""
    library = {}
    with open(residue_library_path) as library_file:
        for line in library_file:
            data = line.split()
            if not data or data[0].startswith('#'):
                continue
            library[f"{data[0]}:{data[1]}"] = (data[2], float(data[3]))
    return library


def get_pdb_total_charge(pdb_file_path: str) -> float:
    """Go from a CMIP PDB file to its total charge (Biopython does not read the charges of the CMIP format)."""
    total_charge: float = 0.0
    with open(pdb_file_path) as pdb_file:
        for line in pdb_file:
            if line[0:6].strip().upper() in ["ATOM", "HETATM"] and len(line) > 63:
                total_charge += float(line[55:63].strip())
    return total_charge


def probe_params_grid(probe_id: int = 0, readgrid: int = 2, pbfocus: int = 1, perfill: float = 0.6,
                      grid_int: tuple[float, float, float] = (0.5, 0.5, 0.5)) -> dict[str, str]:
    """Go from the settings of a probe (outer) grid to its CMIP params."""
    grid_dict = {}
    grid_dict[f"readgrid{probe_id}"] = f"{readgrid}"
    grid_dict[f"perfill{probe_id}"] = f"{perfill}"
    grid_dict['pbfocus'] = f"{pbfocus}"
    grid_dict[f"grid_int{probe_id}"] = _grid_line('INT', grid_int, probe_id)

    return grid_dict


def params_grid(grid_type: str, readgrid: int = 0, perfill: float = 0.8,
                grid_int: tuple[float, float, float] = (0.5, 0.5, 0.5),
                grid_dim: tuple[float, float, float] = (64, 64, 64),
                grid_cen: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> dict[str, str]:
    """Go from an execution type and the settings of its grid to the CMIP params of the grid."""
    # Old readgrid values: 2 percentage of the protein minimum distance, 4 protein minimum distance,
    # 5 distance to the centre of mass, 0 (interaction) and 3 explicit input grid
    grid_dict = {}
    grid_dict["readgrid"] = f"{readgrid}"

    if grid_type in ['pb_interaction_energy', 'mip_pos', 'mip_neu', 'mip_neg', 'docking']:
        grid_dict['grid_cen'] = _grid_line('CEN', grid_cen)
        grid_dict['grid_dim'] = _grid_line('DIM', grid_dim)
        grid_dict['grid_int'] = _grid_line('INT', grid_int)
    elif grid_type in ['solvation', 'titration']:
        grid_dict['perfill'] = f"{perfill}"
        grid_dict['grid_int'] = _grid_line('INT', grid_int)

    return grid_dict


def params_preset(execution_type: str) -> dict[str, Any]:
    """Go from an execution type to its preset CMIP params."""
    params_dict: dict[str, Any] = {}
    grid_dict = {}
    probe_grid_dict = {}
    execution_type = execution_type.strip()
    if execution_type == 'titration':
        grid_dict = params_grid(grid_type=execution_type, readgrid=2, perfill=0.8, grid_int=(0.5, 0.5, 0.5))
        params_dict = {
            'title': 'Titration',
            'tipcalc': 1,
            'calcgrid': 1,
            'irest': 0,
            'orest': 0,
            'coorfmt': 2,
            'dields': 2,
            'titration': 1, 'inifoc': 2, 'cutfoc': -0.5, 'focus': 1, 'ninter': 10, 'clhost': 1, 'titcut': 20.,
            'titwat': 10, 'titip': 10, 'titim': 10
        }
    elif execution_type in ['mip_pos', 'mip_neu', 'mip_neg']:
        probe, carmip = {'mip_pos': ('positive', 1), 'mip_neu': ('neutral', 0), 'mip_neg': ('negative', -1)}[execution_type]
        grid_dict = params_grid(grid_type=execution_type, readgrid=2)
        params_dict = {
            'title': f'MIP {probe} probe',
            'tipcalc': 0,
            'calcgrid': 1,
            'irest': 0,
            'orest': 0,
            'coorfmt': 2,
            'dields': 2,
            'cubeoutput': 1,
            'fvdw': 0.8,
            'carmip': carmip,
            'tipatmip': "'OW'"
        }
    elif execution_type == 'solvation':
        grid_dict = params_grid(grid_type=execution_type, readgrid=2, perfill=0.2,
                                grid_int=(0.5, 0.5, 0.5))
        params_dict = {
            'title': 'Solvation & MEP',
            'tipcalc': 0,
            'calcgrid': 1,
            'irest': 0,
            'orest': 0,
            'coorfmt': 2,
            'cubeoutput': 1, 'vdw': 0, 'pbelec': 1,
            'novdwgrid': 1, 'solvenergy': 1, 'dielc': 1, 'dielsol': 80
        }

    elif execution_type == 'pb_interaction_energy':
        grid_dict = params_grid(grid_type=execution_type, readgrid=2)
        probe_grid_dict = probe_params_grid(probe_id=0, readgrid=2, pbfocus=1, perfill=0.6,
                                            grid_int=(1.5, 1.5, 1.5))
        params_dict = {
            'title': 'Docking Interaction energy calculation. PB electrostatics',
            'tipcalc': 3,
            'calcgrid': 1,
            'irest': 0,
            'orest': 0,
            'coorfmt': 2,
            'fvdw': 0.8, 'pbelec': 1, 'pbinic': 2, 'wgp': 0, 'ebyatom': 1
        }

    elif execution_type == 'docking':
        grid_dict = params_grid(grid_type=execution_type, readgrid=2)

        params_dict = {
            'title': 'Docking Mehler Solmajer dielectric',
            'tipcalc': 2,
            'calcgrid': 1,
            'irest': 0,
            'orest': 1,
            'coorfmt': 2,
            'fvdw': 0.8, 'dields': 2, 'focus': 1, 'cutfoc': 100,
            'tiprot': 5, 'inifoc': 5, 'ninter': 20,
            'clhost': 1, 'minout': 50, 'splitpdb': 0
        }

    elif execution_type == 'docking_rst':
        params_dict = {
            'title': 'Docking from restart file',
            'readgrid': 0,
            'tipcalc': 2,
            'calcgrid': 1,
            'irest': 2,
            'orest': 1,
            'coorfmt': 2,
            'fvdw': 0.8, 'dields': 2, 'focus': 1, 'cutfoc': 100,
            'tiprot': 5, 'inifoc': 5, 'ninter': 20,
            'clhost': 1, 'minout': 50, 'splitpdb': 0, 'cutelec': 10.0
        }
    elif execution_type == 'check_only':
        params_dict = {
            'title': 'Check_only dry run of CMIP',
            'CHECKONLY': 1,
            'readgrid': 2,
            'calcgrid': 1,
            'tipcalc': 0,
            'irest': 0,
            'ebyatom': 1,
            'coorfmt': 2,
            'fvdw': 0.8
        }

    return {**params_dict, **grid_dict, **probe_grid_dict}


def read_params_file(input_params_path: str) -> dict[str, str]:
    """Go from a CMIP params file to its title and params, the INT, CEN and DIM params of the grids
    joined in grid_int, grid_cen and grid_dim."""
    params_dict = {}
    with open(input_params_path) as input_params_file:
        params_dict['title'] = input_params_file.readline().strip()
        for line in input_params_file:
            line = line.replace(' ', '').strip()
            if line.startswith('&'):
                continue
            # Skip the empty items of blank lines and trailing commas
            for param in filter(None, line.split(',')):
                param_key, param_value = param.split("=")
                if len(param_key) > 3 and param_key[:3] in ('INT', 'CEN', 'DIM'):
                    grid_key = f"grid_{param_key[:3].lower()}"
                    params_dict[grid_key] = f"{params_dict[grid_key]},{param}" if grid_key in params_dict else param
                else:
                    params_dict[param_key] = param_value
    return params_dict


def write_params_file(output_params_path: str, params_dict: dict[str, str]) -> str:
    """Go from a dictionary of a title and CMIP params to a params file; return its path."""
    with open(output_params_path, 'w') as output_params_file:
        output_params_file.write(f"{params_dict.pop('title', 'Untitled')}\n")
        output_params_file.write("&cntrl\n")
        for params_key, params_value in params_dict.items():
            if params_key.startswith('grid_'):
                output_params_file.write(f" {params_value}\n")
            else:
                output_params_file.write(f" {params_key} = {params_value}\n")
        output_params_file.write("&end\n")
    return output_params_path


def create_params_file(output_params_path: str, input_params_path: Optional[str] = None,
                       params_preset_dict: Optional[dict] = None, params_properties_dict: Optional[dict] = None) -> str:
    """Go from a preset, a CMIP params file and the params property, each one overriding the previous,
    to a CMIP params file; return its path."""
    params_dict = {**(params_preset_dict or {}),
                   **(read_params_file(input_params_path) if input_params_path else {}),
                   **(params_properties_dict or {})}
    return write_params_file(output_params_path, params_dict)


def mark_residues(residue_list: list[str], input_cmip_pdb_path: str, output_cmip_pdb_path: str, out_log: Optional[logging.Logger] = None, global_log: Optional[logging.Logger] = None) -> None:
    """Go from a CMIP PDB file to a copy with an "X" before the atom type of the residues in **residue_list**
    ("Chain:Resnum" codes), or of all the residues if it is empty."""
    if not residue_list:
        fu.log("Empty residue_list all residues will be marked", out_log, global_log)
    else:
        fu.log(f"Residue list: {residue_list}", out_log, global_log)

    with open(input_cmip_pdb_path) as pdb_file_in, open(output_cmip_pdb_path, 'w') as pdb_file_out:
        residue_set_used = set()

        res_counter = 0
        for line in pdb_file_in:
            if _is_atom(line):
                residue_code = _get_residue_code(line)
                used_residue = _get_residue_code_in_list(residue_code, residue_list)
                if not residue_list or used_residue:
                    res_counter += 1
                    residue_set_used.add(used_residue)
                    line = _mark_pdb_atom(line)
            pdb_file_out.write(line)
        fu.log(f"{res_counter} residues have been marked", out_log, global_log)

        if residue_list:
            unused_residues = set(residue_list) - residue_set_used
            if unused_residues:
                fu.log(f"The following residues where present in the residue_list and have not been marked: {unused_residues}", out_log, global_log)


def _mark_pdb_atom(line: str) -> str:
    newline = list(line)
    newline.insert(64, 'X')
    return ''.join(newline)


def _get_residue_code_in_list(input_residue, residue_list):
    if not residue_list:
        return None
    for res_code in residue_list:
        if input_residue == res_code:
            return res_code
        chain_rescode, resnum_rescode = res_code.split(":")
        chain_input, resnum_input = input_residue.split(":")
        if not chain_rescode:
            if resnum_rescode == resnum_input:
                return res_code
        if not resnum_rescode:
            if chain_rescode == chain_input:
                return res_code
    return None


def _get_residue_code(line: str) -> str:
    return _get_chain(line)+":"+_get_resnum(line)


def _get_chain(line: str) -> str:
    return line[21].upper()


def _get_resnum(line: str) -> str:
    return line[22:27].strip()


def _is_atom(line: str) -> bool:
    return line[0:6].strip().upper() in ["ATOM", "HETATM"]
