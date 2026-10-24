import json
import re

def get_full_player_link():
    # قراءة الملف النصي المحلي
    with open("matches_db.txt", "r", encoding="utf-8") as f:
        database = json.load(f)
        
    for item in database:
        url = item["url"]
        
        # استخراج معرف المباراة (match id) من الرابط الأصلي
        match_id_search = re.search(r'match=(\d+)', url)
        if match_id_search:
            match_id = match_id_search.group(1)
            
            # بناء رابط المشغل الكامل والمباشر مع المفتاح الثابت المستخرج من كود الصفحة
            player_url = f"https://912acsss8af382.sirtv.top/playerv5.php?match={match_id}&key=9f39972b67d6ce22189507d008acwc26"
            
            print(f"📄 الرابط الأساسي: {url}")
            print(f"✅ رابط المشغل الكامل والمباشر:")
            print(f"   🔗 {player_url}")

if __name__ == "__main__":
    get_full_player_link()