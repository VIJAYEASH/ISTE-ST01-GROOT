from ailogic import choose_green_signal

vehicle_counts = {
    "RoadA": 6,
    "RoadB": 10,
    "RoadC": 4,
    "RoadD": 7
}

green = choose_green_signal(vehicle_counts)

print("\nVehicle Counts")
print("----------------")

for road, count in vehicle_counts.items():
    print(f"{road} : {count}")

print("\n====================")
print("GREEN SIGNAL :", green)
print("====================")