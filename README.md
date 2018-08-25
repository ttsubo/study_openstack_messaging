# study_openstack_messaging

## Docker Image Build

```
$ docker build -t ttsubo/ubuntu:latest docker/build/ubuntu/.
$ docker build -t ttsubo/rabbitmq:latest docker/build/rabbitmq/.
$ docker build -t ttsubo/haproxy:latest docker/build/haproxy/.
```

## Run on docker-compose
```
$ docker-compose -f docker/docker-compose-single.yaml up -d
```
or
```
$ docker-compose -f docker/docker-compose-multiple.yaml up -d
```
or
```
$ docker-compose -f docker/docker-compose-multiple-roundrobin.yaml up -d
```
Checking result
```
$ tail -f docker/log/heat-1-api.log
$ tail -f docker/log/heat-1-engine.log
$ tail -f docker/log/heat-2-engine.log
$ tail -f docker/log/heat-3-engine.log
```
## Run on kubernetes(minikube)
```
$ kubectl apply -f kubernetes/openstack_messaging.yaml
service "rabbit-1-server" created
deployment "rabbit-1-server-pod" created
deployment "heat-engine-pod" created
deployment "heat-api-pod" created
```
Checking status of pods
```
$ kubectl get pods
NAME                                  READY     STATUS    RESTARTS   AGE
heat-api-pod-6c486dcb79-bp5sp         1/1       Running   0          1m
heat-engine-pod-77974d8fbb-snjj4      1/1       Running   0          1m
rabbit-1-server-pod-97dfd456b-rbs8z   1/1       Running   0          1m
```
Checking status of services
```
$ kubectl get services
NAME              TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                          AGE
kubernetes        ClusterIP   10.96.0.1     <none>        443/TCP                          1h
rabbit-1-server   NodePort    10.102.20.8   <none>        5672:30228/TCP,15672:31210/TCP   16m
```
Checking webui address/port
```
$ minikube service rabbit-1-server --url
http://192.168.99.100:30228
http://192.168.99.100:31210
```
Checking result
```
$ kubectl exec -it heat-api-pod-6c486dcb79-bp5sp tail /log/heat-1-api.log
2018-08-25 23:54:58,159:INFO:### Response: id=[206], host=[heat-engine-pod-77974d8fbb-snjj4], content=[I'm fine!]
2018-08-25 23:54:59,170:INFO:### Response: id=[207], host=[heat-engine-pod-77974d8fbb-snjj4], content=[I'm fine!]
2018-08-25 23:55:00,181:INFO:### Response: id=[208], host=[heat-engine-pod-77974d8fbb-snjj4], content=[I'm fine!]
2018-08-25 23:55:01,193:INFO:### Response: id=[209], host=[heat-engine-pod-77974d8fbb-snjj4], content=[I'm fine!]
```
```
$ kubectl exec -it heat-engine-pod-77974d8fbb-snjj4 tail /log/heat-1-engine.log
2018-08-25 23:54:58,154:INFO:### Request: id=[206], host=[heat-api-pod-6c486dcb79-bp5sp], content=[How are you?]
2018-08-25 23:54:59,164:INFO:### Request: id=[207], host=[heat-api-pod-6c486dcb79-bp5sp], content=[How are you?]
2018-08-25 23:55:00,176:INFO:### Request: id=[208], host=[heat-api-pod-6c486dcb79-bp5sp], content=[How are you?]
2018-08-25 23:55:01,187:INFO:### Request: id=[209], host=[heat-api-pod-6c486dcb79-bp5sp], content=[How are you?]
```
