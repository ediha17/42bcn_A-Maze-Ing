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
    except Exception as e:
        raise etry







if __name__ == "__main__":
    main()
