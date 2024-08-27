from pathlib import Path
import numpy as np

# The heinous mess of keylines I use to decide where to parse
ELASTIC_CS_HEADER = "0    ANGLE          SIGMA/             SIGMA              RUTHERFORD         % PER    % PER"
ELASTIC_CS_FOOTER = "1                                              P T O L E M Y"
ELASTIC_CS_FOOTER_ALT = "0TOTAL REACTION CROSS SECTION"

# Ugh
DWBA_CS_HEADER = "0  C.M.  REACTION     REACTION   LOW L  HIGH L   % FROM"
DWBA_CS_FOOTER = "1                                                      P T O L E M Y"
DWBA_CS_FOOTER_ALT = "0TOTAL:"

# Don't even @ me about the LX's
DWBA_LXS_PER_ROW = 3
DWBA_HEADER_WORDS_PER_LX = 3


def parse_elastic_differential_cross_section(
    ptolemy_path: Path, parsed_path: Path
) -> None:
    """Parse the PTOLEMY output of elastic scattering

    Writes the result to a Numpy (.npz) file
    This is the easy case

    Parameters
    ----------
    ptolemy_path: Path
        Path to the PTOLEMY output
    parsed_path: Path
        Path to which the parsed data will be written
    """
    # We have no idea how much data there is
    cm_angles = []
    cm_cross = []

    with open(ptolemy_path, "r") as pt_file:
        pt_lines = pt_file.readlines()
        idx = 0
        while idx < len(pt_lines):
            cur_line = pt_lines[idx]
            # The outputs contain a ton of extra crap
            # that is good to check, but not relevant for use in experiment
            # There's no way to know how far to jump to reach the actual
            # cross section
            # The cross section is also for some unknowable reason broken into
            # blocks each with a header and footer. These blocks are not
            # fixed in size soooooooo we just go until we don't
            if cur_line.startswith(ELASTIC_CS_HEADER):  # This is objectively bad
                idx += 2  # Skip current line, next line as headers
                while not (
                    pt_lines[idx].startswith(ELASTIC_CS_FOOTER)
                    or pt_lines[idx].startswith(ELASTIC_CS_FOOTER_ALT)
                ):
                    row = pt_lines[idx]
                    entries = row.split()
                    if len(entries) == 0:
                        idx += 1
                        continue
                    cm_angles.append(float(entries[0]))
                    cm_cross.append(float(entries[3]))
                    idx += 1
            else:
                idx += 1

    cm_angle_array = np.array(cm_angles)
    cm_cross_array = np.array(cm_cross)

    np.savez_compressed(parsed_path, angle=cm_angle_array, cross=cm_cross_array)


def parse_dwba_differential_cross_section(
    ptolemy_path: Path, parsed_path: Path
) -> None:
    """Parse the PTOLEMY output of DWBA scattering

    Writes the result to a Numpy (.npz) file
    This is the not easy case

    Parameters
    ----------
    ptolemy_path: Path
        Path to the PTOLEMY output
    parsed_path: Path
        Path to which the parsed data will be written
    """

    # We reeaally don't know how much data there is
    cm_angles = []
    cm_cross = []
    cm_cross_ls = None
    l_values = []
    lxs_per_row = []
    rows_per_line = 0  # Gross

    with open(ptolemy_path, "r") as pt_file:
        pt_lines = pt_file.readlines()
        idx = 0

        # The problem with the DWBA output is that in addition to all the madness of
        # the problems we had with elastic, we now also have the fun of each "output" line
        # no longer is equivalent to one row of the data table in the file. The lines get too
        # long and because Fortran sucks they handle this by making a new line underneath with partial
        # data. This happens for the L-values of the transfer. We need to pre parse these and determine how
        # many rows go to one line
        while idx < len(pt_lines):
            cur_line = pt_lines[idx]
            if cur_line.startswith(DWBA_CS_HEADER):
                idx += 4  # Skip current line, next line as headers
                # Figure out how many l-values encountered, number of extra line breaks
                while True:
                    lx_entries = pt_lines[idx].replace("+", "").split()
                    if len(lx_entries) == 0:
                        idx += 1
                        break
                    line_lxs = int(len(lx_entries) / DWBA_HEADER_WORDS_PER_LX)
                    lxs_per_row.append(line_lxs)
                    for lidx in range(line_lxs):
                        l_values.append(
                            int(lx_entries[2 + lidx * DWBA_HEADER_WORDS_PER_LX])
                        )
                    idx += 1

                cm_cross_ls = [[] for _ in range(sum(lxs_per_row))]
                rows_per_line = int(
                    np.ceil(float(sum(lxs_per_row)) / float(DWBA_LXS_PER_ROW))
                )
                break
            else:
                idx += 1

        if cm_cross_ls is None:
            raise Exception("Did not find any lxs while parsing DWBA!")

        print(f"Found {sum(lxs_per_row)} lxs: {l_values}")
        # Now that we know how many rows go to a line, parsing is mostly the same as before
        # except we also need to extract the different Lx's from the table
        idx = 0
        while idx < len(pt_lines):
            cur_line = pt_lines[idx]
            if cur_line.startswith(DWBA_CS_HEADER):
                idx += 4 + rows_per_line  # Skip current line, next line as headers
                # Parse the cross-section
                while not (
                    pt_lines[idx].startswith(DWBA_CS_FOOTER)
                    or pt_lines[idx].startswith(DWBA_CS_FOOTER_ALT)
                ):
                    row = pt_lines[idx]
                    entries = row.split()
                    if len(entries) == 0:
                        idx += 1
                        continue
                    cm_angles.append(float(entries[0]))
                    cm_cross.append(float(entries[1]))
                    for ridx in range(rows_per_line):
                        lx_row = pt_lines[idx + ridx]
                        lx_entries = lx_row.split()
                        for i in range(lxs_per_row[ridx]):
                            start_idx = 0
                            array_idx = ridx * DWBA_LXS_PER_ROW + i
                            if ridx == 0:
                                start_idx = 9
                            cm_cross_ls[array_idx].append(
                                float(lx_entries[start_idx + i])
                            )
                    idx += rows_per_line
            else:
                idx += 1

    cm_angle_array = np.array(cm_angles)
    cm_cross_array = np.array(cm_cross)
    cm_cross_ls_array = np.array(cm_cross_ls)
    ls_array = np.array(l_values)
    np.savez_compressed(
        parsed_path,
        angle=cm_angle_array,
        cross=cm_cross_array,
        cross_ls=cm_cross_ls_array,
        l_values=ls_array,
    )
