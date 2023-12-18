import adafruit_dht
import time
import asyncio

GPIO_PIN: int = 17

am2302 = adafruit_dht.DHT22(GPIO_PIN)

async def read_humidity():
    while True:
        try:
            humidity_percent = am2302.humidity
            print(f"Luftfeuchtigkeit: {humidity_percent}%")
        except RuntimeError as e:
            print(f"Fehler beim Lesen des Sensors: {e}")

        await asyncio.sleep(2)

if __name__ == '__main__':
    print('Lesen der Luftfeuchtigkeit...')
    try:
        asyncio.run(read_humidity())
    except KeyboardInterrupt:
        pass
