def lz77_compress(text, sb_size=None, lab_size=None):

    compressed = []
    i = 0
    n = len(text)

    while i < n:
        best_offset = 0
        best_length = 0

        # Maximum lookahead limit defined by LAB size and remaining text
        max_search_len = min(lab_size, n - i)

        # Search Buffer start index (limits lookback offset)
        search_start = max(0, i - sb_size)

        # Search backward inside Search Buffer range
        for j in range(i - 1, search_start - 1, -1):
            length = 0
            while length < max_search_len and text[j + length] == text[i + length]:
                length += 1

            if length > best_length:
                best_length = length
                best_offset = i - j

        # Case 1: Match reaches the end of string (no character left for next_symbol)
        if i + best_length == n:
            compressed.append((best_offset, best_length, "NULL"))
            break

        # Case 2: Cap match length if it fills the LAB (reserve 1 slot for next_symbol
        if best_length >= lab_size:
            best_length = lab_size - 1

        next_char = text[i + best_length]
        compressed.append((best_offset, best_length, next_char))

        # Advance pointer past matched length + next_char
        i += best_length + 1

    return compressed



text = "CABRACADABRARRARRAD"


combinations = [
    (2, 5),
    (3, 8),
    (7, 6),
    (20, 20)
]

for sb, lab in combinations:
    result = lz77_compress(text, sb_size=sb, lab_size=lab)
    output_str = ", ".join([f"<{o},{l},{c}>" for o, l, c in result])
    print(f"SB = {sb:2d} | LAB = {lab:2d} -> [{output_str}]")