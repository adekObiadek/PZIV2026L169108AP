import pickle

from storage import create_initial_data, get_objects_by_class


def test_object_list_can_be_serialized_and_deserialized_with_pickle():
    data = create_initial_data()
    plants = get_objects_by_class(data, "Plant")

    serialized_plants = pickle.dumps(plants)
    deserialized_plants = pickle.loads(serialized_plants)

    assert deserialized_plants == plants
