from app.providers import OpenAICompatibleProvider

def test_provider_builds_configuration():
    provider = OpenAICompatibleProvider("test-key", "https://example.test/v1/", "test-model")
    assert provider.base_url == "https://example.test/v1"
    assert provider.model == "test-model"
    assert provider.api_key == "test-key"
