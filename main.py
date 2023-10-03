import asyncio
import datetime
import json
import os
import time

import pytz
import requests
from aiomqtt import Client
from dotenv import load_dotenv
from schedule import every, repeat, run_pending


@repeat(every(5).seconds)
def trigger():
    device_ip = os.getenv('MYSTROM_SERVER_ADDRESS')
    mqtt_ip = os.getenv('MQTT_SERVER_ADDRESS')
    mqtt_user = os.getenv('MQTT_SERVER_USER')
    mqtt_pw = os.getenv('MQTT_SERVER_PASSWORD')
    mqtt_client_id = os.getenv('MQTT_CLIENT_ID')
    mqtt_topic = os.getenv('MYSTROM_TOPIC')
    mqtt_tz = os.getenv('MYSTROM_SERVER_TZ')
    request_data_and_push(device_ip, mqtt_ip, mqtt_user, mqtt_pw, mqtt_client_id, mqtt_topic, mqtt_tz)


def request_data_and_push(device_ip: str, ip: str, user: str, pw: str, client_id: str, topic: str, tz: str):
    try:
        # noinspection HttpUrlsUsage
        response = requests.get(f'http://{device_ip}/report')
    except requests.ConnectionError:
        print(f'Device with ip address {device_ip} seems to be '
              f'not reachable.')
        return
    except requests.Timeout:
        print(f'Request to device with ip address {device_ip} '
              f'timed out.')
        return
    except requests.RequestException:
        print(f'Request to device with ip address {device_ip} '
              f'failed.')
        return

    try:
        response = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print(f'Request to device with ip address {device_ip} '
              f'returns invalid JSON response.')
        return

    # print(response.__repr__())

    asyncio.run(push(response, client_id, topic, ip, user, pw, tz))


async def push(response: dict, client_id: str, topic: str, ip: str, user: str, pw: str, tz: str):

    berlin_timezone = pytz.timezone(tz)
    current_time = datetime.datetime.now(berlin_timezone)
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S')
    async with Client(hostname=ip, username=user, password=pw, client_id=client_id) as client:
        payload = f'{{"Time": "{formatted_time}", "{response["boot_id"]}": {{' \
            f'"power": {response["power"]}, ' \
            f'"Ws": {response["Ws"]}, ' \
            f'"relay": {"true" if response["relay"] else "true"}, ' \
            f'"temperature": {response["temperature"]} }} }}'
        # noinspection PyTypeChecker
        await client.publish(topic, payload=payload)


if __name__ == '__main__':

    load_dotenv()

    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        run_pending()
        time.sleep(1)
