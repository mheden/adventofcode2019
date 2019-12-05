from utils import read_file


def check_password(pwd):
    doubles = 0
    fail = 0
    last_digit = None
    for p in pwd:
        if p == last_digit:
            doubles += 1
        if last_digit is not None and p < last_digit:
            fail += 1
        last_digit = p
    return doubles > 0 and fail == 0


def check_password2(pwd):
    doubles = [0 for _ in range(0, 10)]
    fail = 0
    last_digit = None
    for p in pwd:
        if p == last_digit:
            doubles[int(p)] += 1
        if last_digit is not None and p < last_digit:
            fail += 1
        last_digit = p
    try:
        return doubles.index(1) and fail == 0
    except ValueError:
        return False


print("#--- part1 ---#")

assert(check_password('111111') is True)
assert(check_password('223450') is False)
assert(check_password('123789') is False)

print(sum([check_password(str(pwd)) for pwd in range(168630, 718098)]))


print("#--- part2 ---#")

assert(check_password2('112233') is True)
assert(check_password2('123444') is False)
assert(check_password2('111122') is True)

print(sum([check_password2(str(pwd)) for pwd in range(168630, 718098)]))
