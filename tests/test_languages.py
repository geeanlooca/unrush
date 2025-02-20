from unrush.languages import get_language_code, normalize_language_list


def test_get_language_code() -> None:
    assert get_language_code("it") == "it"
    assert get_language_code("ita") == "it"
    assert get_language_code("italian") == "it"


def test_normalize_language_list() -> None:
    langs = ["og", "it", "NATIVE"]
    lang_codes = normalize_language_list(langs)

    assert lang_codes == ["original", "it"]

    langs = ["og", "fR", "ita", "NATIVE", "It", "Original", "FRA"]
    lang_codes = normalize_language_list(langs)
    assert lang_codes == ["original", "fr", "it"]
