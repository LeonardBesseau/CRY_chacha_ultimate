import collections


# Rotate a vector
def rotate(l, n):
    return l[-n:] + l[:-n]


def vector_xor(a, b):
    out = [0] * len(a)
    for i in range(len(a)):
        out[i] = a[i] ^ b[i]
    return out


def roll(nb, n, max_size=32):
    a = int(nb[2:])
    a += n
    a = a % max_size
    if a < 10:
        return nb[:2] + "0" + str(a)
    else:
        return nb[:2] + str(a)


def roll_1(a, nb):
    out = []
    for i in a:
        out.append(roll(i, nb))
    return out


def quarter_round(a, b, c, d):
    out_a = [a, b]
    out_d = roll_1([d] + out_a, 16)
    out_c = [c] + out_d
    out_b = roll_1([b] + out_c, 12)
    out_a_2 = out_a + out_b
    out_d_2 = roll_1(out_a_2 + out_d, 8)
    out_c_2 = out_c + out_d_2
    out_b_2 = roll_1(out_b + out_c_2, 7)
    return out_a_2, out_b_2, out_c_2, out_d_2


def z(a, b, c, d):
    return a + roll(b, 5), b, c, d


def compute_decal(op, size_block=32):
    ops = [op[i:i + 4] for i in range(0, len(op), 4)]
    output = []
    for i in ops:
        bloc = i[0]
        bloc_decal = 0
        if bloc == "b":
            bloc_decal = 1
        elif bloc == "c":
            bloc_decal = 2
        elif bloc == "d":
            bloc_decal = 3

        additional_decal = int(i[2:])
        output.append((bloc_decal, additional_decal, bloc_decal * size_block + additional_decal))

    duplicate = [item for item, count in collections.Counter(output).items() if count > 1 and count % 2 == 0]
    if len(duplicate) > 0:
        for i in duplicate:
            output.remove(i)
            output.remove(i)

    output.sort(key=lambda tup: tup[2])
    return output


def create_vector(bit_set, size_vector=128, size_block=32):
    vector = [0] * size_vector
    for i in bit_set:
        index = i[1]
        if index == 0:
            vector[(i[0]) * size_block] = 1
        else:
            vector[(i[0]+1) * size_block - index] = 1
    return vector


def create_matrix(array_vec, size_vector=128, size_block=32):
    matrix = []
    for i in array_vec:
        v = i
        vec = [i[j:j + size_block] for j in range(0, len(i), size_block)]

        for j in range(size_block):
            t = []
            for k in vec:
                t += rotate(k, j)

            matrix.append(t)
    return matrix


def compute(a, b, size_block=32):
    a1 = a + roll(b, 1, size_block)
    b1 = b + a + roll(b, 0, size_block)

    return a1, b1


def q(a, b, c, d):
    a1 = roll(a, 00) + roll(b, 00) + roll(b, 12) + roll(c, 12) + roll(d, 28) + roll(a, 28) + roll(b, 28)
    b1 = roll(b, 19) + roll(c, 19) + roll(d, 3) + roll(a, 3) + roll(b, 3) + roll(c, 7) + roll(d, 23) + roll(a,
                                                                                                            23) + roll(
        b, 23) + roll(a, 15) + roll(b, 15) + roll(b, 27) + roll(c, 27) + roll(d, 11) + roll(a, 11) + roll(b, 11) + roll(
        d, 31) + roll(a, 31) + roll(b, 31)
    c1 = roll(c, 0) + roll(d, 16) + roll(a, 16) + roll(b, 16) + roll(a, 8) + roll(b, 8) + roll(b, 20) + roll(c,
                                                                                                             20) + roll(
        d, 4) + roll(a, 4) + roll(b, 4) + roll(d, 24) + roll(a, 24) + roll(b, 24)
    d1 = roll(a, 8) + roll(b, 8) + roll(b, 20) + roll(c, 20) + roll(d, 4) + roll(a, 4) + roll(b, 4) + roll(d,
                                                                                                           24) + roll(a,
                                                                                                                      24) + roll(
        b, 24)
    return a1, b1, c1, d1


