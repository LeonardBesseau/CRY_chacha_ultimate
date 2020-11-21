import base64
import copy

m = "You will have trouble finding the flag. The original ChaCha20 is"
c = "0C1dXd6CI4K9Wr55upsJKGWUgtvLWaLTTp3fidbnm6vN8M299QHhhJzXGpyz+MtUFnA7zDb2HPH2DgIa8QuGgvoTB/Lmvc3QESI9jGfuO1p3lhkE3LAv5EKkAj7tbrPI2kd06CPCgg=="


# Computes the Chacha20 initial state with given key, position and nonce
def initialState(key, pos, nonce):
    return [0x61707865, 0x3320646e,
            0x79622d32, 0x6b206574] + key + pos + nonce


# Cyclic shift left
def roll(x, n):
    return (x << n) % (2 << 31) + (x >> (32 - n))


def quarter_round(a, b, c, d):
    a = (a ^ b)
    d = roll(d ^ a, 16)
    c = (c ^ d)
    b = roll(b ^ c, 12)
    a = (a ^ b)
    d = roll(d ^ a, 8)
    c = (c ^ d)
    b = roll(b ^ c, 7)
    return a, b, c, d


def test(a, b, c, d):
    a1 = "(a ^ b)"
    d1 = "roll(d^" + a1 + ", 16)"
    c1 = "(c^" + d1 + ")"
    b1 = "roll(b^" + c1 + ", 12)"
    a1 = "(" + a1 + "^" + b1 + ")"
    d1 = "roll(" + d1 + "^" + a1 + ", 8)"
    c1 = "(" + c1 + "^" + d1 + ")"
    b1 = "roll(" + b1 + "^" + c1 + ", 7)"
    return a1, b1, c1, d1


# Double round on a Chacha20 state seen as a 16 32-bit integer array
def double_round(state):
    state[0], state[4], state[8], state[12] = quarter_round(state[0], state[4], state[8], state[12])
    state[1], state[5], state[9], state[13] = quarter_round(state[1], state[5], state[9], state[13])
    state[2], state[6], state[10], state[14] = quarter_round(state[2], state[6], state[10], state[14])
    state[3], state[7], state[11], state[15] = quarter_round(state[3], state[7], state[11], state[15])
    state[0], state[5], state[10], state[15] = quarter_round(state[0], state[5], state[10], state[15])
    state[1], state[6], state[11], state[12] = quarter_round(state[1], state[6], state[11], state[12])
    state[2], state[7], state[8], state[13] = quarter_round(state[2], state[7], state[8], state[13])
    state[3], state[4], state[9], state[14] = quarter_round(state[3], state[4], state[9], state[14])


def chacha(state):
    for _ in range(10):
        double_round(state)
    return state


# Converts a 32-bit word into 4 bytes
def w2b(word):
    return [(word & 0x000000ff), ((word & 0x0000ff00) >> 8),
            ((word & 0x00ff0000) >> 16), ((word & 0xff000000) >> 24)]


# Converts four bytes into a 32-bit word
def _b2w(bytes):
    return (bytes[0] + (bytes[1] << 8) + (bytes[2] << 16) + (bytes[3] << 24)) & 0xffffffff


# Converts a 64 byte array into a Chacha state
def streamToState(stream):
    res = []
    for i in range(16):
        res.append(_b2w(stream[i * 4:(i + 1) * 4]))
    return res


# Converts a chacha state into a bitstring for final xoring operation
def from_little_endian(state):
    res = []
    for i in state:
        res = res + w2b(i)
    return res


# Final xoring operation: plaintext XOR bit stream
def finalXor(pt_array, state):
    stream = from_little_endian(state)
    ciphertext = []
    for i in range(64):
        ciphertext.append(stream[i] ^ pt_array[i])
    return bytes(ciphertext)


def chacha_encrypt(plaintext, key, pos, nonce):
    plaintext = copy.deepcopy(plaintext)
    key = copy.deepcopy(key)
    pos = copy.deepcopy(pos)
    nonce = copy.deepcopy(nonce)
    if len(plaintext) != 64:
        print("plaintext needs to be 512 bits not " + str(len(plaintext)))
        return
    pt_array = bytearray(plaintext, "utf8")
    init_state = initialState(key, pos, nonce)
    cp = copy.deepcopy(init_state)
    final_state = chacha(cp)
    stream = []
    for i in range(len(init_state)):
        stream.append(init_state[i] ^ final_state[i])
    return finalXor(pt_array, stream)


def chacha_decrypt(plaintext, key, pos, nonce):
    plaintext = copy.deepcopy(plaintext)
    key = copy.deepcopy(key)
    pos = copy.deepcopy(pos)
    nonce = copy.deepcopy(nonce)
    if len(plaintext) != 64:
        print("plaintext needs to be 512 bits not " + str(len(plaintext)))
        return
    pt_array = copy.deepcopy(plaintext)
    init_state = initialState(key, pos, nonce)
    cp = copy.deepcopy(init_state)

    print("init", end=' ')
    print(init_state)

    final_state = chacha(cp)

    stream = []
    print("state", end=' ')
    print(final_state)
    for i in range(16):
        stream.append(init_state[i] ^ final_state[i])
    print("stream", end=' ')
    print(stream)

    return finalXor(pt_array, stream)


