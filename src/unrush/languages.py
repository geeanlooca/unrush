from langcodes import find, standardize_tag
from langcodes.tag_parser import LanguageTagError
from loguru import logger

ACCEPTED_ORIGINAL_LANGUAGE_KEYWORDS = set(["original", "og", "native"])
ORIGINAL_LANGUAGE_KEYWORD = "original"


def get_language_code(language: str) -> str:
    if language in ACCEPTED_ORIGINAL_LANGUAGE_KEYWORDS:
        return ORIGINAL_LANGUAGE_KEYWORD

    try:
        lang_code = standardize_tag(language)
        return lang_code
    except LanguageTagError as e:
        logger.warning(f"Could not parse {language} as tag: {e}")

    try:
        lang_code = find(language)
        return lang_code.to_tag()
    except LookupError as e:
        logger.error(f"Could not interpret {language} as language: {e}")

    logger.warning("Returning language code as is...")

    return language


def normalize_language_list(languages: list[str]) -> list[str]:
    """Transforms languages in language codes, preserving the specifying order."""

    seen_languages = set()
    ordered_list = []

    for language in languages:
        lang_code = get_language_code(language.casefold())

        if lang_code not in seen_languages:
            ordered_list.append(lang_code)

        seen_languages.add(lang_code)

    return ordered_list
