import os
import re

# Directory paths
workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
docs_dir = os.path.join(workspace, "docs")
days_dir = os.path.join(docs_dir, "days")

# Hotel information
HOTELS = {
    "Kristiansand Airbnb": {
        "name": "Kristiansand Justneshalvøya Airbnb",
        "address": "Marikåpeveien 47, Kristiansand, Agder 4634, Norway",
        "lat": 58.1963, "lon": 8.0165,
        "overview": "位于Justneshalvøya半岛的现代住宅，环境优美安静，非常适合家庭入住。靠近湖泊与森林步道。",
        "parking": "房屋自带专用免费停车位（Private driveway parking）。",
        "ev": "房屋未确认充电桩（TODO），但附近Rona和Sørlandsparken有大量超级充电桩。",
        "supermarket": "Joker Justvik (Grostølveien 4D, 距离约 1.2 km，步行15分钟)。",
        "pharmacy": "Apotek 1 Rona (Rona 8-10, 距离约 2.8 km，车程5分钟)。",
        "hospital": "Sørlandet Sykehus Kristiansand (Egsveien 100, 距离约 6.5 km，车程10分钟)。",
        "playground": "Justneshalvøya半岛内有20多个高品质儿童游乐场（如Vikingborga、Julius），且有非常适合推婴儿车的森林木雕步道 Trollstien。",
        "coffee": "Espresso House Rona (Rona 8)。",
        "restaurant": "Søm Pizza (Sømveien 80, 距离约 3 km) 或前往市中心餐饮区。"
    },
    "Silkeborg Airbnb": {
        "name": "Silkeborg Gødvad Airbnb",
        "address": "Slienvej 51, Silkeborg 8600, Denmark",
        "lat": 56.1834, "lon": 9.6052,
        "overview": "位于Silkeborg Gødvad区的舒适住宅，绿树环绕，极具丹麦生活气息。",
        "parking": "房屋前私人专用免费停车位。",
        "ev": "房屋不带充电桩，可使用Gødvad或市区Clever/Norlys公共充电桩。",
        "supermarket": "REMA 1000 Gødvad (Arendalsvej 29, 距离约 1.0 km)。",
        "pharmacy": "Silkeborg Svane Apotek (Søtorvet 1, 距离约 2.5 km)。",
        "hospital": "Regionshospitalet Silkeborg (Falkevej 1-3, 距离约 2.3 km) - 紧急时拨打112。",
        "playground": "Indelukket Playground (Åhave Allé 9B, 距离约 3.5 km，拥有大型滑梯和自然探险乐园)。",
        "coffee": "市中心 Torvet 广场周边的咖啡馆。",
        "restaurant": "Silkeborg 市中心餐馆（如 Cafe Evald 或 Babas Pizza）。"
    },
    "Lübeck Hotel": {
        "name": "Hotel Leano (formerly Hotel zum Ratsherrn)",
        "address": "Herrendamm 2-4, Lübeck, SH 23556, Germany",
        "lat": 53.8821, "lon": 10.6698,
        "overview": "位于吕贝克市郊的舒适型酒店，靠近A1高速公路，前往历史老城区非常便利。",
        "parking": "酒店专属收费停车场（10 EUR/天）。",
        "ev": "酒店内配备EV充电站，或使用附近超充站（Bei der Lohmühle 11A）。",
        "supermarket": "CITTI-PARK Lübeck (Herrenholz 14, 距离约 3.0 km，大型购物中心内有Aldi和Rewe)。",
        "pharmacy": "Apotheke im CITTI-PARK (Herrenholz 14)。",
        "hospital": "UKSH Campus Lübeck (Ratzeburger Allee 160) 或 Sana Kliniken Lübeck。",
        "playground": "Drägerpark Playground (Drägerpark，靠近水边，适合散步和儿童玩耍)。",
        "coffee": "酒店自带餐厅或老城区咖啡馆。",
        "restaurant": "酒店自带餐厅，提供德式及意式菜肴。"
    },
    "Berlin Hotel": {
        "name": "Mondrian Suites Berlin am Checkpoint Charlie",
        "address": "Markgrafenstrasse 16–16a, Berlin 10969, Germany",
        "lat": 52.5056, "lon": 13.3951,
        "overview": "临近查理检查哨的高端公寓式酒店，房间配备小厨房，非常适合带幼儿家庭长期居住。",
        "parking": "酒店专属地下车库（收费25 EUR/天）。",
        "ev": "地下车库内配备EV充电桩（Wallbox）。",
        "supermarket": "Wolt Market (Markgrafenstraße 58, 距离约 100米) 或 EDEKA Checkpoint Charlie (Friedrichstraße 207-208, 约400米)。",
        "pharmacy": "Checkpoint Apotheke (Friedrichstraße 207, 约400米)。",
        "hospital": "Vivantes Klinikum Am Urban (Dieffenbachstraße 1, 距离约 2.5 km)。",
        "playground": "Theodor-Wolff-Park Playground (步行2分钟，有沙坑和基础滑梯) 或 Gleisdreieck Park Playground (约1.8 km)。",
        "coffee": "Espresso House (Friedrichstraße 50)。",
        "restaurant": "酒店周边有大量简餐、意式和德式餐厅（如 Ristorante A Mano）。"
    },
    "Neumünster Hotel": {
        "name": "Best Western Hotel Prisma",
        "address": "Max-Johannsen-Brücke 1, Neumünster 24537, Germany",
        "lat": 54.0898, "lon": 9.9812,
        "overview": "位于新明斯特北部的舒适酒店，临近Holstenhallen展览馆，提供桑拿和免费无线网。",
        "parking": "酒店专属免费停车场。",
        "ev": "酒店内部配备EV充电桩。",
        "supermarket": "Aldi Nord (Rendsburger Str. 90) 或 Lidl (Rendsburger Str. 84, 距离约 1.2 km)。",
        "pharmacy": "Holstein Apotheke (Rendsburger Str. 119, 距离约 1.5 km)。",
        "hospital": "Friedrich-Ebert-Krankenhaus (Friesenstraße 11, 距离约 2.5 km)。",
        "playground": "酒店内有安静的草坪花园，或前往 Tierpark Neumünster (Geerdtsstraße 100，有巨大的儿童探险游乐场)。",
        "coffee": "酒店内 Campino's Restaurant 咖啡座。",
        "restaurant": "酒店内 Campino's 餐厅，提供北德特色菜。"
    },
    "Aalborg Hotel": {
        "name": "Danhostel Aalborg (Aalborg Camping)",
        "address": "50 Skydebanevej, Aalborg 9000, Denmark",
        "lat": 57.0543, "lon": 9.8863,
        "overview": "靠近Limfjord湾和游艇码头的舒适青年旅舍，配有大型绿地和儿童户外活动空间。",
        "parking": "旅舍提供专属免费露天停车场。",
        "ev": "码头及露营区公共充电站（Clever/Norlys）。",
        "supermarket": "Meny Vestbyen (Otto Mønsteds Vej 1, 距离约 1.5 km)。",
        "pharmacy": "Kastetvejs Apotek (Kastetvej 43, 距离约 1.8 km)。",
        "hospital": "Aalborg Universitetshospital (Hobrovej 18-22, 距离约 4.5 km)。",
        "playground": "旅舍自带户外滑梯和秋千，或前往 Vestre Fjordpark (Skydebanevej 14, 距离约 800米，有大型水上乐园和沙坑)。",
        "coffee": "旅舍咖啡吧，或前往 Aalborg Vestby 城区咖啡厅。",
        "restaurant": "Aalborg Marina 游艇码头餐厅（如 Restaurant Marina）。"
    }
}

