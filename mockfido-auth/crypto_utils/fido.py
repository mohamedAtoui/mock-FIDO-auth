from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

def generate_keypair():
    """
    Generates an RSA key pair (private and public key).
    
    Returns:
        tuple: A tuple containing (private_key, public_key) where:
            - private_key: RSAPrivateKey object
            - public_key: RSAPublicKey object derived from the private key
    
    Key specifications:
        - Public exponent: 65537 (standard for RSA)
        - Key size: 2048 bits (recommended minimum for security)
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()

def serialize_public_key(public_key):
    """
    Serializes a public key to PEM format for storage or transmission.
    
    Args:
        public_key: RSAPublicKey object to be serialized
    
    Returns:
        str: PEM-encoded public key as a string (in SubjectPublicKeyInfo format)
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

def sign_challenge(private_key, challenge: str) -> bytes:
    """
    Signs a challenge string using the private key with PSS padding.
    
    Args:
        private_key: RSAPrivateKey object for signing
        challenge: String message to be signed
    
    Returns:
        bytes: The digital signature as bytes
    
    Signing specifications:
        - Padding: PSS (Probabilistic Signature Scheme) with:
            - MGF1 mask generation function using SHA256
            - Maximum salt length for security
        - Hash algorithm: SHA256
    """
    return private_key.sign(
        challenge.encode(),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

def verify_signature(public_key, challenge: str, signature: bytes) -> bool:
    """
    Verifies a signature against a challenge using the public key.
    
    Args:
        public_key: RSAPublicKey object for verification
        challenge: Original string message that was signed
        signature: bytes signature to verify
    
    Returns:
        bool: True if signature is valid, False if invalid
    
    Verification specifications:
        - Uses same padding and hash algorithm as signing (PSS/SHA256)
        - Will return False rather than raising exception if invalid
    """
    try:
        public_key.verify(
            signature,
            challenge.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False