from pathlib import Path
from spyral_utils.nuclear import NuclearDataMap, NucleusData
from fractions import Fraction
from io import TextIOWrapper

from .potentials import create_parameters
from .config import Config, deserialize_config


def create_elastic_scattering_input(
    config: Config,
    target: NucleusData,
    projectile: NucleusData,
    output: TextIOWrapper,
):
    """Generate a PTOLEMY input for elastic scattering reactions

    Parameters
    ----------
    config: Config
        The hieroglyph configuration
    target: spyral_utils.nuclear.NucleusData
        The target nucleus
    projectile: spyral_utils.nuclear.NucleusData
        The projectile nucleus
    output: TextIOWrapper
        The handle to the file to be written to
    """
    potential = create_parameters(
        config.projectile_energy,
        config.target.z,
        config.target.a,
        potential=config.incoming_potential,
    )

    # Write the Ptolemy Config
    output.write(f"CHANNEL {projectile} + {target}\n")
    output.write(f"ELAB {config.projectile_energy}\n")
    output.write("r0target\n")
    output.write(f"JBIGA={Fraction(config.target.j)}\n")
    output.write(
        f"ANGLEMIN {config.angle_min} ANGLEMAX {config.angle_max} ANGLESTEP {config.angle_step}\n"
    )
    output.write("ELASTIC\n")
    for key in potential.keys():
        output.write(f"{key} {potential[key]}\n")
    output.write(";\n")
    output.write("RETURN\n")


def create_inelastic_scattering_input(
    config: Config,
    target: NucleusData,
    projectile: NucleusData,
    output: TextIOWrapper,
):
    """Generate a PTOLEMY input for inelastic scattering reactions

    Parameters
    ----------
    config: Config
        The hieroglyph configuration
    target: spyral_utils.nuclear.NucleusData
        The target nucleus
    projectile: spyral_utils.nuclear.NucleusData
        The projectile nucleus
    output: TextIOWrapper
        The handle to the file to be written to
    """
    potential_in = create_parameters(
        config.projectile_energy,
        config.target.z,
        config.target.a,
        potential=config.incoming_potential,
    )
    potential_out = create_parameters(
        config.projectile_energy - config.residual.excitation,
        config.target.z,
        config.target.a,
        potential=config.incoming_potential,
    )

    # Write the Ptolemy config
    output.write(
        f"REACTION {target}({projectile}, {projectile}){target}({Fraction(config.residual.j)}{config.residual.parity} {config.residual.excitation})\n"
    )
    output.write(f"ELAB {config.projectile_energy}\n")
    output.write("PARAMETERSET ineloca2 r0target\n")
    output.write(f"JBIGA={Fraction(config.target.j)}\n")
    output.write("INCOMING\n")
    for key, value in potential_in.items():
        output.write(f"{key} {value}\n")
    output.write(";\n")
    output.write("OUTGOING\n")
    for key, value in potential_out.items():
        output.write(f"{key} {value}\n")
    output.write(";\n")
    output.write(
        f"ANGLEMIN {config.angle_min} ANGLEMAX {config.angle_max} ANGLESTEP {config.angle_step}\n"
    )
    output.write(";\n")
    output.write("RETURN\n")


