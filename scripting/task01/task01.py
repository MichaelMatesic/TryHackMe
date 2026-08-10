import base64

with open("b64_1550406728131.txt", "r") as f:
    b64_encoded = f.read().strip()

for i in range(50):
    b64_encoded = base64.b64decode(b64_encoded)

b64_decoded = b64_encoded if isinstance(b64_encoded, str) else b64_encoded.decode("utf-8")

print(f"Decoded: {b64_decoded}")