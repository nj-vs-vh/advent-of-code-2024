def checksum(blocks: list[tuple[int, int | None]]) -> int:
    blocks = [b for b in blocks if b[0] > 0]
    res = 0
    offset = 0
    for b in blocks:
        blen, bid = b
        if bid != None:
            res += bid * (blen * offset + blen * (blen - 1) // 2)
        offset += blen
    return res


def part_1(inp: str, debug: bool):
    blocks = [(int(ch), i // 2 if i % 2 == 0 else None) for i, ch in enumerate(inp)]
    write = 0
    read = len(blocks) - 1
    while read > write:
        while blocks[write][1] != None or blocks[write][0] == 0:
            write += 1
        write_len, _ = blocks[write]

        while blocks[read][1] == None or blocks[read][0] == 0:
            read -= 1
        read_len, read_id = blocks[read]

        if read_len >= write_len:
            blocks[write] = (write_len, read_id)
            blocks[read] = (read_len - write_len, read_id)
        else:
            blocks.insert(write, (read_len, read_id))
            write += 1
            blocks[write] = (write_len - read_len, None)
            blocks[read + 1] = (read_len, None)

    print(checksum(blocks))


def part_2(inp: str, debug: bool):
    blocks = [(int(ch), i // 2 if i % 2 == 0 else None) for i, ch in enumerate(inp)]
    read = len(blocks) - 1
    while read > 0:
        while blocks[read][1] == None or blocks[read][0] == 0:
            read -= 1
        read_len, read_id = blocks[read]
        for write in range(read):
            write_len, write_id = blocks[write]
            if write_len >= read_len and write_id is None:
                blocks[write] = (read_len, read_id)
                if write_len > read_len:
                    blocks.insert(write + 1, (write_len - read_len, None))
                    read += 1
                blocks[read] = (read_len, None)
                break
        read -= 1

    if debug:
        print(blocks)
    print(checksum(blocks))