def q(a, b, c, d):
    a1 = roll(a, 00) ^ roll(b, 00) ^ roll(b, 12) ^ roll(c, 12) ^ roll(d, 28) ^ roll(a, 28) ^ roll(b, 28)
    b1 = roll(b, 19) ^ roll(c, 19) ^ roll(d, 3) ^ roll(a, 3) ^ roll(b, 3) ^ roll(c, 7) ^ roll(d, 23) ^ roll(a,
                                                                                                            23) ^ roll(
        b, 23) ^ roll(a, 15) ^ roll(b, 15) ^ roll(b, 27) ^ roll(c, 27) ^ roll(d, 11) ^ roll(a, 11) ^ roll(b, 11) ^ roll(
        d, 31) ^ roll(a, 31) ^ roll(b, 31)
    c1 = roll(c, 0) ^ roll(d, 16) ^ roll(a, 16) ^ roll(b, 16) ^ roll(a, 8) ^ roll(b, 8) ^ roll(b, 20) ^ roll(c,
                                                                                                             20) ^ roll(
        d, 4) ^ roll(a, 4) ^ roll(b, 4) ^ roll(d, 24) ^ roll(a, 24) ^ roll(b, 24)
    d1 = roll(a, 8) ^ roll(b, 8) ^ roll(b, 20) ^ roll(c, 20) ^ roll(d, 4) ^ roll(a, 4) ^ roll(b, 4) ^ roll(d,
                                                                                                           24) ^ roll(a,
                                                                                                                      24) ^ roll(
        b, 24)
    return a1, b1, c1, d1


def invert_finalXor(pt_array, state):
    stream = state
    ciphertext = pt_array
    output = []
    for i in range(64):
        output.append(stream[i] ^ ciphertext[i])
    return streamToState(output)


if __name__ == '__main__':
    plaintext = 'You will have trouble finding the flag. My version of ChaCha20 i'
    c = "/5FiR7ntSYLygEr/eVYlwCA23WQ56m/kznMXN5HspHeNrwtqr4iMjZgPkVCSHkYGoh5SeYkUaPTuH2XVcnHewcJ2UgFI7EZFVsHizsg9XNHGE6K6b326iEGkRj2ICfDzE6rTiddbZ955YjBR4imUur1/n9Nw"

    keyFound = [0x171c2bf4,
                0xe1bce487,
                0x768c572a,
                0x557a19ca,
                0x23cb52a8,
                0xca5a99d9,
                0xfeae25c,
                0xa3b1830c]

    nonce = [0x90eaf83a, 0xca97123e]
    # av = initialState(keyFound, [0, 0], nonce)

    # print(av)
    # av[0], av[4], av[8], av[12] = q(av[0], av[4], av[8], av[12])
    # print(av)
    # av[1], av[5], av[9], av[13] = q(av[1], av[5], av[9], av[13])
    # print(av)
    # av[2], av[6], av[10], av[14] = q(av[2], av[6], av[10], av[14])
    # print(av)
    # av[3], av[7], av[11], av[15] = q(av[3], av[7], av[11], av[15] )
    # print(av)
    # av[0], av[5], av[10], av[15] = q(av[0], av[5], av[10], av[15])
    # print(av)
    # av[1], av[6], av[11], av[12] = q(av[1], av[6], av[11], av[12])
    # print(av)
    # av[2], av[7], av[8], av[13] = q(av[2], av[7], av[8], av[13])
    # print(av)
    # av[3], av[4], av[9], av[14] = q(av[3], av[4], av[9], av[14])
    # print(av)
    # init_state = initialState(keyFound, [0, 0], nonce)
    # print(init_state)
    # for i in init_state:
    #     print(hex(i))
    # for i in range(10):
    #     double_round(init_state)

    # print(init_state)
    # print("hello")
    # init = initialState(keyFound, [0, 0], nonce)
    # for i in range(16):
    #     init_state[i] = init[i] ^ init_state[i]
    # print(init_state)
    # init = initialState([0, 0, 0, 0, 0, 0, 0, 0], [0, 0], [0, 0])
    # for i in range(16):
    #     init_state[i] = init[i] ^ init_state[i]
    # print(init_state)
    c1 = chacha_encrypt(plaintext, keyFound, [0, 0], nonce)
    arr = []
    t = bytearray(plaintext, "utf8")
    for i in range(64):
        arr.append(t[i] ^ c1[i])
    print("test_stream ", end=' ')
    print(streamToState(arr))
    print(base64.b64encode(c1))
    print(chacha_decrypt(c1, keyFound, [0, 0], nonce))

    print()
    print("Test to find stream from unknown")
    c1 = base64.b64decode(c)
    t = bytearray(plaintext, "utf8")
    arr = []
    for i in range(64):
        arr.append(t[i] ^ c1[i])
    print(streamToState(arr))


    key_found = [3305947535, 3287107494, 3534216904, 3503964662, 2013964433,
            80122982, 2633959450, 3042788487]
    nonce = [435862908, 346180266]

    init_state = initialState(key_found, [0,1], nonce)
    cp = copy.deepcopy(init_state)
    final_state = chacha(cp)
    stream1 = []
    for i in range(len(init_state)):
        stream1.append(init_state[i] ^ final_state[i])

    stream2 = from_little_endian(stream1)
    ciphertext = []
    for i in range(64):
        if(64+ i < len(c1)):
            ciphertext.append(stream2[i] ^ c1[64+i])

    print(bytes(ciphertext))


