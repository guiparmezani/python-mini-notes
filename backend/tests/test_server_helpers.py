from datetime import datetime

from server import parse_note_id, serialize_note, validate_note_payload


def test_serialize_note_converts_database_row_to_api_shape():
    created_at = datetime(2026, 6, 10, 14, 30, 0)
    row = (1, "Study Python", "Practice pytest", ["python", "tests"], created_at)

    note = serialize_note(row)

    assert note == {
        "id": 1,
        "title": "Study Python",
        "body": "Practice pytest",
        "tags": ["python", "tests"],
        "created_at": "2026-06-10T14:30:00",
    }


def test_validate_note_payload_accepts_and_trims_valid_payload():
    payload = {
        "title": "  Study Python  ",
        "body": "  Practice validation  ",
        "tags": ["python", "api"],
    }

    cleaned_note, error = validate_note_payload(payload)

    assert error is None
    assert cleaned_note == {
        "title": "Study Python",
        "body": "Practice validation",
        "tags": ["python", "api"],
    }


def test_validate_note_payload_defaults_missing_tags_to_empty_list():
    payload = {
        "title": "Study Python",
        "body": "Practice validation",
    }

    cleaned_note, error = validate_note_payload(payload)

    assert error is None
    assert cleaned_note["tags"] == []


def test_validate_note_payload_rejects_missing_title():
    cleaned_note, error = validate_note_payload({
        "title": "   ",
        "body": "Practice validation",
        "tags": [],
    })

    assert cleaned_note is None
    assert error == "Title is required"


def test_validate_note_payload_rejects_missing_body():
    cleaned_note, error = validate_note_payload({
        "title": "Study Python",
        "body": "   ",
        "tags": [],
    })

    assert cleaned_note is None
    assert error == "Body is required"


def test_validate_note_payload_rejects_tags_that_are_not_a_list():
    cleaned_note, error = validate_note_payload({
        "title": "Study Python",
        "body": "Practice validation",
        "tags": "python, api",
    })

    assert cleaned_note is None
    assert error == "Tags must be a list"


def test_validate_note_payload_rejects_non_string_tags():
    cleaned_note, error = validate_note_payload({
        "title": "Study Python",
        "body": "Practice validation",
        "tags": ["python", 123],
    })

    assert cleaned_note is None
    assert error == "Each tag must be a string"


def test_parse_note_id_returns_integer_for_valid_note_path():
    assert parse_note_id("/notes/42") == 42


def test_parse_note_id_returns_none_for_invalid_note_path():
    assert parse_note_id("/notes/not-a-number") is None
