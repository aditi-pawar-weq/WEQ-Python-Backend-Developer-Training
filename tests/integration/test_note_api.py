import pytest


@pytest.mark.asyncio
async def test_create_note_api(async_client):
    payload = {
        "title": "API Note",
        "content": "API Content"
    }

    response = await async_client.post("/notes/", json=payload)

    assert response.status_code == 200
    body = response.json()

    assert body["success"] is True
    assert body["data"]["title"] == "API Note"
    assert "request_id" in body


@pytest.mark.asyncio
async def test_list_notes_api(async_client):
    response = await async_client.get("/notes/")

    assert response.status_code == 200
    body = response.json()

    assert body["success"] is True
    assert isinstance(body["data"], list)
