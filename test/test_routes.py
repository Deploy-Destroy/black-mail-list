import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, UTC
from app.routes import blacklist_bp, health_bp
from app.models import Blacklist

@pytest.fixture
def client():
    from flask import Flask
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['API_TOKEN'] = 'blacklist-secret-token-2024'
    app.register_blueprint(blacklist_bp, url_prefix='/blacklists')
    app.register_blueprint(health_bp, url_prefix='')
    return app.test_client()

@pytest.fixture
def mock_db():
    with patch('app.routes.db') as mock:
        # Configurar el mock para la consulta
        mock.session.query.return_value = mock.session
        mock.session.filter_by.return_value = mock.session
        mock.session.first.return_value = None
        yield mock

@pytest.fixture
def mock_blacklist_model():
    with patch('app.routes.Blacklist') as mock:
        yield mock

@pytest.fixture
def mock_require_token():
    with patch('app.routes.require_token') as mock:
        mock.return_value = lambda f: f
        yield mock

@pytest.fixture
def auth_headers():
    return {'Authorization': 'Bearer blacklist-secret-token-2024'}

def test_health_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "API running"}

def test_create_blacklist_success(client, mock_db, mock_require_token, mock_blacklist_model, auth_headers):
    test_data = {
        'email': 'test@example.com',
        'app_uuid': '123e4567-e89b-12d3-a456-426614174000',
        'blocked_reason': 'Test reason'
    }
    
    # Crear una instancia mock de Blacklist
    mock_blacklist_instance = MagicMock()
    mock_blacklist_instance.to_dict.return_value = {
        'email': test_data['email'],
        'app_uuid': test_data['app_uuid'],
        'blocked_reason': test_data['blocked_reason']
    }
    
    # Configurar el mock del modelo para devolver la instancia mock
    mock_blacklist_model.return_value = mock_blacklist_instance
    
    mock_db.session.add.return_value = None
    mock_db.session.commit.return_value = None
    
    response = client.post('/blacklists', json=test_data, headers=auth_headers)
    
    assert response.status_code == 201
    assert response.json['success'] is True
    assert response.json['message'] == 'Email agregado a la lista negra exitosamente'
    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()

def test_create_blacklist_missing_fields(client, mock_require_token, auth_headers):
    test_data = {
        'email': 'test@example.com',
        'app_uuid': '123e4567-e89b-12d3-a456-426614174000'
    }
    
    response = client.post('/blacklists', json=test_data, headers=auth_headers)
    
    assert response.status_code == 400
    assert response.json['success'] is False
    assert 'Faltan campos requeridos' in response.json['message']

def test_check_blacklist_found(client, mock_db, mock_require_token, mock_blacklist_model, auth_headers):
    test_email = 'test@example.com'
    mock_blacklist = MagicMock()
    mock_blacklist.email = test_email
    mock_blacklist.blocked_reason = 'Test reason'
    mock_blacklist.app_uuid = '123e4567-e89b-12d3-a456-426614174000'
    mock_blacklist.created_at = datetime.now(UTC)
    mock_blacklist.request_ip = '127.0.0.1'
    mock_blacklist.request_time = datetime.now(UTC)
    
    # Configurar el mock para devolver el objeto mock_blacklist
    mock_blacklist_model.query = mock_db.session
    mock_db.session.filter_by.return_value = mock_db.session
    mock_db.session.first.return_value = mock_blacklist
    
    response = client.get(f'/blacklists/{test_email}', headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json['success'] is True
    assert response.json['is_blacklisted'] is True
    assert response.json['data']['email'] == test_email

def test_check_blacklist_not_found(client, mock_db, mock_require_token, mock_blacklist_model, auth_headers):
    test_email = 'notfound@example.com'
    
    # Configurar el mock para devolver None (email no encontrado)
    mock_blacklist_model.query = mock_db.session
    mock_db.session.filter_by.return_value = mock_db.session
    mock_db.session.first.return_value = None
    
    response = client.get(f'/blacklists/{test_email}', headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json['success'] is True
    assert response.json['is_blacklisted'] is False
    assert 'El email no está en la lista negra' in response.json['message'] 