## Envirornment
* RabbitMQ : 3.2.4
* oslo.messaging: 1.4.2

## How to build Docker Image

```
$ docker build -t ttsubo/ubuntu:juno dockerfile/ubuntu/.
$ docker build -t ttsubo/rabbitmq:juno dockerfile/rabbitmq/.
$ docker build -t ttsubo/haproxy-1:juno dockerfile/haproxy-1/.
$ docker build -t ttsubo/haproxy-2:juno dockerfile/haproxy-2/.
```

## How to Run
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

root@rabbit-1-server:/# ./rabbitmqadmin list queues name messages node slave_nodes
+------------------------------------------------+----------+------------------------+-----------------------------------------------+
|                      name                      | messages |          node          |                  slave_nodes                  |
+------------------------------------------------+----------+------------------------+-----------------------------------------------+
| engine                                         | 0        | rabbit@rabbit-1-server | rabbit@rabbit-3-server rabbit@rabbit-2-server |
| engine.heat-engine                             | 0        | rabbit@rabbit-1-server | rabbit@rabbit-3-server rabbit@rabbit-2-server |
| engine_fanout_2b2414c23f814e77a5e5a7961d48a63e | 0        | rabbit@rabbit-1-server | rabbit@rabbit-3-server rabbit@rabbit-2-server |
| engine_fanout_712588666789458596a8dc2ece2df0ec | 0        | rabbit@rabbit-1-server | rabbit@rabbit-3-server rabbit@rabbit-2-server |
| engine_fanout_c044236f81be4b77bb401ca7941a13b2 | 0        | rabbit@rabbit-2-server | rabbit@rabbit-3-server rabbit@rabbit-1-server |
| reply_80682df99e7d4fbe849da1131d01bca7         | 0        | rabbit@rabbit-3-server | rabbit@rabbit-1-server rabbit@rabbit-2-server |
+------------------------------------------------+----------+------------------------+-----------------------------------------------+
```
## Checking current list_queues in rabbitmq
```
root@rabbit-1-server:/# rabbitmqctl list_queues name messages messages_unacknowledged consumers auto_delete
Listing queues ...
engine	0	0	3	false
engine.heat-engine	0	0	3	false
engine_fanout_2b2414c23f814e77a5e5a7961d48a63e	0	0	1	true
engine_fanout_712588666789458596a8dc2ece2df0ec	0	0	1	true
engine_fanout_c044236f81be4b77bb401ca7941a13b2	0	0	1	true
reply_80682df99e7d4fbe849da1131d01bca7	0	0	1	true
...done.
```
## Checking heat-api/heat-engine results via rabbitmq
```
$ tail -f log/heat-1-api.log
$ tail -f log/heat-1-engine.log
```