def number_to_vector(number, vector_size=32):
    s = bin(number)[2:]
    if len(s) < vector_size:
        s = "0" * (vector_size - len(s)) + s
    output = [0] * vector_size
    for i in range(len(s)):
        output[i] = int(s[i])
    output.reverse()
    return output


def useless(array):
    s = ""
    for i in array:
        block = i[0]
        nb = str(int(i[2:]))
        s += "roll(" + block + "," + nb + ")^"
    return s[:-1]


def r(x, n):
    return (x << n) % (2 << 31) + (x >> (32 - n))

def r1(x, n, max_size=32):
    return (x << n) % (2 << (max_size-1)) + (x >> (max_size - n))


# a1, b1, c1, d1 = quarter_round("a_00", "b_00", "c_00", "d_00")
# print(a1)
# print(b1)
# print(c1)
# print(d1)
# print(useless(a1))
# print(useless(b1))
# print(useless(c1))
# print(useless(d1))

a1, b1, c1, d1 = q("a_00", "b_00", "c_00", "d_00")
print(a1)
print(b1)
print(c1)
print(d1)

v1 = create_vector(compute_decal(a1))
# print(v1[:32])
# print(v1)
v2 = create_vector(compute_decal(b1))
v3 = create_vector(compute_decal(c1))
v4 = create_vector(compute_decal(d1))

matrix = create_matrix([v1, v2, v3, v4])

source = number_to_vector(1634760805) + number_to_vector(387722230) + number_to_vector(600527528) + number_to_vector(0)
crypted = number_to_vector(916420071) + number_to_vector(1413802654) + number_to_vector(2086383521) + number_to_vector(
    201558885)

# size_block = 32
# x = compute("a_00", "b_00", size_block)
# M = []
#
# size_vector = size_block * len(x)
# for xi in x:
#     print(xi)
#     v1 = create_vector(compute_decal(xi, size_block), size_vector=size_vector, size_block=size_block)
#     M.append(v1)
#     print(v1)
#
# M1 = create_matrix(M, size_vector, size_block)
# print("Matrix")
# for i in M1:
#     print(i)
#
# print(M1)
#
# print(rotate([0,1,0], 0))
# matrix = M1
# a = 127
# b = 214
# source = number_to_vector(a, size_block) + number_to_vector(b, size_block)
# tmp = a ^ r1(b, 1, size_block)
# print(tmp)
# crypted = number_to_vector(tmp, size_block) + number_to_vector(a, size_block)
# print(source)
# print(crypted)

with open('mat.sage', 'w') as output:
    output.write("source = vector(GF(2),[")
    for i in range(len(source) - 1):
        output.write("%d," % source[i])
    output.write("%d" % source[-1])
    output.write("])\n")
    output.write("crypted = vector(GF(2),[")
    for item in range(len(crypted) - 1):
        output.write("%d," % crypted[item])
    output.write("%d" % crypted[-1])
    output.write("])\n")
    output.write("A = matrix(GF(2),[")
    for i in range(len(matrix) - 1):
        output.write("[")
        for item in range(len(matrix[i]) - 1):
            output.write("%d," % matrix[i][item])
        output.write("%d" % matrix[i][-1])
        output.write("],")
    output.write("[")
    for item in range(len(matrix[-1]) - 1):
        output.write("%d," % matrix[-1][item])
    output.write("%d" % matrix[-1][-1])
    output.write("]")
    output.write("])\n")

# print(number_to_vector(1634760805) + number_to_vector(387722230) + number_to_vector(600527528) + number_to_vector(0))
# print(number_to_vector(1634760805 ^ r(387722230, 5)) + number_to_vector(387722230) + number_to_vector(
#     600527528) + number_to_vector(
#     0))
#
# print(r(1,6))
# print(roll("x_00",6))
# print(create_vector(compute_decal(roll("x_00",6)), 8,8))
# print(number_to_vector(64,8))
