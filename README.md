# study_openstack_messaging

## Docker Image Build

```
$ docker build -t ttsubo/ubuntu:juno docker/build/ubuntu/.
$ docker build -t ttsubo/rabbitmq:3.2.4 docker/build/rabbitmq/.
```

## Run on kubernetes(minikube)
Applying openstack_messaging.yaml
```
$ kubectl apply -f <(istioctl kube-inject -f kubernetes/openstack_messaging.yaml)
service "rabbit-1-server" created
deployment "rabbit-1-server-pod" created
deployment "heat-engine-pod" created
deployment "heat-api-pod" created
```
Applying gateway.yaml
```
$ kubectl apply -f kubernetes/gateway.yaml 
gateway "openstack-messaging-gateway" created
virtualservice "openstack-messaging" created
```
Checking status of pods
```
$ kubectl get pods
NAME                                   READY     STATUS    RESTARTS   AGE
heat-api-pod-7ff755f585-wbm28          2/2       Running   0          53s
heat-engine-pod-7b9ffb4886-jk8kw       2/2       Running   0          53s
rabbit-1-server-pod-6d74b54494-w76vs   2/2       Running   1          53s
```
Checking status of services
```
$ kubectl get services
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)              AGE
kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP              15d
rabbit-1-server   ClusterIP   10.100.144.186   <none>        5672/TCP,15672/TCP   1m
```
Checking webui address/port
```
$ export INGRESS_HOST=$(minikube ip)
$ export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
$ export GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT
$ curl -o /dev/null -s -w "%{http_code}\n" http://${GATEWAY_URL}/
200
$ open http://${GATEWAY_URL}/
```
Checking result
```
$ kubectl exec -it heat-api-pod-7ff755f585-wbm28 -c heat-api-pod tail /log/heat-1-api.log
2018-09-09 07:21:36,572:INFO:### Response: id=[444], host=[heat-engine-pod-7b9ffb4886-jk8kw], content=[I'm fine!]
2018-09-09 07:21:37,580:INFO:### Response: id=[445], host=[heat-engine-pod-7b9ffb4886-jk8kw], content=[I'm fine!]
2018-09-09 07:21:38,589:INFO:### Response: id=[446], host=[heat-engine-pod-7b9ffb4886-jk8kw], content=[I'm fine!]
2018-09-09 07:21:39,612:INFO:### Response: id=[447], host=[heat-engine-pod-7b9ffb4886-jk8kw], content=[I'm fine!]
2018-09-09 07:21:40,635:INFO:### Response: id=[448], host=[heat-engine-pod-7b9ffb4886-jk8kw], content=[I'm fine!]
```
```
$ kubectl exec -it heat-engine-pod-7b9ffb4886-jk8kw -c heat-engine-pod tail /log/heat-1-engine.log
2018-09-09 07:21:40,631:INFO:### Request: id=[448], host=[heat-api-pod-7ff755f585-wbm28], content=[How are you?]
2018-09-09 07:21:41,639:INFO:### Request: id=[449], host=[heat-api-pod-7ff755f585-wbm28], content=[How are you?]
2018-09-09 07:21:42,660:INFO:### Request: id=[450], host=[heat-api-pod-7ff755f585-wbm28], content=[How are you?]
2018-09-09 07:21:43,667:INFO:### Request: id=[451], host=[heat-api-pod-7ff755f585-wbm28], content=[How are you?]
2018-09-09 07:21:44,675:INFO:### Request: id=[452], host=[heat-api-pod-7ff755f585-wbm28], content=[How are you?]
```
Delete all
```
$ kubectl delete -f <(istioctl kube-inject -f kubernetes/openstack_messaging.yaml)
$ kubectl delete gateway openstack-messaging-gateway
$ kubectl delete virtualservice openstack-messaging
```
