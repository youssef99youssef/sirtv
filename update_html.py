import json
import os

def list_saved_matches():
    if not os.path.exists("matches_db.txt"):
        print("❌ لا يوجد قاعدة بيانات مخزنة حالياً.")
        return
        
    # قراءة قاعدة البيانات المحلية
    with open("matches_db.txt", "r", encoding="utf-8") as f:
        database = json.load(f)
        
    print(f"📋 قائمة المباريات المخزنة حالياً في النظام ({len(database)} مباراة):\n")
    print("=" * 60)
    
    for i, match in enumerate(database, 1):
        print(f"رقم المباراة في القائمة: {i}")
        print(f"📌 معرف المباراة (Match ID): {match.get('match_id')}")
        print(f"🔗 رابط المشغل المباشر: {match.get('player_url')}")
        print("-" * 60)

if __name__ == "__main__":
    list_saved_matches()