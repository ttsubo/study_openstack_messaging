FROM rabbitmq:3.7.2-management
MAINTAINER Toshiki Tsuboi <t.tsubo2000@gmail.com>

COPY start-rabbitmq.sh /usr/local/bin/
COPY pre-entrypoint.sh /
COPY rabbitmq.config /etc/rabbitmq/

EXPOSE 5672 15672 25672 4369 9100 9101 9102 9103 9104 9105
ENTRYPOINT ["/pre-entrypoint.sh"]
CMD ["start-rabbitmq.sh"]
