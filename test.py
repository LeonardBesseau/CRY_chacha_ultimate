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
        bloc_decal = ord(i[0]) - ord('a')
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
            vector[(i[0] + 1) * size_block - index] = 1
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


def compute(a, b, c, d, size_block=32):
    c1 = c + roll(b, 1, size_block)
    b1 = b + a + roll(b, 1, size_block)

    return a, b1, c1, d


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


def invert_double_round(state):
    state[3], state[4], state[9], state[14] = q(state[3], state[4], state[9], state[14])
    state[2], state[7], state[8], state[13] = q(state[2], state[7], state[8], state[13])
    state[1], state[6], state[11], state[12] = q(state[1], state[6], state[11], state[12])
    state[0], state[5], state[10], state[15] = q(state[0], state[5], state[10], state[15])
    state[3], state[7], state[11], state[15] = q(state[3], state[7], state[11], state[15])
    state[2], state[6], state[10], state[14] = q(state[2], state[6], state[10], state[14])
    state[1], state[5], state[9], state[13] = q(state[1], state[5], state[9], state[13])
    state[0], state[4], state[8], state[12] = q(state[0], state[4], state[8], state[12])


def q1(array):
    a = array[3]
    b = array[4]
    c = array[9]
    d = array[14]
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

    return array[0], array[1], array[2], a1, b1, array[5], array[6], array[7], array[8], c1, array[10], array[11], \
           array[
               12], array[13], d1, array[15]


def q2(array):
    a = array[2]
    b = array[7]
    c = array[8]
    d = array[13]
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

    return array[0], array[1], a1, array[3], array[4], array[5], array[6], b1, c1, array[9], array[10], array[11], \
           array[
               12], d1, array[14], array[15]


def q3(array):
    a = array[1]
    b = array[6]
    c = array[11]
    d = array[12]
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

    return array[0], a1, array[2], array[3], array[4], array[5], b1, array[7], array[8], array[9], array[10], c1, d1, \
           array[
               13], array[14], array[15]


def q4(array):
    a = array[0]
    b = array[5]
    c = array[10]
    d = array[15]
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

    return a1, array[1], array[2], array[3], array[4], b1, array[6], array[7], array[8], array[9], c1, array[11], array[
        12], array[13], array[14], d1


def q5(array):
    a = array[3]
    b = array[7]
    c = array[11]
    d = array[15]
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

    return array[0], array[1], array[2], a1, array[4], array[5], array[6], b1, array[8], array[9], array[10], c1, array[
        12], array[13], array[14], d1


def q6(array):
    a = array[2]
    b = array[6]
    c = array[10]
    d = array[14]
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

    return array[0], array[1], a1, array[3], array[4], array[5], b1, array[7], array[8], array[9], c1, array[11], array[
        12], array[13], d1, array[15]


def q7(array):
    a = array[1]
    b = array[5]
    c = array[9]
    d = array[13]
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

    return array[0], a1, array[2], array[3], array[4], b1, array[6], array[7], array[8], c1, array[10], array[11], \
           array[
               12], d1, array[14], array[15]


def q8(array):
    a = array[0]
    b = array[4]
    c = array[8]
    d = array[12]
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

    return a1, array[1], array[2], array[3], b1, array[5], array[6], array[7], c1, array[9], array[
        10], array[11], d1, array[13], array[14], array[15]


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
    return (x << n) % (2 << (max_size - 1)) + (x >> (max_size - n))


def write_double_list(out, array):
    out.write("[")
    for i in range(len(array) - 1):
        out.write("[")
        for item in range(len(array[i]) - 1):
            out.write("%d," % array[i][item])
        out.write("%d" % array[i][-1])
        out.write("],")
    out.write("[")
    for item in range(len(array[-1]) - 1):
        out.write("%d," % array[-1][item])
    out.write("%d" % array[-1][-1])
    out.write("]]")


def write_simple_list(out, array):
    out.write("[")
    for i in range(len(array) - 1):
        out.write("%d," % array[i])
    out.write("%d" % array[-1])
    out.write("]")


def vector_from_list(list):
    out = []
    for i in list:
        out += number_to_vector(i)
    return out


def vector_to_number(vec):
    out = 0
    for i in range(len(vec)):
        if vec[i] == 1:
            out += 2 ** i
    return out


