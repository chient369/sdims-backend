import hashlib
import os
import hmac


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2 with SHA-256.
    
    Args:
        password: The password to hash
        
    Returns:
        str: The hashed password in format 'algorithm$iterations$salt$hash'
    """
    # Generate a random salt
    salt = os.urandom(32)
    
    # Number of iterations for PBKDF2
    iterations = 100000
    
    # Hash the password
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations,
        dklen=64
    )
    
    # Format: algorithm$iterations$salt$hash
    return (
        f"pbkdf2_sha256${iterations}$"
        f"{salt.hex()}$"
        f"{password_hash.hex()}"
    )


def verify_password(stored_password_hash: str, provided_password: str) -> bool:
    """
    Verify a password against a stored hash.
    
    Args:
        stored_password_hash: The stored password hash (from hash_password)
        provided_password: The password to verify
        
    Returns:
        bool: True if the password matches, False otherwise
    """
    try:
        # Parse the stored hash
        algorithm, iterations, salt, stored_hash = stored_password_hash.split('$')
        
        # Ensure the algorithm is what we expect
        if algorithm != "pbkdf2_sha256":
            return False
        
        # Convert parameters to appropriate types
        iterations = int(iterations)
        salt = bytes.fromhex(salt)
        stored_hash = bytes.fromhex(stored_hash)
        
        # Hash the provided password
        provided_hash = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt,
            iterations,
            dklen=64
        )
        
        # Compare the hashes in constant time (to prevent timing attacks)
        return hmac.compare_digest(stored_hash, provided_hash)
    except (ValueError, TypeError, AttributeError) as e:
        # If any parsing errors occur, return False
        return False 