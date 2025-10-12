```bash
curl --location --request POST 'https://solar.local/auth/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "user",
    "password": "123"
}'
```



```bash
curl --location --request GET 'https://solar.local/healthz'

```


```bash
curl --location --request GET '192.168.1.83:31000/auth/upsert_user?username=test_user2&password=123&role=operator' \
--header 'Accept: application/json' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJleHAiOjE3NTg1NjYwMzcsInJvbGUiOiJvcGVyYXRvciJ9.O-I7Xms6sP-xrKOhQ3R-FpsAHwgyx2rkFKgH3D4cnqU'

```



```bash
curl --location --request POST '192.168.1.163:8080/v1/set_load_working_mode?deviceId=2&modeCode=15' \
--header 'Accept: application/json'

```


```bash

```