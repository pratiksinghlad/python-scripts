"""Requests Example - HTTP Operations

Demonstrates:
- GET and POST requests
- Headers and parameters
- JSON handling
- Error handling
- Session management
"""
import json
from typing import Dict, Any

def demonstrate_basic_requests():
    """Show basic HTTP requests"""
    print("=== Basic HTTP Requests ===")
    
    try:
        import requests
        
        # GET request
        response = requests.get('https://httpbin.org/get')
        print(f"GET Status Code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        # GET with parameters
        params = {'key1': 'value1', 'key2': 'value2'}
        response = requests.get('https://httpbin.org/get', params=params)
        data = response.json()
        print(f"GET with params - URL: {data['url']}")
        
        # POST request
        post_data = {'username': 'testuser', 'password': 'testpass'}
        response = requests.post('https://httpbin.org/post', data=post_data)
        print(f"POST Status Code: {response.status_code}")
        
    except ImportError:
        print("❌ requests not installed. Install with: pip install requests")
        print("Showing request structure without actual HTTP calls...\n")
        simulate_requests()

def simulate_requests():
    """Simulate requests for demonstration when library not available"""
    print("=== Simulated Request Examples ===")
    
    # Show what a typical request would look like
    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json_data = json_data
            self.headers = {'Content-Type': 'application/json'}
        
        def json(self):
            return self._json_data
    
    # Simulate API responses
    mock_get_response = MockResponse(200, {
        'status': 'success',
        'data': {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}
    })
    
    print(f"Mock GET response: {mock_get_response.status_code}")
    print(f"Mock data: {mock_get_response.json()}")
    print()

def demonstrate_json_handling():
    """Show JSON request/response handling"""
    print("=== JSON Handling ===")
    
    try:
        import requests
        
        # POST JSON data
        json_data = {
            'name': 'Alice',
            'email': 'alice@example.com',
            'age': 30
        }
        
        response = requests.post('https://httpbin.org/post', json=json_data)
        response_data = response.json()
        
        print("Sent JSON data:")
        print(json.dumps(json_data, indent=2))
        print(f"Server received: {response_data['json']}")
        
    except ImportError:
        print("Example of JSON handling:")
        sample_data = {'name': 'Alice', 'email': 'alice@example.com'}
        print(f"Would send: {json.dumps(sample_data, indent=2)}")
    
    print()

def demonstrate_error_handling():
    """Show proper error handling for HTTP requests"""
    print("=== Error Handling ===")
    
    try:
        import requests
        from requests.exceptions import RequestException, Timeout, ConnectionError
        
        urls_to_test = [
            'https://httpbin.org/status/404',  # 404 error
            'https://httpbin.org/delay/1',     # Slow response
            'https://nonexistent-domain-12345.com'  # Connection error
        ]
        
        for url in urls_to_test:
            try:
                response = requests.get(url, timeout=0.5)
                response.raise_for_status()  # Raises exception for HTTP errors
                print(f"✅ {url}: Success ({response.status_code})")
                
            except ConnectionError:
                print(f"❌ {url}: Connection failed")
            except Timeout:
                print(f"⏱️ {url}: Request timed out")
            except requests.exceptions.HTTPError as e:
                print(f"🚫 {url}: HTTP error {e.response.status_code}")
            except RequestException as e:
                print(f"❌ {url}: Request failed - {e}")
    
    except ImportError:
        print("Error handling example (simulated):")
        print("✅ https://api.example.com/users: Success (200)")
        print("🚫 https://api.example.com/missing: HTTP error 404")
        print("❌ https://invalid-domain.com: Connection failed")
    
    print()

def demonstrate_headers_auth():
    """Show custom headers and authentication"""
    print("=== Headers and Authentication ===")
    
    try:
        import requests
        
        # Custom headers
        headers = {
            'User-Agent': 'MyApp/1.0',
            'Authorization': 'Bearer fake-token-123',
            'Content-Type': 'application/json'
        }
        
        response = requests.get('https://httpbin.org/headers', headers=headers)
        received_headers = response.json()['headers']
        
        print("Sent custom headers:")
        for key, value in headers.items():
            print(f"  {key}: {value}")
        
        print(f"Server received Authorization: {received_headers.get('Authorization', 'Not found')}")
        
    except ImportError:
        print("Headers example:")
        print("  User-Agent: MyApp/1.0")
        print("  Authorization: Bearer fake-token-123")
        print("  Content-Type: application/json")
    
    print()

def demonstrate_session_usage():
    """Show session usage for persistent connections"""
    print("=== Session Usage ===")
    
    try:
        import requests
        
        # Using session for multiple requests
        with requests.Session() as session:
            # Set default headers for all requests in this session
            session.headers.update({'User-Agent': 'MyApp-Session/1.0'})
            
            # Multiple requests using the same session
            for i in range(3):
                response = session.get(f'https://httpbin.org/get?request={i}')
                data = response.json()
                print(f"Request {i}: {data['args']}")
        
        print("Session completed - connection reused for efficiency")
        
    except ImportError:
        print("Session example (simulated):")
        print("Request 0: {'request': '0'}")
        print("Request 1: {'request': '1'}")
        print("Request 2: {'request': '2'}")
        print("Session completed - connection reused for efficiency")
    
    print()

class APIClient:
    """Example API client class"""
    
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        
        try:
            import requests
            self.session = requests.Session()
            if api_key:
                self.session.headers.update({'Authorization': f'Bearer {api_key}'})
        except ImportError:
            self.session = None
    
    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make GET request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        if self.session:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        else:
            # Simulated response
            return {
                'status': 'simulated',
                'url': url,
                'params': params or {}
            }
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        if self.session:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        else:
            # Simulated response
            return {
                'status': 'simulated',
                'url': url,
                'data_received': data
            }

def demonstrate_api_client():
    """Show usage of API client class"""
    print("=== API Client Class ===")
    
    client = APIClient('https://httpbin.org', 'fake-api-key-123')
    
    try:
        # GET request
        get_result = client.get('/get', {'param1': 'value1'})
        print(f"GET result keys: {list(get_result.keys())}")
        
        # POST request
        post_data = {'name': 'Test User', 'email': 'test@example.com'}
        post_result = client.post('/post', post_data)
        print(f"POST result keys: {list(post_result.keys())}")
        
    except Exception as e:
        print(f"API client demo (may be simulated): {e}")
    
    print()

if __name__ == '__main__':
    print("🌐 REQUESTS EXAMPLES 🌐")
    print("=" * 50)
    
    demonstrate_basic_requests()
    demonstrate_json_handling()
    demonstrate_error_handling()
    demonstrate_headers_auth()
    demonstrate_session_usage()
    demonstrate_api_client()
    
    print("✅ HTTP requests examples completed!")