# mystrom-python-mqtt
Requests data from MyStrom switch and push to a mqtt server.

## Environment Variables
`MQTT_SERVER_ADDRESS` - the hostnamo or ip address of the mqtt server

## Run
### With python
```sh
export MQTT_SERVER_ADDRESS=...
python -m main
```

### With Docker Container
```sh
docker run \
    --name mystrom-python \
    -e "MQTT_SERVER_ADDRESS=..." \
    nksdaoxxso/mystrom-python-mqtt:latest
```
