from dataclasses import dataclass, field
from spyral_utils.nuclear import NuclearDataMap
from pathlib import Path
from json import load

from .convert import convert_to_target_ke


@dataclass
class NucleusParameters:
    z: int = 0
    a: int = 0
    j: float = 0.0
    parity: str = "+"
    excitation: float = 0.0


@dataclass
class Config:
    """Defines an input configuration to hieroglyph's create

    Attributes
    ----------
    ptolemy_config_path: str
        The path to the PTOLEMY input file that will be created
    target: NucleusParameters
        Parameters for the target nucleus
    projectile: NucleusParameters
        Parameters for the projectile nucleus
    ejectile: NucleusParameters
        Parameters for the ejectile nucleus
    residual: NucleusParameters
        Parameters for the residual nucleus
    projectile_energy: float
        The kinetic energy of the projectile (beam energy) in MeV
    incoming_potential: str
        The optical model potential for the incoming channel
    outgoing_potential: str
        The optical model potential for the outgoing channel
    orbital_n: int
        The n value of the populated oribital
    orbital_l: int
        The l value of the populated orbital
    orbital_j: int
        The j value of the populated orbital
    angle_min: float
        The minimum angle to calculate (degerees)
    angle_max: float
        The maximum angle to calculate (degrees)
    angle_step: float
        The angle step size (degrees)

    Methods
    -------
    sanitize(nuc_map)
        Convert the config from inverse kinematics to normal kinematics
    """

    ptolemy_config_path: str = "Invalid"
    target: NucleusParameters = field(default_factory=lambda: NucleusParameters())
    projectile: NucleusParameters = field(default_factory=lambda: NucleusParameters())
    ejectile: NucleusParameters = field(default_factory=lambda: NucleusParameters())
    residual: NucleusParameters = field(default_factory=lambda: NucleusParameters())
    projectile_energy: float = 0.0
    incoming_potential: str = "Invalid"
    outgoing_potential: str = "Invalid"
    orbital_n: int = 0
    orbital_l: int = 0
    orbital_j: float = 0.0
    angle_min: float = 0.0
    angle_max: float = 0.0
    angle_step: float = 0.0

    def sanitize(self, nuc_map: NuclearDataMap):
        """Convert inverse kinematics to normal kinematics

        If the configuration is already in normal kinematics,
        nothing happens.

        Parameters
        ----------
        nuc_map: spyral_utils.nuclear.NuclearDataMap
            The map of nucleus masses
        """
        if self.target.a < self.projectile.a:
            orig_target = self.target
            orig_proj = self.projectile
            orig_target_data = nuc_map.get_data(self.target.z, self.target.a)
            orig_proj_data = nuc_map.get_data(self.projectile.z, self.projectile.a)
            orig_proj_energy = self.projectile_energy
            self.projectile_energy = convert_to_target_ke(
                orig_proj_energy, orig_proj_data, orig_target_data
            )
            self.target = orig_proj
            self.projectile = orig_target
        if self.residual.a < self.ejectile.a:
            orig_eject = self.ejectile
            orig_resid = self.residual
            self.residual = orig_eject
            self.ejectile = orig_resid


def deserialize_config(path: Path) -> Config:
    """Deserialize a configuration from a JSON file

    Parameters
    ----------
    path: Path
        The path to the JSON file

    Returns
    -------
    Config
        The parsed configuration
    """
    config = Config()
    with open(path, "r") as input_path:
        json_data = load(input_path)
        for key in config.__dict__.keys():
            if isinstance(config.__dict__[key], NucleusParameters):
                config.__dict__[key] = NucleusParameters(**json_data[key])
            else:
                config.__dict__[key] = json_data[key]
    return config
