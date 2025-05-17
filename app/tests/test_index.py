import json
import pytest
from index import lambda_handler

def test_lambda_handler_returns_200():
    event = {"key": "value"}
    context = None
    response = lambda_handler(event, context)
    assert response["statusCode"] == 200

def test_lambda_handler_body_contains_message():
    event = {"foo": "bar"}
    context = None
    response = lambda_handler(event, context)
    body = json.loads(response["body"])
    assert "message" in body
    assert body["message"] == "Hello from Lambda!"

def test_lambda_handler_body_contains_input():
    event = {"test": 123}
    context = None
    response = lambda_handler(event, context)
    body = json.loads(response["body"])
    assert "input" in body
    assert body["input"] == event

def test_lambda_handler_with_empty_event():
    event = {}
    context = None
    response = lambda_handler(event, context)
    body = json.loads(response["body"])
    assert body["input"] == {}

def test_lambda_handler_with_none_event():
    event = None
    context = None
    response = lambda_handler(event, context)
    body = json.loads(response["body"])
    assert body["input"] is None