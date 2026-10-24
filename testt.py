import requests
import json
import os
import re

def process_match(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    print(f"جاري الاتصال بالرابط ومعالجة البيانات...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        html_content = response.text
        
        match_id_search = re.search(r'match=(\d+)', url)
        if not match_id_search:
            print("❌ لم يتم العثور على معرف المباراة في الرابط.")
            return
        
        match_id = match_id_search.group(1)
        player_url = f"https://912acsss8af382.sirtv.top/playerv5.php?match={match_id}&key=9f39972b67d6ce22189507d008acwc26"
        
        api_url = f"https://www.koora-l.live/game/{match_id}"
        print(f"جاري جلب محتوى وبيانات الـ API للمباراة {match_id}...")
        api_response = requests.get(api_url, headers=headers)
        
        api_data = {}
        if api_response.status_code == 200:
            try:
                api_data = api_response.json()
                print("✅ تم جلب محتوى وبيانات الـ API بنجاح!")
            except:
                print("⚠️ تعذر تحليل بيانات الـ API.")
        
        new_match_data = {
            "url": url,
            "match_id": match_id,
            "player_url": player_url,
            "api_data": api_data,
            "content": html_content
        }
        
        database = []
        if os.path.exists("matches_db.txt"):
            try:
                with open("matches_db.txt", "r", encoding="utf-8") as f:
                    database = json.load(f)
            except:
                database = []
                
        exists_idx = next((i for i, m in enumerate(database) if m.get("match_id") == match_id), None)
        if exists_idx is not None:
            database[exists_idx] = new_match_data
            print(f"⚠️ تم تحديث بيانات المباراة (رقم {match_id}) في قاعدة البيانات.")
        else:
            database.append(new_match_data)
            print(f"✅ تمت إضافة المباراة رقم {match_id} مع بيانات الـ API بنجاح! (الإجمالي: {len(database)} مباراة)")
            
        with open("matches_db.txt", "w", encoding="utf-8") as f:
            json.dump(database, f, ensure_ascii=False, indent=4)
            
        update_web_dashboard(database)
    else:
        print("❌ فشل الاتصال بالصفحة.")

def update_web_dashboard(matches):
    matches_html = ""
    for match in matches:
        match_id = match.get('match_id')
        player_url = match.get('player_url')
        api_data = match.get('api_data', {})
        
        # استخراج اسم الفريقين والنتيجة والتشكيلة إن وجدت في الـ API
        home_team = api_data.get('homeTeam', {}).get('name', 'الفريق الأول') if isinstance(api_data.get('homeTeam'), dict) else api_data.get('home', 'الفريق الأول')
        away_team = api_data.get('awayTeam', {}).get('name', 'الفريق الثاني') if isinstance(api_data.get('awayTeam'), dict) else api_data.get('away', 'الفريق الثاني')
        score = api_data.get('score', 'VS')
        lineup = api_data.get('lineup', 'التشكيلة غير متوفرة حالياً')
        
        matches_html += f"""
        <div class="match-card" onclick="loadPlayer('{player_url}', '{home_team} ضد {away_team}', '{score}', '{lineup}')">
            <h3>{home_team} {score} {away_team}</h3>
            <p>انقر لمشاهدة البث المباشر وتفاصيل المباراة</p>
        </div>
        """
        
    html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة بث المباريات المباشرة</title>
    <style>
        body {{
            background-color: #0a0e27;
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            background: linear-gradient(135deg, #7877c6, #ff80c0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 30px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .match-card {{
            background: linear-gradient(145deg, #1a1f3a, #0f1225);
            border: 1px solid rgba(120, 119, 198, 0.2);
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }}
        .match-card:hover {{
            border-color: #ff80c0;
            transform: translateY(-3px);
            box-shadow: 0 4px 20px rgba(255, 0, 128, 0.2);
        }}
        .match-card h3 {{
            margin: 0 0 10px 0;
            font-size: 18px;
            color: #38bdf8;
        }}
        .match-card p {{
            margin: 0;
            font-size: 13px;
            color: rgba(255, 255, 255, 0.5);
        }}
        .player-wrapper {{
            position: relative;
            width: 100%;
            padding-top: 56.25%;
            background: #000;
            border-radius: 16px;
            overflow: hidden;
            border: 2px solid rgba(120, 119, 198, 0.3);
            display: none;
        }}
        iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }}
        #active-title {{
            text-align: center;
            margin-bottom: 10px;
            color: #22c55e;
            font-weight: bold;
            font-size: 20px;
        }}
        .details-box {{
            margin-top: 20px;
            background: #111827;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #374151;
            display: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>منصة بث المباريات المباشرة</h1>
        
        <div class="grid">
            {matches_html}
        </div>

        <div id="active-title"></div>
        <div class="player-wrapper" id="playerWrapper">
            <iframe id="mainPlayer" src="" width="640" height="360" frameborder="0" allowfullscreen scrolling="no"></iframe>
        </div>

        <div class="details-box" id="detailsBox">
            <h3>تفاصيل وتشكيلة المباراة:</h3>
            <div id="lineupContent"></div>
        </div>
    </div>

    <script>
        function loadPlayer(url, title, score, lineup) {{
            const wrapper = document.getElementById('playerWrapper');
            const player = document.getElementById('mainPlayer');
            const titleElem = document.getElementById('active-title');
            const detailsBox = document.getElementById('detailsBox');
            const lineupContent = document.getElementById('lineupContent');
            
            player.src = url;
            wrapper.style.display = 'block';
            detailsBox.style.display = 'block';
            
            titleElem.innerText = title + " (" + score + ")";
            lineupContent.innerText = typeof lineup === 'object' ? JSON.stringify(lineup, null, 2) : lineup;
            
            window.scrollTo({{ top: wrapper.offsetTop - 20, behavior: 'smooth' }});
        }}
    </script>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ تم تحديث واجهة الموقع وعرض النتيجة والتشكيلة بنجاح!")

if __name__ == "__main__":
    target_url = "https://yassirtv.com/hard/2908c7d4425d87350.html?match=4789443"
    process_match(target_url)