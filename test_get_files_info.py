from functions.get_files_info import get_files_info

if __name__ == "__main__":
    print(f"Result for current directory \n{get_files_info("calculator", ".")}")
    print(f"Result for 'pkg' directory \n{get_files_info("calculator", "pkg")}")
    print(f"Result for '/bin't directory \n{get_files_info("calculator", "/bin")}")
    print(f"Result for '../' directory \n{get_files_info("calculator", "../")}")
    