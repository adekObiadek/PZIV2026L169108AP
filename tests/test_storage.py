from models import Plant, Sensor, WateringSchedule
from storage import create_initial_data, get_objects_by_class


def test_create_initial_data_creates_12_objects():
    data = create_initial_data()

    assert len(data) == 12


def test_get_objects_by_class_returns_4_objects_for_each_class():
    data = create_initial_data()

    plants = get_objects_by_class(data, "Plant")
    sensors = get_objects_by_class(data, "Sensor")
    schedules = get_objects_by_class(data, "WateringSchedule")

    assert len(plants) == 4
    assert len(sensors) == 4
    assert len(schedules) == 4
    assert all(isinstance(item, Plant) for item in plants)
    assert all(isinstance(item, Sensor) for item in sensors)
    assert all(isinstance(item, WateringSchedule) for item in schedules)
