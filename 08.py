from utils import read_file, BIGNUM


def unpack(width, height, data):
    data = list(data)

    ix = 0
    layers = []
    while ix < len(data):
        row = ""
        for _ in range(height):
            for _ in range(width):
                row += data[ix]
                ix += 1
        layers.append(row)
    return layers


def combine(layers):
    image = layers[-1]
    for layer in reversed(layers[0:-1]):
        image = ''.join([image[i] if layer[i] == '2' else layer[i] for i in range(len(layer))])
    return image


def print_images(width, height, image):
    for y in range(height):
        for x in range(width):
            print(image[y * width + x].replace('0', ' ').replace('1', '\u2588').replace('2', ' '), end='')
        print()


print("#--- part1 ---#")

assert(unpack(3, 2, "123456789012") == ['123456', '789012'])

layers = unpack(25, 6, read_file('08.txt')[0])
fewest = BIGNUM
products = []
for layer in layers:
    data = []
    for row in layer:
        data += row
    if data.count('0') < fewest:
        fewest = data.count('0')
        products.append(data.count('1') * data.count('2'))
print(products[-1])


print("#--- part2 ---#")

layers = unpack(2, 2, "0222112222120000")
assert(combine(layers) == "0110")

layers = unpack(25, 6, read_file('08.txt')[0])
print_images(25, 6, combine(layers))
