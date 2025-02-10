def compress_file(content):
    content = list(content)
    result = ""
    counter = 0
    for i in range(0,len(content)-1):
        counter = 0
        for j in range(i, len(content)-1):
            if content[i] == content[j]:
                counter += 1
            else:
                result += str(counter) + content[i]
                counter = 0
                i = j
    return result
print(compress_file("aaaaab"))