def list_number_from_vector(vec, size_block):
    vec1 = [vec[j:j + size_block] for j in range(0, len(vec), size_block)]
    out = [0] * len(vec1)
    for i in range(len(vec1)):
        out[i] = vector_to_number(vec1[i])
    return out


for i in range(16):
    print("v" + str(i) + " = create_vector(compute_decal(" + chr(ord('a') + i) + "),512)")

var = ["a_00", "b_00", "c_00", "d_00", "e_00", "f_00", "g_00", "h_00", "i_00", "j_00", "k_00", "l_00", "m_00", "n_0",
       "o_00", "p_00"]

MATRIX = []
for _ in range(8):
    if _ == 0:
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = q1(var)
    elif _ == 1:
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = q2(var)
    elif _ == 2:
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = q3(var)
    elif _ == 3:
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = q4(var)
    elif _ == 4:
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = q5(var)
    elif _ == 5:
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = q6(var)
    elif _ == 6:
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = q7(var)
    else:
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = q8(var)

    v0 = create_vector(compute_decal(a), 512)
    v1 = create_vector(compute_decal(b), 512)
    v2 = create_vector(compute_decal(c), 512)
    v3 = create_vector(compute_decal(d), 512)
    v4 = create_vector(compute_decal(e), 512)
    v5 = create_vector(compute_decal(f), 512)
    v6 = create_vector(compute_decal(g), 512)
    v7 = create_vector(compute_decal(h), 512)
    v8 = create_vector(compute_decal(i), 512)
    v9 = create_vector(compute_decal(j), 512)
    v10 = create_vector(compute_decal(k), 512)
    v11 = create_vector(compute_decal(l), 512)
    v12 = create_vector(compute_decal(m), 512)
    v13 = create_vector(compute_decal(n), 512)
    v14 = create_vector(compute_decal(o), 512)
    v15 = create_vector(compute_decal(p), 512)
    MATRIX.append(
        create_matrix([v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15], size_vector=512))

source = vector_from_list(
    [1634760805, 857760878, 2036477234, 1797285236, 387722230, 3787248775, 1988908842, 1434065354, 600527528,
     3311049177, 267051612, 2746319628, 0, 0, 2431318074, 3398898238])
crypted = vector_from_list(
    [916420071, 857760878, 2036477234, 1797285236, 1413802654, 3787248775, 1988908842, 1434065354, 2086383521,
     3311049177, 267051612, 2746319628, 201558885, 0, 2431318074, 3398898238])
crypted_1 = vector_from_list(
    [916420071, 727751081, 2036477234, 1797285236, 1413802654, 2183909122, 1988908842, 1434065354, 2086383521,
     4244143838, 267051612, 2746319628, 201558885, 2303407515, 2431318074, 3398898238])
cr2 = vector_from_list(
    [916420071, 727751081, 1296651692, 1797285236, 1413802654, 2183909122, 1392316882, 1434065354, 2086383521,
     4244143838, 3858945431, 2746319628, 201558885, 2303407515, 1808443599, 3398898238])
cr3 = vector_from_list(
    [916420071, 727751081, 1296651692, 2293941562, 1413802654, 2183909122, 1392316882, 4028420512, 2086383521,
     4244143838, 3858945431, 4144005159, 201558885, 2303407515, 1808443599, 976353254])
cr4 = vector_from_list(
    [502642807, 727751081, 1296651692, 2293941562, 1413802654, 995485818, 1392316882, 4028420512, 2086383521,
     4244143838, 1563928898, 4144005159, 201558885, 2303407515, 1808443599, 4130796112])
cr5 = vector_from_list(
    [502642807, 1205547541, 1296651692, 2293941562, 1413802654, 995485818, 2413971847, 4028420512, 2086383521,
     4244143838, 1563928898, 827948797, 3309800260, 2303407515, 1808443599, 4130796112])
cr6 = vector_from_list(
    [502642807, 1205547541, 3119806417, 2293941562, 1413802654, 995485818, 2413971847, 391361877, 2928628919,
     4244143838, 1563928898, 827948797, 3309800260, 1665388296, 1808443599, 4130796112])
