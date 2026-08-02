def choose_green_signal(counts):

    max_vehicles = -1
    selected_road = ""

    for road, count in counts.items():

        if count > max_vehicles:
            max_vehicles = count
            selected_road = road

    return selected_road