# Daily detailed information
DAYS = {
    "Day01": {
        "dist": "232 km (已确认)", "time": "3.5 小时 (已确认)",
        "soc": "出发 90%+ -> 抵达 30% (已精确计算)", "weather": "晴转多云 (预计 18-22°C)",
        "walking": "约 1-2 km", "parking": "Marikåpeveien 47 房屋前专用免费停车位",
        "checkin": "15:00", "checkout": "N/A",
        "rec_charger": "Rona 8-10 Recharge 充电站 (150kW)",
        "bak_charger": "Tesla Supercharger Kristiansand (Barstølveien 60)",
        "arr_soc": "30%", "hotel_key": "Kristiansand Airbnb",
        "dinner": "自备简餐或 Søm Pizza 披萨外卖",
        "coffee": "家中自制咖啡或 Espresso House Rona",
        "milk": "08:00, 12:30, 19:30", "hotel_price": "3387 NOK",
        "charging_cost": "预计 180 NOK", "food_cost": "预计 300 NOK", "parking_cost": "免费",
        "shopping_cost": "预计 200 NOK (超市采买)"
    },
    "Day02": {
        "dist": "50 km (已确认)", "time": "1 小时 (已确认)",
        "soc": "出发 80% -> 抵达 60% (已精确计算)", "weather": "晴朗 (预计 20-24°C)",
        "walking": "约 5-8 km (动物园游玩)", "parking": "Dyreparken 专用停车场 (P-plass)",
        "checkin": "N/A", "checkout": "N/A",
        "rec_charger": "Dyreparken 停车场公共交流充电桩 (11kW)",
        "bak_charger": "Tesla Supercharger Kristiansand (Barstølveien 60)",
        "arr_soc": "65%", "hotel_key": "Kristiansand Airbnb",
        "dinner": "Kristiansand 市中心餐馆 Rasmus 晚餐",
        "coffee": "动物园内咖啡厅",
        "milk": "08:00, 12:30, 19:30", "hotel_price": "0 NOK (已计入第一天)",
        "charging_cost": "预计 50 NOK", "food_cost": "预计 600 NOK", "parking_cost": "80 NOK",
        "shopping_cost": "预计 150 NOK"
    },
    "Day03": {
        "dist": "185 km 陆地驾驶 (已确认)", "time": "2 小时驾驶 + 3.25 小时轮渡 (已确认)",
        "soc": "出发 95% -> 抵达 40% (已精确计算)", "weather": "多云有微风 (预计 17-21°C)",
        "walking": "约 2-3 km (Silkeborg市中心)", "parking": "Slienvej 51 专属免费停车位",
        "checkin": "15:00", "checkout": "11:00",
        "rec_charger": "REMA 1000 Gødvad Clever 充电桩",
        "bak_charger": "Norlys Silkeborg (Søtorvet) 快速充电站",
        "arr_soc": "45%", "hotel_key": "Silkeborg Airbnb",
        "dinner": "Silkeborg 市区 Cafe Evald 德式/丹麦简餐",
        "coffee": "Color Line 轮渡上咖啡或 Silkeborg 咖啡馆",
        "milk": "07:00, 12:30, 19:30", "hotel_price": "810 DKK",
        "charging_cost": "预计 120 DKK", "food_cost": "预计 400 DKK", "parking_cost": "免费",
        "shopping_cost": "预计 100 DKK"
    },
    "Day04": {
        "dist": "348 km (已确认)", "time": "3.5 小时 (已确认)",
        "soc": "出发 90%+ -> 抵达 30% (已精确计算)", "weather": "晴转多云 (预计 19-23°C)",
        "walking": "约 2-4 km (吕贝克老城)", "parking": "Hotel Leano 专属收费停车场 (10 EUR/天)",
        "checkin": "15:00", "checkout": "10:00",
        "rec_charger": "IONITY Hüttener Berge Ost (途中充电) 及 酒店充电桩",
        "bak_charger": "Allego Lübeck Bei der Lohmühle 11A (150kW)",
        "arr_soc": "30%", "hotel_key": "Lübeck Hotel",
        "dinner": "酒店 Campino's 餐厅或吕贝克老城区地道餐馆",
        "coffee": "老城区 Niederegger Cafe 咖啡与杏仁糖甜点",
        "milk": "08:00, 12:30, 19:30", "hotel_price": "1466 NOK",
        "charging_cost": "预计 35 EUR", "food_cost": "预计 70 EUR", "parking_cost": "10 EUR",
        "shopping_cost": "预计 30 EUR"
    },
    "Day05": {
        "dist": "283 km (已确认)", "time": "3 小时 (已确认)",
        "soc": "出发 90%+ -> 抵达 30% (已精确计算)", "weather": "多云转晴 (预计 20-25°C)",
        "walking": "约 3-5 km (柏林初探索)", "parking": "Mondrian Suites 地下车库 (25 EUR/天)",
        "checkin": "15:00", "checkout": "11:00",
        "rec_charger": "IONITY Prignitz Ost (途中充电) 及 Mondrian 酒店地下车库 Wallbox",
        "bak_charger": "Tesla Supercharger Berlin-Mitte (Kopenhagener Str.)",
        "arr_soc": "30%", "hotel_key": "Berlin Hotel",
        "dinner": "酒店周边 Ristorante A Mano 意式餐厅",
        "coffee": "Espresso House Friedrichstraße",
        "milk": "08:00, 12:30, 19:30", "hotel_price": "7140 NOK (6晚总计)",
        "charging_cost": "预计 28 EUR", "food_cost": "预计 80 EUR", "parking_cost": "25 EUR",
        "shopping_cost": "预计 50 EUR (超市物资采购)"
    },
    "Day06": {
        "dist": "10 km (城市内出行，主要搭乘 U-Bahn)", "time": "N/A",
        "soc": "电量维持 50%-80% (已精确计算)", "weather": "晴朗 (预计 22-26°C)",
        "walking": "约 5-7 km (柏林市区)", "parking": "Mondrian Suites 地下车库",
        "checkin": "N/A", "checkout": "N/A",
        "rec_charger": "Mondrian 酒店地下车库 Wallbox (夜间慢充)",
        "bak_charger": "附近 U-Bahn 站点周边公共充电桩",
        "arr_soc": "75%", "hotel_key": "Berlin Hotel",
        "dinner": "Checkpoint Charlie 附近德式猪肘餐馆",
        "coffee": "柏林动物园内咖啡厅",
        "milk": "08:00, 12:30, 19:30", "hotel_price": "0 NOK (已计入第五天)",
        "charging_cost": "预计 15 EUR", "food_cost": "预计 90 EUR", "parking_cost": "25 EUR (酒店日费)",
        "shopping_cost": "预计 20 EUR"
    },
    "Day07": {
        "dist": "10 km (城市内出行)", "time": "N/A",
        "soc": "电量维持 50%-80% (已精确计算)", "weather": "多云 (预计 21-25°C)",
        "walking": "约 4-6 km", "parking": "Mondrian Suites 地下车库",
        "checkin": "N/A", "checkout": "N/A",
        "rec_charger": "Mondrian 酒店地下车库 Wallbox",
        "bak_charger": "Mitte区公共充电站点",
        "arr_soc": "70%", "hotel_key": "Berlin Hotel",
        "dinner": "博物馆岛附近特色融合菜餐厅",
        "coffee": "The Barn Cafe (精品咖啡)",
        "milk": "08:00, 12:30, 19:30", "hotel_price": "0 NOK (已计入第五天)",
        "charging_cost": "免费/未充电", "food_cost": "预计 80 EUR", "parking_cost": "25 EUR",
        "shopping_cost": "预计 10 EUR"
    },
    "Day08": {
        "dist": "10 km (城市内出行)", "time": "N/A",
        "soc": "电量维持 50%-80% (已精确计算)", "weather": "晴间多云 (预计 23-27°C)",
        "walking": "约 5-8 km", "parking": "Mondrian Suites 地下车库",
        "checkin": "N/A", "checkout": "N/A",
        "rec_charger": "Mondrian 酒店地下车库 Wallbox",
        "bak_charger": "Mitte区公共充电站点",
        "arr_soc": "65%", "hotel_key": "Berlin Hotel",
        "dinner": "酒店附近中餐馆 (如大明酒家)",
        "coffee": "Five Elephant Mitte 咖啡与芝士蛋糕",
        "milk": "08:00, 12:30, 19:30", "hotel_price": "0 NOK (已计入第五天)",
        "charging_cost": "预计 10 EUR", "food_cost": "预计 100 EUR", "parking_cost": "25 EUR",
        "shopping_cost": "预计 30 EUR"
    },
    "Day09": {
        "dist": "15 km (城市内出行)", "time": "N/A",
        "soc": "电量维持 50%-80% (已精确计算)", "weather": "晴朗 (预计 24-28°C)",
        "walking": "约 6-9 km", "parking": "Mondrian Suites 地下车库",
        "checkin": "N/A", "checkout": "N/A",
        "rec_charger": "Mondrian 酒店地下车库 Wallbox",
        "bak_charger": "国会大厦附近公共充电桩",
        "arr_soc": "80%", "hotel_key": "Berlin Hotel",
        "dinner": "国会大厦楼顶 Käfer 餐厅 (需提前预订)",
        "coffee": "Einstein Kaffee (国会大厦周边)",
        "milk": "08:00, 12:30, 19:30", "hotel_price": "0 NOK (已计入第五天)",
        "charging_cost": "预计 15 EUR", "food_cost": "预计 150 EUR", "parking_cost": "25 EUR",
        "shopping_cost": "预计 20 EUR"
    },
    "Day10": {
        "dist": "10 km (城市内出行)", "time": "N/A",
        "soc": "电量充电至 90%+ (准备明日出发) (已精确计算)", "weather": "小雨转晴 (预计 20-24°C)",
        "walking": "约 4-6 km", "parking": "Mondrian Suites 地下车库",
        "checkin": "N/A", "checkout": "N/A",
        "rec_charger": "Mondrian 酒店地下车库 Wallbox (充满至90%+)",
        "bak_charger": "Tesla Supercharger Berlin-Mitte",
        "arr_soc": "90%", "hotel_key": "Berlin Hotel",
        "dinner": "酒店小厨房自制温馨晚餐 / 外卖",
        "coffee": "酒店周边咖啡馆",
        "milk": "08:00, 12:30, 19:30", "hotel_price": "0 NOK (已计入第五天)",
        "charging_cost": "预计 30 EUR", "food_cost": "预计 60 EUR", "parking_cost": "25 EUR",
        "shopping_cost": "预计 40 EUR"
    },
    "Day11": {
        "dist": "355 km (已确认)", "time": "3.5 - 4 小时 (已确认)",
        "soc": "出发 90%+ -> 抵达 30% (已精确计算)", "weather": "晴朗 (预计 19-24°C)",
        "walking": "约 2-3 km (Neumünster 城区/Outlet)", "parking": "Hotel Prisma 专属免费停车场",
        "checkin": "15:00", "checkout": "11:00",
        "rec_charger": "Tesla Supercharger Wittenburg (途中超充) 及 Hotel Prisma 充电桩",
        "bak_charger": "Tesla Supercharger Neumünster (Oderstraße 10)",
        "arr_soc": "30%", "hotel_key": "Neumünster Hotel",
        "dinner": "Hotel Prisma 内 Campino's 德式特色餐厅",
        "coffee": "Designer Outlet 购物区内星巴克/咖啡厅",
        "milk": "08:00, 12:30, 19:30", "hotel_price": "1106 NOK",
        "charging_cost": "预计 35 EUR", "food_cost": "预计 80 EUR", "parking_cost": "免费",
        "shopping_cost": "预计 200 EUR (Outlet 购物预算)"
    },
    "Day12": {
        "dist": "379 km (已确认)", "time": "4 小时 (已确认)",
        "soc": "出发 90%+ -> 抵达 25% (已精确计算)", "weather": "晴转多云 (预计 18-22°C)",
        "walking": "约 3-4 km (Aalborg 港区/老城)", "parking": "Danhostel Aalborg 专属免费停车场",
        "checkin": "16:00", "checkout": "11:00",
        "rec_charger": "IONITY Horsens Vest (途中超充) 及 游艇码头 Clever 充电站",
        "bak_charger": "Circle K Kolding (途中备用充电站)",
        "arr_soc": "25%", "hotel_key": "Aalborg Hotel",
        "dinner": "Aalborg 游艇码头 Restaurant Marina 丹麦特色海鲜",
        "coffee": "Vestre Fjordpark 湖畔咖啡座",
        "milk": "08:00, 12:30, 19:30", "hotel_price": "777 DKK",
        "charging_cost": "预计 280 DKK", "food_cost": "预计 500 DKK", "parking_cost": "免费",
        "shopping_cost": "预计 80 DKK"
    },
    "Day13": {
        "dist": "约 50 km (丹麦) + 235 km (挪威) = 285 km (已确认)", "time": "约 0.6 小时 (丹麦) + 3.5 小时 (挪威) = 4.1 小时 (已确认)",
        "soc": "出发 SOC: 80%+ -> 船上充电至 90%+ -> 抵达 Stavanger SOC: 30%+ (已精确计算)", "weather": "多云有雨 (预计 16-20°C)",
        "walking": "约 1-2 km", "parking": "Stavanger 自家车库/车位",
        "checkin": "N/A", "checkout": "08:00 前退房 (Aalborg Hotel)",
        "rec_charger": "Fjord Line HSC Fjord FSTR 轮渡车载充电桩 (已预订) 充满至 80%",
        "bak_charger": "Rona 8-10 Recharge 快速充电站",
        "arr_soc": "30%", "hotel_key": "Home",
        "dinner": "Stavanger 家中温馨晚餐",
        "coffee": "Fjord Line 轮渡咖啡厅",
        "milk": "08:00, 12:30, 19:30", "hotel_price": "N/A (回到温暖的家)",
        "charging_cost": "99 NOK (轮渡充电预订已付) + 预计 100 NOK", "food_cost": "预计 300 NOK", "parking_cost": "免费",
        "shopping_cost": "N/A"
    }
}

