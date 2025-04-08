from typing import Dict, Any, List
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

from sensitive_content_cleaner.recognizer.custom_recognizers import (
    ja_currency_recognizer,
    ja_deny_word_recognizer,
    ja_internal_phone_number_recognizer,
)
from sensitive_content_cleaner.recognizer.localized_predefined_recognizers import ja_phone_recognizer


class PresidioEngine:
    """
    Microsoft Presidio の分析エンジンと匿名化エンジンを集約したクラス
    """

    def __init__(
        self,
        nlp_configuration: Dict[str, Any] = None,
        supported_languages: List[str] = None,
    ):
        """
        PresidioEngineのインスタンスを初期化

        Args:
            nlp_configuration (Dict[str, Any], optional): NLPエンジンの設定辞書
            supported_languages (List[str], optional): サポートする言語のリスト
        """
        if nlp_configuration is None:
            nlp_configuration = {
                "nlp_engine_name": "spacy",
                "models": [
                    {"lang_code": "ja", "model_name": "ja_core_news_trf"},
                    # {"lang_code": "en", "model_name": "en_core_web_lg"},
                ],
            }

        if supported_languages is None:
            supported_languages = ["ja"]

        # NLPエンジンの初期化
        provider = NlpEngineProvider(nlp_configuration=nlp_configuration)
        nlp_engine = provider.create_engine()

        # AnalyzerとAnonymizerの初期化
        self.analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=supported_languages)

        # #####ここ切り出す#####
        self.analyzer.registry.add_recognizer(ja_phone_recognizer())
        self.analyzer.registry.add_recognizer(ja_currency_recognizer())
        self.analyzer.registry.add_recognizer(ja_deny_word_recognizer())
        self.analyzer.registry.add_recognizer(ja_internal_phone_number_recognizer())

        # ##########

        self.anonymizer = AnonymizerEngine()

    def analyze(self, text: str, language: str = None, **kwargs):
        """
        テキストを分析して個人情報を検出

        Args:
            text (str): 分析するテキスト
            language (str, optional): テキストの言語
            **kwargs: AnalyzerEngineの追加パラメータ

        Returns:
            List[RecognizerResult]: 検出された個人情報のリスト
        """
        # return self.analyzer.analyze(text=text, language=language, **kwargs)
        return self.analyzer.analyze(text=text, language=language)

    def anonymize(self, text: str, analyzer_results=None, language: str = None, **kwargs):
        """
        テキストを匿名化

        Args:
            text (str): 匿名化するテキスト
            analyzer_results: 分析結果（Noneの場合は分析を実行）
            language (str, optional): テキストの言語
            **kwargs: 追加のパラメータ

        Returns:
            AnonymizerResult: 匿名化されたテキストと関連するメタデータ
        """
        # 分析結果がない場合は分析を実行
        if analyzer_results is None:
            analyzer_results = self.analyze(text=text, language=language)

        return self.anonymizer.anonymize(text=text, analyzer_results=analyzer_results, **kwargs)

    def analyze_and_anonymize(
        self,
        text: str,
        language: str = None,
        analyzer_kwargs: Dict[str, Any] = None,
        anonymizer_kwargs: Dict[str, Any] = None,
    ):
        """
        テキストを分析して匿名化する便利なメソッド

        Args:
            text (str): 処理するテキスト
            language (str, optional): テキストの言語
            analyzer_kwargs (Dict[str, Any], optional): Analyzerに渡す追加パラメータ
            anonymizer_kwargs (Dict[str, Any], optional): Anonymizerに渡す追加パラメータ

        Returns:
            Tuple[List[RecognizerResult], AnonymizerResult]: 分析結果と匿名化結果のタプル
        """
        if analyzer_kwargs is None:
            analyzer_kwargs = {}

        if anonymizer_kwargs is None:
            anonymizer_kwargs = {}

        # 分析を実行
        analyzer_results = self.analyze(text=text, language=language, **analyzer_kwargs)

        # 匿名化を実行
        anonymized_result = self.anonymizer.anonymize(text=text, analyzer_results=analyzer_results, **anonymizer_kwargs)

        return analyzer_results, anonymized_result

    def process_text_list(
        self,
        texts: List[str],
        language: str = None,
        analyzer_kwargs: Dict[str, Any] = None,
        anonymizer_kwargs: Dict[str, Any] = None,
    ):
        """
        テキストのリスト（配列）を一括で分析して匿名化する

        Args:
            texts (List[str]): 処理するテキストのリスト
            language (str, optional): テキストの言語
            analyzer_kwargs (Dict[str, Any], optional): Analyzerに渡す追加パラメータ
            anonymizer_kwargs (Dict[str, Any], optional): Anonymizerに渡す追加パラメータ

        Returns:
            List[Tuple[List[RecognizerResult], AnonymizerResult]]: 各テキストの分析結果と匿名化結果のリスト
        """
        if language is None:
            language = "ja"

        if analyzer_kwargs is None:
            analyzer_kwargs = {}

        if anonymizer_kwargs is None:
            anonymizer_kwargs = {}

        results = []

        for text in texts:
            # 空のテキストはスキップ
            if not text or not text.strip():
                results.append(([], None))
                continue

            # 各テキストに対して分析と匿名化を実行
            analyzer_results, anonymized_result = self.analyze_and_anonymize(
                text=text, language=language, analyzer_kwargs=analyzer_kwargs, anonymizer_kwargs=anonymizer_kwargs
            )

            results.append((analyzer_results, anonymized_result))

        return results
