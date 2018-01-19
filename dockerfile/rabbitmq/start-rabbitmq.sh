#!/bin/bash

hostname=`hostname`

if [ -z "$CLUSTER_WITH" -o "$CLUSTER_WITH" = "$hostname" ]; then
  echo "Running as single server"
  rabbitmq-server
else
  echo "Running as clustered server"
  /usr/sbin/rabbitmq-server -detached
  rabbitmqctl stop_app

  echo "Joining cluster $CLUSTER_WITH"
  rabbitmqctl join_cluster ${ENABLE_RAM:+--ram} rabbit@$CLUSTER_WITH

  rabbitmqctl start_app
  rabbitmqctl set_policy all '.*' '{"ha-sync-mode":"automatic", "ha-mode": "all"}' -p /

  # Tail to keep the a foreground process active..
  tail -f /var/log/rabbitmq/*
fi
