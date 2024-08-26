# hieroglyph

hieroglyph is a Python application which provides a clean way to make PTOLEMY files readable and usable for modern applications. hieroglyph can generate a [PTOLEMY](https://www.phy.anl.gov/theory/research/ptolemy/) input based on a JSON configuration and can parse PTOLEMY output files and convert them into numpy (.npz) files. hieroglphy is based upon the digios and Cleopatra codes from ANL. 

## Installation

Download the repository from GitHub using `git clone https://github.com/gwm17/hieroglyph.git`.

From within the repository, create a virtual environment using 

```bash
python -m venv .venv
```

and then simply install the dependencies using

```bash
pip install -r requirements.txt
```

Then activate your venv using

```bash
source .venv/bin/activate
```

(Note these steps shown are for Linux/MacOS. Windows will be different, but is supported by hieroglyph)

## Use

hieroglyph has 3 main commands: `create`, `parse-elastic`, and `parse-dwba`.

### create

The create command will take in a JSON reaction configuration and create a PTOLEMY input file based on the JSON. The format is shown below

```json
{
    "ptolemy_config_path": "test.txt",
    "target": {
        "z": 1,
        "a": 2,
        "j": 1.0,
        "parity": "+",
        "excitation": 0.0
    },
    "projectile": {
        "z": 6,
        "a": 16,
        "j": 0.0,
        "parity": "+",
        "excitation": 0.0
    },
    "ejectile": {
        "z": 6,
        "a": 16,
        "j": 0.0,
        "parity": "+",
        "excitation": 0.0
    },
    "residual": {
        "z": 1,
        "a": 2,
        "j": 1.0,
        "parity": "+",
        "excitation": 0.0
    },
    "projectile_energy": 184.131,
    "incoming_potential": "an-cai",
    "outgoing_potential": "an-cai",
    "orbital_n": 0,
    "orbital_l": 0,
    "orbital_j": 0.0,
    "angle_min": 0.0,
    "angle_max": 90.0,
    "angle_step": 1.0
}
```

This description is for elastic scattering of 16C on deuterium. hieroglyph accepts both inverse and normal kinematics (it will handle the transformation for you). The list of available optical models is given below

- `an-cai`
- `daehnick`
- `bojowald`
- `koning-delaroche-proton`

More will be added (and more information can be found in `hieroglyph/potentials.py`).

### parse-elastic

Takes in a PTOLEMY elastic scattering calculation output and converts it into a numpy (.npz) file containing the following arrays:

- `angle`: The list of center-of-mass angles
- `cross`: The center-of-mass differential cross section

Note that the indicies correlate between the two arrays (i.e. `angle[0]` is the angle of `cross[0]`).

### parse-dwba

Takes in a PTOLEMY DWBA scattering calculation output and converts it into a numpy (.npz) file containing the following arrays:

- `angle`: The list of center-of-mass angles
- `cross`: The center-of-mass differential cross section
- `l_values`: The set of orbital angular momenta from the calculation
- `cross_ls`: The center-of-mass differential cross section for each l

Note that the indicies correlate in the following way: 

- `angle[0]` is the angle of `cross[0]`
- `l_values[0]` is the l of `cross_ls[0, :]`
- `angle_[0]` is the angle of `cross_ls[*, 0]`

## Requirements

Requires Python > 3.10

Obviously, you need to have the PTOLEMY application installed somewhere to actually perform the PTOLEMY calculations.