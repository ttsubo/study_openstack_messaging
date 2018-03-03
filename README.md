## Docker Image Build

```
$ docker build -t ttsubo/ubuntu:juno dockerfile/ubuntu/.
$ docker build -t ttsubo/rabbitmq:juno dockerfile/rabbitmq/.
$ docker build -t ttsubo/haproxy:juno dockerfile/haproxy/.
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
## Checking master/slave in rabbitmq
```
$ docker exec -it rabbit-1-server bash
```
```
root@rabbit-1-server:/# curl localhost:15672/cli/rabbitmqadmin > rabbitmqadmin
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 36110  100 36110    0     0  11.2M      0 --:--:-- --:--:-- --:--:-- 17.2M

root@rabbit-1-server:/# chmod 755 rabbitmqadmin

root@rabbit-1-server:/# ./rabbitmqadmin list queues name messages node slave_nodes
+------------------------------------------------+----------+------------------------+------------------------------------------------------+
|                      name                      | messages |          node          |                     slave_nodes                      |
+------------------------------------------------+----------+------------------------+------------------------------------------------------+
| engine                                         | 0        | rabbit@rabbit-2-server | ["rabbit@rabbit-3-server", "rabbit@rabbit-1-server"] |
| engine.heat-engine                             | 0        | rabbit@rabbit-2-server | ["rabbit@rabbit-3-server", "rabbit@rabbit-1-server"] |
| engine_fanout_3d8fd318c9794aa1937fb4787cdee52a | 0        | rabbit@rabbit-2-server | ["rabbit@rabbit-3-server", "rabbit@rabbit-1-server"] |
| engine_fanout_783b40f64d6d439493d6aed0495f8a08 | 0        | rabbit@rabbit-2-server | ["rabbit@rabbit-3-server", "rabbit@rabbit-1-server"] |
| engine_fanout_baf085305e9849818a71790ca547b9da | 0        | rabbit@rabbit-2-server | ["rabbit@rabbit-3-server", "rabbit@rabbit-1-server"] |
| reply_ce56ff8b44924629883a22ccbce62308         | 0        | rabbit@rabbit-2-server | ["rabbit@rabbit-3-server", "rabbit@rabbit-1-server"] |
+------------------------------------------------+----------+------------------------+------------------------------------------------------+
```

## Checking result
```
$ tail -f log/heat-1-api.log
$ tail -f log/heat-1-engine.log
$ tail -f log/heat-2-engine.log
$ tail -f log/heat-3-engine.log
```
