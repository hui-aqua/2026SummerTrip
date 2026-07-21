import os
import re

# Directory paths
workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
docs_dir = os.path.join(workspace, "docs")
days_dir = os.path.join(docs_dir, "days")
manifest_path = os.path.join(workspace, "MANIFEST.yaml")

HOTELS = {
    "Kristiansand Airbnb": {
        "name": "Kristiansand Justneshalvøya Airbnb",
        "address": "Marikåpeveien 47, Kristiansand, Agder 4634, Norway",
        "parking": "房屋自带专用免费停车位（Private driveway parking）。",
        "ev": "房屋未配备或尚未确认专属充电桩，但附近 Rona 和 Sørlandsparken 有大量超级充电桩。",
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
        "address": "Markgrafenstrasse 16-16a, Berlin 10969, Germany",
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

hotel_keys = {
    "Day01": "Kristiansand Airbnb", "Day02": "Kristiansand Airbnb",
    "Day03": "Silkeborg Airbnb", "Day04": "Lübeck Hotel",
    "Day05": "Berlin Hotel", "Day06": "Berlin Hotel", "Day07": "Berlin Hotel", "Day08": "Berlin Hotel", "Day09": "Berlin Hotel", "Day10": "Berlin Hotel",
    "Day11": "Neumünster Hotel", "Day12": "Aalborg Hotel", "Day13": "Home"
}

DAYS_DATA = {
    "Day01": {
        "dist": "约 232 km",
        "time": "约 3小时30分纯驾驶；含午餐、充电和幼儿休息，建议按4.5小时预留",
        "soc": "建议 95% 出发 → 预计 25–40% 抵达",
        "walking": "约 1-2 km",
        "parking": "Marikåpeveien 47 房屋前专用免费停车位",
        "checkin": "15:00",
        "checkout": "N/A",
        "departure_soc": "95%",
        "rec_charger": "Kristiansand Rona / Sørlandsparken 区域慢速/快速补电 (如 Rona 8-10 Recharge)",
        "bak_charger": "Tesla Supercharger Kristiansand (Barstølveien 60) 或其他 CCS 快充",
        "arrival_soc": "25–40%",
        "switch_condition": "若导航预测抵达住宿低于 20%，则在途中 Lyngdal 或 Mandal 提前补电。",
        "charge_target": "途中通常充至 75–80%，避免高 SOC 阶段充电速度急剧下降。",
        "live_confirm": "出发前通过车辆导航或充电 App 确认开放状态、兼容性和占用情况。",
        "breakfast": "Stavanger 家中",
        "lunch": "途中服务区或自备便当",
        "dinner": "自备简餐或 Søm Pizza 披萨外带",
        "coffee": "途中自备或 Rona 8-10 充电站附近咖啡馆",
        "rec_first": "**Søm Pizza** (Sømveien 80, 距离住宿约3km，可外带或外送，最适合控制第一天抵达后的晚餐时间)。",
        "rec_backup": "Kristiansand 市中心家庭友好餐厅 (仅在抵达时间较早、孩子状态良好时考虑)。",
        "rec_fallback": "Airbnb 简餐 (如果旅途严重延误，直接在住宿做简易餐饮)。",
        "hotel_price": "已预订 (3387 NOK)",
        "charging_budget": "预计 180 NOK",
        "food_budget": "预计 300 NOK",
        "parking_budget": "免费",
        "shopping_budget": "预计 200 NOK",
        "custom_walking": "步行路线：从住宿散步前往 Justneshalvøya 半岛林荫道"
    },
    "Day02": {
        "dist": "约 40–50 km 本地往返",
        "time": "累计驾驶约 50–70分钟",
        "soc": "建议 80%+ 出发 → 预计 60–75% 抵达",
        "walking": "约 5-8 km (动物园游玩)",
        "parking": "Dyreparken 专用停车场 (P-plass)",
        "checkin": "N/A",
        "checkout": "N/A",
        "departure_soc": "80%+",
        "rec_charger": "Dyreparken 停车场公共交流充电桩 (11kW)",
        "bak_charger": "Sørlandsparken 区域快充 / Tesla Supercharger Kristiansand (Barstølveien 60)",
        "arrival_soc": "60–75%",
        "switch_condition": "Dyreparken 交流桩较多但较抢手，以实际空位为准；若无空位，则离园后直接前往备用快充站补电。",
        "charge_target": "离园后建议将车辆补至 90–100%，避免 Day03 清晨临时充电影响行程。",
        "live_confirm": "可通过相关充电 App 实时查看 Dyreparken 充电桩的占用情况情况。",
        "breakfast": "Airbnb 内自制",
        "lunch": "Dyreparken 园内餐馆",
        "dinner": "Kristiansand 市区家庭友好餐厅",
        "coffee": "园内咖啡厅",
        "rec_first": "**Drivhuset** (Dyreparken 园内，适合快速午餐、三明治与饮料) 或 **Gorines Vertshus** (Dyreparken 园内，提供披萨等儿童更易接受的食物)。",
        "rec_backup": "**Setra** (Dyreparken 园内，如果需要坐下来吃较完整的挪威本地餐食) / **Rasmus Landspiseri** (市中心，晚餐首选)。",
        "rec_fallback": "Airbnb 自备简餐 (游玩后若 Noora 极度疲劳，直接回住所做饭或外卖)。",
        "hotel_price": "已预订 (0 NOK，已计入第一天)",
        "charging_budget": "预计 50 NOK",
        "food_budget": "预计 600 NOK",
        "parking_budget": "80 NOK",
        "shopping_budget": "预计 150 NOK",
        "custom_walking": "步行路线：Kristiansand 动物园内部游览路线"
    },
    "Day03": {
        "dist": "约 185 km 丹麦陆地驾驶 (轮渡航程单独计算，不计入陆地距离)",
        "time": "约 2小时10分纯驾驶；含下船、午餐和幼儿休息，建议按3.5小时预留 (不含轮渡航行时间)",
        "soc": "建议 95% 出发 → 预计 45–60% 抵达",
        "walking": "约 2-3 km (Silkeborg市中心)",
        "parking": "Slienvej 51 专属免费停车位",
        "checkin": "15:00",
        "checkout": "11:00",
        "departure_soc": "95%",
        "rec_charger": "Silkeborg 住宿周边 REMA 1000 Gødvad Clever 充电桩或快充桩",
        "bak_charger": "Aalborg 或 Hobro 沿线充电区域",
        "arrival_soc": "45–60%",
        "switch_condition": "如果下船后导航预测抵达 Silkeborg 住宿低于 25%，则在途中 Aalborg 或 Hobro 提前充电 10–15 分钟。",
        "charge_target": "途中补电仅需充至能够安全抵达目的地的 SOC 即可，抵达 Silkeborg 后再慢充充满。",
        "live_confirm": "出发前通过 Clever / Norlys App 确认沿线及目的地充电桩的占用情况和可用状态。",
        "breakfast": "Airbnb 内自制",
        "lunch": "轮渡上简餐",
        "dinner": "Silkeborg 市区 Cafe Evald 德式/丹麦简餐",
        "coffee": "轮渡咖啡厅或 Silkeborg 咖啡馆",
        "rec_first": "**Cafe Evald** (Papirfabrikken 10, Silkeborg, 适合较早的晚餐，出餐快，环境对孩子友好)。",
        "rec_backup": "Silkeborg 市中心披萨店或外带餐厅。",
        "rec_fallback": "REMA 1000 Gødvad (距离住宿 1km) 采购食材，回 Airbnb 自制简餐。",
        "hotel_price": "已预订 (810 DKK)",
        "charging_budget": "预计 120 DKK",
        "food_budget": "预计 400 DKK",
        "parking_budget": "免费",
        "shopping_budget": "预计 100 DKK",
        "custom_walking": "步行路线：Ferry 离船区及 Silkeborg 湖畔散步道"
    },
    "Day04": {
        "dist": "约 348 km",
        "time": "约 3小时45分纯驾驶；含午餐、充电 and 幼儿休息，建议按5–5.5小时预留",
        "soc": "建议 90–95% 出发 → 预计 25–40% 抵达 (中途充电一次)",
        "walking": "约 2-4 km (吕贝克老城)",
        "parking": "Hotel Leano 专属收费停车场 (10 EUR/天)",
        "checkin": "15:00",
        "checkout": "10:00",
        "departure_soc": "90–95%",
        "rec_charger": "IONITY Hüttener Berge Ost 快充站 (目标充至 75–80%)",
        "bak_charger": "Flensburg/Harrislee CCS 快充站 (途中备用) 及 Lübeck Bei der Lohmühle 快充站",
        "arrival_soc": "25–40%",
        "switch_condition": "若导航预测抵达主充电站低于 12–15%，应在 Flensburg/Harrislee 提前补电。",
        "charge_target": "途中通常充至 75–80%，避免高 SOC 阶段充电速度急剧下降。",
        "live_confirm": "出发前通过 IONITY App 确认充电桩状态，并检查吕贝克 Bei der Lohmühle 桩的空闲状态。",
        "breakfast": "Airbnb 内自制",
        "lunch": "途中充电服务区",
        "dinner": "酒店餐厅或附近外带",
        "coffee": "Café Niederegger (吕贝克老城区，仅限时间宽裕时前往)",
        "rec_first": "**Café Niederegger** (Breite Str. 89, Lübeck, 如果 16:30 前顺利入住，可以去老城区品尝标志性杏仁糖蛋糕和咖啡)；若入住较晚，首选酒店内部餐厅或外带。",
        "rec_backup": "**Schiffergesellschaft** (吕贝克老城历史餐厅，适合体验古朴德式风情，需早抵达)。",
        "rec_fallback": "酒店 Prisma 内 Campino's 德式特色餐厅或外带。如果入住时间晚于 17:00，则直接取消老城区晚餐行程。",
        "hotel_price": "已预订 (1466 NOK)",
        "charging_budget": "预计 35 EUR",
        "food_budget": "预计 70 EUR",
        "parking_budget": "10 EUR",
        "shopping_budget": "预计 30 EUR",
        "custom_walking": "步行路线：吕贝克运河小径及 Holstentor（荷尔斯登门）老城游览"
    },
    "Day05": {
        "dist": "约 283 km",
        "time": "约 3小时纯驾驶；含午餐、充电和幼儿休息，建议按4小时15分预留",
        "soc": "建议 90% 出发 → 预计 25–40% 抵达",
        "walking": "约 3-5 km (柏林初探索)",
        "parking": "Mondrian Suites 地下车库 (25 EUR/天)",
        "checkin": "15:00",
        "checkout": "11:00",
        "departure_soc": "90%",
        "rec_charger": "A24 沿线 Prignitz 区域快充站 (途中充电)",
        "bak_charger": "Wittenberge 或 Neuruppin 区域 CCS 快充站",
        "arrival_soc": "25–40%",
        "switch_condition": "如果导航预测抵达柏林酒店低于 20%，必须在中途补电。",
        "charge_target": "抵达酒店后使用地下车库 Wallbox 慢充补充电量。",
        "live_confirm": "在车机导航中监控电量，并实时查看 Prignitz 快充站的使用状态。",
        "breakfast": "酒店内早餐",
        "lunch": "途中服务区",
        "dinner": "酒店周边意式/德式餐厅",
        "coffee": "Espresso House Friedrichstraße",
        "rec_first": "**Ristorante A Mano** (Mitte 意式餐厅，意面和披萨更易被幼儿接受，且出餐迅速)。",
        "rec_backup": "**LIU Chengdu Weidao (刘成都味道)** (Sichuan 担担面，为 Noora 单独安排不辣的面条/辅食)。",
        "rec_fallback": "酒店小厨房自制温馨简餐 (由于当天傍晚包含会议报到注册/欢迎活动，自制或外卖时间最灵活)。",
        "hotel_price": "已预订 (7140 NOK，6晚总计)",
        "charging_budget": "预计 28 EUR",
        "food_budget": "预计 80 EUR",
        "parking_budget": "25 EUR",
        "shopping_budget": "预计 50 EUR",
        "custom_walking": "步行路线：从 Checkpoint Charlie 步行至 Mondrian Suites 酒店"
    },
    "Day06": {
        "dist": "城市内建议不开车，以 U-Bahn、S-Bahn 和步行为主，车辆停放酒店地下车库。",
        "time": "无 (车辆静置地下车库)",
        "soc": "电量维持在 50–80% 即可",
        "walking": "约 5-7 km (柏林市区)",
        "parking": "Mondrian Suites 地下车库",
        "checkin": "N/A",
        "checkout": "N/A",
        "departure_soc": "50–80%",
        "rec_charger": "Mondrian 酒店地下车库 Wallbox (夜间慢充)",
        "bak_charger": "附近 U-Bahn 站点周边公共充电桩",
        "arrival_soc": "50-80%",
        "switch_condition": "日常出行车辆静置酒店车库，不安排任何快充。仅在 SOC 偏低时利用夜间闲暇在酒店地下车库慢充补电。",
        "charge_target": "仅在低于约 45–50% 时在酒店 Wallbox 充电，充至 80% 即可。",
        "live_confirm": "在酒店前台确认车位 Wallbox 激活方式 和 收费标准。",
        "breakfast": "酒店内",
        "lunch": "景点周边就近简餐",
        "dinner": "酒店附近特色餐厅 / 小厨房自制",
        "coffee": "柏林动物园内咖啡厅",
        "rec_first": "**Mondrian 酒店小厨房自制** / 附近高品质意面披萨店 (最符合带幼儿作息，晚餐灵活度极高)。",
        "rec_backup": "**LIU Chengdu Weidao (刘成都味道)** / **Peking Ente Berlin (北京烤鸭店)** (中餐备选)；**Max und Moritz** (德餐备选)。",
        "rec_fallback": "外卖或 Wolt Market 超市采购后在酒店房间用餐，保障 Noora 20:00 准时入睡。",
        "hotel_price": "已预订 (0 NOK，已计入第五天)",
        "charging_budget": "预计 15 EUR",
        "food_budget": "预计 90 EUR",
        "parking_budget": "25 EUR",
        "shopping_budget": "预计 20 EUR",
        "custom_walking": "步行路线：从酒店步行至地铁站，及动物园内部推车散步",
        "custom_metro": "从 Kochstraße (靠近酒店) 搭乘 U6 至 Stadtmitte，换乘 U2 直达 Zoologischer Garten (动物园)"
    },
    "Day07": {
        "dist": "城市内建议不开车，以 U-Bahn、S-Bahn 和步行为主，车辆停放酒店地下车库。",
        "time": "无 (车辆静置地下车库)",
        "soc": "电量维持在 50–80% 即可",
        "walking": "约 4-6 km",
        "parking": "Mondrian Suites 地下车库",
        "checkin": "N/A",
        "checkout": "N/A",
        "departure_soc": "50–80%",
        "rec_charger": "Mondrian 酒店地下车库 Wallbox (慢充)",
        "bak_charger": "Mitte区公共充电站点",
        "arrival_soc": "50-80%",
        "switch_condition": "日常出行车辆静置酒店车库，不安排任何快充。仅在 SOC 偏低时利用夜间闲暇在酒店地下车库慢充补电。",
        "charge_target": "在酒店 Wallbox 夜间慢充至 70–80% 即可。",
        "live_confirm": "日常无需特别确认快充桩。",
        "breakfast": "酒店内",
        "lunch": "柏林动物园内餐馆",
        "dinner": "博物馆岛附近特色融合菜餐厅",
        "coffee": "The Barn Cafe (精品咖啡)",
        "rec_first": "**Mondrian 酒店小厨房自制** / 附近高品质意面披萨店 (最符合带幼儿作息，晚餐灵活度极高)。",
        "rec_backup": "**LIU Chengdu Weidao (刘成都味道)** / **Peking Ente Berlin (北京烤鸭店)** (中餐备选)；**Max und Moritz** (德餐备选)。",
        "rec_fallback": "外卖或 Wolt Market 超市采购后在酒店房间用餐，保障 Noora 20:00 准时入睡。",
        "hotel_price": "已预订 (0 NOK，已计入第五天)",
        "charging_budget": "免费/未充电",
        "food_budget": "预计 80 EUR",
        "parking_budget": "25 EUR",
        "shopping_budget": "预计 10 EUR",
        "custom_walking": "步行路线：蒂尔加滕公园林荫道推车散步",
        "custom_metro": "搭乘 U-Bahn 往返蒂尔加滕公园与酒店"
    },
    "Day08": {
        "dist": "城市内建议不开车，以 U-Bahn、S-Bahn 和步行为主，车辆停放酒店地下车库。",
        "time": "无 (车辆静置地下车库)",
        "soc": "电量维持在 50–80% 即可",
        "walking": "约 5-8 km",
        "parking": "Mondrian Suites 地下车库",
        "checkin": "N/A",
        "checkout": "N/A",
        "departure_soc": "50–80%",
        "rec_charger": "Mondrian 酒店地下车库 Wallbox (慢充)",
        "bak_charger": "Mitte区公共充电站点",
        "arrival_soc": "50-80%",
        "switch_condition": "日常出行车辆静置酒店车库，不安排任何快充。仅在 SOC 偏低时利用夜间闲暇在酒店地下车库慢充补电。",
        "charge_target": "在酒店 Wallbox 夜间慢充至 70–80% 即可。",
        "live_confirm": "日常无需特别确认快充桩。",
        "breakfast": "酒店早餐",
        "lunch": "博物馆岛附近德餐或个人面食",
        "dinner": "大会晚宴 (ICMCF Congress Dinner)",
        "coffee": "Five Elephant Mitte 咖啡与芝士蛋糕",
        "rec_first": "**大会正式晚宴 (Congress Dinner)** (Noora 备用静音耳罩，预计在晚宴中婴儿车上入睡)。",
        "rec_backup": "**LIU Chengdu Weidao (刘成都味道)** / 附近中餐馆 (如大明酒家，仅在不参加晚宴时考虑)。",
        "rec_fallback": "外卖或 Wolt Market 超市采购后在酒店房间用餐，保障 Noora 20:00 准时入睡。",
        "hotel_price": "已预订 (0 NOK，已计入第五天)",
        "charging_budget": "预计 10 EUR",
        "food_budget": "预计 100 EUR",
        "parking_budget": "25 EUR",
        "shopping_budget": "预计 30 EUR",
        "custom_walking": "步行路线：博物馆岛历史街区推车散步",
        "custom_metro": "搭乘 U-Bahn/S-Bahn 往返博物馆岛与晚宴会场"
    },
    "Day09": {
        "dist": "城市内建议不开车，以 U-Bahn、S-Bahn 和步行为主，车辆停放酒店地下车库。",
        "time": "无 (车辆静置地下车库)",
        "soc": "电量维持在 50–80% 即可",
        "walking": "约 6-9 km",
        "parking": "Mondrian Suites 地下车库",
        "checkin": "N/A",
        "checkout": "N/A",
        "departure_soc": "50–80%",
        "rec_charger": "Mondrian 酒店地下车库 Wallbox (慢充)",
        "bak_charger": "国会大厦附近公共充电桩",
        "arrival_soc": "50-80%",
        "switch_condition": "日常出行车辆静置酒店车库，不安排任何快充。仅在 SOC 偏低时利用夜间闲暇在酒店地下车库慢充补电。",
        "charge_target": "在酒店 Wallbox 夜间慢充至 70–80% 即可。",
        "live_confirm": "日常无需特别确认快充桩。",
        "breakfast": "酒店内",
        "lunch": "勃兰登堡门周边简餐/自备便当",
        "dinner": "国会大厦楼顶 Käfer 餐厅 (需提前预订)",
        "coffee": "Einstein Kaffee (国会大厦周边)",
        "rec_first": "**Käfer Dachgarten-Restaurant** (Platz der Republik 1, Berlin, 位于国会大厦圆顶顶楼，提供精致的现代德餐，需提前预约及安检)。",
        "rec_backup": "**Peking Ente Berlin (北京烤鸭店)** (Voßstraße 1, Berlin Mitte, 靠近勃兰登堡门，主打烤鸭)。",
        "rec_fallback": "外卖或 Wolt Market 超市采购后在酒店房间用餐，保障 Noora 20:00 准时入睡。",
        "hotel_price": "已预订 (0 NOK，已计入第五天)",
        "charging_budget": "预计 15 EUR",
        "food_budget": "预计 150 EUR",
        "parking_budget": "25 EUR",
        "shopping_budget": "预计 20 EUR",
        "custom_walking": "步行路线：酒店 → 勃兰登堡门 → 国会大厦 (步行往返约 3.5 km)",
        "custom_metro": "搭乘 U-Bahn 往返国会大厦与酒店"
    },
    "Day10": {
        "dist": "城市内建议不开车，以 U-Bahn、S-Bahn 和步行为主，车辆停放酒店地下车库。",
        "time": "无 (车辆静置地下车库)",
        "soc": "建议充电至 90–95% 准备明日长途行驶",
        "walking": "约 4-6 km",
        "parking": "Mondrian Suites 地下车库",
        "checkin": "N/A",
        "checkout": "N/A",
        "departure_soc": "50–80%",
        "rec_charger": "Mondrian 酒店地下车库 Wallbox (充满至 90%~95%)",
        "bak_charger": "Tesla Supercharger Berlin-Mitte",
        "arrival_soc": "90–95%",
        "switch_condition": "如果酒店 Wallbox 慢充不可用，应提前使用 Berlin 城区快充桩或 Tesla Supercharger 将电量充至 90% 以上。",
        "charge_target": "今晚必须将电量充至 90–95%，为明日北上回程做好电量储备。",
        "live_confirm": "检查酒店充电桩运行状态，或者确认 Berlin-Mitte 超充站是否开放和空闲。",
        "breakfast": "酒店早餐",
        "lunch": "Ristorante A Mano (意式面食，非常适合孩子)",
        "dinner": "酒店小厨房自制温馨晚餐 / 附近特色餐厅",
        "coffee": "Einstein Kaffee (附近的精品咖啡馆)",
        "rec_first": "**酒店小厨房自制晚餐** (由于明天需要长途自驾，今晚最适合在房间自己做饭，同时能安心整理打包行李)。",
        "rec_backup": "酒店附近意面披萨店外带，省时省力。",
        "rec_fallback": "Wolt Market 超市熟食或零食补给，不安排任何正式预约的晚餐，全家保持充足休息。",
        "hotel_price": "已预订 (0 NOK，已计入第五天)",
        "charging_budget": "预计 30 EUR",
        "food_budget": "预计 60 EUR",
        "parking_budget": "25 EUR",
        "shopping_budget": "预计 40 EUR",
        "custom_walking": "步行路线：酒店周边或 Mall of Berlin 步行街",
        "custom_metro": "搭乘 U-Bahn 往返 Mall of Berlin 购物中心"
    },
    "Day11": {
        "dist": "约 355 km",
        "time": "约 3小时45分纯驾驶；含午餐、充电和幼儿休息，建议按5小时预留",
        "soc": "建议 90–95% 出发 → 预计抵达 Neumünster SOC: 25–40% (在 Outlet 购物充电后约 70–80%)",
        "walking": "约 2-3 km (Neumünster 城区/Outlet)",
        "parking": "Hotel Prisma 专属免费停车场",
        "checkin": "15:00",
        "checkout": "11:00",
        "departure_soc": "90–95%",
        "rec_charger": "Tesla Supercharger Wittenburg (途中超充) 及 Neumünster Designer Outlet 停车场内 Tesla 充电桩",
        "bak_charger": "Wittenburg 沿线快充站 或 Neumünster 城区快充",
        "arrival_soc": "25–40% (Outlet充电前) / 70–80% (Outlet充电后)",
        "switch_condition": "如果导航预测抵达 Neumünster Outlet 充电站低于 15%，应在途中 Wittenburg 提前补充 15 分钟。",
        "charge_target": "在 Wittenburg 途中充至 75% 左右，到达 Outlet 后利用购物时间通过 Tesla 快充补电至 80% 左右。",
        "live_confirm": "出发前确认 Wittenburg 和 Neumünster Supercharger 的枪头占用和收费情况。",
        "breakfast": "酒店自理",
        "lunch": "途中服务区",
        "dinner": "Hotel Prisma 内 Campino's 德式特色餐厅",
        "coffee": "Designer Outlet 购物区内星巴克/咖啡厅",
        "rec_first": "**Hotel Prisma 内 Campino's 餐厅** (入住后直接在酒店餐厅享用丰盛的北德特色晚餐，省去抱疲劳孩子到处找餐厅的麻烦)。",
        "rec_backup": "**Designer Outlet 内部餐饮区** (仅在购物按计划顺利进行、全家状态极佳时使用，不安排市中心正式晚餐)。",
        "rec_fallback": "酒店附近 Aldi Nord/Lidl 采购面包、生鲜及辅食回房间用晚餐。",
        "hotel_price": "已预订 (1106 NOK)",
        "charging_budget": "预计 35 EUR",
        "food_budget": "预计 80 EUR",
        "parking_budget": "免费",
        "shopping_budget": "预计 200 EUR",
        "custom_walking": "步行路线：酒店至 Designer Outlet Neumünster 往返路线"
    },
    "Day12": {
        "dist": "约 379 km",
        "time": "约 4小时纯驾驶；含午餐、充电和幼儿休息，建议按5.5小时预留",
        "soc": "建议 90–95% 出发 → 预计 25–40% 抵达",
        "walking": "约 3-4 km (Aalborg 港区/老城)",
        "parking": "Danhostel Aalborg 专属免费停车场",
        "checkin": "16:00",
        "checkout": "11:00",
        "departure_soc": "90–95%",
        "rec_charger": "IONITY Horsens Vest 快充站 (目标充至 75–80%)",
        "bak_charger": "Circle K Kolding (途中备用) / Aarhus 沿线 CCS 快充",
        "arrival_soc": "25–40%",
        "switch_condition": "如果到 Kolding 前导航预测抵达 Horsens 低于 12–15%，应在 Kolding 提前充电 15 分钟。",
        "charge_target": "途中补电以 75–80% 为宜，抵达 Aalborg 酒店后再慢充或使用码头公共充电站。",
        "live_confirm": "出发前确认 IONITY Horsens 站和 Kolding 站的可用充电桩数量。",
        "breakfast": "酒店早餐",
        "lunch": "途中充电服务区",
        "dinner": "Aalborg 游艇码头简餐或住宿周边餐厅",
        "coffee": "Vestre Fjordpark 湖畔咖啡座",
        "rec_first": "**Restaurant Marina** (Aalborg 游艇码头附近，提供优质海鲜和传统丹麦简餐，离青年旅舍极近，适合带娃步行前往)。",
        "rec_backup": "Aalborg 市中心家庭友好餐馆 (仅限抵达较早、天气良好且孩子状态极佳时选择)。",
        "rec_fallback": "Meny Vestbyen 超市 (距离旅舍 1.5km) 采购食材回旅舍厨房自制晚餐 (旅舍有完整厨房，很方便自制)。",
        "hotel_price": "已预订 (777 DKK)",
        "charging_budget": "预计 280 DKK",
        "food_budget": "预计 500 DKK",
        "parking_budget": "免费",
        "shopping_budget": "预计 80 DKK",
        "custom_walking": "步行路线：酒店周边林荫道或 Limfjord 峡湾边散步步道"
    },
    "Day13": {
        "dist": "约 50 km (丹麦) + 235 km (挪威) = 285 km",
        "time": "约 4小时10分纯驾驶 (丹麦约40分，挪威约3.5小时)；另需计算轮渡时间与上下船等待，建议按 8-9小时预留总行程",
        "soc": "建议 80–90% 从 Aalborg 出发 (下船预计 65%+) → 预计抵达 Stavanger SOC: 30%+",
        "walking": "约 1-2 km",
        "parking": "Stavanger 自家车库/车位",
        "checkin": "N/A",
        "checkout": "08:00 前退房 (Aalborg Hotel)",
        "departure_soc": "80–90%",
        "rec_charger": "Fjord Line HSC Fjord FSTR 轮渡车载充电桩 (已预订船上充电，但最终电量无法预先百分百保证)",
        "bak_charger": "Kristiansand Rona 快速充电站 或 E39 沿线 Mandal / Lyngdal 快充站",
        "arrival_soc": "30%+",
        "switch_condition": "下船时如果发现船上充电未成功或电量低于 65%，或者导航预测抵达 Stavanger 低于 15%，应在 Kristiansand 补电 15–20分钟再上路。",
        "charge_target": "安全回家电量即可，通常在路途中充至 50% 左右即足够直达 Stavanger 家中。",
        "live_confirm": "登船时主动向工作人员出示“Ladepunkt el-bil”预订凭证，确保车辆在充电区域停放。",
        "breakfast": "旅舍内自理或自备简餐",
        "lunch": "HSC Fjord FSTR 轮渡上简餐 (无需在途中安排正式餐厅停留)",
        "dinner": "Stavanger 家中温馨晚餐",
        "coffee": "Fjord Line 轮渡咖啡厅",
        "rec_first": "**Stavanger 家中温馨晚餐** (回到温暖的家，自制晚餐或外卖，最适合结束长途跋涉的旅程)。",
        "rec_backup": "途中 E39 快餐店 (如 McDonald's / Circle K，仅作紧急应急之用)。",
        "rec_fallback": "轮渡简餐与自备零食 (把晚餐推迟到回家之后，不在路上作任何不必要的停留)。",
        "hotel_price": "N/A (回到温暖的家)",
        "charging_budget": "99 NOK (轮渡充电预订已付) + 预计 100 NOK",
        "food_budget": "预计 300 NOK",
        "parking_budget": "免费",
        "shopping_budget": "N/A",
        "custom_walking": "步行路线：轮渡停靠区及返回 Stavanger 沿途路线"
    }
}

def clean_day_plan(day_key, data):
    file_path = os.path.join(days_dir, f"{day_key}.md")
    if not os.path.exists(file_path):
        print(f"Skipping: {day_key}.md (not found)")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Date extraction from title
    date_match = re.search(r"# Day \d+ \((.*?)\)", content)
    date_val = date_match.group(1) if date_match else "2026-07-22"
    
    # 2. Reconstruct Dashboard safely
    dash_m = re.search(r"## Dashboard\n(.*?)(?=\n---|\n## )", content, re.DOTALL)
    if dash_m:
        dash_block = dash_m.group(1)
        dash = {}
        for line in dash_block.strip().split("\n"):
            m = re.match(r"^-\s*\*\*(.*?)\*\*:\s*(.*)", line.strip())
            if m:
                key_name = re.split(r"[（(]", m.group(1))[0].strip()
                dash[key_name] = m.group(2).strip()
                
        # Reconstruct clean dashboard
        highlights_val = dash.get("今日亮点", "N/A").replace(" (TODO)", "").replace("(TODO)", "")
        hotel_val = dash.get("入住酒店", "TODO").replace(" (TODO)", "").replace("(TODO)", "")
        
        new_dash_block = f"""- **日期（Date）**: {date_val}
- **行驶距离（Driving Distance）**: {data['dist']}
- **行驶时间（Driving Time）**: {data['time']}
- **预计剩余电量（Expected SOC）**: {data['soc']}
- **天气（Weather）**: 出发前 48 小时更新；当天早晨再次确认
- **步行距离（Walking Distance）**: {data['walking']}
- **入住酒店（Hotel）**: {hotel_val}
- **停车场（Parking）**: {data['parking']}
- **办理入住（Check-in）**: {data['checkin']}
- **办理退房（Check-out）**: {data['checkout']}
- **今日亮点（Highlights）**: {highlights_val}
"""
        content = content.replace(dash_block, new_dash_block)
        
    # 3. Reconstruct Charging strategy
    charging_m = re.search(r"## Charging\n(.*?)(?=\n---|\n## )", content, re.DOTALL)
    if charging_m:
        charging_block = f"""
Departure SOC: {data['departure_soc']}

Recommended charger:
{data['rec_charger']}

Backup charger:
{data['bak_charger']}

Arrival SOC:
{data['arrival_soc']}

### Charging decision rule

- **切换条件**：{data['switch_condition']}
- **充电目标**：{data['charge_target']}
- **实时确认**：{data['live_confirm']}
"""
        content = content.replace(charging_m.group(1), charging_block)
        
    # 4. Reconstruct Meals
    meals_m = re.search(r"## Meals\n(.*?)(?=\n---|\n## )", content, re.DOTALL)
    if meals_m:
        meals_block = f"""
Breakfast: {data['breakfast']}
Lunch: {data['lunch']}
Dinner: {data['dinner']}
Coffee: {data['coffee']}

### 推荐餐厅 (Recommended Restaurants)

- **首选 (First Choice)**: {data['rec_first']}
- **备选 (Backup)**: {data['rec_backup']}
- **最稳方案 (Safe Fallback)**: {data['rec_fallback']}
- **执行原则**：餐厅预约不是硬性节点。如果抵达延误或 Noora 疲劳，立即改为外带、超市采购或住宿简餐。
"""
        content = content.replace(meals_m.group(1), meals_block)
        
    # 5. Reconstruct Expense
    expense_m = re.search(r"## Expense\n(.*?)(?=\n---|\n## )", content, re.DOTALL)
    if expense_m:
        expense_block = f"""- **住宿（Hotel）**: {data['hotel_price']}
- **充电（Charging）**: 预算：{data['charging_budget']}；实际：旅行中填写
- **餐饮（Food）**: 预算：{data['food_budget']}；实际：旅行中填写
- **停车（Parking）**: 预算：{data['parking_budget']}；实际：旅行中填写
- **购物（Shopping）**: 预算：{data['shopping_budget']}；实际：旅行中填写
"""
        content = content.replace(expense_m.group(1), expense_block)
        
    # 6. Reconstruct Journal (removes TODO, keeps travel input wording)
    journal_m = re.search(r"## Journal\n(.*?)(?=\n---|\n## |\Z)", content, re.DOTALL)
    if journal_m:
        journal_content = journal_m.group(1)
        journal_content = re.sub(r"(\*\*精选照片（Best Photo）\*\*:\s*)(TODO|旅行中填写.*)", r"\g<1>旅行中填写", journal_content)
        journal_content = re.sub(r"(\*\*今日回忆（Today's Memory）\*\*:\s*)(TODO|旅行中填写.*)", r"\g<1>旅行中填写", journal_content)
        journal_content = re.sub(r"(\*\*趣味瞬间（Funny Moment）\*\*:\s*)(TODO|旅行中填写.*)", r"\g<1>旅行中填写", journal_content)
        journal_content = re.sub(r"(\*\*Noora的新发现（Noora Learned）\*\*:\s*)(TODO|旅行中填写.*)", r"\g<1>旅行中填写", journal_content)
        content = content.replace(journal_m.group(1), journal_content)
        
    # 7. Route section replacements
    route_m = re.search(r"## Route\n(.*?)(?=\n---|\n## )", content, re.DOTALL)
    if route_m:
        route_block = route_m.group(1)
        new_route_block = route_block
        
        # Replace walking route
        new_route_block = re.sub(r"(步行路线（Walking route）：|步行路线：)(TODO.*|.*TODO.*)", rf"\g<1>{data['custom_walking']}", new_route_block)
        
        # Replace parking
        new_route_block = re.sub(r"(停车（Parking）：|停车：)(TODO.*|.*TODO.*)", rf"\g<1>{data['parking']}", new_route_block)
        
        # Replace metro/S-Bahn if custom_metro exists
        if "custom_metro" in data:
            new_route_block = re.sub(r"(地铁路线（Metro）：|地铁/轻轨（Metro/S-Bahn）：)(TODO.*|.*TODO.*)", rf"\g<1>{data['custom_metro']}", new_route_block)
            
        content = content.replace(route_block, new_route_block)
        
    # 8. Hotel section replacements
    hotel_key = hotel_keys.get(day_key)
    hotel = HOTELS.get(hotel_key)
    hotel_m = re.search(r"## Hotel\n(.*?)(?=\n---|\n## )", content, re.DOTALL)
    if hotel_m:
        if hotel_key == "Home":
            hotel_block = """Address: Stavanger Home
Parking: 家中车库
EV: 家中充电桩
Supermarket: Stavanger 当地超市
Pharmacy: Stavanger 当地药店
Hospital: Stavanger 医院
Playground: 家附近游乐场
Nearby Coffee: 常用咖啡店
Nearby Restaurant: 常用餐厅
"""
        elif hotel:
            hotel_block = f"""Address: {hotel['address']}
Parking: {hotel['parking']}
EV: {hotel['ev']}
Supermarket: {hotel['supermarket']}
Pharmacy: {hotel['pharmacy']}
Hospital: {hotel['hospital']}
Playground: {hotel['playground']}
Nearby Coffee: {hotel['coffee']}
Nearby Restaurant: {hotel['restaurant']}
"""
        else:
            hotel_block = ""
            
        if hotel_block:
            content = content.replace(hotel_m.group(1), hotel_block)
            
    # 9. Map block replacement
    map_block_pattern = r"\(OpenStreetMap placeholder\)\nTODO|OpenStreetMap placeholder\nTODO"
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
    else:
        map_html = f"""
```mermaid
graph TD
    A["Aalborg Hotel"] --> F["Hirtshals Ferry Port"]
    F --> K["Kristiansand Ferry Port"]
    K --> H["Stavanger Home"]
```
*(已在网页版集成 Leaflet.js 交互式地图)*"""
    content = re.sub(map_block_pattern, map_html, content)
    
    # 10. Clean up remaining (TODO) tags in general text if any
    content = content.replace(" (TODO)", "").replace("(TODO)", "")
    
    # Write updated content back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed and cleaned: {day_key}.md")

def update_manifest():
    if not os.path.exists(manifest_path):
        print("MANIFEST.yaml not found!")
        return
        
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_todo_block = """  maps: true
  routing: true
  restaurants: true
  charging: true
  weather: dynamic
  budget: true
  journal: travel_input"""
    
    if "todo:" in content:
        parts = content.split("todo:")
        header = parts[0]
        # Skip the lines that belong to todo section
        lines = parts[1].strip().split("\n")
        remaining_lines = []
        for line in lines:
            if line.startswith(" ") or line.startswith("-") or not line.strip():
                continue
            else:
                remaining_lines.append(line)
        content = header + "todo:\n" + new_todo_block + "\n" + "\n".join(remaining_lines)
        
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")
    print("MANIFEST.yaml updated successfully.")

if __name__ == "__main__":
    print("Starting roadbook todo refinement...")
    for day_key, data in DAYS_DATA.items():
        clean_day_plan(day_key, data)
    update_manifest()
    
    # Run compiler scripts
    print("\nRunning compilation scripts...")
    os.system("python scripts/compile_roadbook.py")
    os.system("python scripts/compile_consolidated_md.py")
    print("Roadbook todo refinement complete!")
