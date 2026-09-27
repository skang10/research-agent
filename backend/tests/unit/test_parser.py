import pytest

from app.retrieval.parser import UnsupportedFileTypeError, VanillaParser


def test_parse_text_plain():
    parser = VanillaParser()
    content = b"Hello, world!"
    content_type = "text/plain"
    result = parser.parse(content, content_type)
    assert result == "Hello, world!"


def test_parse_unsupported_content_type():
    parser = VanillaParser()
    content = b"Hello, world!"
    content_type = "application/json"
    with pytest.raises(UnsupportedFileTypeError) as exc_info:
        parser.parse(content, content_type)
    assert str(exc_info.value) == "Unsupported file type: application/json"
