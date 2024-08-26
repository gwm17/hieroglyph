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
        """Convert inverse kinematics to normal kinematics"""
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
    config = Config()
    with open(path, "r") as input_path:
        json_data = load(input_path)
        for key in config.__dict__.keys():
            if isinstance(config.__dict__[key], NucleusParameters):
                config.__dict__[key] = NucleusParameters(**json_data[key])
            else:
                config.__dict__[key] = json_data[key]
    return config
