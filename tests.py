from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file


def print_content(path, label):
    result = get_file_content("calculator", path)
    print(f'get_file_content("calculator", "{path}"):')
    print(f"Result for {label}:")
    if isinstance(result, tuple):
        for part in result:
            print(part)
    else:
        print(result)
    print()


def main():
    # Demonstrate run_python_file results
    tests = [
        ("main.py default", "main.py", []),
        ("main.py with expression", "main.py", ["3 + 5"]),
        ("tests.py", "tests.py", []),
        ("outside working dir", "../main.py", []),
        ("missing file", "nonexistent.py", []),
        ("not a python file", "lorem.txt", []),
    ]
    for label, path, args in tests:
        print(f'run_python_file("calculator", "{path}", {args}):')
        print(run_python_file("calculator", path, args))
        print()


if __name__ == "__main__":
    main()
