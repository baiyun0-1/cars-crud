from app import database
from app.schemas import CarInput

def test_saved_car_can_be_read_from_sqlite(database_path):
    database.initialize(database_path)

    saved = database.create_car(
        database_path,
        CarInput(make="Toyota", model="Yaris", year=2020, color="Blue"),
    )
    loaded = database.get_car(database_path, saved.id)

    assert loaded is not None
    assert loaded.id == saved.id
    assert loaded.make == "Toyota"
    assert loaded.year == 2020
def test_deleting_one_car_keeps_the_other(database_path):
    database.initialize(database_path)
    # 创建第一辆车
    first = database.create_car(
        database_path,
        CarInput(make="Toyota", model="Camry", year=2022, color="White")
    )
    # 创建第二辆车
    second = database.create_car(
        database_path,
        CarInput(make="Honda", model="Accord", year=2023, color="Black")
    )

    # 删除第一辆车
    database.delete_car(database_path, first.id)

    # 断言：第一辆车找不到
    loaded_first = database.get_car(database_path, first.id)
    assert loaded_first is None

    # 断言：第二辆车还存在
    loaded_second = database.get_car(database_path, second.id)
    assert loaded_second is not None
    assert loaded_second.id == second.id

    # 断言：list_cars 结果里面只有1条记录
    all_cars = database.list_cars(database_path)
    assert len(all_cars) == 1
