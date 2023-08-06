import rosbag
import importlib
import os
import argparse

ros_primitive_types = [
    "bool",
    "byte",
    "char",
    "int8",
    "uint8",
    "int16",
    "uint16",
    "int32",
    "uint32",
    "int64",
    "uint64",
    "float32",
    "float64",
    "string",
]


def _map_ros_messages(original_message, new_msg):
    message_fields = _get_message_fields(original_message)
    for field_name, field_type in message_fields:
        field_value = getattr(original_message, field_name)
        try:
            _map_value(field_type=field_type, field_value=field_value, field_name=field_name, new_msg=new_msg)
        except AttributeError:
            pass
    return new_msg

def _map_value(field_type, field_value, field_name, new_msg):
    if field_type in ros_primitive_types or _is_field_type_a_primitive_array(field_type):
        setattr(new_msg, field_name, field_value)
        return
    elif _is_field_type_an_array(field_type):
        field_value = _map_ros_array(
            field_type, field_value, field_name, new_msg
        )
        setattr(new_msg, field_name, field_value)
        return

    _map_ros_messages(field_value, getattr(new_msg, field_name))

def _is_field_type_a_primitive_array(field_type):
    bracket_index = field_type.find("[")
    if bracket_index < 0:
        return False
    list_type = field_type[:bracket_index]
    return list_type in ros_primitive_types

def _get_message_fields(message):
    return zip(message.__slots__, message._slot_types)

def _is_field_type_an_array(field_type):
    return field_type.find("[") >= 0

def _map_ros_array(field_type, field_value, field_name, new_msg):
    # use index to raise ValueError if '[' not present
    list_type = field_type[: field_type.index("[")]
    data_class = _get_msg_attribute(list_type)()
    return [
        _map_ros_messages(value, data_class)
        for value in field_value
    ]
    
def update_bag(original_bag: rosbag.Bag, data_class, topic_name: str, new_bag):
    for topic, msg, t in original_bag.read_messages(topics=topic_name):
        new_msg = _map_ros_messages(msg, data_class())
        new_bag.write(topic, new_msg, t)


def init(bag: rosbag.Bag, new_bag: rosbag.Bag):
    bag_topics = bag.get_type_and_topic_info().topics
    for topic, topic_tuple in bag_topics.items():
        x = topic_tuple.msg_type
        update_bag(bag, _get_msg_attribute(x), topic, new_bag)
    new_bag.close()
    bag.close()

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bag-file", dest="bag", help="Path of the bag file")
    options = parser.parse_args()
    if not options.bag:
        parser.error("[-] Please specify a bag file path to be updated, use --help for more info")
    return options

def _get_msg_attribute(topic_path):
    attr = ""
    topic_path = topic_path.split("/")
    import_string = topic_path[0]
    for i in range(len(topic_path)):
        if i == 0:
            continue
        if i == len(topic_path) - 1:
            import_string = import_string + ".msg"
            data_class = importlib.import_module(import_string)
            return getattr(data_class, topic_path[i])
            break
        import_string = import_string + "." + topic_path[i]
    

def main(*args):
    options = get_arguments()
    bag_base_name = os.path.basename(options.bag).replace('.bag', '')
    new_bag_name = bag_base_name + '.new.bag'
    init(rosbag.Bag(options.bag), rosbag.Bag(new_bag_name, "w"))
    print("New bag file written to: " + os.path.join(os.getcwd(), new_bag_name))

if __name__ == "__main__":
    main()
