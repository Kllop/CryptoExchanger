import hashlib

result = hashlib.md5(b'GeeksforGeeks')

print("The byte equivalent of hash is : ", end ="")
print(result.hexdigest())