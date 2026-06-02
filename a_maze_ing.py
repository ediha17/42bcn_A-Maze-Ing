import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Error")
        return
    try:
        whith open(sys.argv[1], "r") as conf_file:
            for line in conf_file:
                clean_ln: str = line.strip()
                if not clean_ln or clean_ln.startswith("#")
                    continue
                if not "=" in clean_ln or clean_ln.count("=") != 1:
                    print(f"Error: Invalid syntax in line: '{clean_ln}'")
                    return
                else:
                    key: str
                    value: str
                    key, value = clean_ln.split("=")
                    key = key.strip()
                    value = value.strip()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
