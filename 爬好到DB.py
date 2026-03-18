import yfinance as yf
import pymssql
import schedule
import time
from datetime import datetime

# =========================
# 資料庫連線設定
# =========================
server = "k94701210.database.windows.net"
database = "free-sql-db-2916645"
user = "dbeng"
password = "Ab123456"   # ⚠️ 建議改用環境變數

# =========================
# 取得股票資料
# =========================
def get_stock_data(stock_id):
    tick = yf.Ticker(stock_id)
    info = tick.fast_info
    
    sid = stock_id.split(".")[0]

    return {
        "sid": sid,
        "price": info.last_price,
        "sname": tick.info.get("shortName") or "Unknown"
    }

# =========================
# 寫入資料庫
# =========================
def insert_db(data):
    INS_SQL = """
        INSERT INTO dbo.stocks (sid, sname, price, pdate)
        VALUES (%s, %s, %s, %s)
    """

    try:
        conn = pymssql.connect(server, user, password, database)
        cursor = conn.cursor()

        cursor.execute(
            INS_SQL,
            (
                data["sid"],
                data["sname"],
                float(data["price"]),
                datetime.now()
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        print(f"✅ 寫入成功: {data['name']} {data['price']}")

    except Exception as e:
        print(f"❌ DB錯誤: {e}")

# =========================
# 主執行邏輯
# =========================
def job():
    print("🚀 開始抓資料...")

    stocks = ["2330.TW"]

    for s in stocks:
        data = get_stock_data(s)
        insert_db(data)

    print("⏱ 完成一次更新\n")

# =========================
# 排程（每30秒）
# =========================
schedule.every(5).seconds.do(job).until("21:00")

print("📡 系統啟動...")

while True:
    schedule.run_pending()
    time.sleep(1)


