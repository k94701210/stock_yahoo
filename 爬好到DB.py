import time
import random
from playwright.sync_api import sync_playwright
# 修正導入方式：直接導入整個模組
import playwright_stealth as stealth 
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ... (中間網址設定不變)

def get_chapters_stealth():
    with sync_playwright() as p:
        # headless=False 讓你可以看到瀏覽器視窗，這對過驗證很重要
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # 修正後的呼叫方式：模組名.函數名
        stealth.stealth_sync(page)
        
        links = []
        # 建議優先嘗試不帶 .htm 的版本
        target_url = "https://www.69shuba.com/book/58764/" 
        
        print(f"正在嘗試開啟目錄：{target_url}")
        try:
            page.goto(target_url, wait_until="networkidle", timeout=60000)
            
            # --- 重要：如果看到驗證碼，請手動點擊 ---
            print("檢查瀏覽器視窗中...如有驗證碼請手動完成。")
            time.sleep(10) # 留 10 秒讓你觀察或手動操作

            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # 69書吧目錄解析
            catalog = soup.select('.catalog ul li a')
            for a in catalog:
                href = a.get('href')
                if href and ('.htm' in href or 'book' in href):
                    links.append({
                        'title': a.text.strip(),
                        'url': urljoin(target_url, href)
                    })
            
            if links:
                print(f"✅ 成功找到 {len(links)} 個章節！")
            
        except Exception as e:
            print(f"❌ 發生錯誤: {e}")
        
        browser.close()
        return links