cr7 = vector_from_list(
    [502642807, 1205547541, 3119806417, 2932436313, 3211992917, 995485818, 2413971847, 391361877, 2928628919,
     3645482179, 1563928898, 827948797, 3309800260, 1665388296, 2732223785, 4130796112])
matrix = MATRIX[-1]

print(source)

a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = q8(var)
print(a)
print(e)
print(i)
print(m)
print(b)
print(g)
print("END")
a, b, c, d = q("a_00", "e_00", "i_00", "m_00")
print(a)
print(b)
print(c)
print(d)

# a1, b1, c1, d1 = quarter_round("a_00", "b_00", "c_00", "d_00")
# print(a1)
# print(b1)
# print(c1)
# print(d1)
# print(useless(a1))
# print(useless(b1))
# print(useless(c1))
# print(useless(d1))

# a1, b1, c1, d1 = q("a_00", "b_00", "c_00", "d_00")
# print(a1)
# print(b1)
# print(c1)
# print(d1)
#
# v1 = create_vector(compute_decal(a1))
# v2 = create_vector(compute_decal(b1))
# v3 = create_vector(compute_decal(c1))
# v4 = create_vector(compute_decal(d1))
#
# matrix = create_matrix([v1, v2, v3, v4])
#
# source = number_to_vector(1634760805) + number_to_vector(387722230) + number_to_vector(600527528) + number_to_vector(0)
# crypted = number_to_vector(916420071) + number_to_vector(1413802654) + number_to_vector(2086383521) + number_to_vector(
#     201558885)

# size_block = 3
# x = compute("a_00", "b_00", "c_00", "d_00", size_block)
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
# matrix = M1
# a = 7
# b = 1
# c = 3
# d = 4
# source = number_to_vector(a, size_block) + number_to_vector(b, size_block) + number_to_vector(c,
#                                                                                               size_block) + number_to_vector(
#     d, size_block)
# tmp = a ^ r1(b, 1, size_block)
# print(tmp)
# tmp ^= a
# crypted = number_to_vector(tmp, size_block) + number_to_vector(a ^ b, size_block) + number_to_vector(c,
#                                                                                                      size_block) + number_to_vector(
#     d, size_block)
# print(source)
# print(crypted)

init = [*number_to_vector(1634760805), *number_to_vector(857760878), *number_to_vector(2036477234),
        *number_to_vector(1797285236), *number_to_vector(387722230), *number_to_vector(3787248775),
        *number_to_vector(1988908842), *number_to_vector(1434065354), *number_to_vector(600527528),
        *number_to_vector(3311049177), *number_to_vector(267051612), *number_to_vector(2746319628),
        *number_to_vector(0),
        *number_to_vector(0), *number_to_vector(2431318074), *number_to_vector(3398898238)]

state = [*number_to_vector(557917748), *number_to_vector(4084551956), *number_to_vector(1985290451),
         *number_to_vector(1918908990), *number_to_vector(2307479201), *number_to_vector(3072051967),
         *number_to_vector(505085456), *number_to_vector(468493604), *number_to_vector(828384094),
         *number_to_vector(4251025916), *number_to_vector(1804726735), *number_to_vector(171438156),
         *number_to_vector(3943143913), *number_to_vector(2797858791), *number_to_vector(1617251236),
         *number_to_vector(264329373)]

stream = vector_from_list(
    [1076977233, 3226809722, 255266273, 423649098, 2660597079, 1453792888, 1754704186, 1318501614, 313225718, 943396901,
     1685787539, 2844160832, 3943143913, 2797858791, 4035949470, 3310766755])

decode = vector_from_list(
    [1729625766, 3995436238, 2301356242, 2991683100, 146752335, 2366229084, 1501435808, 533777654, 107843560,
     2913136590, 649164501, 1865772279, 376598733, 2620077295, 3020774543, 2835235136]

)

