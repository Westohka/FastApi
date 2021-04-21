from fastapi.testclient import TestClient

import main

client = TestClient( main.app )

def test_read_messages():
    response = client.get( "/msg" )

    assert response.status_code == 200
    assert response.json() == []

def test_create_user():
    response = client.post( "/usr", json = {
        "login": "test",
        "password": "test"
    } )

    assert response.status_code == 200

