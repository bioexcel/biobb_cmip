""" Representation functions for package biobb_cmip.cmip """
import re
from pathlib import Path
from typing import List, Dict, Mapping, Union, Set, Sequence, Tuple, List
import logging
import biobb_common.tools.file_utils as fu

def get_energies_byat(cmip_energies_byat_out: Union[str, Path],  cutoff: float) -> Tuple[List[str], Dict[str, List[float]]]:

    with open(cmip_energies_byat_out, 'r') as energies_file:
        atom_list = []
        energy_dict = {"ES": [], "VDW": [], "ES&VDW": []}
        for line in energies_file:
            atom_list.append(line[6:12].strip())
            vdw = float(line[42:53])
            es = float(line[57:68])
            both = float(line[72:83])
            if both > 100:
                vdw = 0.0
                es = 0.0
                both = 0.0

            energy_dict["ES"].append(es)
            energy_dict["VDW"].append(vdw)
            energy_dict["ES&VDW"].append(both)

    return atom_list, energy_dict

def get_energies_byres(cmip_energies_byat_out: Union[str, Path]) -> Tuple[List[str], Dict[str, List[float]]]:
    residues = []
    energy_dict = {"ES": [], "VDW": [], "ES&VDW": []}
    with open(cmip_energies_byat_out, 'r') as energies_file:
        for line in energies_file:
            chain = line[21:22].strip()
            residue_id = line[22:28].strip()
            residue = chain+':'+residue_id
            vdw = float(line[42:53])
            es = float(line[57:68])
            both = float(line[72:83])
            if both > 100:
                vdw = 0.0
                es = 0.0
                both = 0.0
            # Values greater than 100 are represented as 0
            # This step is performed to filter 'infinity' values
            energies = (vdw, es, both) if both < 100 else (0, 0, 0)
            if residue in residues:
                index =  residues.index(residue)
                energy_dict["ES"][index] += es
                energy_dict["VDW"][index] += vdw
                energy_dict["ES&VDW"][index] += both
            else:
                residues.append(residue)
                energy_dict["ES"].append(es)
                energy_dict["VDW"].append(vdw)
                energy_dict["ES&VDW"].append(both)

        return residues, energy_dict


def create_box_representation(cmip_log_path: Union[str, Path], cmip_pdb_path: Union[str, Path]) -> Tuple[str, List[List[str]]]:
    return _create_box_representation_file(cmip_log_path, cmip_pdb_path), _get_atom_pair()

def _create_box_representation_file(cmip_log_path: Union[str, Path], cmip_pdb_path: Union[str, Path]) -> str:
    vertex_list = _get_vertex_list(cmip_log_path)

    cmip_pdb_path = Path(cmip_pdb_path).resolve()
    boxed_pdb_path = cmip_pdb_path.parent.joinpath("boxed_"+str(cmip_pdb_path.name))
    with open(cmip_pdb_path) as cmip_pdb_file:
        pdb_lines = cmip_pdb_file.readlines()
        if pdb_lines[-1].strip().upper() == "END":
            pdb_lines = pdb_lines[:-1]
    with open(boxed_pdb_path, 'w') as boxed_pdb_file:
        for pdb_line in pdb_lines:
            boxed_pdb_file.write(pdb_line)
        for i, v in enumerate(vertex_list):
            boxed_pdb_file.write('HETATM10000 ZN' + str(i) + '   ZN Z9999    ' + v + '  1.00 50.00          ZN\n')
        boxed_pdb_file.write("END")
    return str(boxed_pdb_path)


def _get_vertex_list(cmip_log_path: Union[str, Path]) -> List[str]:
    origin, size = get_grid(cmip_log_path)
    vertex = []
    vertex.append(_pdb_coord_formatter(origin[0]) + _pdb_coord_formatter(origin[1]) + _pdb_coord_formatter(origin[2]))
    vertex.append(_pdb_coord_formatter(origin[0] + size[0]) + _pdb_coord_formatter(origin[1]) + _pdb_coord_formatter(origin[2]))
    vertex.append(_pdb_coord_formatter(origin[0]) + _pdb_coord_formatter(origin[1] + size[1]) + _pdb_coord_formatter(origin[2]))
    vertex.append(_pdb_coord_formatter(origin[0]) + _pdb_coord_formatter(origin[1]) + _pdb_coord_formatter(origin[2] + size[2]))
    vertex.append(_pdb_coord_formatter(origin[0] + size[0]) + _pdb_coord_formatter(origin[1] + size[1]) + _pdb_coord_formatter(origin[2]))
    vertex.append(_pdb_coord_formatter(origin[0] + size[0]) + _pdb_coord_formatter(origin[1]) + _pdb_coord_formatter(origin[2] + size[2]))
    vertex.append(_pdb_coord_formatter(origin[0]) + _pdb_coord_formatter(origin[1] + size[1]) + _pdb_coord_formatter(origin[2] + size[2]))
    vertex.append(_pdb_coord_formatter(origin[0] + size[0]) + _pdb_coord_formatter(origin[1] + size[1]) + _pdb_coord_formatter(origin[2] + size[2]))
    return vertex


def get_grid(cmip_log_path: Union[str, Path]) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    origin = None
    size = None
    with open(cmip_log_path) as log_file:
        for line in log_file:
            origin_match = re.match(r"Grid origin:\s+([-+]?(?:\d*\.\d+|\d+))\s+([-+]?(?:\d*\.\d+|\d+))\s+([-+]?(?:\d*\.\d+|\d+))", line.strip())
            if origin_match and not origin:
                origin = float(origin_match.group(1)), float(origin_match.group(2)), float(origin_match.group(3))
            size_match = re.match(r"Grid Size:\s+([-+]?(?:\d*\.\d+|\d+))\s+([-+]?(?:\d*\.\d+|\d+))\s+([-+]?(?:\d*\.\d+|\d+))", line.strip())
            if size_match and not size:
                size = float(size_match.group(1)), float(size_match.group(2)), float(size_match.group(3))
    return origin, size

def _pdb_coord_formatter(coordinate: float) -> str:
    return str(round(coordinate, 3)).rjust(8)

def _get_atom_pair() -> List[List[str]]:
    return [[ "9999:Z.ZN0", "9999:Z.ZN1" ],
            [ "9999:Z.ZN0", "9999:Z.ZN2" ],
            [ "9999:Z.ZN0", "9999:Z.ZN3" ],
            [ "9999:Z.ZN1", "9999:Z.ZN4" ],
            [ "9999:Z.ZN1", "9999:Z.ZN5" ],

            [ "9999:Z.ZN2", "9999:Z.ZN4" ],
            [ "9999:Z.ZN2", "9999:Z.ZN6" ],

            [ "9999:Z.ZN3", "9999:Z.ZN5" ],
            [ "9999:Z.ZN3", "9999:Z.ZN6" ],

            [ "9999:Z.ZN4", "9999:Z.ZN7" ],
            [ "9999:Z.ZN5", "9999:Z.ZN7" ],
            [ "9999:Z.ZN6", "9999:Z.ZN7" ]]
