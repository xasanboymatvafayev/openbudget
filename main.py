import os
import json
import requests
from datetime import datetime
from pytz import timezone

# =============================================
# Manba @UzCoderTeam & @PHPfunctiones
# =============================================

API_KEY = "8729966274:AAGdPXHgTqm5igxXIIaHQFccDbeBHKUhPRE"  # Bot Token
BASE_URL = f"https://api.telegram.org/bot{API_KEY}/"

tz = timezone("Asia/Tashkent")
now = datetime.now(tz)
time_str = now.strftime("%H:%M")
date_str = now.strftime("%d.%m.%Y")

silka = "https://openbudget.uz/boards/initiatives/initiative/53/d6f3976f-8313-49e7-8678-e4e84d85b0ab"
minimal = "10000"
administrator = "6365371142"


# =============================================
# Helper functions
# =============================================

def bot(method, steps=None):
    if steps is None:
        steps = {}
    url = BASE_URL + method
    try:
        response = requests.post(url, data=steps)
        return response.json()
    except Exception as e:
        print(f"cURL error: {e}")
        return None


def bot_file(method, files=None, steps=None):
    if steps is None:
        steps = {}
    url = BASE_URL + method
    try:
        response = requests.post(url, data=steps, files=files)
        return response.json()
    except Exception as e:
        print(f"cURL error: {e}")
        return None


def read_file(path, default=""):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return default


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def delete_file(path):
    try:
        os.remove(path)
    except:
        pass


def ensure_dirs(cid):
    os.makedirs("data", exist_ok=True)
    os.makedirs("step", exist_ok=True)
    os.makedirs(f"step/{cid}", exist_ok=True)


def send_vote_photo(cid, num, caption):
    """Send vote example photo, cache file_id after first send"""
    cache_path = f"data/vote_photo_{num}.txt"
    cached = read_file(cache_path)
    photo_path = f"vote{num}.jpg"

    if cached.strip():
        bot("sendPhoto", {
            "chat_id": cid,
            "photo": cached.strip(),
            "caption": caption,
            "parse_mode": "html"
        })
    elif os.path.exists(photo_path):
        with open(photo_path, "rb") as f:
            result = bot_file("sendPhoto",
                files={"photo": f},
                steps={"chat_id": cid, "caption": caption, "parse_mode": "html"}
            )
        if result and result.get("ok"):
            file_id = result["result"]["photo"][-1]["file_id"]
            write_file(cache_path, file_id)


# =============================================
# Keyboard definitions
# =============================================

def get_home_keyboard(is_admin):
    if is_admin:
        return json.dumps({
            "resize_keyboard": True,
            "keyboard": [
                [{"text": "🛅 Ovoz berish"}],
                [{"text": "💳 Hisobim"}, {"text": "🔄 Pul yechib olish"}],
                [{"text": "👨🏻‍💻 Boshqaruv paneli"}, {"text": "📊 Statistika"}],
            ]
        })
    else:
        return json.dumps({
            "resize_keyboard": True,
            "keyboard": [
                [{"text": "🛅 Ovoz berish"}],
                [{"text": "💳 Hisobim"}, {"text": "🔄 Pul yechib olish"}],
            ]
        })


ovoz_yes_kb = json.dumps({
    "resize_keyboard": True,
    "keyboard": [
        [{"text": "🙋‍♂️ Ovoz berdim"}],
        [{"text": "◀️ Ortga"}],
    ]
})

panel_kb = json.dumps({
    "resize_keyboard": True,
    "keyboard": [
        [{"text": "📝 Pochta tizimi"}, {"text": "📢 Kanallar boshqaruvi"}],
        [{"text": "🔐 Blok tizimi"}, {"text": "⚙ Bot sozlamalari"}],
        [{"text": "📋 Adminlar boshqaruvi"}, {"text": "🙋‍♂️ Ovoz berish narxini uzgartirish"}],
        [{"text": "◀️ Ortga"}],
    ]
})

message_manager_kb = json.dumps({
    "resize_keyboard": True,
    "keyboard": [
        [{"text": "💬 Forward xabar yuborish"}],
        [{"text": "👨🏻‍💻 Boshqaruv paneli"}],
    ]
})

channel_manager_kb = json.dumps({
    "resize_keyboard": True,
    "keyboard": [
        [{"text": "📢 Kanal qoʻshish"}, {"text": "📢 Kanalni oʻchirish"}],
        [{"text": "📋 Kanallar roʻyxati"}, {"text": "📋 Kanallar roʻyxatini oʻchirish"}],
        [{"text": "👨🏻‍💻 Boshqaruv paneli"}],
    ]
})

