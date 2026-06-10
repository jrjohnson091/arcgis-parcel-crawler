import requests

from app.models import Params
from app.parcel_request import fetch_page


class MockResponse:
    def __init__(
        self,
        *,
        status_code=200,
        headers=None,
        json_data=None,
        text="",
        json_error=None,
        raise_error=None,
    ):
        self.status_code = status_code
        self.headers = headers or {"Content-Type": "application/json"}
        self._json_data = json_data
        self.text = text
        self._json_error = json_error
        self._raise_error = raise_error

    def raise_for_status(self):
        if self._raise_error:
            raise self._raise_error

    def json(self):
        if self._json_error:
            raise self._json_error
        return self._json_data

    def test_fetch_page_handles_request_exception(monkeypatch, capsys):
        def mock_get(*args, **kwargs):
            raise requests.exceptions.Timeout("request timed out")

        monkeypatch.setattr("app.parcel_request.requests.get", mock_get)

        result = fetch_page(Params(returnCountOnly=False))

        captured = capsys.readouterr()

        assert result is None
        assert "Request Error" in captured.out
        assert "request timed out" in captured.out


def test_fetch_page_handles_non_json_html_response(monkeypatch, capsys):
    html = """
    <html>
      <title>Application Error</title>
      <p>Could not access any server machines.</p>
    </html>
    """

    def mock_get(*args, **kwargs):
        return MockResponse(
            headers={"Content-Type": "text/html"},
            text=html,
        )

    monkeypatch.setattr("app.parcel_request.requests.get", mock_get)

    result = fetch_page(Params(returnCountOnly=False))

    captured = capsys.readouterr()

    assert result is None
    assert "Non-JSON response from ArcGIS server" in captured.out
    assert "Content-Type: text/html" in captured.out
    assert "Could not access any server machines" in captured.out


def test_fetch_page_handles_json_decode_error(monkeypatch, capsys):
    def mock_get(*args, **kwargs):
        return MockResponse(
            headers={"Content-Type": "application/json"},
            text="not valid json",
            json_error=ValueError("bad json"),
        )

    monkeypatch.setattr("app.parcel_request.requests.get", mock_get)

    result = fetch_page(Params(returnCountOnly=False))

    captured = capsys.readouterr()

    assert result is None
    assert "JSON Decode Error" in captured.out
    assert "bad json" in captured.out
    assert "not valid json" in captured.out


def test_fetch_page_handles_arcgis_json_error(monkeypatch, capsys):
    def mock_get(*args, **kwargs):
        return MockResponse(
            json_data={
                "error": {
                    "code": 404,
                    "message": "Layer not found",
                    "details": [],
                }
            }
        )

    monkeypatch.setattr("app.parcel_request.requests.get", mock_get)

    result = fetch_page(Params(returnCountOnly=False))

    captured = capsys.readouterr()

    assert result is None
    assert "ArcGIS Server Error (Code 404)" in captured.out
    assert "Layer not found" in captured.out


def test_fetch_page_returns_records_only_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(json_data={"count": 123})

    monkeypatch.setattr("app.parcel_request.requests.get", mock_get)

    result = fetch_page(Params(returnCountOnly=True))

    assert result.count == 123
