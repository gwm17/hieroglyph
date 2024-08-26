import vector
import numpy as np
from spyral_utils.nuclear import NucleusData


def convert_to_target_ke(
    KE_proj: float, projectile: NucleusData, target: NucleusData
) -> float:
    p_proj = np.sqrt(KE_proj * (KE_proj + 2.0 * projectile.mass))
    proj_vec = vector.MomentumObject4D(
        px=0.0, py=0.0, pz=p_proj, E=KE_proj + projectile.mass
    )
    target_vec = vector.MomentumObject4D(px=0.0, py=0.0, pz=0.0, E=target.mass)

    target_as_proj = target_vec.boostCM_of(proj_vec)
    return target_as_proj.E - target_as_proj.M
