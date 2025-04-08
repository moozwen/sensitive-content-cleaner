from presidio_analyzer import PatternRecognizer, Pattern


def ja_currency_recognizer():
    """
    日本語テキスト内の日本円金額表記を認識するための認識器を作成します。

    「1,000円」や「500円」などの日本円の金額表記を検出します。
    カンマ区切りの数字に続く「円」という文字のパターンを認識します。

    Returns:
        PatternRecognizer: 日本語テキスト内の円金額表記を検出するための設定済み認識器

    例:
        「商品価格は1,000円です」→ 「1,000」を検出
        「500円になります」→ 「500」を検出
    """
    expected_confidence_level = 0.4

    regex = r"(\d{1,3}(,\d{3})*)(?=[一-龯]?円)"
    pattern = Pattern(name="japanese currency - yen", regex=regex, score=expected_confidence_level)

    return PatternRecognizer(
        supported_entity="JA_CURRENCY",
        name="ja_currency",
        supported_language="ja",
        patterns=[pattern],
        context=["円", "¥", "金額"],
    )


def ja_internal_phone_number_recognizer():
    """
    日本語テキスト内の内線電話番号を認識するための認識器を作成します。

    「内線:1234」や「内線：2345」などの内線電話番号表記を検出します。
    「内線:」または「内線：」の後に続く4桁の数字を認識します。

    Returns:
        PatternRecognizer: 日本語テキスト内の内線電話番号を検出するための設定済み認識器

    例:
        「お問い合わせは内線:1234まで」→ 「1234」を検出
        「内線：2345にご連絡ください」→ 「2345」を検出
    """
    expected_confidence_level = 0.4

    regex = r"(?<=内線[:|：])\s*(\d{4})"
    pattern = Pattern(name="japanese internal phone number", regex=regex, score=expected_confidence_level)

    return PatternRecognizer(
        supported_entity="JA_INT_PHONE",
        name="ja_internal_phone_number",
        supported_language="ja",
        patterns=[pattern],
        context=["内線"],
    )


def ja_deny_word_recognizer():
    """
    特定の単語やフレーズをPII検出から除外するための認識器を作成します。

    会社名、製品コード、クレジットカード番号の例など、PII検出で誤検出する可能性のある
    特定の単語やフレーズを検出し、それらを「DENY」エンティティとしてマークします。
    これにより、これらの単語やフレーズは他のPII検出から除外されます。

    Returns:
        PatternRecognizer: 除外すべき単語やフレーズを検出するための設定済み認識器

    除外リストの例:
        - 会社名（「株式会社テクノソリューションズ」など）
        - 製品/案件コード（「TS-2023-0456」など）
        - サンプルクレジットカード番号（「VISA/4444-5555-6666-7777」など）
    """
    expected_confidence_level = 0.9

    return PatternRecognizer(
        supported_entity="DENY",
        name="deny words",
        supported_language="ja",
        deny_list=[
            "株式会社テクノソリューションズ",
            "株式会社フューチャーインダストリーズ",
            "テクノソリューションズ",
            "フューチャーインダストリーズ",
            "フューチャーインダストリーズ本社",
            "松本物産",
            "TS-2023-0456",
            "AX-78901234",
            "VISA/4444-5555-6666-7777",
        ],
        deny_list_score=expected_confidence_level,
    )
