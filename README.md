# NirahMQ

A complete Home Assistant MQTT Python library with ease of use in mind

## Example

Below is an example of a simple Text component:

```python
from nirahmq.components import Text
from nirahmq.device import Device, DeviceInfo, DiscoveryInfo, OriginInfo
from nirahmq.mqtt import MQTTClient


def callback(text: Text, payload: str) -> None:
    print(f"Got new text: `{payload}`")
    text.set_text(payload)


dinfo = DiscoveryInfo(
    device=DeviceInfo(
        name="NirahMQ Test Device",
        identifiers="NirahMQ-Test-Device"
    ),
    origin=OriginInfo(
        name="Python Program"
    ),
    components={
        'component1': Text(command_topic="~/cmd", state_topic="~/state", command_callback=callback)
    }
)

with (MQTTClient("homeassistant.lan", 1883, "user", r"password") as client,
      Device(client, dinfo, "node_id") as device):
    input("Press enter to continue...\n")
```
