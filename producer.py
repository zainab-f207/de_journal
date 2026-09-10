from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

drivers = ["driver_1", "driver_2", "driver_3"]

for i in range(10):
    event = {
        "driver_id": random.choice(drivers),
        "latitude": round(31.5 + random.uniform(-0.1, 0.1), 4),
        "longitude": round(74.3 + random.uniform(-0.1, 0.1), 4),
        "timestamp": time.time()
    }
    producer.send("driver_locations", value=event)
    print(f"Sent: {event}")
    time.sleep(1)

producer.flush()
print("All events sent")