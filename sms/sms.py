import  requests
import urllib.parse

def send_sms(phone, text):
    encoded_message = urllib.parse.quote_plus(text)
    phone = str(phone)
    phone = phone.replace(" ", "")
    phone = phone.replace("-", "")
    encoded_phone = urllib.parse.quote_plus(phone)
    url = (
        f"https://smsapp.uz/new/services/send.php?"
        f"key=9c814445b0b6c20584176ba8d1c9e5fe562a9c7e"
        f"&number={encoded_phone}"
        f"&message={encoded_message}"
        f"&option=1&type=sms&useRandomDevice=1&prioritize=0"
    )

    response = requests.get(url)

    status_text = "Muvaffaqiyatli yuborildi." if response.status_code == 200 else "Xatolik mavjud!"
    print(f"Status: {status_text}\nJavob: {response.text}")
    return f"Status: {status_text}\nJavob: {response.text}"



