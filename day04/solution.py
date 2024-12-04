def part_1(inp: str, debug: bool):
    mat = [list(line) for line in inp.splitlines()]
    width = len(mat[0])
    height = len(mat)
    xmas_count = 0
    for i, row in enumerate(mat):
        for j, letter in enumerate(row):
            if letter != "X":
                continue
            for di, dj in (
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (1, -1),
                (-1, -1),
                (-1, 1),
            ):
                for step, letter in zip((1, 2, 3), ("M", "A", "S")):
                    i_l = i + di * step
                    j_l = j + dj * step
                    if not (0 <= i_l < width and 0 <= j_l < height and mat[i_l][j_l] == letter):
                        break
                else:
                    xmas_count += 1

    print(xmas_count)


def part_2(inp: str, debug: bool):
    mat = [list(line) for line in inp.splitlines()]
    width = len(mat[0])
    height = len(mat)
    x_mas_count = 0
    for i, row in enumerate(mat):
        for j, letter in enumerate(row):
            if letter != "A":
                continue
            for ms_rotation in ("MMSS", "MSMS", "SSMM", "SMSM"):
                for (di, dj), letter in zip(
                    (
                        (-1, -1),
                        (1, -1),
                        (-1, 1),
                        (1, 1),
                    ),
                    ms_rotation,
                ):
                    i_l = i + di
                    j_l = j + dj
                    if not (0 <= i_l < width and 0 <= j_l < height and mat[i_l][j_l] == letter):
                        break
                else:
                    x_mas_count += 1
    print(x_mas_count)
