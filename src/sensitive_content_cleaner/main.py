from jsonargparse import auto_cli
from sensitive_content_cleaner.presidio_engine import PresidioEngine
from sensitive_content_cleaner.text_parser import read_text_file_to_list


def main(file_path: str, output_path: str = "./data/anonymized_text.txt"):
    texts = read_text_file_to_list(file_path=file_path)

    engine = PresidioEngine()
    list_results = engine.process_text_list(texts=texts)

    anonymized_texts = []

    # 結果を表示
    for i, (analyzer_results, anonymized_result) in enumerate(list_results):
        if anonymized_result:
            print(f"\n文章 {i+1}:")
            print(f"元のテキスト: {texts[i]}")
            print(f"匿名化されたテキスト: {anonymized_result.text}")

            # 匿名化テキストを出力用リストに追加
            anonymized_texts.append(anonymized_result.text)

            if analyzer_results:
                print("検出された情報:")
                for result in analyzer_results:
                    print(f"  {result.entity_type}: {texts[i][result.start:result.end]}")
        else:
            print(f"\n文章 {i+1}: 空または処理不要")

    # 匿名化テキストをファイルに書き出す
    with open(output_path, "w", encoding="utf-8") as output_file:
        for anonymized_text in anonymized_texts:
            output_file.write(anonymized_text + "\n")


if __name__ == "__main__":
    auto_cli(main)