blok_manager_kb = json.dumps({
    "resize_keyboard": True,
    "keyboard": [
        [{"text": "✅ Blokdan olish"}, {"text": "❌ Bloklash"}],
        [{"text": "📋 Bloklanganlar roʻyxati"}, {"text": "📋 Bloklanganlar roʻyxatini oʻchirish"}],
        [{"text": "👨🏻‍💻 Boshqaruv paneli"}],
    ]
})

bot_manager_kb = json.dumps({
    "resize_keyboard": True,
    "keyboard": [
        [{"text": "✅ Botni yoqish"}, {"text": "❌ Botni o'chirish"}],
        [{"text": "👨🏻‍💻 Boshqaruv paneli"}],
    ]
})

admins_manager_kb = json.dumps({
    "resize_keyboard": True,
    "keyboard": [
        [{"text": "➕ Admin qoʻshish"}, {"text": "🛑 Adminlikdan olish"}],
        [{"text": "📋 Adminlar roʻyxati"}, {"text": "📋 Adminlar roʻyxatini oʻchirish"}],
        [{"text": "👨🏻‍💻 Boshqaruv paneli"}],
    ]
})

ortga_kb = json.dumps({
    "resize_keyboard": True,
    "keyboard": [
        [{"text": "◀️ Ortga"}],
    ]
})


# =============================================
# Main webhook handler
# =============================================

