import streamlit as st
import secrets
import string
import json

# Common weak passwords list (can be expanded)
WEAK_PASSWORDS = {"password", "123456", "qwerty", "letmein", "12345678", "abcdef"}

def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True, avoid_ambiguous=True):
    characters = string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    
    if avoid_ambiguous:
        characters = characters.translate(str.maketrans('', '', '0O1lI|'))
    
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def check_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1
    
    if password in WEAK_PASSWORDS:
        return "Weak (Common Password)"
    
    strength_levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    return strength_levels[min(score, len(strength_levels) - 1)]

def save_password(password):
    with open("passwords.json", "a") as file:
        json.dump({"password": password}, file)
        file.write("\n")

def main():
    st.title("🔐 Password Generator")
    
    length = st.slider("Password Length", min_value=8, max_value=32, value=12)
    upper = st.checkbox("Include Uppercase Letters", value=True)
    digits = st.checkbox("Include Numbers", value=True)
    symbols = st.checkbox("Include Symbols", value=True)
    ambiguous = st.checkbox("Avoid Ambiguous Characters", value=True)
    
    if st.button("Generate Password"):
        password = generate_password(length, upper, digits, symbols, ambiguous)
        strength = check_strength(password)
        
        st.text_input("Generated Password", password, disabled=True)
        st.write(f"**Password Strength:** {strength}")
        
        if st.button("Save Password"):
            save_password(password)
            st.success("Password saved successfully!")

if __name__ == "__main__":
    main()
    