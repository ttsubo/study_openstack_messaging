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
## Checking master/slave nodes in rabbitmq
```
$ docker exec -it rabbit-1-server bash
```
```
root@rabbit-1-server:/# curl localhost:15672/cli/rabbitmqadmin > rabbitmqadmin
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 36110  100 36110    0     0  11.2M      0 --:--:-- --:--:-- --:--:-- 17.2M

root@rabbit-1-server:/# chmod 755 rabbitmqadmin

root@rabbit-1-server:/# ./rabbitmqctl list_queues name messages messages_unacknowledged consumers auto_delete
bash: ./rabbitmqctl: No such file or directory
root@rabbit-1-server:/# ./rabbitmqadmin list queues name messages node slave_nodes
+------------------------------------------------+----------+------------------------+------------------------------------------------------+
|                      name                      | messages |          node          |                     slave_nodes                      |
+------------------------------------------------+----------+------------------------+------------------------------------------------------+
| engine                                         | 0        | rabbit@rabbit-1-server | ["rabbit@rabbit-3-server", "rabbit@rabbit-2-server"] |
| engine.heat-engine                             | 0        | rabbit@rabbit-1-server | ["rabbit@rabbit-3-server", "rabbit@rabbit-2-server"] |
| engine_fanout_b615c7a0257e44a394170e755ad81d9b | 0        | rabbit@rabbit-2-server | ["rabbit@rabbit-3-server", "rabbit@rabbit-1-server"] |
| engine_fanout_be317fc5cd7440deb12d30a3fa00d3a5 | 0        | rabbit@rabbit-1-server | ["rabbit@rabbit-3-server", "rabbit@rabbit-2-server"] |
| engine_fanout_e5ac8ef4c02b48f4a6e8297ae99b713d | 0        | rabbit@rabbit-1-server | ["rabbit@rabbit-3-server", "rabbit@rabbit-2-server"] |
| reply_86216dccef824f3fa81cc47335aa15bc         | 0        | rabbit@rabbit-3-server | ["rabbit@rabbit-1-server", "rabbit@rabbit-2-server"] |
+------------------------------------------------+----------+------------------------+------------------------------------------------------+
```
## Checking current list_queues in rabbitmq
```
root@rabbit-1-server:/# /usr/lib/rabbitmq/bin/rabbitmqctl list_queues name messages messages_unacknowledged consumers auto_delete
Listing queues ...
reply_86216dccef824f3fa81cc47335aa15bc	0	0	1	true
engine.heat-engine	0	0	3	false
engine_fanout_b615c7a0257e44a394170e755ad81d9b	0	0	1	true
engine_fanout_e5ac8ef4c02b48f4a6e8297ae99b713d	0	0	1	true
engine_fanout_be317fc5cd7440deb12d30a3fa00d3a5	0	0	1	true
engine	0	0	3	false
```
## Checking heat-api/heat-engine results via rabbitmq
```
$ tail -f log/heat-1-api.log
$ tail -f log/heat-1-engine.log
$ tail -f log/heat-2-engine.log
$ tail -f log/heat-3-engine.log
```
