import hashlib

def find_value(secret, start):
    found = False
    index = 1

    while not found:
        m = hashlib.md5()
        m.update('{}{}'.format(secret, index))
        result = m.hexdigest()

        if result.startswith(start):
            return index
            break

        index += 1

assert find_value('abcdef', '00000') == 609043
assert find_value('pqrstuv', '00000') == 1048970
print find_value('iwrupvqb', '00000')
print find_value('iwrupvqb', '000000')
