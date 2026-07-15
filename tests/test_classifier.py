import pytest

from hr_assistant.classifier import classify_request


@pytest.mark.parametrize("text,topic", [
    ("Je souhaite prendre des congés et partir en vacances", "leave"),
    ("How can I request annual leave and holiday?", "leave"),
    ("Ich brauche meine Lohnabrechnung und mein Gehalt", "payroll"),
    ("Necesito trabajar desde casa en remoto", "remote_work"),
])
def test_multilingual_topic_examples(text, topic):
    result = classify_request(text)
    assert result.topic == topic
    assert result.confidence >= 0.60


def test_sensitive_topic_is_detected_by_same_classifier():
    result = classify_request("I want to report harassment")
    assert result.sensitive is True