with open('mat.sage', 'w') as output:
    output.write("init = vector(GF(2),")
    write_simple_list(output, init)
    output.write(")\n")
    output.write("state = vector(GF(2),")
    write_simple_list(output, state)
    output.write(")\n")
    output.write("stream = vector(GF(2),")
    write_simple_list(output, stream)
    output.write(")\n")

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

    output.write("cr1 = vector(GF(2),")
    write_simple_list(output, crypted_1)
    output.write(")\n")
    output.write("cr2 = vector(GF(2),")
    write_simple_list(output, cr2)
    output.write(")\n")
    output.write("cr3 = vector(GF(2),")
    write_simple_list(output, cr3)
    output.write(")\n")
    output.write("cr4 = vector(GF(2),")
    write_simple_list(output, cr4)
    output.write(")\n")
    output.write("cr5 = vector(GF(2),")
    write_simple_list(output, cr5)
    output.write(")\n")
    output.write("cr6 = vector(GF(2),")
    write_simple_list(output, cr6)
    output.write(")\n")
    output.write("cr7 = vector(GF(2),")
    write_simple_list(output, cr7)
    output.write(")\n")
    output.write("decode = vector(GF(2),")
    write_simple_list(output, decode)
    output.write(")\n")
    for i in range(len(MATRIX)):
        output.write(chr(ord('A') + i) + " = matrix(GF(2),")
        write_double_list(output, MATRIX[i])
        output.write(")\n")

    output.write("def double_round(state):\n"
                 "\tstate[0], state[4], state[8], state[12] = resolve(state[0], state[4], state[8], state[12])\n"
                 "\tstate[1], state[5], state[9], state[13] = resolve(state[1], state[5], state[9], state[13])\n"
                 "\tstate[2], state[6], state[10], state[14] = resolve(state[2], state[6], state[10], state[14])\n"
                 "\tstate[3], state[7], state[11], state[15] = resolve(state[3], state[7], state[11], state[15])\n"
                 "\tstate[0], state[5], state[10], state[15] = resolve(state[0], state[5], state[10], state[15])\n"
                 "\tstate[1], state[6], state[11], state[12] = resolve(state[1], state[6], state[11], state[12])\n"
                 "\tstate[2], state[7], state[8], state[13] = resolve(state[2], state[7], state[8], state[13])\n"
                 "\tstate[3], state[4], state[9], state[14] = resolve(state[3], state[4], state[9], state[14])\n")

    output.write("def resolve(a, b, c, d):\n"
                 "\tl = [*a ,*b ,*c , *d]\n"
                 "\tvec = A * vector(GF(2),l)\n"
                 "\treturn vec.list()[0:32], vec.list()[32:64], vec.list()[64:96], vec.list()[96:]\n")

    output.write("def invert_double_round(state):\n"
                 "\tstate[3], state[4], state[9], state[14] = resolve(state[3], state[4], state[9], state[14])\n"
                 "\tstate[2], state[7], state[8], state[13] = resolve(state[2], state[7], state[8], state[13])\n"
                 "\tstate[1], state[6], state[11], state[12] = resolve(state[1], state[6], state[11], state[12])\n"
                 "\tstate[0], state[5], state[10], state[15] = resolve(state[0], state[5], state[10], state[15])\n"
                 "\tstate[3], state[7], state[11], state[15] = resolve(state[3], state[7], state[11], state[15])\n"
                 "\tstate[2], state[6], state[10], state[14] = resolve(state[2], state[6], state[10], state[14])\n"
                 "\tstate[1], state[5], state[9], state[13] = resolve(state[1], state[5], state[9], state[13])\n"
                 "\tstate[0], state[4], state[8], state[12] = resolve(state[0], state[4], state[8], state[12])\n")

    output.write("def r1(a):\n"
                 "\tvec = A * a\n"
                 "\treturn \n")

    output.write("J = A*B*C*D*E*F*G*H\n")
    output.write("J1 = J^10\n")

    output.write("P = MatrixSpace(GF(2), 512,512)\n")

    output.write("K2 = (J1+P.identity_matrix()).inverse()")

    # print(number_to_vector(1634760805) + number_to_vector(387722230) + number_to_vector(600527528) + number_to_vector(0))
    # print(number_to_vector(1634760805 ^ r(387722230, 5)) + number_to_vector(387722230) + number_to_vector(
    #     600527528) + number_to_vector(
    #     0))
    #
    # print(r(1,6))
    # print(roll("x_00",6))
    # print(create_vector(compute_decal(roll("x_00",6)), 8,8))
    # print(number_to_vector(64,8))

result = [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0,
          1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0,
          1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1,
          0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1,
          0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1,
          1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0,
          1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0,
          0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0,
          0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0,
          0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0,
          1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0,
          1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0]

print(list_number_from_vector(result, 32))
