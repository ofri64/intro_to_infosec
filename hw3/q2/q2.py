import assemble

patch1_path = "patch1.asm"
patch2_path = "patch2.asm"

def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()

    small_dead_zone_begin_offset = 0x633
    small_dead_zone_end_offset = 0x63A
    large_dead_zone_begin_offset = 0x5CD
    large_dead_zone_end_offset = 0x631

    patch1_bin = assemble.assemble_file(patch1_path)
    patch1_len = len(patch1_bin)
    patch2_bin = assemble.assemble_file(patch2_path)
    patch2_len = len(patch2_bin)

    # patch small dead zone
    data = data[:small_dead_zone_begin_offset] + str(patch1_bin) + data[small_dead_zone_begin_offset + patch1_len:]
    # patch large dead zone
    data = data[:large_dead_zone_begin_offset] + str(patch2_bin) + data[large_dead_zone_begin_offset + patch2_len:]

    with open(path + '.patched', 'wb') as writer:
        writer.write(data)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <readfile-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
