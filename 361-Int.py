"""Description
ElsieFour (LC4) is a low-tech authenticated encryption algorithm that can be computed by hand. Rather than operating on
octets, the cipher operates on this 36-character alphabet:
#_23456789abcdefghijklmnopqrstuvwxyz
Each of these characters is assigned an integer 0–35. The cipher uses a 6x6 tile substitution-box (s-box) where each
tile is one of these characters. A key is any random permutation of the alphabet arranged in this 6x6 s-box.
Additionally a marker is initially placed on the tile in the upper-left corner. The s-box is permuted and the marked
moves during encryption and decryption.
See the illustrations from the paper (album).
Each tile has a positive "vector" derived from its value: (N % 6, N / 6), referring to horizontal and vertical movement
respectively. All vector movement wraps around, modulo-style.
To encrypt a single character, locate its tile in the s-box, then starting from that tile, move along the vector of the
tile under the marker. This will be the ciphertext character (the output).
Next, the s-box is permuted. Right-rotate the row containing the plaintext character. Then down-rotate the column
containing the ciphertext character. If the tile on which the marker is sitting gets rotated, marker goes with it.
Finally, move the marker according to the vector on the ciphertext tile.
Repeat this process for each character in the message.
Decryption is the same, but it (obviously) starts from the ciphertext character, and the plaintext is computed by
moving along the negated vector (left and up) of the tile under the marker. Rotation and marker movement remains the
same (right-rotate on plaintext tile, down-rotate on ciphertext tile).
If that doesn't make sense, have a look at the paper itself. It has pseudo-code and a detailed step-by-step example.
Input Description
Your program will be fed two lines. The first line is the encryption key. The second line is a message to be decrypted.
Output Description
Print the decrypted message.
Sample Inputs
s2ferw_nx346ty5odiupq#lmz8ajhgcvk79b
tk5j23tq94_gw9c#lhzs
#o2zqijbkcw8hudm94g5fnprxla7t6_yse3v
b66rfjmlpmfh9vtzu53nwf5e7ixjnp
Sample Outputs
aaaaaaaaaaaaaaaaaaaa
be_sure_to_drink_your_ovaltine
Challenge Input
9mlpg_to2yxuzh4387dsajknf56bi#ecwrqv
grrhkajlmd3c6xkw65m3dnwl65n9op6k_o59qeq
Bonus
Also add support for encryption. If the second line begins with % (not in the cipher alphabet), then it should be
encrypted instead.
7dju4s_in6vkecxorlzftgq358mhy29pw#ba
%the_swallow_flies_at_midnight
hemmykrc2gx_i3p9vwwitl2kvljiz
If you want to get really fancy, also add support for nonces and signature authentication as discussed in the paper.
The interface for these is up to you.
Credit
This challenge was suggested by user /u/skeeto, many thanks! If you have any challenge ideas, please share them in
/r/dailyprogrammer_ideas and there's a good chance we'll use them."""


def find_vector(character):
    CONST_ALPHABET = '#_23456789abcdefghijklmnopqrstuvwxyz'

    d = {c: i for i, c in enumerate(CONST_ALPHABET)}
    value = d.get(character)
    vector = (value % 6, value // 6)
    return vector


def int_key_grid(encryption_key):

    key_grid = []
    for x in range(0, 36, 6):
        key_grid.append(list(encryption_key[x:x+6]))
    return key_grid


def decrypt_character(ecnrypted_char, key_grid, vector):
    for row, c in enumerate(key_grid):
        try:
            col = c.index(ecnrypted_char)
            char_index = (row,col)
        except ValueError:
            continue
    return key_grid[char_index[0] - vector[1]][char_index[1] - vector[0]]


def update_key_row(key_grid, decrypted_character):
    for row, c in enumerate(key_grid):
        if decrypted_character in c:
            break

    temp_list = [key_grid[row][-1]] + key_grid[row]
    key_grid[row] = temp_list[:-1]
    return key_grid


def update_key_column(key_grid, encrypted_character):
    for row, c in enumerate(key_grid):
        try:
            column = c.index(encrypted_character)
            break
        except ValueError:
            continue
    temp = [key_grid[i][column] for i in range(len(key_grid))]
    for i in range(len(temp) - 1):
        key_grid[i + 1][column] = temp[i]
    key_grid[0][column] = temp[-1]
    return key_grid


def update_marker(key_grid, grid_marker, vector):
    for row, c in enumerate(key_grid):
        try:
            col = c.index(grid_marker)
            char_index = [row,col]
            break
        except ValueError:
            continue
    if char_index[0] + vector[1] >= 6:
        char_index[0] -= 6
    if char_index[1] + vector[0] >= 6:
        char_index[1] -= 6
    grid_marker = key_grid[char_index[0] + vector[1]][char_index[1] + vector[0]]
    return grid_marker


def decrypt_message(key, message):
    grid = int_key_grid(key)
    marker = grid[0][0]
    decrypted_message = ''

    for x in message:
        decrypted_character = decrypt_character(x, grid, find_vector(marker))
        grid = update_key_row(grid, decrypted_character)
        grid = update_key_column(grid, x)
        marker = update_marker(grid, marker, find_vector(x))
        decrypted_message += decrypted_character
    print(decrypted_message)



decrypt_message('s2ferw_nx346ty5odiupq#lmz8ajhgcvk79b', 'tk5j23tq94_gw9c#lhzs')
decrypt_message('#o2zqijbkcw8hudm94g5fnprxla7t6_yse3v', 'b66rfjmlpmfh9vtzu53nwf5e7ixjnp')
decrypt_message('9mlpg_to2yxuzh4387dsajknf56bi#ecwrqv', 'grrhkajlmd3c6xkw65m3dnwl65n9op6k_o59qeq')