def handle_update(update):
    back = "◀️ Ortga"

    message = update.get("message")
    if not message:
        return

    text = message.get("text", "")
    cid = str(update["message"]["chat"]["id"])
    uid = str(message["from"]["id"])
    mid = message["message_id"]
    chat_id = str(message["chat"]["id"])
    name = message["chat"].get("first_name", "")
    photo = message.get("photo")

    ensure_dirs(cid)

    if not os.path.exists(f"step/{cid}/money.txt"):
        write_file(f"step/{cid}/money.txt", "0")
    if not os.path.exists("data/paynet.txt"):
        write_file("data/paynet.txt", "20000")

    step = read_file(f"step/{cid}/{cid}.txt")
    num = read_file(f"step/{cid}/1.txt")
    money = read_file(f"step/{cid}/money.txt", "0")
    blocks = read_file("data/blocks.txt")
    holat = read_file("data/bot.txt")
    kanal = read_file("data/kanal.txt")
    channel = read_file("data/channel.txt")
    paynet = read_file("data/paynet.txt", "20000")
    statistika = read_file("data/statistika.txt")
    admins = read_file("data/admins.txt")

    admin_list = [administrator, admins.strip()]
    is_admin = cid in admin_list or cid == administrator

    home = get_home_keyboard(is_admin)

    # Track statistics
    if uid not in statistika:
        write_file("data/statistika.txt", statistika + "\n" + uid)
        statistika = read_file("data/statistika.txt")

    # Block check
    if not is_admin and uid in blocks:
        bot("sendMessage", {
            "chat_id": cid,
            "text": f"<b>⚠️ Kechirasiz <a href='tg://user?id={cid}'>{name}</a>\n\n📛 Siz botdan bloklangansiz!\n\n👨🏻‍💻 Blokdan chiqish uchun bot administratoriga murojaat qiling!</b>",
            "parse_mode": "html",
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": "👨‍💻 Administrator", "url": f"tg://user?id={administrator}"}]
                ]
            })
        })
        return

    # Bot off check
    if not is_admin and holat == "off":
        bot("sendMessage", {
            "chat_id": chat_id,
            "text": "<b>🛠 Texnik xizmat davom etmoqda!\n\n▪ Bot mamuriyati ushbu bot ichida baʼzi texnik ishlarni olib bormoqda.\n▪ Shu sababdan menyu adminlar tomonidan oʻchirilgan va hozirda foydalanuvchilar uchun mavjud emas.\n▪ Barcha funksiyalar tugallangandan keyin tiklanadi.\n\n📝 Keyinroq qaytib keling va bot holatini tekshirish uchun /start tugmasini bosing!</b>",
            "parse_mode": "html",
            "reply_markup": json.dumps({"remove_keyboard": True})
        })
        return

    # Channel subscription check
    if message and channel == "true":
        ids = [i for i in kanal.split("\n") if i.strip()]
        keyboards = []
        for i, ch_id in enumerate(ids[1:], start=1):
            ch_clean = ch_id.replace("@", "")
            keyboards.append([{"text": f"{i}- kanal", "url": f"https://t.me/{ch_clean}"}])
        keyboard2 = json.dumps({"inline_keyboard": keyboards})

        if ids:
            get_status = bot("getChatMember", {"chat_id": ids[-1], "user_id": uid})
            status = get_status.get("result", {}).get("status", "") if get_status else ""
            if not is_admin and status not in ("member", "administrator", "creator"):
                bot("sendMessage", {
                    "chat_id": cid,
                    "text": f"<b>❌ Kechirasiz <a href='tg://user?id={cid}'>{name}</a> siz bizning kanallarimizga obuna boʻlmasangiz botdan foydalana olmaysiz!\n🔰 Obuna boʻlib botga qayta /start bosing!</b>",
                    "parse_mode": "html",
                    "reply_markup": keyboard2
                })
                return

    # =============================================
    # /start or back button
    # =============================================
    if text == "/start" or text == back:
        delete_file(f"step/{cid}/{cid}.txt")
        bot("sendMessage", {
            "chat_id": cid,
            "text": f"<b>👋 Salom <a href='tg://user?id={cid}'>{name}</a> botimizga xush kelibsiz!\n🔰 Quyidagi menyular orqali botdan foydalaning 👇</b>",
            "parse_mode": "html",
            "reply_markup": home
        })

    # =============================================
    # Voting — Telegram orqali ovoz berish O'CHIRILDI
    # =============================================
    if text == "🛅 Ovoz berish":
        bot("sendMessage", {
            "chat_id": cid,
            "text": f"<b>🙋‍♂️ Ovoz berish uchun havola:\n{silka}</b>",
            "parse_mode": "html",
            "reply_markup": home
        })
        bot("sendMessage", {
            "chat_id": cid,
            "text": f"<b>Aziz foydalanuvchi siz oʻz ovozingizni berish orqali botdan {paynet} so'm paynet sohibi boʼlishiz mumkin.\nUnutmang sizning ovozingiz bizning 72-maktabimiz obodonlashtirish uchun juda muhim.</b>",
            "parse_mode": "html",
            "reply_markup": home
        })
        # Namuna skrinshtolar
        send_vote_photo(cid, 1, "<b>1️⃣ SMS kodni tasdiqlash sahifasi — shu ko'rinishda skrinshot oling</b>")
        send_vote_photo(cid, 2, "<b>2️⃣ Ovoz qabul qilindi sahifasi — shu ko'rinishda skrinshot oling</b>")
        bot("sendMessage", {
            "chat_id": cid,
            "text": f"<b>⚠️ Eslatma: Ovoz berganingizdan so'ng yuqoridagi 2 xil ko'rinishdagi skrinshotni yuboring!\n\n'🙋‍♂️ Ovoz berdim' tugmasini bosib ikkala skrinshotni yuboring — admin tasdiqlasa hisobingizga {paynet} so'm pul qo'shiladi!</b>",
            "parse_mode": "html",
            "reply_markup": ovoz_yes_kb
        })

    if text == "🙋‍♂️ Ovoz berdim":
        bot("sendMessage", {
            "chat_id": cid,
            "text": f"<b>✅️ Yaxshi! Endi ovoz berganligingizni tasdiqlash uchun 2 ta skrinshotni yuboring:\n\n1️⃣ SMS kodni tasdiqlash sahifasi\n2️⃣ Ovoz qabul qilindi sahifasi\n\nAdmin tasdiqlasa hisobingizga {paynet} so'm pul tushuriladi.</b>",
            "parse_mode": "html",
            "reply_markup": ortga_kb
        })
        write_file(f"step/{cid}/{cid}.txt", "ovoz_yes")

    if photo and step == "ovoz_yes":
        bot("sendMessage", {
            "chat_id": cid,
            "text": f"<b>Rasm adminga yuborildi! Admin tasdiqlasa hisobingizga {paynet} so'm tashlanadi!</b>",
            "parse_mode": "html",
            "reply_markup": home
        })
        delete_file(f"step/{cid}/{cid}.txt")
        bot("forwardMessage", {
            "chat_id": administrator,
            "from_chat_id": cid,
            "message_id": mid
        })
        yes_data = read_file("data/yes.txt")
        if uid in yes_data:
            oo = "ushbu foydalanuvchi avval ovoz bergan"
        else:
            oo = "ushbu foydalanuvchi ovoz bermagan"
        bot("sendMessage", {
            "chat_id": administrator,
            "text": f"<b>👥 <a href='tg://user?id={cid}'>{name}</a> foydalanuvchi ovoz berganligihaqida ariza berdi!\n\nOvoz bergan bo'lsa <code>/berdi1 {cid}</code> buyrug'ini yuboring — hisobiga {paynet} so'm o'tkaziladi.\n\n♨️ {oo}\n⏰ Soat: {time_str} | 📆 Sana: {date_str}</b>",
            "parse_mode": "html",
            "reply_markup": home
        })

    if text.startswith("/berdi1 "):
        target_id = text.split(" ")[1]
        yes_data = read_file("data/yes.txt")
        write_file("data/yes.txt", yes_data + "\n" + target_id)
        target_money = read_file(f"step/{target_id}/money.txt", "0")
        new_balance = int(target_money) + int(paynet)
        write_file(f"step/{target_id}/money.txt", str(new_balance))
        bot("sendMessage", {
            "chat_id": target_id,
            "text": f"<b>✅️ Hurmatli foydalanuvchi arizangiz tasdiqlandi va hisobingizga {paynet} so'm tushurildi!\n\n⏰ Soat: {time_str} | 📆 Sana: {date_str}</b>",
            "parse_mode": "html",
            "reply_markup": home
        })
        bot("sendMessage", {
            "chat_id": administrator,
            "text": f"<b>👥 Foydalanuvchi hisobiga {paynet} so'm qo'shildi!\n⏰ Soat: {time_str} | 📆 Sana: {date_str}</b>",
            "parse_mode": "html",
            "reply_markup": home
        })

    # =============================================
    # Balance
    # =============================================
    if text == "💳 Hisobim":
        bot("sendMessage", {
            "chat_id": cid,
            "text": f"<b>💰 Hisobda {money} so'm mavjud</b>",
            "parse_mode": "html",
            "reply_markup": home
        })

    # =============================================
    # Withdrawal — karta raqami ham qabul qilinadi
    # =============================================
    if text == "🔄 Pul yechib olish":
        bot("sendMessage", {
            "chat_id": cid,
            "text": f"<b>👉 Pul yechib olish uchun telefon raqam yoki karta raqamini kiriting.\n\nTel raqam namunasi: +998931234567\nKarta namunasi: 1101122334458566\n</b>\n\nℹ️ <i>Minimal pul yechish miqdori: {minimal} so'm</i>",
            "parse_mode": "html",
            "reply_markup": ortga_kb
        })
        write_file(f"step/{cid}/{cid}.txt", "money_yech")

    if step == "money_yech":
        clean_text = text.replace(" ", "")
        is_phone = text.startswith("+998") and len(text) >= 13
        is_card = clean_text.isdigit() and len(clean_text) == 16
        if is_phone or is_card:
            bot("sendMessage", {
                "chat_id": cid,
                "text": f"<b>👉 Pul yechib olish uchun miqdorni kiriting.</b>\n\nℹ️ <i>Minimal pul yechish miqdori: {minimal} so'm</i>",
                "parse_mode": "html",
                "reply_markup": ortga_kb
            })
            write_file(f"step/{cid}/{cid}.txt", "money_yech11")
            write_file(f"step/{cid}/1.txt", text)
        else:
            bot("sendMessage", {
                "chat_id": cid,
                "text": f"<b>❌️ Noto'g'ri kiritildi! Qayta kiriting.\n\nTel raqam namunasi: +998931234567\nKarta namunasi: 1101122334458566</b>\n\nℹ️ <i>Minimal pul yechish miqdori: {minimal} so'm</i>",
                "parse_mode": "html",
                "reply_markup": ortga_kb
            })

    if step == "money_yech11":
        if text.isdigit() and int(text) >= int(minimal) and int(money) >= int(text):
            new_balance = int(money) - int(text)
            write_file(f"step/{cid}/money.txt", str(new_balance))
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>Adminga pul yechib olish uchun arizangiz yuborildi!</b>",
                "parse_mode": "html",
                "reply_markup": home
            })
            bot("sendMessage", {
                "chat_id": administrator,
                "text": f"<b>👥 <a href='tg://user?id={cid}'>{name}</a> pul yechib olish haqida ariza berdi!\n\n🔔 Pul miqdori: {text} so'm\n\n⏳️ Raqam: {num}\n\n✅️ Pul tashlab bergan bo'lsangiz <code>/pulyes {cid}</code> yuboring.\n\n⏰ Soat: {time_str} | 📆 Sana: {date_str}</b>",
                "parse_mode": "html",
                "reply_markup": home
            })
            delete_file(f"step/{cid}/{cid}.txt")
        else:
            bot("sendMessage", {
                "chat_id": cid,
                "text": f"<b>⚠️ Kechirasiz, hisob yetarli emas yoki miqdor noto'g'ri.</b>\n\nℹ️ <i>Minimal: {minimal} so'm | Hisobingizda: {money} so'm</i>",
                "parse_mode": "html",
                "reply_markup": ortga_kb
            })

    if text.startswith("/pulyes "):
        target_id = text.split(" ")[1]
        yes_data = read_file("data/yes.txt")
        write_file("data/yes.txt", yes_data + "\n" + target_id)
        bot("sendMessage", {
            "chat_id": target_id,
            "text": f"<b>✅️ Hurmatli foydalanuvchi arizangiz tasdiqlandi, raqamingizga pul tashlandi.\n\n⏰ Soat: {time_str} | 📆 Sana: {date_str}</b>",
            "parse_mode": "html",
            "reply_markup": home
        })
        bot("sendMessage", {
            "chat_id": administrator,
            "text": f"<b>👥 Foydalanuvchiga pul tashlaganingiz haqida xabar berildi.\n⏰ Soat: {time_str} | 📆 Sana: {date_str}</b>",
            "parse_mode": "html",
            "reply_markup": home
        })

    # =============================================
    # Statistics
    # =============================================
    if text == "📊 Statistika":
        count = statistika.count("\n")
        bot("sendMessage", {
            "chat_id": cid,
            "text": f"<b>👥 Bot foydalanuvchilari: {count} nafar\n⏰ Soat: {time_str} | 📆 Sana: {date_str}</b>",
            "parse_mode": "html",
            "reply_markup": ortga_kb
        })

    # =============================================
    # Admin panel
    # =============================================
    if text == "👨🏻‍💻 Boshqaruv paneli":
        if is_admin:
            delete_file(f"step/{cid}/{cid}.txt")
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>👨🏻‍💻 Boshqaruv paneliga xush kelibsiz!\n📋 Quyidagi boʻlimlardan birini tanlang!</b>",
                "parse_mode": "html",
                "reply_markup": panel_kb
            })
        else:
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>👨‍💻 Bu bo'limni faqat bot administratori ishlata oladi!</b>",
                "parse_mode": "html",
                "reply_markup": home
            })

    # =============================================
    # Mail system
    # =============================================
    if is_admin and text == "📝 Pochta tizimi":
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>📝 Pochta tizimi boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!</b>",
            "parse_mode": "html",
            "reply_markup": message_manager_kb
        })

    if text == "💬 Forward xabar yuborish":
        write_file(f"step/{cid}/{cid}.txt", "forward")
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>👥 Foydalanuvchilarga yuboriladigan xabarni forward qiling!</b>",
            "parse_mode": "html",
            "reply_markup": ortga_kb,
            "disable_web_page_preview": True
        })

    forward_result = None
    if step == "forward" and text not in ("/start", back, "👨🏻‍💻 Boshqaruv paneli"):
        delete_file(f"step/{cid}/{cid}.txt")
        users = [u for u in statistika.split("\n") if u.strip()]
        for user_id in users:
            forward_result = bot("forwardMessage", {
                "chat_id": user_id,
                "from_chat_id": cid,
                "message_id": mid
            })

    if forward_result:
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>👥 Forward xabaringiz barcha bot foydalanuvchilariga yuborildi!✅</b>",
            "parse_mode": "html",
            "reply_markup": message_manager_kb
        })

    # =============================================
    # Channel management
    # =============================================
    if is_admin and text == "📢 Kanallar boshqaruvi":
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>📢 Kanallar boshqaruvi boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!</b>",
            "parse_mode": "html",
            "reply_markup": channel_manager_kb
        })

    if is_admin and text == "📢 Kanal qoʻshish":
        write_file(f"step/{cid}/{cid}.txt", "kanal")
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>📡 Kanal qo'shish uchun kanal havolasini yuboring!\n🔰 Masalan: @UzCoderTeam</b>",
            "parse_mode": "html",
            "reply_markup": ortga_kb
        })

    if step == "kanal" and text not in ("/start", back, "👨🏻‍💻 Boshqaruv paneli"):
        if text not in kanal:
            write_file("data/kanal.txt", kanal + "\n" + text)
            write_file("data/channel.txt", "true")
            delete_file(f"step/{cid}/{cid}.txt")
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📡 Kanalingiz botga muvaffaqiyatli qo'shildi!\n🤖 Endi botni kanalingizga admin qiling!</b>",
                "parse_mode": "html",
                "reply_markup": channel_manager_kb
            })

    if is_admin and text == "📢 Kanalni oʻchirish":
        write_file(f"step/{cid}/{cid}.txt", "delete")
        soni = kanal.count("@")
        bot("sendMessage", {
            "chat_id": cid,
            "text": f"<b>📡 Kanalni oʻchirish uchun kanal havolasini yuboring!\n\n🔰 Masalan: @UzCoderTeam\n\n👇 Botga ulangan kanallar:\n{kanal}\n\n📝 Jami kanallar soni: {soni} ta</b>",
            "parse_mode": "html",
            "reply_markup": ortga_kb
        })

    if step == "delete" and text not in ("/start", back, "👨🏻‍💻 Boshqaruv paneli"):
        if text in kanal:
            new_kanal = kanal.replace("\n" + text, "")
            write_file("data/kanal.txt", new_kanal)
            delete_file(f"step/{cid}/{cid}.txt")
            bot("sendMessage", {
                "chat_id": cid,
                "text": f"<b>🔰 {text} muvaffaqiyatli oʻchirildi! ✅</b>",
                "parse_mode": "html",
                "reply_markup": channel_manager_kb
            })

    if is_admin and text == "📋 Kanallar roʻyxati":
        if not kanal.strip():
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 Botga ulangan kanallar mavjud emas!</b>",
                "parse_mode": "html",
                "reply_markup": channel_manager_kb
            })
        else:
            bot("sendMessage", {
                "chat_id": cid,
                "text": f"<b>📋 Kanallar roʻyxati:\n{kanal}</b>",
                "parse_mode": "html",
                "reply_markup": channel_manager_kb
            })

    if is_admin and text == "📋 Kanallar roʻyxatini oʻchirish":
        delete_file("data/kanal.txt")
        delete_file("data/channel.txt")
        if not kanal.strip():
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 Botga ulangan kanallar mavjud emas!</b>",
                "parse_mode": "html",
                "reply_markup": channel_manager_kb
            })
        else:
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 Kanallar roʻyxati muvaffaqiyatli oʻchirildi!</b>",
                "parse_mode": "html",
                "reply_markup": channel_manager_kb
            })

    # =============================================
    # Block system
    # =============================================
    if is_admin and text == "🔐 Blok tizimi":
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>🔐 Blok tizimi boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!</b>",
            "parse_mode": "html",
            "reply_markup": blok_manager_kb
        })

    if is_admin and text == "✅ Blokdan olish":
        write_file(f"step/{cid}/{cid}.txt", "unblock")
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>🚫 Blokdan olinadigan foydalanuvchini ID raqamini kiriting!</b>",
            "parse_mode": "html",
            "reply_markup": ortga_kb
        })

    if is_admin and step == "unblock" and text not in ("/start", back, "👨🏻‍💻 Boshqaruv paneli"):
        delete_file(f"step/{cid}/{cid}.txt")
        if text not in blocks:
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>👨🏻‍💻 Ushbu foydalanuvchi botdan bloklanmagan!</b>",
                "parse_mode": "html",
                "reply_markup": blok_manager_kb
            })
        else:
            new_blocks = blocks.replace(text, " ")
            write_file("data/blocks.txt", new_blocks)
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>🔰 Foydalanuvchi blokdan olindi! ✅</b>",
                "parse_mode": "html",
                "reply_markup": blok_manager_kb
            })
            bot("sendMessage", {
                "chat_id": text,
                "text": "<b>🎉 Siz blokdan muvaffaqiyatli olindingiz!\n\n🔄 Yana botni ishlatishingiz mumkin!\n\n🤖 Botga qayta /start bosing ✅</b>",
                "parse_mode": "html",
                "reply_markup": home
            })

    if is_admin and text == "❌ Bloklash":
        write_file(f"step/{cid}/{cid}.txt", "block")
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>🚫 Bloklanadigan foydalanuvchini ID raqamini kiriting!</b>",
            "parse_mode": "html",
            "reply_markup": ortga_kb
        })

    if is_admin and step == "block" and text not in ("/start", back, "👨🏻‍💻 Boshqaruv paneli"):
        if text not in blocks:
            write_file("data/blocks.txt", blocks + "\n" + text)
            delete_file(f"step/{cid}/{cid}.txt")
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>🔰 Foydalanuvchi bloklandi! ✅</b>",
                "parse_mode": "html",
                "reply_markup": blok_manager_kb
            })
            bot("sendMessage", {
                "chat_id": text,
                "text": "<b>🚫 Siz bizning botimizdan bloklandingiz!\n\n🔄 Endi botdan foydalana olmaysiz!\n\n👨‍💻 Blokdan chiqish uchun bot administratoriga murojaat qiling!</b>",
                "parse_mode": "html",
                "reply_markup": json.dumps({"remove_keyboard": True})
            })
        else:
            delete_file(f"step/{cid}/{cid}.txt")
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>👨🏻‍💻 Ushbu foydalanuvchi botdan allaqachon bloklangan!</b>",
                "parse_mode": "html",
                "reply_markup": blok_manager_kb
            })

    if is_admin and text == "📋 Bloklanganlar roʻyxati":
        if not blocks.strip():
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 Botdan bloklanganlar mavjud emas!</b>",
                "parse_mode": "html",
                "reply_markup": blok_manager_kb
            })
        else:
            bot("sendMessage", {
                "chat_id": cid,
                "text": f"<b>📋 Botdan bloklanganlar roʻyxati:\n{blocks}</b>",
                "parse_mode": "html",
                "reply_markup": blok_manager_kb
            })

    if is_admin and text == "📋 Bloklanganlar roʻyxatini oʻchirish":
        delete_file("data/blocks.txt")
        if not blocks.strip():
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 Botdan bloklanganlar mavjud emas!</b>",
                "parse_mode": "html",
                "reply_markup": blok_manager_kb
            })
        else:
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 Bloklanganlar roʻyxati muvaffaqiyatli oʻchirildi!</b>",
                "parse_mode": "html",
                "reply_markup": blok_manager_kb
            })

    # =============================================
    # Bot settings
    # =============================================
    if is_admin and text == "⚙ Bot sozlamalari":
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>⚙ Bot sozlamalari boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!</b>",
            "parse_mode": "html",
            "reply_markup": bot_manager_kb
        })

    if is_admin and text == "✅ Botni yoqish":
        delete_file("data/bot.txt")
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>⚠️ Bot muvaffaqiyatli yoqildi!</b>",
            "parse_mode": "html",
            "reply_markup": bot_manager_kb
        })

    if is_admin and text == "❌ Botni o'chirish":
        write_file("data/bot.txt", "off")
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>⚠️ Bot muvaffaqiyatli oʻchirildi!</b>",
            "parse_mode": "html",
            "reply_markup": bot_manager_kb
        })

    # =============================================
    # Admins management
    # =============================================
    if is_admin and text == "📋 Adminlar boshqaruvi":
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>📋 Adminlar boshqaruvi boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!</b>",
            "parse_mode": "html",
            "reply_markup": admins_manager_kb
        })

    if is_admin and text == "➕ Admin qoʻshish":
        write_file(f"step/{cid}/{cid}.txt", "setadmins")
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>👨‍💻 Administrator qoʻshish uchun foydalanuvchi ID raqamini kiriting</b>",
            "parse_mode": "html",
            "reply_markup": ortga_kb
        })

    if step == "setadmins" and text not in ("/start", back, "👨🏻‍💻 Boshqaruv paneli"):
        if text.isdigit():
            if text in statistika:
                write_file("data/admins.txt", admins + "\n" + text)
                delete_file(f"step/{cid}/{cid}.txt")
                bot("sendMessage", {
                    "chat_id": cid,
                    "text": f"<b>📝 <a href='tg://user?id={text}'>{text}</a> ID raqamli foydalanuvchi botga administrator qilib tayinlandi!</b>",
                    "parse_mode": "html",
                    "reply_markup": admins_manager_kb
                })
                bot("sendMessage", {
                    "chat_id": text,
                    "text": "<b>👨‍💻 Siz botga administrator qilib tayinlandingiz!</b>",
                    "parse_mode": "html",
                    "reply_markup": home
                })
            else:
                delete_file(f"step/{cid}/{cid}.txt")
                bot("sendMessage", {
                    "chat_id": cid,
                    "text": "<b>👨‍💻 Ushbu foydalanuvchi bazada mavjud emas!</b>",
                    "parse_mode": "html",
                    "reply_markup": admins_manager_kb
                })
        else:
            delete_file(f"step/{cid}/{cid}.txt")
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 ID raqam kiritayotganda faqat raqamlardan foydalaning!</b>",
                "parse_mode": "html",
                "reply_markup": admins_manager_kb
            })

    if is_admin and text == "🛑 Adminlikdan olish":
        if not admins.strip():
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 Botda administratorlar mavjud emas!</b>",
                "parse_mode": "html",
                "reply_markup": admins_manager_kb
            })
        else:
            write_file(f"step/{cid}/{cid}.txt", "deladmins")
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>👨‍💻 Administratorni olib tashlash uchun foydalanuvchi ID raqamini kiriting</b>",
                "parse_mode": "html",
                "reply_markup": ortga_kb
            })

    if step == "deladmins" and text not in ("/start", back, "👨🏻‍💻 Boshqaruv paneli"):
        if text.isdigit():
            if text in admins:
                delete_file(f"step/{cid}/{cid}.txt")
                new_admins = admins.replace("\n" + text, "")
                write_file("data/admins.txt", new_admins)
                bot("sendMessage", {
                    "chat_id": cid,
                    "text": f"<b>📋 <a href='tg://user?id={text}'>{text}</a> ID raqamli foydalanuvchi bot administratorligidan olib tashlandi!</b>",
                    "parse_mode": "html",
                    "reply_markup": admins_manager_kb
                })
                bot("sendMessage", {
                    "chat_id": text,
                    "text": "<b>👨‍💻 Siz bot administratorligidan olib tashlandingiz!</b>",
                    "parse_mode": "html",
                    "reply_markup": home
                })
            else:
                bot("sendMessage", {
                    "chat_id": cid,
                    "text": f"<b>📋 <a href='tg://user?id={text}'>{text}</a> ID raqamli foydalanuvchi botda administrator emas!</b>",
                    "parse_mode": "html",
                    "reply_markup": admins_manager_kb
                })
        else:
            delete_file(f"step/{cid}/{cid}.txt")
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 ID raqam kiritayotganda faqat raqamlardan foydalaning!</b>",
                "parse_mode": "html",
                "reply_markup": admins_manager_kb
            })

    if is_admin and text == "📋 Adminlar roʻyxati":
        if not admins.strip():
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 Botda administratorlar mavjud emas!</b>",
                "parse_mode": "html",
                "reply_markup": admins_manager_kb
            })
        else:
            bot("sendMessage", {
                "chat_id": cid,
                "text": f"<b>📋 Administratorlar roʻyxati:\n{admins}</b>",
                "parse_mode": "html",
                "reply_markup": admins_manager_kb
            })

    if is_admin and text == "📋 Adminlar roʻyxatini oʻchirish":
        if not admins.strip():
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 Botda administratorlar mavjud emas!</b>",
                "parse_mode": "html",
                "reply_markup": admins_manager_kb
            })
        else:
            delete_file("data/admins.txt")
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 Administratorlar roʻyxati muvaffaqiyatli oʻchirildi!</b>",
                "parse_mode": "html",
                "reply_markup": admins_manager_kb
            })

    # =============================================
    # Change vote price
    # =============================================
    if is_admin and text == "🙋‍♂️ Ovoz berish narxini uzgartirish":
        write_file(f"step/{cid}/{cid}.txt", "setpey")
        bot("sendMessage", {
            "chat_id": cid,
            "text": "<b>🙋‍♂️ Ovoz berish narxini kiriting</b>",
            "parse_mode": "html",
            "reply_markup": ortga_kb
        })

    if step == "setpey" and text not in ("/start", back, "👨🏻‍💻 Boshqaruv paneli"):
        if text.isdigit():
            delete_file(f"step/{cid}/{cid}.txt")
            write_file("data/paynet.txt", text)
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📝 Ovoz berish narxi muvaffaqiyatli uzgartirildi!</b>",
                "parse_mode": "html",
                "reply_markup": panel_kb
            })
        else:
            delete_file(f"step/{cid}/{cid}.txt")
            bot("sendMessage", {
                "chat_id": cid,
                "text": "<b>📋 Narx kiritayotganda faqat raqamlardan foydalaning!</b>",
                "parse_mode": "html",
                "reply_markup": panel_kb
            })


# =============================================
# Webhook entry point (Flask)
# =============================================

from flask import Flask, request

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    if update:
        handle_update(update)
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

# =============================================
# Manba @UzCoderTeam & @PHPfunctiones
# =============================================
