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
root@rabbit-1-server:/# ./rabbitmqadmin list queues name messages node slave_nodes
+------------------------------------------------+----------+------------------------+-----------------------------------------------+
|                      name                      | messages |          node          |                  slave_nodes                  |
+------------------------------------------------+----------+------------------------+-----------------------------------------------+
| engine                                         | 0        | rabbit@rabbit-1-server | rabbit@rabbit-3-server rabbit@rabbit-2-server |
| engine.heat-engine                             | 0        | rabbit@rabbit-1-server | rabbit@rabbit-3-server rabbit@rabbit-2-server |
| engine_fanout_d3dbc757d8c8491daf905fa3ae0edea3 | 0        | rabbit@rabbit-1-server | rabbit@rabbit-3-server rabbit@rabbit-2-server |
| reply_114ce15e745c40a49d09aa9d95b52faa         | 0        | rabbit@rabbit-1-server | rabbit@rabbit-3-server rabbit@rabbit-2-server |
+------------------------------------------------+----------+------------------------+-----------------------------------------------+
```
## Checking status of cluster among rabbitmq nodes
```
root@rabbit-1-server:/# rabbitmqctl cluster_status
Cluster status of node 'rabbit@rabbit-1-server' ...
[{nodes,[{disc,['rabbit@rabbit-1-server','rabbit@rabbit-2-server',
                'rabbit@rabbit-3-server']}]},
 {running_nodes,['rabbit@rabbit-3-server','rabbit@rabbit-2-server',
                 'rabbit@rabbit-1-server']},
 {partitions,[]}]
...done.
```
## Checking current list_queues in rabbitmq
```
root@rabbit-1-server:/# rabbitmqctl list_queues name messages messages_unacknowledged consumers auto_delete
Listing queues ...
engine  0       0       1       false
engine.heat-engine      0       0       1       false
engine_fanout_d3dbc757d8c8491daf905fa3ae0edea3  0       0       1       true
reply_114ce15e745c40a49d09aa9d95b52faa  0       0       1       true
...done.
```
## Checking current queue policies in list_queues
```
root@rabbit-1-server:/# rabbitmqctl list_queues name policy pid slave_pids
Listing queues ...
engine  all     <'rabbit@rabbit-1-server'.2.671.0>      [<'rabbit@rabbit-3-server'.3.878.0>, <'rabbit@rabbit-2-server'.1.1015.0>]
engine.heat-engine      all     <'rabbit@rabbit-1-server'.2.674.0>      [<'rabbit@rabbit-3-server'.3.876.0>, <'rabbit@rabbit-2-server'.1.1013.0>]
engine_fanout_d3dbc757d8c8491daf905fa3ae0edea3  all     <'rabbit@rabbit-1-server'.2.677.0>      [<'rabbit@rabbit-3-server'.3.883.0>, <'rabbit@rabbit-2-server'.1.1021.0>]
reply_114ce15e745c40a49d09aa9d95b52faa  all     <'rabbit@rabbit-1-server'.2.718.0>      [<'rabbit@rabbit-3-server'.3.899.0>, <'rabbit@rabbit-2-server'.1.1048.0>]
...done.
```
## Checking whether mirrored queues are synchronised, or not in list_queues
```
root@rabbit-1-server:/# rabbitmqctl list_queues name slave_pids synchronised_slave_pids
Listing queues ...
engine  [<'rabbit@rabbit-3-server'.3.878.0>, <'rabbit@rabbit-2-server'.1.1015.0>]       [<'rabbit@rabbit-3-server'.3.878.0>, <'rabbit@rabbit-2-server'.1.1015.0>]
engine.heat-engine      [<'rabbit@rabbit-3-server'.3.876.0>, <'rabbit@rabbit-2-server'.1.1013.0>]       [<'rabbit@rabbit-3-server'.3.876.0>, <'rabbit@rabbit-2-server'.1.1013.0>]
engine_fanout_d3dbc757d8c8491daf905fa3ae0edea3  [<'rabbit@rabbit-3-server'.3.883.0>, <'rabbit@rabbit-2-server'.1.1021.0>]       [<'rabbit@rabbit-3-server'.3.883.0>, <'rabbit@rabbit-2-server'.1.1021.0>]
reply_114ce15e745c40a49d09aa9d95b52faa  [<'rabbit@rabbit-3-server'.3.899.0>, <'rabbit@rabbit-2-server'.1.1048.0>]       [<'rabbit@rabbit-3-server'.3.899.0>, <'rabbit@rabbit-2-server'.1.1048.0>]
...done.
```
## Checking heat-api/heat-engine results via rabbitmq
```
$ tail -f log/heat-1-api.log
$ tail -f log/heat-1-engine.log
```
