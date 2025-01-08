from os import path
from sys import argv
from os import system

if __name__ == "__main__":
    asset_file = ""
    port = "8000"

    if len(argv) <= 1:
        exit("Usage: python3 keibitay [yakei_result.txt file] {port (Default: 8000)}")
    elif len(argv) >= 3:
        port = argv[2]
    asset_file = argv[1]

    _file = open(path.join(path.split(__file__)[0], "assets", "info.txt"), "w", encoding = "utf-8")
    _file.write(f"{asset_file}\n{port}")
    _file.close()

    system(f"uvicorn server:app --reload --host 0.0.0.0 --port 8000")
