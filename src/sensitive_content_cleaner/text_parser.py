from typing import List


def read_text_file_to_list(file_path: str) -> List[str]:
    lines = []

    # ファイルを開いて読み込む
    with open(file_path, "r", encoding="utf-8") as file:
        # 1行ずつ読み込んでリストに追加
        for line in file:
            # 改行文字を削除
            cleaned_line = line.rstrip("\n")
            # 空白行でなければリストに追加
            if cleaned_line.strip():
                lines.append(cleaned_line)

    return lines