def create_transfer_input(
    config: Config,
    target: NucleusData,
    projectile: NucleusData,
    ejectile: NucleusData,
    residual: NucleusData,
    output: TextIOWrapper,
):
    """Generate a PTOLEMY input for transfer reactions

    Parameters
    ----------
    config: Config
        The hieroglyph configuration
    target: spyral_utils.nuclear.NucleusData
        The target nucleus
    projectile: spyral_utils.nuclear.NucleusData
        The projectile nucleus
    ejectile: spyral_utils.nuclear.NucleusData
        The ejectile nucleus
    residual: spyral_utils.nuclear.NucleusData
        The residual nucleus
    output: TextIOWrapper
        The handle to the file to be written to
    """
    Q = (
        target.mass
        + projectile.mass
        - (ejectile.mass + residual.mass + config.residual.excitation)
    )
    potential_in = create_parameters(
        config.projectile_energy,
        config.target.z,
        config.target.a,
        potential=config.incoming_potential,
    )
    potential_out = create_parameters(
        config.projectile_energy + Q,
        config.residual.z,
        config.residual.a,
        potential=config.outgoing_potential,
    )

    # Write the Ptolemy config
    output.write(
        f"REACTION {target}({projectile}, {ejectile}){residual}({Fraction(config.residual.j)}{config.residual.parity} {config.residual.excitation})\n"
    )
    output.write(f"ELAB {config.projectile_energy}\n")
    # dp, pd
    if projectile.A < 3 and projectile.Z == 1 and ejectile.A < 3 and ejectile.Z == 1:
        output.write("PARAMETERSET dpsb r0target\n")
        output.write("lstep=1 lmin=0 lmax=30 maxlextrap=0 asymptopia=50 \n")
        output.write("PROJECTILE\n")
        output.write("wavefunction av18 \n")
        output.write("r0=1 a=0.5 l=0 rc0=1.2\n")
    # others
    else:
        # Idk if this is right, but this matches cleopatra
        output.write("PARAMETERSET alpha3 r0target\n")
        output.write("lstep=1 lmin=0 lmax=30 maxlextrap=0 asymptopia=50 \n")
        output.write("PROJECTILE\n")
        output.write("wavefunction phiffer\n")
        # dt,td
        if projectile.Z == 1 and ejectile.Z == 1:
            output.write(
                "nodes=0 l=0 jp=1/2 spfacp=1.30 v=172.88 r=0.56 a=0.69 param1=0.64 param2=1.15 rc=2.0\n"
            )
        # 3hea
        elif projectile.Z == 2 and ejectile.Z == 2:
            output.write(
                "nodes=0 l=0 jp=1/2 spfacp=1.61 v=202.21 r=.93 a=.66 param1=.81 param2=.87 rc=2.0 $ rc=2 is a quirk\n"
            )
        # 3hed, d3he
        else:
            output.write(
                "nodes=0 l=0 jp=1/2 spfacp=1.31 v=179.94 r=0.54 a=0.68 param1=0.64 param2=1.13 rc=2.0\n"
            )
    output.write(";\n")
    output.write("TARGET\n")
    output.write(f"JBIGA={Fraction(config.target.j)}\n")
    output.write(
        f"nodes={config.orbital_n} L={config.orbital_l} jp={Fraction(config.orbital_j)}\n"
    )
    output.write("r0=1.25 a=.65\n")
    output.write("vso=6 rso0=1.10 aso=.65\n")
    output.write("rc0=1.3\n")
    output.write(";\n")
    output.write("INCOMING\n")
    for key, value in potential_in.items():
        output.write(f"{key} {value}\n")
    output.write(";\n")
    output.write("OUTGOING\n")
    for key, value in potential_out.items():
        output.write(f"{key} {value}\n")
    output.write(";\n")
    output.write(
        f"ANGLEMIN {config.angle_min} ANGLEMAX {config.angle_max} ANGLESTEP {config.angle_step}\n"
    )
    output.write(";\n")
    output.write("RETURN\n")


def create_input(path: Path):
    """From a hieroglyph JSON file, create a PTOLEMY input file

    Auto-detects whether the configuration is for elastic,
    inelastic, or transfer and calls the appropriate
    function.

    Parameters
    ----------
    path: Path
        The path to the JSON configuration file
    """
    if not path.exists():
        raise Exception(f"Configuration path {path} does not exist!")

    nuc_map = NuclearDataMap()
    config = deserialize_config(path)
    config.sanitize(nuc_map)

    target = nuc_map.get_data(config.target.z, config.target.a)
    projectile = nuc_map.get_data(config.projectile.z, config.projectile.a)
    ejectile = nuc_map.get_data(config.ejectile.z, config.ejectile.a)
    residual = nuc_map.get_data(config.residual.z, config.residual.a)
    ptolemy_path = Path(config.ptolemy_config_path)

    with open(ptolemy_path, "w") as ptolemy_config:
        if projectile.Z == ejectile.Z and projectile.A == ejectile.A:
            # Check both case of normal and inverse kinematic inelastic
            if config.residual.excitation == 0.0:
                create_elastic_scattering_input(
                    config, target, projectile, ptolemy_config
                )
            else:
                create_inelastic_scattering_input(
                    config, target, projectile, ptolemy_config
                )
        else:
            if projectile.A - ejectile.A > 1:
                raise Exception("Currently only support single-nucleon transfer!")
            elif projectile.A == ejectile.A:
                raise Exception("Currently do not support p/n exchange!")

            create_transfer_input(
                config, target, projectile, ejectile, residual, ptolemy_config
            )
