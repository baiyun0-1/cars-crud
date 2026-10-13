import re
from playwright.sync_api import expect

def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")

    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()
def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 打开新建车辆页面，创建 Honda Civic 2022
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_role("button", name="Create car").click()

    # 2. 点击 Edit car 链接进入编辑页
    page.get_by_role("link", name="Edit car").click()

    # 3. 修改：车型改为Accord，年份改为2023
    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")

    # 4. 保存修改
    page.get_by_role("button", name="Save changes").click()

    # 5. 断言详情页标题是 Honda Accord
    expect(page.get_by_role("heading", name="Honda Accord")).to_be_visible()

    # 6. 刷新页面
    page.reload()

    # 7. 刷新后再次校验，数据仍然保留
    expect(page.get_by_role("heading", name="Honda Accord")).to_be_visible()
    # 校验年份2023存在
    expect(page.get_by_text("2023")).to_be_visible()
