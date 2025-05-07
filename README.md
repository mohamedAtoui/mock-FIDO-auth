# Mock FIDO2 Authentication

A simple demonstration of FIDO2-like authentication using Streamlit. This application simulates the core concepts of FIDO2 authentication in a simplified way.
'<img width="1607" alt="Screenshot 2025-05-07 at 18 43 19" src="https://github.com/user-attachments/assets/dee67490-f11b-4af8-bd37-4384dcd175fa" />

## Features

- User registration with public/private key pairs
- Email-based challenge-response authentication
- Secure signature verification
- Simple and intuitive web interface

## Requirements

- Python 3.x
- Streamlit
- Cryptography
- Yagmail (for email functionality)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirement.txt
```

## Running the Application

Start the application with:
```bash
streamlit run app.py
```


## How It Works

1. **Registration**:
   - Users provide a username and email
   - The system generates a public/private key pair
   - The public key is stored for future authentication

2. **Authentication**:
   - User enters their username
   - System generates a challenge and sends it via email
   - User signs the challenge with their private key
   - System verifies the signature using the stored public key

## Security Notes

This is a mock implementation for educational purposes. In a real FIDO2 implementation:
- Keys would be stored in a secure hardware device
- The private key would never leave the authenticator
- Additional security measures would be implemented

## Project Structure

- `app.py`: Main Streamlit application
- `crypto_utils/`: Cryptographic operations
- `services/`: User and email service implementations
- `storage/`: Data persistence layer 
