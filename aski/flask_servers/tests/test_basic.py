import pytest

def get_select_model_options(client, app):
    assert client.get('/get_model_checklist').status_code == 401
    
