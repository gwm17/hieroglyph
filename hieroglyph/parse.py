from pathlib import Path
import numpy as np

ELASTIC_CS_HEADER = "0    ANGLE          SIGMA/             SIGMA              RUTHERFORD         % PER    % PER"
ELASTIC_CS_FOOTER = "1                                              P T O L E M Y"
ELASTIC_CS_FOOTER_ALT = "0TOTAL REACTION CROSS SECTION"

DWBA_CS_HEADER = "0  C.M.  REACTION     REACTION   LOW L  HIGH L   % FROM"
DWBA_CS_FOOTER = "1                                                      P T O L E M Y"
DWBA_CS_FOOTER_ALT = "0TOTAL:"

DWBA_LXS_PER_ROW = 3
DWBA_HEADER_WORDS_PER_LX = 3


def parse_elastic_differential_cross_section(
    ptolemy_path: Path, parsed_path: Path
) -> None:
    cm_angles = []
    cm_cross = []

    with open(ptolemy_path, "r") as pt_file:
        pt_lines = pt_file.readlines()
        idx = 0
        while idx < len(pt_lines):
            cur_line = pt_lines[idx]
            if cur_line.startswith(ELASTIC_CS_HEADER):
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
    cm_angles = []
    cm_cross = []
    cm_cross_ls = None
    l_values = []
    lxs_per_row = []
    rows_per_line = 0

    with open(ptolemy_path, "r") as pt_file:
        pt_lines = pt_file.readlines()
        idx = 0
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
                            cm_cross_ls[array_idx].append(float(entries[start_idx + i]))
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
