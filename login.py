import os
import time
import requests
from playwright.sync_api import sync_playwright

UZANTONOMO = os.environ.get("UZANTONOMO", "")
PASVORTO = os.environ.get("PASVORTO", "")
TELEGRAM_SIGNALO = os.environ.get("TELEGRAM_SIGNALO", "")
TELEGRAM_BABILO_ID = os.environ.get("TELEGRAM_BABILO_ID", "")

fail_msgs = [
    "Invalid credentials.",
    "Not connected to server.",
    "Error with the login: login size should be between 2 and 50 (currently: 1)"
]

mesaĝaj_partoj = []
mesaĝaj_partoj.append("🌐 netlib.re 域名保活报告")

def ensaluta_konto(playwright, UZANTONOMO, PWD):
    mesaĝaj_partoj.append(f"🧑‍💻 开始登录账号: {UZANTONOMO}")
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.netlib.re/")
        time.sleep(5)

        mesaĝaj_partoj.append("👆 正在点击登录")
        page.get_by_text("Login").click()
        time.sleep(2)
        mesaĝaj_partoj.append("✍️ 正在输入账号")
        page.get_by_role("textbox", name="Username").fill(UZANTONOMO)
        time.sleep(2)
        mesaĝaj_partoj.append("🔑 正在输入密码")
        page.get_by_role("textbox", name="Password").fill(PASVORTO)
        time.sleep(2)
        page.get_by_role("button", name="Validate").click()
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        success_text = "You are the exclusive owner of the following domains."
        if page.query_selector(f"text={success_text}"):
            mesaĝaj_partoj.append(f"☑️ 账号 {UZANTONOMO} 登录成功")
            mesaĝaj_partoj.append("🎉 账号已保活！")
            time.sleep(5)
        else:
            failed_msg = None
            for msg in fail_msgs:
                if page.query_selector(f"text={msg}"):
                    failed_msg = msg
                    break
            if failed_msg:
                mesaĝaj_partoj.append(f"⛔ 账号 {UZANTONOMO} 登录失败: {failed_msg}")
            else:
                mesaĝaj_partoj.append(f"💥 账号 {UZANTONOMO} 登录失败: 未知错误")

        context.close()
        browser.close()

    except Exception as e:
        mesaĝaj_partoj.append(f"⚠️ 账号 {UZANTONOMO} 登录异常: {e}")

def sendi_telegraman_mesaĝon(teksto):
    url = f"https://api.telegram.org/bot{TELEGRAM_SIGNALO}/sendMessage"
    utila_ŝarĝo = {
        "chat_id": TELEGRAM_BABILO_ID,
        "text": teksto
    }
    try:
        response = requests.post(url, data=utila_ŝarĝo)
        if response.status_code == 200:
            print("📨 Telegram 通知已发送")
        else:
            print(f"⚠️ Telegram 发送失败: {response.text}")
    except Exception as e:
        print(f"⚠️ Telegram 异常: {e}")

def sendi_kaj_presi(mesaĝo):
    print(mesaĝo)
    sendi_telegraman_mesaĝon(mesaĝo)

def Ruli():
    with sync_playwright() as playwright:
        ensaluta_konto(playwright, UZANTONOMO, PASVORTO)
        fina_mesaĝo = "\n".join(mesaĝaj_partoj)
        sendi_kaj_presi(fina_mesaĝo)
        time.sleep(2)

if __name__ == "__main__":
    Ruli()
