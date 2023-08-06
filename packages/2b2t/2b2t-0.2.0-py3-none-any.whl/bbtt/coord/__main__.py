import enum

USAGE = """\
i2w <x> <z>: convert coordinate in 8K radar image to the corresponding coordinate in 2b2t world
image2world <x> <z>: convert coordinate in 8K radar image to the corresponding coordinate in 2b2t world
w2i <x> <z>: convert coordinate in 2b2t world to the corresponding coordinate in 8K radar image
world2image <x> <z>: convert coordinate in 2b2t world to the corresponding coordinate in 8K radar image
q (or quit, exit): exit program
h (or help): show this help menu\
"""


class RadarImageType(enum.Enum):
    RADAR_4K = (3840, 2160, 8)
    RADAR_8K = (7680, 4320, 4)


def world_to_image(loc, image_type=RadarImageType.RADAR_8K) -> tuple[int, int]:
    """
    Given a coordinate in 2b2t overworld, return the corresponding pixel coordinate in radar image.
    """
    x, z = loc
    off_x, off_z, chunks_per_pixel = image_type.value[0] // 2, image_type.value[1] // 2, image_type.value[2]
    return 3840 + x // 16 // chunks_per_pixel, 2160 + z // 16 // chunks_per_pixel


def image_to_world(loc, image_type=RadarImageType.RADAR_8K) -> tuple[int, int]:
    """
    Given a position in radar image, return the center coordinate of the corresponding range in 2b2t overworld.
    """
    x, z = loc
    off_x, off_z, chunks_per_pixel = image_type.value[0] // 2, image_type.value[1] // 2, image_type.value[2]
    x, z = x - off_x, z - off_z
    return (x + 0.5) * 16 * chunks_per_pixel, (z + 0.5) * 16 * chunks_per_pixel


def main():
    """ REPL """
    try:
        while True:
            inp = input('>').strip().split(' ') or None
            func = {
                'i2w': image_to_world,
                'image2world': image_to_world,
                'w2i': world_to_image,
                'world2image': world_to_image
            }.get(inp[0])
            if not func:
                cmd = inp[0] if len(inp) > 0 else None
                if cmd == 'q' or cmd == 'quit' or cmd == 'exit':
                    return
                elif cmd == 'h' or cmd == 'help':
                    print(USAGE)
                else:
                    print('Invalid command. Run \'help\' for usage description.')
                continue
            print(func((int(inp[1]), int(inp[2]))))
    except KeyboardInterrupt:
        pass  # Ignore Ctrl-C event


if __name__ == '__main__':
    main()
