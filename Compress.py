import math


def lz77_compress(text, sb_size=11, lab_size=11):
    compressed = []
    i = 0
    n = len(text)

    while i < n:
        best_offset = 0
        best_length = 0

        max_search_len = min(lab_size, n - i)
        search_start = max(0, i - sb_size)

        for j in range(i - 1, search_start - 1, -1):
            length = 0
            while length < max_search_len and text[j + length] == text[i + length]:
                length += 1

            if length > best_length:
                best_length = length
                best_offset = i - j

        if i + best_length == n:
            compressed.append((best_offset, best_length, "NULL"))
            break

        if best_length >= lab_size:
            best_length = lab_size - 1

        next_char = text[i + best_length]
        compressed.append((best_offset, best_length, next_char))

        i += best_length + 1

    return compressed




def lz77_decompress(compressed):
    output = ""
    for offset, length, char in compressed:
        start_position = len(output) - offset
        for k in range(length):
            output += output[start_position + k]
        if char != "NULL":
            output += char
    return output




def calculate_sizes(text, compressed):

    num_symbols = len(text)
    orig_bits = num_symbols * 8

    if not compressed:
        return {}


    max_position = max(tag[0] for tag in compressed)
    max_length = max(tag[1] for tag in compressed)


    pos_bits = (math.ceil(math.log2(max_position + 1)) if max_position > 0 else 1)
    len_bits = math.ceil(math.log2(max_length + 1)) if max_length > 0 else 1
    symbol_bits = 8


    tag_size = pos_bits + len_bits + symbol_bits
    num_tags = len(compressed)
    comp_bits = num_tags * tag_size


    compression_ratio = orig_bits / comp_bits if comp_bits > 0 else 0


    return {
        "num_symbols": num_symbols,
        "orig_bits": orig_bits,
        "max_position": max_position,
        "max_length": max_length,
        "pos_bits": pos_bits,
        "len_bits": len_bits,
        "symbol_bits": symbol_bits,
        "tag_size": tag_size,
        "num_tags": num_tags,
        "comp_bits": comp_bits,
        "compression_ratio": compression_ratio,
    }




user_text = input(
    "Enter text to compress (default: CABRACADABRARRARRAD): ").strip()

text = user_text if user_text else "CABRACADABRARRARRAD"

user_sb = input("Enter Search Buffer (SB) size (default: 11): ").strip()
sb_size = int(user_sb) if user_sb.isdigit() else 11

user_lab = input("Enter Look-Ahead Buffer (LAB) size (default: 11): ").strip()
lab_size = int(user_lab) if user_lab.isdigit() else 11




result = lz77_compress(text, sb_size=sb_size, lab_size=lab_size)
decompressed = lz77_decompress(result)
info = calculate_sizes(text, result)

output_str = ", ".join([f"<{o},{l},'{c}'>" for o, l, c in result])



print("\n" + "=" * 60)
print(" LZ77 COMPRESSION REPORT ")
print("=" * 60)
print(f" Tags Generated: [{output_str}]")
print("-" * 60)

print(f" Original Size    = {info['num_symbols']} Symbols * 8 Bits = {info['orig_bits']} Bits")
print(f" Max Position     = {info['max_position']} -> Stored in {info['pos_bits']} Bits")
print(f" Max Length       = {info['max_length']} -> Stored in {info['len_bits']} Bits")

print( f" Tag Size         = {info['pos_bits']} + {info['len_bits']} + {info['symbol_bits']} = {info['tag_size']} Bits")
print(f" Number of Tags   = {info['num_tags']} Tags")
print(f" Compressed Size  = {info['num_tags']} * {info['tag_size']} = {info['comp_bits']} Bits")

print("-" * 60)
print(f" Compression Ratio: {info['compression_ratio']:.2f}")
print(f" Match Verified:    {decompressed == text}")
print("=" * 60)