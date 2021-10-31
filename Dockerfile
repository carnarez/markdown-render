# compile the http server
# with musl instead of libc to reduce even further the size of the executable

FROM alpine:latest as thttpd

WORKDIR /usr/src

COPY thttpd.patch thttpd.patch

ARG THTTPD_VERSION=2.29
RUN apk --no-cache add curl gcc make musl-dev patch tar \
 && curl -sf -o thttpd-${THTTPD_VERSION}.tar.gz http://acme.com/software/thttpd/thttpd-${THTTPD_VERSION}.tar.gz \
 && tar -xf thttpd-${THTTPD_VERSION}.tar.gz \
 && cd thttpd-${THTTPD_VERSION} \
 && patch -p1 < ../thttpd.patch \
 && ./configure \
 && make CCOPT="-O2 -g -static" thttpd \
 && install -m 755 thttpd /usr/bin


# render markdown to html
# requires a libc-based distribution (not musl as alpine)

FROM python:slim as render

WORKDIR /usr/src

COPY requirements.txt /tmp/requirements.txt

COPY render.py render.py
COPY markdown.md markdown.md
COPY template.html template.html

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends -y git make \
 && pip install -r /tmp/requirements.txt \
 && mkdir -p /usr/local/www \
 && python render.py markdown.md > /usr/local/www/index.html


# run as root, but there is literally NOTHING in this container
# and this is for local development

FROM scratch

WORKDIR /

COPY --from=thttpd /usr/bin/thttpd /bin/thttpd
COPY --from=render /usr/local/www /www

COPY style*.css /www/

ENTRYPOINT ["/bin/thttpd", "-D", "-l", "/dev/null", "-d", "/www"]
