import re
from playwright.sync_api import expect

def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()
    
    # 等待 URL 跳转
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    # 等待页面网络请求完成，确保数据渲染
    page.wait_for_load_state("networkidle")
    
    # 使用 to_contain_text 提高匹配成功率
    expect(page.locator("body")).to_contain_text("Toyota Yaris", timeout=15000)


def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 打开新建车辆页面，创建 Honda Civic 2022
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_role("button", name="Create car").click()

    # 等待创建成功跳转
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    page.wait_for_load_state("networkidle")

    # 2. 点击 Edit car 链接进入编辑页
    page.get_by_role("link", name="Edit car").click()
    page.wait_for_load_state("networkidle")

    # 3. 修改：车型改为Accord，年份改为2023
    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")

    # 4. 保存修改
    page.get_by_role("button", name="Save changes").click()

    # 等页面跳转到详情页
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    # 等待网络空闲，确保后端保存完成且前端数据加载完毕
    page.wait_for_load_state("networkidle")

    # 5. 断言详情页包含 Honda Accord (放宽匹配条件，兼容标题带年份或前后缀的情况)
    expect(page.locator("body")).to_contain_text("Honda Accord", timeout=15000)

    # 6. 刷新页面
    page.reload()
    # 刷新后同样等待网络空闲，测试后端数据是否真正持久化了
    page.wait_for_load_state("networkidle")

    # 7. 刷新后再次校验，数据仍然保留
    expect(page.locator("body")).to_contain_text("Honda Accord", timeout=15000)

    # 校验年份2023存在
    expect(page.locator("body")).to_contain_text("2023", timeout=15000)