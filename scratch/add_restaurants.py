import os
import re

days_dir = r"d:\AppleICloud\iCloudDrive\2026SummerTrip\docs\days"

REST_REC = {
    "Day01": """
### 推荐餐厅 (Recommended Restaurants)
- **Local Food**:
  - **Rasmus Landspiseri** (Markens gate 8, Kristiansand): 本地高评分传统挪威餐厅，推荐鳕鱼和排骨。
  - **Bønder i Byen** (Rådhusgata 16, Kristiansand): 农场直达风格的挪威本地特色料理，环境温馨。
- **Chinese/Asian Food**:
  - **Restaurant Østen** (Markens gate 45, Kristiansand): 位于市中心步行街，主打粤式及中式融合菜，对中国胃友好。""",
    "Day02": """
### 推荐餐厅 (Recommended Restaurants)
- **Local Food**:
  - **Sjøhuset** (Østre Strandgate 12a, Kristiansand): 位于 Fiskebrygga（鱼码头）附近，提供绝佳的海边景观以及当地新鲜捕捞的海鲜（如鳕鱼、青口贝和野生虾）。
- **Chinese/Asian Food**:
  - **Le’s Kitchen** (Kristian IVs gate 15, Kristiansand): 靠近市中心的中式/亚洲菜馆，家庭式温馨氛围，提供高性价比的中式炒面和炒饭。""",
    "Day03": """
### 推荐餐厅 (Recommended Restaurants)
- **Local Food**:
  - **Cafe Evald** (Papirfabrikken 10, Silkeborg): 坐落在运河边的纸厂旧址，提供高品质的丹麦三明治（Smørrebrød）及本地简餐。
  - **Svostrup Kro** (Svostrupvej 58, Silkeborg): 运河畔极具历史感的古老丹麦客栈餐厅，主打传统丹麦经典菜肴。
- **Chinese/Asian Food**:
  - **Restaurant King Buffet** (Borgergade 12, Silkeborg): 经典的亚洲中式自助餐厅，提供寿司、热菜及蒙古铁板烧，分量充足。""",
    "Day04": """
### 推荐餐厅 (Recommended Restaurants)
- **Local Food**:
  - **Schiffergesellschaft** (Breite Str. 2, Lübeck): 吕贝克最著名的历史地标级餐厅，始于16世纪，提供正宗北德水手风味（如鲱鱼、煎鱼和北德炖肉）。
  - **Fangfrisch** (An der Untertrave 51, Lübeck): 运河旁的现代鱼类小馆，食材非常新鲜，主打各类本地煎鱼和海鲜三明治。
- **Chinese/Asian Food**:
  - **Shanghai-Restaurant** (Koberg 6, Lübeck): 开业于 1966 年，是吕贝克历史最悠久的中餐厅，口味正宗，环境雅致。""",
    "Day05": """
### 推荐餐厅 (Recommended Restaurants)
- **Local Food**:
  - **Schnitzelei Mitte** (Chausseestraße 8, Berlin Mitte): 提供高品质的德式大炸猪排（Wiener Schnitzel）以及德式传统冷盘小吃，环境现代舒适。
- **Chinese/Asian Food**:
  - **LIU Chengdu Weidao (刘成都味道)** (Kronenstraße 72, Berlin Mitte): 距离入住酒店很近，主打正宗四川担担面、红油抄手及小吃，味道惊艳。""",
    "Day06": """
### 推荐餐厅 (Recommended Restaurants)
- **Local Food**:
  - **Max und Moritz** (Oranienstraße 162, Berlin Kreuzberg): 始于 1902 年的百年老店，原汁原味的旧柏林酒馆风格，提供经典德式肉丸（Königsberger Klopse）和脆皮烤猪肘。
- **Chinese/Asian Food**:
  - **Wen Cheng Handpulled Noodles (温城大面)** (Tempelhofer Ufer 36, Berlin Kreuzberg): 柏林爆火的手拉裤带面，配以香辣泼油，非常适合带娃在 Kreuzberg 活动后前往。""",
    "Day07": """
### 推荐餐厅 (Recommended Restaurants)
- **Local Food**:
  - **Brauhaus Georgsbräu** (Spreeufer 4, Berlin Mitte): 位于历史悠久的 Nikolaiviertel（尼古拉小区），主打自酿淡啤酒以及超大份的传统巴伐利亚烤猪肘。
- **Chinese/Asian Food**:
  - **Ming Dynastie (大明酒家 - 施普雷河店)** (Brückenstraße 6, Berlin Mitte): 就在施普雷河畔，主打经典川菜和广式点心，分量足且座位宽敞，适合全家聚餐。""",
    "Day08": """
### 推荐餐厅 (Recommended Restaurants)
- **Local Food**:
  - **Trio** (Linienstraße 208, Berlin Mitte): 本地极高评分的现代德餐馆，提供精致的传统德式丸子和季节性北德菜，需要提前预订。
- **Chinese/Asian Food**:
  - **Sanku Maots’ai (三库冒菜)** (Mitte / 附近): 特色四川自选冒菜和手擀面，汤底香辣浓郁，适合自由度较高的学术休会日尝鲜。""",
    "Day09": """
### 推荐餐厅 (Recommended Restaurants)
- **Local Food**:
  - **Käfer Dachgarten-Restaurant** (Platz der Republik 1, Berlin): 位于国会大厦圆顶顶楼，提供精致的现代德餐。可以一边俯瞰柏林全景一边享用本地食材制作的美食（需提前预约及安检）。
- **Chinese/Asian Food**:
  - **Peking Ente Berlin (北京烤鸭店)** (Voßstraße 1, Berlin Mitte): 靠近勃兰登堡门和波茨坦广场，主打正宗挂炉北京烤鸭，不需提前一天预定即可享用。""",
    "Day10": """
### 推荐餐厅 (Recommended Restaurants)
- **Local Food**:
  - **Clärchens Ballhaus** (Auguststraße 24, Berlin Mitte): 拥有百年历史的跳舞大厅餐厅，庭院优美，提供经典柏林炸猪排与本地啤酒。
- **Chinese/Asian Food**:
  - **Long March Canteen (长征食堂)** (Wrangelstraße 20, Berlin Kreuzberg): 极具设计感的现代中式点心店，主打精致粤式蒸点和中式鸡尾酒，氛围高级。""",
    "Day11": """
### 推荐餐厅 (Recommended Restaurants)
- **Local Food**:
  - **Postkeller** (Großflecken 34, Neumünster): 位于市中心广场，提供正宗汉堡/北德风味肉食、新鲜啤酒和舒适的阳光露台。
- **Chinese/Asian Food**:
  - **China-Restaurant "Shanghai"** (Plöner Str. 11, Neumünster): 诺伊明斯特本地口碑极佳的中餐厅，提供铁板牛肉和香酥鸭等经典菜式。""",
    "Day12": """
### 推荐餐厅 (Recommended Restaurants)
- **Local Food**:
  - **Mortens Kro** (Mølleå 4, Aalborg): 奥尔堡极富盛名的精品北欧餐厅，主打精致的海鲜冷盘和创意丹麦料理。
  - **Restaurant Fusion** (Slotspladsen 4, Aalborg): 坐落在奥尔堡港口旁，将本地新鲜海产与日式/亚洲料理技术完美结合的融合餐厅。
- **Chinese/Asian Food**:
  - **Guangzhou Dimsum Restaurant (广州酒家)** (Danmarksgade 41, Aalborg): 提供非常地道纯正的粤式点心（烧麦、虾饺、肠粉），非常适合抚慰旅途尾声的中国胃。""",
    "Day13": """
### 推荐餐厅 (Recommended Restaurants)
- **Local/Ferry Food**:
  - **Fjord Line 船上自助餐厅**: 提供丰盛的斯堪的纳维亚海鲜自助、肉食及甜点。
  - **Stavanger Home**: 回家享用自制温馨晚餐。"""
}

for i in range(1, 14):
    day_key = f"Day{i:02d}"
    day_file = os.path.join(days_dir, f"{day_key}.md")
    if not os.path.exists(day_file):
        print(f"Skipping {day_key} (not found)")
        continue
        
    with open(day_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if restaurant recommendations already exist
    if "### 推荐餐厅" in content or "Recommended Restaurants" in content:
        # Let's strip the existing one out first
        content = re.sub(r"### 推荐餐厅 \(Recommended Restaurants\).*?(?=\n---|\n##|$)", "", content, flags=re.DOTALL)
        
    # Find ## Meals section
    pattern = r"(## Meals\s*\n.*?)(?=\n---)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        original_meals = match.group(1).strip()
        new_meals_section = original_meals + "\n" + REST_REC[day_key].strip()
        # Replace
        content = content.replace(original_meals, new_meals_section)
        
        with open(day_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully enriched {day_key} meals section!")
    else:
        print(f"Error: Could not find ## Meals section in {day_key}")
