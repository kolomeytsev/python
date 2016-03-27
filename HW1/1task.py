letters_up = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
letters_low = [chr(x) for x in range(ord('a'), ord('z') + 1)]


def give_new_letter(alphabet, ch, x):
    new_id = (alphabet.index(ch) + x) % 26
    return alphabet[new_id]


def code(text, x):
    res = ''
    for ch in text:
        if ch in letters_up:
            res += give_new_letter(letters_up, ch, x)
        elif ch in letters_low:
            res += give_new_letter(letters_low, ch, x)
        else:
            res += ch
    return res

x = int(raw_input())
text = raw_input()
print code(text, x)
