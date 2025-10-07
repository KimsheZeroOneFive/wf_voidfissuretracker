import json
from datetime import datetime
from urllib.request import urlopen
from config import API_URL, REQUIRED_FISSURE_FIELDS

def fetch_fissures():
    try:
        with urlopen(API_URL) as response:
            fissures = json.loads(response.read().decode())
            
        validated = []
        for f in fissures:
            # Skip storm fissures
            if f.get('isStorm', False):
                continue
            
            # Validate required fields
            if not all(field in f for field in REQUIRED_FISSURE_FIELDS):
                continue
            
            try:
                # Parse expiry datetime
                expiry_str = f['expiry'].replace('Z', '+00:00')
                expiry = datetime.fromisoformat(expiry_str)
                validated.append((f, expiry, f.get('isHard', False)))
            except ValueError:
                continue
        
        return validated, None
    
    except Exception as e:
        return None, f"Network/Parse Error: {str(e)}"
