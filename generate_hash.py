import streamlit_authenticator as stauth

# Replace with your actual password
passwords = ['@Password']

# Generate hash
hashed_passwords = stauth.Hasher(passwords).generate()

# Output
for i, hashed in enumerate(hashed_passwords):
    print(f"Hashed password {i+1}: {hashed}")