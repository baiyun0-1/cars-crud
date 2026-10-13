def test_post_car_returns_201_and_json(client):
    payload = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 2018,
        "color": "Black",
    }

    response = client.post("/api/cars", json=payload)

    assert response.status_code == 201
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert car["model"] == "Fiesta"
    assert response.headers["location"] == f"/api/cars/{car['id']}"

    def test_invalid_year_is_not_saved(client):
        payload = {
            "make": "Ford",
            "model": "Fiesta",
            "year": 1800,
            "color": "Black",
        }
        # 提交非法年份数据
        response_post = client.post("/api/cars", json=payload)
        # 断言返回422校验错误
        assert response_post.status_code == 422

        # 查询全部车辆
        response_get = client.get("/api/cars")
        car_list = response_get.json()
        # 列表为空，数据没有存入数据库
        assert car_list == []

