from functions.get_files_info import get_files_info

test_cases = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../")
]

for item in test_cases:
    print(f"Result for {'current' if item[1] == '.' else "'"+item[1]+"'"} directory:\n{get_files_info(*item)}")

# print(get_files_info("calculator", "."))
# print(get_files_info("calculator", "pkg"))
# print(get_files_info("calculator", "/bin"))
# print(get_files_info("calculator", "../"))