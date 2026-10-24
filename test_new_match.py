import requests
import json
import re

# الرابط الجديد للمباراة المطلوبة
url = "https://yassirtv.com/hard/2908c7d4425d87350.html?match=4789443"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

print("جاري الاتصال بالرابط الجديد وجلب محتوى المباراة...")
response = requests.get(url, headers=headers)
print(f"رمز الاستجابة من الموقع: {response.status_code}")

if response.status_code == 200:
    html_content = response.text
    
    # استخراج معرف المباراة (match id) تلقائياً من الرابط
    match_id_search = re.search(r'match=(\d+)', url)
    match_id = match_id_search.group(1) if match_id_search else "unknown"
    
    # بناء رابط المشغل الكامل تلقائياً للمباراة الجديدة
    player_url = f"https://912acsss8af382.sirtv.top/playerv5.php?match={match_id}&key=9f39972b67d6ce22189507d008acwc26"
    
    # حفظ البيانات في ملف matches_db.txt
    database_list = [{
        "url": url,
        "match_id": match_id,
        "player_url": player_url,
        "content": html_content
    }]
    
    with open("matches_db.txt", "w", encoding="utf-8") as f:
        json.dump(database_list, f, ensure_ascii=False, indent=4)
        
    print(f"✅ تم جلب وحفظ صفحة المباراة رقم {match_id} بنجاح داخل matches_db.txt!")
    print(f"🔗 رابط المشغل المتولد للمباراة الجديدة:")
    print(f"   {player_url}")
else:
    print("❌ فشل الاتصال بالصفحة الجديدة.")