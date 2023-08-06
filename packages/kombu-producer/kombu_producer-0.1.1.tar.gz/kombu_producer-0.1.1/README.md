# Kombu Producer
### _Python library that implements a simple Kombu producer_


### Installation
```shell
pip install kombu-producer
```

### Publishing event with payload
```shell
from kombu_producer import KombuProducer
from json import dumps

KombuProducer(
            exchange_name="<EXCHANGE_NAMED>",
            exchange_type="<EXCHANGE_TYPE>",
            routing_key="<ROUTING_KEY>",
            broker_url="<BROKER_URL>"
        ).publish_payload(
            payload=dumps(
                {
                    "event": "<EVENT_NAME>",
                    "data": {
                        "<KEY1>": "<VAL1>",
                        "<KEY2>": "<VAL2>",
                    },
                }
            )
        )
```