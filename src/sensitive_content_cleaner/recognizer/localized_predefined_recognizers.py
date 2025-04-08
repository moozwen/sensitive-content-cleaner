from presidio_analyzer.predefined_recognizers import PhoneRecognizer, EmailRecognizer, CreditCardRecognizer


def ja_phone_recognizer():
    """
    日本語テキスト内の電話番号を認識するための認識器を作成します。

    日本の電話番号形式に特化しており、「電話」「内線」「携帯」などの文脈語を
    使用して検出精度を向上させています。

    Returns:
        PhoneRecognizer: 日本語テキスト内の電話番号を検出するための設定済み認識器
    """
    return PhoneRecognizer(supported_regions=["JP"], supported_language="ja", context=["電話", "内線", "携帯"])


def ja_email_recognizer():
    """
    日本語テキスト内のメールアドレスを認識するための認識器を作成します。

    メールアドレスは国際的な形式に従いますが、この認識器は日本語テキスト内での
    検出に最適化されています。

    Returns:
        EmailRecognizer: 日本語テキスト内のメールアドレスを検出するための設定済み認識器
    """
    return EmailRecognizer(supported_language="ja")


def ja_credit_card_recognizer():
    """
    日本語テキスト内のクレジットカード番号を認識するための認識器を作成します。

    一般的なクレジットカード番号のパターンを認識し、日本語テキスト内での
    検出に最適化されています。

    Returns:
        CreditCardRecognizer: 日本語テキスト内のクレジットカード番号を検出するための設定済み認識器
    """
    return CreditCardRecognizer(supported_language="ja")
