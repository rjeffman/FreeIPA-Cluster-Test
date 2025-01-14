import requests


def test_connection_to_webui():
    resp = requests.get("https://server.ipa.test", verify=False)
    assert resp.url == "https://server.ipa.test/ipa/ui/"
    assert resp.status_code == 200
    assert resp.reason == "OK"
    assert "<title>Identity Management</title>" in resp.text

