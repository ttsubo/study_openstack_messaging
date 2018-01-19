## Docker Image Build

```
$ docker build -t ttsubo/ubuntu:latest dockerfile/ubuntu/.
$ docker build -t ttsubo/rabbitmq:latest dockerfile/rabbitmq/.
$ docker build -t ttsubo/haproxy:latest dockerfile/haproxy/.
```

## Run
```
$ docker-compose -f docker-compose-single.yaml up -d
```
or
```
$ docker-compose -f docker-compose-multiple.yaml up -d
```
or
```
$ docker-compose -f docker-compose-multiple-roundrobin.yaml up -d
```

## Checking result
```
$ tail -f log/heat-1-api.log
$ tail -f log/heat-1-engine.log
$ tail -f log/heat-2-engine.log
$ tail -f log/heat-3-engine.log
```
