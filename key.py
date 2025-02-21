# key.py
import secrets
import string

def generate_random_key(length=32, quote_type="backtick"):
    """Generate a secure random key and format it with backticks or double quotes."""
    characters = string.ascii_letters + string.digits + string.punctuation
    random_key = ''.join(secrets.choice(characters) for _ in range(length))
    
    if quote_type == "backtick":
        return f'API_KEY=`{random_key}`'
    elif quote_type == "double":
        return f'API_KEY="{random_key}"'
    else:
        return random_key

# Example usage
print(generate_random_key(32, "backtick"))  # API_KEY=`random_generated_key`
print(generate_random_key(32, "double"))    # API_KEY="random_generated_key"
