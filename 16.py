from utils import read_file


def phase(num, iterations):
    factor = [0, 1, 0, -1]
    for _ in range(iterations):
        result = []
        for phases in range(1, len(num) + 1):
            sum_ = 0
            for ix, digit in enumerate(num):
                p = ((ix + 1) // phases) & 0x3
                sum_ += factor[p] * int(digit)
            result.append(abs(sum_) % 10)
        num = ''.join(map(str, result))
    return num


print("#--- part1 ---#")

assert(phase("12345678", 1) == "48226158")
assert(phase("12345678", 2) == "34040438")
assert(phase("12345678", 3) == "03415518")
assert(phase("12345678", 4) == "01029498")

assert(phase("80871224585914546619083218645595", 100)[:8] == "24176176")
assert(phase("19617804207202209144916044189917", 100)[:8] == "73745418")
assert(phase("69317163492948606335995924319873", 100)[:8] == "52432133")

print(phase(read_file('16.txt')[0], 100)[:8])
