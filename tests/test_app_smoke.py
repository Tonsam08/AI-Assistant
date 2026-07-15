import os

from streamlit.testing.v1 import AppTest


os.environ["EMBEDDING_BACKEND"] = "lexical"


def run_request(text: str):
    app = AppTest.from_file("app.py", default_timeout=20).run()
    assert not app.exception
    app.text_area[0].set_value(text)
    app.button[0].click().run()
    assert not app.exception
    return app


def test_normal_demo_path_displays_only_the_retained_leave_passage():
    app = run_request("Comment déposer une demande de congés et partir en vacances ?")
    assert app.info[0].value == "Réponse à valider"
    source_headings = [item.value for item in app.markdown if item.value.startswith("**[S")]
    assert len(source_headings) == 1
    assert "Congés payés" in source_headings[0]


def test_sensitive_demo_path_escalates_without_sources():
    app = run_request("Je veux signaler un harcèlement.")
    assert app.info[0].value == "Transmission aux RH"
    assert not any(item.value.startswith("**[S") for item in app.markdown)


def test_incomplete_demo_path_requests_information():
    app = run_request("J'ai une question.")
    assert app.info[0].value == "Informations complémentaires nécessaires"
