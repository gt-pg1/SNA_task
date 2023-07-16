import requests
import json


def get_clearbit_data(email):
    clearbit_url = f"https://person.clearbit.com/v2/combined/find?email={email}"

    headers = {
        "Authorization": "Bearer sk_57801cd88f9954534e76d0f626040d00"
    }

    try:
        response = requests.get(clearbit_url, headers=headers)
        if response.status_code == 200:
            user_data = json.loads(response.text)
            print(f"Full Name: {user_data['person']['name']['fullName']}")
            print(f"Email: {user_data['person']['email']}")
            print(f"Location: {user_data['person']['location']}")
            print(f"Timezone: {user_data['person']['timeZone']}")
            print(f"Employment: {user_data['person']['employment']}")
            print(f"Facebook Handle: {user_data['person']['facebook']['handle']}")
            print(f"GitHub: {user_data['person']['github']['handle']}")
            print(f"LinkedIn: {user_data['person']['linkedin']['handle']}")
            print(f"Avatar URL: {user_data['person']['avatar']}")
            print(f"Company Name: {user_data['company']['name']}")
            print(f"Company Domain: {user_data['company']['domain']}")
            print(f"Company Founded Year: {user_data['company']['foundedYear']}")
            print(f"Company Description: {user_data['company']['description']}")
            print(f"Company Location: {user_data['company']['location']}")
            print(f"Company TimeZone: {user_data['company']['timeZone']}")
            print(f"Company Logo URL: {user_data['company']['logo']}")
            print(f"Company Facebook: {user_data['company']['facebook']['handle']}")
            print(f"Company LinkedIn: {user_data['company']['linkedin']['handle']}")
            print(f"Company Twitter: {user_data['company']['twitter']['handle']}")
            print(f"Company Employees: {user_data['company']['metrics']['employees']}")
            print(f"Company Annual Revenue: {user_data['company']['metrics']['estimatedAnnualRevenue']}")
        else:
            print(f"An error occurred while trying to fetch user data from Clearbit: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to fetch user data from Clearbit: {e}")
