"""
test_api.py – API tests for JSONPlaceholder.

These tests demonstrate:
  • GET / POST / PUT / DELETE request testing
  • Status-code assertions
  • Response-structure validation
  • Data-driven testing with @pytest.mark.parametrize
"""

import json
import logging
import os
import pytest

# Import our reusable API client
from utils.api_client import APIClient

# ──────────────────────────────────────────────
# Setup: load test data and create a client
# ──────────────────────────────────────────────

# Resolve paths relative to the project root (one level up from tests/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(PROJECT_ROOT, "test_data.json")

with open(DATA_FILE, "r") as f:
    TEST_DATA = json.load(f)

API_DATA = TEST_DATA["api"]
BASE_URL = API_DATA["base_url"]

# Configure logging so we can see request details when running with -s
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

# Create a single client instance used by every test in this file
client = APIClient(BASE_URL)


# ──────────────────────────────────────────────
# Test 1 – GET all posts
# ──────────────────────────────────────────────
class TestGetPosts:
    """Tests for the /posts endpoint (GET)."""

    def test_get_all_posts_status_code(self):
        """GET /posts should return HTTP 200."""
        response = client.get(API_DATA["posts_endpoint"])
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    def test_get_all_posts_returns_list(self):
        """The response body should be a non-empty JSON list."""
        response = client.get(API_DATA["posts_endpoint"])
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        assert len(data) > 0, "Post list should not be empty"

    def test_post_structure(self):
        """Each post should have the expected keys."""
        response = client.get(API_DATA["posts_endpoint"])
        post = response.json()[0]  # inspect the first post
        expected_keys = {"userId", "id", "title", "body"}
        assert expected_keys.issubset(post.keys()), (
            f"Post is missing keys. Expected {expected_keys}, got {set(post.keys())}"
        )

    def test_get_single_post(self):
        """GET /posts/1 should return the post with id 1."""
        response = client.get(f"{API_DATA['posts_endpoint']}/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1, f"Expected id=1, got id={data['id']}"


# ──────────────────────────────────────────────
# Test 2 – POST (create a resource)
# ──────────────────────────────────────────────
class TestCreatePost:
    """Tests for creating a new post (POST /posts)."""

    def test_create_post_status_code(self):
        """POST /posts should return HTTP 201 (Created)."""
        response = client.post(API_DATA["posts_endpoint"], API_DATA["new_post"])
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    def test_create_post_returns_data(self):
        """The response should echo back the data we sent, plus an id."""
        response = client.post(API_DATA["posts_endpoint"], API_DATA["new_post"])
        data = response.json()
        assert data["title"] == API_DATA["new_post"]["title"]
        assert data["body"] == API_DATA["new_post"]["body"]
        assert "id" in data, "Response should include an 'id' field"


# ──────────────────────────────────────────────
# Test 3 – PUT (update a resource)
# ──────────────────────────────────────────────
class TestUpdatePost:
    """Tests for updating a post (PUT /posts/1)."""

    def test_update_post_status_code(self):
        """PUT /posts/1 should return HTTP 200."""
        response = client.put(
            f"{API_DATA['posts_endpoint']}/1", API_DATA["updated_post"]
        )
        assert response.status_code == 200

    def test_update_post_returns_new_title(self):
        """The response should reflect the updated title."""
        response = client.put(
            f"{API_DATA['posts_endpoint']}/1", API_DATA["updated_post"]
        )
        data = response.json()
        assert data["title"] == API_DATA["updated_post"]["title"]


# ──────────────────────────────────────────────
# Test 4 – DELETE
# ──────────────────────────────────────────────
class TestDeletePost:
    """Tests for deleting a post (DELETE /posts/1)."""

    def test_delete_post_status_code(self):
        """DELETE /posts/1 should return HTTP 200."""
        response = client.delete(f"{API_DATA['posts_endpoint']}/1")
        assert response.status_code == 200


# ──────────────────────────────────────────────
# Test 5 – GET users
# ──────────────────────────────────────────────
class TestGetUsers:
    """Tests for the /users endpoint."""

    def test_get_users_status_code(self):
        """GET /users should return HTTP 200."""
        response = client.get(API_DATA["users_endpoint"])
        assert response.status_code == 200

    def test_users_have_email(self):
        """Every user object should contain an email field."""
        response = client.get(API_DATA["users_endpoint"])
        users = response.json()
        for user in users:
            assert "email" in user, f"User {user.get('id')} is missing 'email'"


# ──────────────────────────────────────────────
# Test 6 – Data-driven example with parametrize
# ──────────────────────────────────────────────
@pytest.mark.parametrize(
    "post_id, expected_status",
    [
        (1, 200),   # existing post
        (2, 200),   # existing post
        (100, 200), # last valid post
    ],
    ids=["post-1", "post-2", "post-100"],
)
def test_get_post_by_id(post_id, expected_status):
    """Parameterised test – fetch individual posts by id."""
    response = client.get(f"{API_DATA['posts_endpoint']}/{post_id}")
    assert response.status_code == expected_status, (
        f"Post {post_id}: expected {expected_status}, got {response.status_code}"
    )
