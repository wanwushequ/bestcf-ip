import base64
import os
from playwright.sync_api import sync_playwright

def run():
    # 获取当前脚本所在目录 (xinyitang3 文件夹)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        url = "https://sub.xinyitang.dpdns.org/sub?host=123&uuid=456"
        print(f"正在通过浏览器访问: {url}")
        
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            content = page.locator("body").inner_text().strip()
            
            if not content:
                print("❌ 未能获取到内容")
                return

            # Base64 解码校验
            try:
                decoded_data = base64.b64decode(content).decode('utf-8')
            except Exception as e:
                print(f"❌ Base64 解码失败: {e}")
                return

            if "vless://" not in decoded_data:
                print("❌ 数据格式非法，未找到 vless 节点")
                return

            # 将临时文件保存在 xinyitang3 目录下
            tmp_path = os.path.join(current_dir, "decoded_nodes.tmp")
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(decoded_data)
            
            print(f"✅ 成功提取并解码节点数据，保存至: {tmp_path}")

        except Exception as e:
            print(f"❌ 运行出错: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()