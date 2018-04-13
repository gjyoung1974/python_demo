# Usage (given build times depend on machine):
#
#    Build SMALL image (no cache; ~20MB, time for build=rebuild = ~360s):
#    docker build --squash="true" -t pci-www:latest .
#
#    Build FAST (rebuild) image (cache; >280MB, build time ~360s, rebuild time ~80s):
#    docker build -t pci-www .
#
#    Clean (remove intermidiet images):
#    docker rmi -f $(docker images -f "dangling=true" -q)
#
#    Run image (on localhost:8080):
#    docker run --name pci-www -p 8080:80 pci-www &
#
#    Run image as virtual host (read more: https://github.com/jwilder/nginx-proxy):
#    docker run -e VIRTUAL_HOST=pci-www.your-domain.com --name pci-www pci-www &

FROM python:3-alpine3.7

# install console and node
RUN apk update &&\
    apk add --no-cache bash \
        openssl \
        make    \
        nodejs  \
        git &&\
    mkdir -p /opt/app

# install pip ( in separate dir due to docker cache)
ADD setup.py /opt/app
RUN cd /opt/app && pip install -e .

# install nodejs dependencies ( in separate dir due to docker cache)
ADD package.json /opt/app
RUN cd /opt/app && npm install

WORKDIR /opt/app/src
ADD  . /opt/app/src

# this is for virtual host purposes
EXPOSE 3000 3001 8080 5000
CMD ["python", "demo/app.py"]

