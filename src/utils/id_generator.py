initial_id = -1


def id_generator():
    global initial_id
    initial_id += 1
    return initial_id
