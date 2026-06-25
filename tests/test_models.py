from models import Plant, Sensor, WateringSchedule


def test_plant_eq_and_str():
    plant = Plant("Monstera", "Monstera deliciosa", "medium")
    same_plant = Plant("Monstera", "Monstera deliciosa", "medium")

    assert plant == same_plant
    assert str(plant) == (
        "Plant(name=Monstera, species=Monstera deliciosa, "
        "water_need=medium)"
    )


def test_sensor_eq_and_str():
    sensor = Sensor("S001", "Monstera", 42)
    same_sensor = Sensor("S001", "Monstera", 42)

    assert sensor == same_sensor
    assert str(sensor) == (
        "Sensor(sensor_id=S001, plant_name=Monstera, humidity=42)"
    )


def test_watering_schedule_eq_and_str():
    schedule = WateringSchedule("Monstera", "08:00", 250)
    same_schedule = WateringSchedule("Monstera", "08:00", 250)

    assert schedule == same_schedule
    assert str(schedule) == (
        "WateringSchedule(plant_name=Monstera, hour=08:00, "
        "water_amount_ml=250)"
    )
