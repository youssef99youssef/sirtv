import requests
import json

url = "https://yassirtv.com/hard/2908c7d4425d87350.html?match=4742029"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

print("جاري الاتصال بموقع البث وحفظ المحتوى...")
response = requests.get(url, headers=headers)
print(f"رمز الاستجابة من الموقع: {response.status_code}")

if response.status_code == 200:
    html_content = response.text
    
    database_list = [{
        "url": url,
        "content": html_content
    }]
    
    with open("matches_db.txt", "w", encoding="utf-8") as f:
        json.dump(database_list, f, ensure_ascii=False, indent=4)
        
    print("✅ تم حفظ الرابط ومحتواه بنجاح داخل ملف matches_db.txt!")
else:
    print("❌ فشل الاتصال بالصفحة المستهدفة.")