import json
import pytest
import fakeredis
from app import app, redis_client

@pytest.fixture(scope="function")
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function", autouse=True)
def mock_redis(monkeypatch):
    """Override the Redis client in the Flask app with fakeredis."""
    fake_redis_client = fakeredis.FakeStrictRedis(decode_responses=True)
    monkeypatch.setattr("app.redis_client", fake_redis_client)
    global redis_client
    redis_client = fake_redis_client  # Ensure global override for consistency

def test_create_cache(client):
    """Test setting a key in Redis."""
    response = client.post("/api/cache", json={"key": "test", "value": "123"})
    assert response.status_code == 201
    assert b"Key `test` set with value `123`" in response.data

    # Verify key exists in Redis
    assert redis_client.get("test") == "123"


def test_create_cache_with_expiration(client):
    """Test setting a key with a specific expiration"""
    response = client.post("/api/cache", json={"key": "expiring_key", "value": "456", "expire": 120})
    assert response.status_code == 201
    assert b"Key `expiring_key` set with value `456`" in response.data

    # Verify key and TTL
    assert redis_client.get("expiring_key") == "456"
    assert redis_client.ttl("expiring_key") == 120


def test_create_cache_with_negative_expiration(client):
    """Test setting a key with a negative expiration (should be rejected)"""
    response = client.post("/api/cache", json={"key": "no_expire", "value": "789", "expire": -1})
    assert response.status_code == 201
    assert b"cannot be set with value `789` with no expiration." in response.data

    # Ensure key was NOT created
    assert redis_client.get("no_expire") is None


def test_get_existing_key(client):
    """Test retrieving an existing key."""
    redis_client.set("existing", "value123", ex=60)
    response = client.get("/api/cache/existing")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["key"] == "existing"
    assert data["value"] == "value123"
    assert data["ttl"] > 0  # TTL should be positive


def test_get_nonexistent_key(client):
    """Test retrieving a nonexistent key"""
    response = client.get("/api/cache/missing")
    assert response.status_code == 404
    assert b"Key not found" in response.data


def test_update_existing_key(client):
    """Test updating an existing key"""
    redis_client.set("update_key", "old_value", ex=60)
    response = client.put("/api/cache/update_key", json={"value": "new_value", "expire": 120})
    assert response.status_code == 200
    assert b"Key `update_key` updated with value `new_value`" in response.data

    # Verify update
    assert redis_client.get("update_key") == "new_value"
    assert redis_client.ttl("update_key") == 120


def test_update_nonexistent_key(client):
    """Test updating a nonexistent key"""
    response = client.put("/api/cache/nonexistent", json={"value": "something"})
    assert response.status_code == 404
    assert b"Key not found" in response.data


def test_delete_existing_key(client):
    """Test deleting an existing key"""
    redis_client.set("delete_me", "bye", ex=60)
    response = client.delete("/api/cache/delete_me")
    assert response.status_code == 200
    assert b"Key delete_me deleted" in response.data

    # Ensure key was removed
    assert redis_client.get("delete_me") is None


def test_delete_nonexistent_key(client):
    """Test deleting a nonexistent key"""
    response = client.delete("/api/cache/does_not_exist")
    assert response.status_code == 404
    assert b"Key not found" in response.data
