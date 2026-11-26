""" Representation functions for package biobb_cmip.cmip """
from biobb_cmip.cmip.common import get_grid
from pathlib import Path
from MDAnalysis.lib.util import inverse_aa_codes  # type: ignore
from typing import Union


def get_energies_byat(cmip_energies_byat_out: Union[str, Path], cutoff: float = 100.0) -> tuple[list[str], dict[str, list[float]]]:
    """Go from a CMIP atom by atom energy file to its atoms and their ES, VDW and ES&VDW energies
    (0.0 for the energies above **cutoff**)."""
    with open(cmip_energies_byat_out, 'r') as energies_file:
        atom_list = []
        energy_dict: dict[str, list] = {"ES": [], "VDW": [], "ES&VDW": []}
        for line in energies_file:
            atom_list.append(line[6:12].strip())
            vdw = float(line[42:53]) if float(line[42:53]) < cutoff else 0.0
            es = float(line[57:68]) if float(line[57:68]) < cutoff else 0.0
            both = float(line[72:83]) if float(line[72:83]) < cutoff else 0.0

            energy_dict["ES"].append(es)
            energy_dict["VDW"].append(vdw)
            energy_dict["ES&VDW"].append(both)

    return atom_list, energy_dict


def get_energies_byres(cmip_energies_byat_out: Union[str, Path], cutoff: float = 100.0) -> tuple[list[str], dict[str, list[float]]]:
    """Go from a CMIP atom by atom energy file to its residues and their ES, VDW and ES&VDW energies
    (the atoms with energies above **cutoff** count 0.0)."""
    residues: list = []
    energy_dict: dict[str, list] = {"ES": [], "VDW": [], "ES&VDW": []}
    with open(cmip_energies_byat_out, 'r') as energies_file:
        for line in energies_file:
            chain = line[21:22].strip()
            residue_id = line[22:28].strip()
            resname = inverse_aa_codes.get(line[17:21].strip().upper(), "X")
            residue = resname+' '+chain+residue_id
            vdw = float(line[42:53]) if float(line[42:53]) < cutoff else 0.0
            es = float(line[57:68]) if float(line[57:68]) < cutoff else 0.0
            both = float(line[72:83]) if float(line[72:83]) < cutoff else 0.0

            if residue in residues:
                index = residues.index(residue)
                energy_dict["ES"][index] += es
                energy_dict["VDW"][index] += vdw
                energy_dict["ES&VDW"][index] += both
            else:
                residues.append(residue)
                energy_dict["ES"].append(es)
                energy_dict["VDW"].append(vdw)
                energy_dict["ES&VDW"].append(both)

        return residues, energy_dict


def create_box_representation(cmip_log_path: Union[str, Path], cmip_pdb_path: Union[str, Path]) -> tuple[str, list[list[str]]]:
    """Go from a CMIP log or JSON box file and a PDB file to a copy of the PDB with the 8 vertices of the grid
    box as ZN atoms (boxed_<name>), and the pairs of vertices of its 12 edges."""
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


def _get_vertex_list(cmip_log_path: Union[str, Path]) -> list[str]:
    origin, size, _ = get_grid(cmip_log_path)
    return [
        _pdb_coord_formatter(origin[0]) + _pdb_coord_formatter(origin[1]) + _pdb_coord_formatter(origin[2]),
        _pdb_coord_formatter(origin[0] + size[0]) + _pdb_coord_formatter(origin[1]) + _pdb_coord_formatter(origin[2]),
        _pdb_coord_formatter(origin[0]) + _pdb_coord_formatter(origin[1] + size[1]) + _pdb_coord_formatter(origin[2]),
        _pdb_coord_formatter(origin[0]) + _pdb_coord_formatter(origin[1]) + _pdb_coord_formatter(origin[2] + size[2]),
        _pdb_coord_formatter(origin[0] + size[0]) + _pdb_coord_formatter(origin[1] + size[1]) + _pdb_coord_formatter(origin[2]),
        _pdb_coord_formatter(origin[0] + size[0]) + _pdb_coord_formatter(origin[1]) + _pdb_coord_formatter(origin[2] + size[2]),
        _pdb_coord_formatter(origin[0]) + _pdb_coord_formatter(origin[1] + size[1]) + _pdb_coord_formatter(origin[2] + size[2]),
        _pdb_coord_formatter(origin[0] + size[0]) + _pdb_coord_formatter(origin[1] + size[1]) + _pdb_coord_formatter(origin[2] + size[2]),
    ]


def _pdb_coord_formatter(coordinate: float) -> str:
    return str(round(coordinate, 3)).rjust(8)


def _get_atom_pair() -> list[list[str]]:
    return [["9999:Z.ZN0", "9999:Z.ZN1"],
            ["9999:Z.ZN0", "9999:Z.ZN2"],
            ["9999:Z.ZN0", "9999:Z.ZN3"],
            ["9999:Z.ZN1", "9999:Z.ZN4"],
            ["9999:Z.ZN1", "9999:Z.ZN5"],

            ["9999:Z.ZN2", "9999:Z.ZN4"],
            ["9999:Z.ZN2", "9999:Z.ZN6"],

            ["9999:Z.ZN3", "9999:Z.ZN5"],
            ["9999:Z.ZN3", "9999:Z.ZN6"],

            ["9999:Z.ZN4", "9999:Z.ZN7"],
            ["9999:Z.ZN5", "9999:Z.ZN7"],
            ["9999:Z.ZN6", "9999:Z.ZN7"]]
