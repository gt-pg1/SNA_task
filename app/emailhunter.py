import requests


def verify_email_with_emailhunter(email):
    """
    Verifies the given email using Email Hunter API.

    Args:
        email (str): The email address to be verified.

    Returns:
        str: The status of the email verification.
    """
    api_key = "e445fe59c7bb96c31bed8244ee83a4366e5d6660"
    response = requests.get(
        f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
    )
    data = response.json()
    return data['data']['status']
