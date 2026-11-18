def validate_article(article_text):

    if not article_text:
        raise ValueError(
            "Article text cannot be empty."
        )

    if len(article_text.strip()) < 20:
        raise ValueError(
            "Article text is too short."
        )

    suspicious_patterns = [

        "ignore previous instructions",

        "ignore all instructions",

        "ignore your instructions",

        "act as",

        "you are chatgpt",

        "system prompt",

        "developer message",

        "roleplay",

        "pretend to",

        "jailbreak",

        "override",

        "new instructions",

        "forget your instructions"
    ]

    lower_text = article_text.lower()

    for pattern in suspicious_patterns:

        if pattern in lower_text:

            raise ValueError(
                f"Potential prompt injection detected: {pattern}"
            )