from functions.get_file_content import get_file_content

if __name__ == "__main__":
    print(f"Result for lorem.txt \n{get_file_content("calculator", "lorem.txt")}")
    print(f"Result for calculator/main.py \n{get_file_content("calculator", "main.py")}")
    print(f"Result for calculator/pkg/calculator.py \n{get_file_content("calculator", "pkg/calculator.py")}")
    print(f"Result for calculator/bin/cat \n{get_file_content("calculator", "/bin/cat")}")
    print(f"Result for calculator/pkg/does_not_exist.py \n{get_file_content("calculator", "pkg/does_not_exist.py")}")