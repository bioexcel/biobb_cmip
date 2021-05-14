""" Common functions for package biobb_cmip.cmip """
import re
import os
from typing import List, Dict, Tuple, Mapping, Union, Set, Sequence


def params_grid(grid_type: str = 'cmip', pbfocus: bool = False, perfill: float = 0.8,
                grid_int: Sequence[float] = (0.5, 0.5, 0.5), grid_dim: Sequence[float] = (64, 64, 64),
                grid_cen: Sequence[float] = (0.0, 0.0, 0.0)) -> Dict[str, str]:
    # grid_type older readgrid equivalences:
    #     interaction = 0 , 3
    #     cmip, titration, pbsolvation = 2, >3

    grid_dict = {}

    pbfocus = '0' if pbfocus else ''
    readgrid = '0' if grid_type == 'interaction' else '2'

    grid_dict[f"READGRID{pbfocus}"] = f"{readgrid}"

    if grid_type == 'interaction':
        grid_dict['grid_cen'] = f"CENX{pbfocus}={grid_cen[0]},CENY{pbfocus}={grid_cen[1]},CENZ{pbfocus}={grid_cen[2]}"
        grid_dict['grid_dim'] = f"DIMX{pbfocus}={grid_dim[0]},DIMY{pbfocus}={grid_dim[1]},DIMZ{pbfocus}={grid_dim[2]}"
        grid_dict['grid_int'] = f"INTX{pbfocus}={grid_int[0]},INTY{pbfocus}={grid_int[1]},INTZ{pbfocus}={grid_int[2]}"
    else:
        grid_dict[f"PERFILL{pbfocus}"] = f"{perfill}"
        grid_dict[
            'grid_int'] = f"INTX{pbfocus}={grid_int[0]},INTY{pbfocus}={grid_int[1]},INTZ{pbfocus}={grid_int[2]}"

    return grid_dict


def params_preset(execution_type: str) -> Dict[str, str]:
    params_dict = {}
    grid_dict = {}
    if execution_type == 'titration':
        grid_dict = params_grid(grid_type='titration')
        params_dict = {
            'title': 'Titration',
            'tipcalc': 1,
            'titration': 1,
            'inifoc': 2,
            'cutfoc': -0.5,
            'focus': 1,
            'ninter': 10,
            'dields': 2,
            'clhost': 1,
            'calcgrid': 1,
            'irest': 0,
            'orest': 0,
            'coorfmt': 2,
            'titwat': 10,
            'titip': 10,
            'titim': 10,
            'titcut': 20.
        }

    return {**params_dict, **grid_dict}


def read_params_file(input_params_path: str) -> Dict[str, str]:
    params_dict = {}
    with open(input_params_path) as input_params_file:
        params_dict['title']: input_params_file.readline()
        for line in input_params_file:
            line = line.replace(' ', '')
            if line.startswith('&'): continue
            param_list = line.split(',')
            for param in param_list:
                param_key, param_value = param.split("=")

                # Grid Values
                if len(param_key) > 3 and param_key[:3].startswith('INT'):
                    if params_dict.get('grid_int'):
                        params_dict['grid_int'] += f",{param_key}={param_value}"
                    else:
                        params_dict['grid_int'] = f"{param_key}={param_value}"
                elif len(param_key) > 3 and param_key[:3].startswith('CEN'):
                    if params_dict.get('grid_cen'):
                        params_dict['grid_cen'] += f",{param_key}={param_value}"
                    else:
                        params_dict['grid_cen'] = f"{param_key}={param_value}"
                elif len(param_key) > 3 and param_key[:3].startswith('DIM'):
                    if params_dict.get('grid_dim'):
                        params_dict['grid_dim'] += f",{param_key}={param_value}"
                    else:
                        params_dict['grid_dim'] = f"{param_key}={param_value}"
                # Rest of parameters
                else:
                    params_dict[param_key] = param_value
    return params_dict


def write_params_file(output_params_path: str, params_dict: Mapping[str, str]) -> str:
    with open(output_params_path, 'w') as output_params_file:
        output_params_file.write(f"{params_dict.pop('title', 'Untitled')}\n")
        output_params_file.write(f"&cntrl\n")
        for params_key, params_value in params_dict.items():
            if params_key in ['grid_int', 'grid_cen', 'grid_dim']:
                output_params_file.write(f" {params_value}\n")
            else:
                output_params_file.write(f" {params_key}{params_value}\n")
        output_params_file.write(f"&end\n")
    return output_params_path


def create_params_file(output_params_path: str, input_params_path: str = None,
                       params_preset_dict: Mapping = None, params_properties_dict: Mapping = None) -> str:
    """ Gets a params dictionary and a presset and returns the path of the created params file for cmip.

    Args:


    Returns:
        str: params file path.
    """
    params_dict = {}

    if params_preset_dict:
        for k, v in params_preset_dict.items():
            params_dict[k] = v
    if input_params_path:
        input_params_dict = read_params_file(input_params_path)
        for k, v in input_params_dict.items():
            params_dict[k] = v
    if params_properties_dict:
        for k, v in params_properties_dict.items():
            params_dict[k] = v

    return write_params_file(output_params_path, params_dict)