def lz77_compress(text, sb_size=11, lab_size=11):
    compressed = []
    i = 0
    n = len(text)

    while i < n:
        best_offset = 0
        best_length = 0

        # Max search limit in look-ahead buffer
        max_search_len = min(lab_size, n - i)

        # Search buffer boundary
        search_start = max(0, i - sb_size)

        for j in range(i - 1, search_start - 1, -1):
            length = 0
            while length < max_search_len and text[j + length] == text[i + length]:
                length += 1

            if length > best_length:
                best_length = length
                best_offset = i - j

        # Case 1: Match reaches end of text
        if i + best_length == n:
            compressed.append((best_offset, best_length, "NULL"))
            break

        # Case 2: Cap match if it fills LAB
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



user_text = input("Enter text to compress (default: CABRACADABRARRARRAD): ").strip()
text = user_text if user_text else "CABRACADABRARRARRAD"

# ب) إدخال حجم الـ Search Buffer (SB)
user_sb = input("Enter Search Buffer (SB) size (default: 11): ").strip()
sb_size = int(user_sb) if user_sb.isdigit() else 11

# جـ) إدخال حجم الـ Look-Ahead Buffer (LAB)
user_lab = input("Enter Look-Ahead Buffer (LAB) size (default: 11): ").strip()
lab_size = int(user_lab) if user_lab.isdigit() else 11








print("\n" + "=" * 55)
print(f" Text:      '{text}'")
print(f" Window:    SB = {sb_size} | LAB = {lab_size}")
print("=" * 55)

# الضغط
result = lz77_compress(text, sb_size=sb_size, lab_size=lab_size)
output_str = ", ".join([f"<{o},{l},{c}>" for o, l, c in result])

print(f"\nCompressed Output:\n[{output_str}]")

# فك الضغط والتأكد
decompressed = lz77_decompress(result)
print(f"\nDecompressed Text: {decompressed}")
print(f"Match Verified:    {decompressed == text}")
print("-" * 55)