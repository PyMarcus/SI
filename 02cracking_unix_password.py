import crypt

PATH: str = "/etc/shadow"
SALT: str = "$6$"


def hash_it(word: str, salt: str) -> str:
    return crypt.crypt(word, salt)


def password() -> str:
    global SALT, PATH
    with open(PATH, 'r') as shadow:
        for line in shadow.readlines():
            word = line.split('$')
            if len(word) > 2:
                SALT = f"${word[1]}${word[2]}${word[3]}$".strip()
                return line.split(':')[1]
        return ""


def read_dict_file(filename: str) -> str or None:
    with open(filename, 'r') as file:
        for line in file.readlines():
            if hash_it(line, SALT) == password():
                return line


if __name__ == '__main__':
    print(read_dict_file('teste.txt'))
