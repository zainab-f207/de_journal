# from kafka import KafkaConsumer
# import json

# consumer = KafkaConsumer(
#     "driver_locations",
#     bootstrap_servers="localhost:29092",
#     value_deserializer=lambda v: json.loads(v.decode("utf-8")),
#     auto_offset_reset="earliest",
#     group_id="location_tracker_group"
# )

# print("Listening for driver location events... (Ctrl+C to stop)")
# for message in consumer:
#     print(f"Received: {message.value}")


from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "driver_locations",
    bootstrap_servers="localhost:29092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="brand_new_group",  # different group_id!
)

print("Listening as a NEW consumer group...")
for message in consumer:
    print(f"Received: {message.value}")