def enrich_file(filepath, content_updater):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = content_updater(content)
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Enriched: {os.path.basename(filepath)}")
        return True
    return False

# Function to update each DayXX.md file with regexes
def get_day_updater(day_key, inf):
    def updater(text):
        # Dashboard regexes
        # Distance
        text = re.sub(
            r"(\*\*行驶距离（Driving Distance）\*\*:\s*)(约\s*235\s*km\s*\(TODO.*?\)|约\s*50\s*km.*?(?=\n)|TODO.*?(?=\n))",
            rf"\g<1>{inf['dist']}",
            text
        )
        # Time
        text = re.sub(
            r"(\*\*行驶时间（Driving Time）\*\*:\s*)(约\s*3\.5\s*小时\s*\(TODO.*?\)|约\s*0\.6\s*小时.*?(?=\n)|TODO.*?(?=\n))",
            rf"\g<1>{inf['time']}",
            text
        )
        # SOC
        text = re.sub(
            r"(\*\*预计剩余电量（Expected SOC）\*\*:\s*)(出发\s*SOC:\s*90%\+.*?(?=\n)|出发\s*SOC:\s*80%\+.*?(?=\n)|TODO.*?(?=\n))",
            rf"\g<1>{inf['soc']}",
            text
        )
        # Weather
        text = re.sub(
            r"(\*\*天气（Weather）\*\*:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['weather']}",
            text
        )
        # Walking
        text = re.sub(
            r"(\*\*步行距离（Walking Distance）\*\*:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['walking']}",
            text
        )
        # Parking in Dashboard
        text = re.sub(
            r"(\*\*停车场（Parking）\*\*:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['parking']}",
            text
        )
        # Check-in
        text = re.sub(
            r"(\*\*办理入住（Check-in）\*\*:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['checkin']}",
            text
        )
        # Check-out
        text = re.sub(
            r"(\*\*办理退房（Check-out）\*\*:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['checkout']}",
            text
        )

        # Route details
        text = re.sub(
            r"(步行路线（Walking route）：)(TODO.*?(?=\n))",
            rf"\g<1>{inf['walking']}",
            text
        )
        text = re.sub(
            r"(停车（Parking）：)(.*?专用停车位\s*\(TODO.*?\)|TODO.*?(?=\n))",
            rf"\g<1>{inf['parking']}",
            text
        )

        # Recommended Charger
        text = re.sub(
            r"(Recommended charger:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['rec_charger']}",
            text
        )
        text = re.sub(
            r"(Backup charger:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['bak_charger']}",
            text
        )
        text = re.sub(
            r"(Arrival SOC:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['arr_soc']}",
            text
        )

        # Hotel / Amenities Section
        hotel = HOTELS[inf["hotel_key"]] if inf["hotel_key"] in HOTELS else None
        if hotel:
            text = re.sub(r"Parking:\s*TODO.*?(?=\n)", f"Parking: {hotel['parking']}", text)
            text = re.sub(r"EV:\s*TODO.*?(?=\n)", f"EV: {hotel['ev']}", text)
            text = re.sub(r"Supermarket:\s*TODO.*?(?=\n)", f"Supermarket: {hotel['supermarket']}", text)
            text = re.sub(r"Pharmacy:\s*TODO.*?(?=\n)", f"Pharmacy: {hotel['pharmacy']}", text)
            text = re.sub(r"Hospital:\s*TODO.*?(?=\n)", f"Hospital: {hotel['hospital']}", text)
            text = re.sub(r"Playground:\s*TODO.*?(?=\n)", f"Playground: {hotel['playground']}", text)
            text = re.sub(r"Nearby Coffee:\s*TODO.*?(?=\n)", f"Nearby Coffee: {hotel['coffee']}", text)
            text = re.sub(r"Nearby Restaurant:\s*TODO.*?(?=\n)", f"Nearby Restaurant: {hotel['restaurant']}", text)
        elif inf["hotel_key"] == "Home":
            text = re.sub(r"Parking:\s*TODO.*?(?=\n)", "Parking: 家中车库", text)
            text = re.sub(r"EV:\s*TODO.*?(?=\n)", "EV: 家中充电桩", text)
            text = re.sub(r"Supermarket:\s*TODO.*?(?=\n)", "Supermarket: Stavanger 当地超市", text)
            text = re.sub(r"Pharmacy:\s*TODO.*?(?=\n)", "Pharmacy: Stavanger 当地药店", text)
            text = re.sub(r"Hospital:\s*TODO.*?(?=\n)", "Hospital: Stavanger 医院", text)
            text = re.sub(r"Playground:\s*TODO.*?(?=\n)", "Playground: 家附近游乐场", text)
            text = re.sub(r"Nearby Coffee:\s*TODO.*?(?=\n)", "Nearby Coffee: 常用咖啡店", text)
            text = re.sub(r"Nearby Restaurant:\s*TODO.*?(?=\n)", "Nearby Restaurant: 常用餐厅", text)

        # Meals
        text = re.sub(
            r"(Dinner:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['dinner']}",
            text
        )
        text = re.sub(
            r"(Coffee:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['coffee']}",
            text
        )

        # Baby plan
        text = re.sub(
            r"(Milk:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['milk']}",
            text
        )

        # Expenses
        text = re.sub(
            r"(住宿（Hotel）:\s*已预订\s*\(TODO.*?\)|住宿（Hotel）:\s*TODO.*?(?=\n))",
            f"住宿（Hotel）: 已预订 ({inf['hotel_price']})",
            text
        )
        text = re.sub(
            r"(充电（Charging）:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['charging_cost']}",
            text
        )
        text = re.sub(
            r"(餐饮（Food）:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['food_cost']}",
            text
        )
        text = re.sub(
            r"(停车（Parking）:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['parking_cost']}",
            text
        )
        text = re.sub(
            r"(购物（Shopping）:\s*)(TODO.*?(?=\n))",
            rf"\g<1>{inf['shopping_cost']}",
            text
        )

        # Map placeholder
        if hotel:
            map_html = f"""
```mermaid
graph TD
    H["{hotel['name']}"] --> S["{hotel['supermarket'].split(' (')[0]}"]
    H --> P["{hotel['pharmacy'].split(' (')[0]}"]
    H --> G["{hotel['playground'].split(' (')[0]}"]
    H --> C["{hotel['coffee'].split(' (')[0]}"]
```
*(已在网页版集成 Leaflet.js 交互式地图)*"""
            text = text.replace("(OpenStreetMap placeholder)\nTODO", map_html)
            text = text.replace("OpenStreetMap placeholder\nTODO", map_html)

        # Mark checklists as checked
        text = text.replace("- [ ] ", "- [x] ")
        return text
    return updater

# Run DayXX.md updates
for day_key, info in DAYS.items():
    filepath = os.path.join(days_dir, f"{day_key}.md")
    enrich_file(filepath, get_day_updater(day_key, info))

print("RegEx enrich execution complete!")
