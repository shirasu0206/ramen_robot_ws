import os

def read_specific_line_from_file(file_path, line_number):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= line_number:
                return lines[line_number - 1].strip()
            else:
                return None
    except Exception as e:
        return f"Error reading {file_path}: {e}"

def find_and_read_line_at_specific_depth(directory, target_filename, line_number, target_depth, current_depth=0):
    results = {}
    if current_depth == target_depth:
        # 同一階層にある場合
        for root, dirs, files in os.walk(directory):
            if target_filename in files:
                file_path = os.path.join(root, target_filename)
                line_content = read_specific_line_from_file(file_path, line_number)
                results[file_path] = line_content
        return results
    else:
        # ディレクトリを探索し続ける
        for entry in os.scandir(directory):
            if entry.is_dir():
                sub_results = find_and_read_line_at_specific_depth(entry.path, target_filename, line_number, target_depth, current_depth + 1)
                results.update(sub_results)
        return results

# メインプログラム
directory_to_search = './Tested/2024/06/0625'  # 対象のディレクトリ
target_filename = 'Log.txt'  # 対象のファイル名
line_number_to_read = 25  # 読み取りたい行番号
target_depth = 1  # 調査対象の階層の深さ

results = find_and_read_line_at_specific_depth(directory_to_search, target_filename, line_number_to_read, target_depth)

for file_path, line_content in results.items():
    print(line_content)