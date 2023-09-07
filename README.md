# mystrom-python-mqtt
Requests data from MyStrom switch and push to a mqtt server.

## Environment Variables
Copy .env.example to .env and define your settings.

`MYSTROM_SERVER_ADDRESS` - ip address of the mystrom device

`MQTT_SERVER_ADDRESS` - ip address of the mqtt server

`MQTT_SERVER_PORT` - port of the mqtt server

`MQTT_SERVER_USER` - username for the mqtt server

`MQTT_SERVER_PASSWORD` - password for the mqtt server

`MQTT_CLIENT_ID` - mqtt client id

`MQTT_CLIENT_TOPIC` - mqtt publish topic

## Run
### With python
#### Create environment
```sh
git clone git@github.com:HenryJobst/mystrom-python-mqtt.git
cd mystrom-python-mqtt
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
#### Execute
```sh
python -m main
```

### With Docker Container
```sh
docker run \
    --name mystrom-python-mqtt \
    --env-file .env \
    nksdaoxxso/mystrom-python-mqtt:latest
```
