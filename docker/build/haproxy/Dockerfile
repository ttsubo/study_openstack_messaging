FROM debian:jessie
MAINTAINER Toshiki Tsuboi <t.tsubo2000@gmail.com>

RUN apt-get update \
 && apt-get install -y libpcre3 --no-install-recommends \
 && apt-get install -y iputils-ping \
 && apt-get install -y vim \
 && apt-get install -y net-tools \
 && apt-get install -y rsyslog \
 && rm -rf /var/lib/apt/lists/*

ENV HAPROXY_MAJOR 1.4
ENV HAPROXY_VERSION 1.4.27
ENV HAPROXY_MD5 459b82968791472427326ea009834c66

# see http://sources.debian.net/src/haproxy/1.5.8-1/debian/rules/ for some helpful navigation of the possible "make" arguments
RUN buildDeps='curl gcc libc6-dev libpcre3-dev libssl-dev make' \
	&& set -x \
	&& apt-get update && apt-get install -y $buildDeps --no-install-recommends && rm -rf /var/lib/apt/lists/* \
	&& curl -SL "http://www.haproxy.org/download/${HAPROXY_MAJOR}/src/haproxy-${HAPROXY_VERSION}.tar.gz" -o haproxy.tar.gz \
	&& echo "${HAPROXY_MD5}  haproxy.tar.gz" | md5sum -c \
	&& mkdir -p /usr/src/haproxy \
	&& tar -xzf haproxy.tar.gz -C /usr/src/haproxy --strip-components=1 \
	&& rm haproxy.tar.gz \
	&& make -C /usr/src/haproxy \
		TARGET=linux2628 \
		USE_PCRE=1 PCREDIR= \
		USE_OPENSSL=1 \
		USE_ZLIB=1 \
		all \
		install-bin \
	&& mkdir -p /usr/local/etc/haproxy \
	&& cp -R /usr/src/haproxy/examples/errorfiles /usr/local/etc/haproxy/errors \
	&& rm -rf /usr/src/haproxy \
	&& apt-get purge -y --auto-remove $buildDeps

COPY docker-entrypoint.sh /
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["haproxy", "-f", "/usr/local/etc/haproxy/haproxy.cfg"]
