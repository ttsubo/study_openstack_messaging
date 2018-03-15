FROM ubuntu:14.04.5
MAINTAINER Toshiki Tsuboi <t.tsubo2000@gmail.com>

# setup erlang

WORKDIR /
ADD https://www.rabbitmq.com/rabbitmq-signing-key-public.asc .
RUN apt-key add rabbitmq-signing-key-public.asc
RUN echo "deb http://www.rabbitmq.com/debian/ testing main" > /etc/apt/sources.list.d/rabbitmq.list \
 && apt-get update \
 && apt-get install -y rabbitmq-server=3.2.4-1 --force-yes \
 && apt-get install -y python \
 && apt-get install -y curl

# Setup RabbitMQ Web Management Console
RUN rabbitmq-plugins enable rabbitmq_management

COPY start-rabbitmq.sh /usr/local/bin/
COPY pre-entrypoint.sh /
COPY docker-entrypoint.sh /
COPY rabbitmq.config /etc/rabbitmq/

ENV GOSU_VERSION 1.10
RUN set -eux; \
	\
	fetchDeps=' \
		ca-certificates \
		wget \
	'; \
	apt-get update; \
	apt-get install -y --no-install-recommends $fetchDeps; \
	rm -rf /var/lib/apt/lists/*; \
	\
	dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
	wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
	\
# verify the signature
	export GNUPGHOME="$(mktemp -d)"; \
	gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
	gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
	rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc; \
	\
	chmod +x /usr/local/bin/gosu; \
# verify that the binary works
	gosu nobody true; \
	\
	apt-get purge -y --auto-remove $fetchDeps


EXPOSE 5672 15672 25672 4369 9100 9101 9102 9103 9104 9105
ENTRYPOINT ["/pre-entrypoint.sh"]
CMD ["start-rabbitmq.sh"]
