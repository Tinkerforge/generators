FROM debian:bullseye

# apt
RUN DEBIAN_FRONTEND=noninteractive apt-get clean
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apt-transport-https debconf-utils
COPY debconf.conf debconf.conf
RUN debconf-set-selections < debconf.conf

# locales
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y locales locales-all
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# user 1/2
RUN adduser --disabled-password --gecos '' foobar

# zip
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y zip

# debian package
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y debhelper dh-golang dh-python lintian

# c bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential mingw-w64 clang clang-tools libgd-dev

# csharp bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y wget mono-complete
RUN wget https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb -O /tmp/packages-microsoft-prod.deb
RUN DEBIAN_FRONTEND=noninteractive dpkg -i /tmp/packages-microsoft-prod.deb
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y dotnet-sdk-6.0
ENV DOTNET_CLI_TELEMETRY_OPTOUT 1

# delphi bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y fpc

# go bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y golang-any

# java bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y default-jdk default-jdk-doc openjdk-11-jdk-headless maven maven-debian-helper libmaven-javadoc-plugin-java

# javascript bindings
RUN wget -q https://deb.nodesource.com/gpgkey/nodesource.gpg.key -O /etc/apt/trusted.gpg.d/nodesource.gpg.asc
RUN echo "deb https://deb.nodesource.com/node_18.x bullseye main" >> /etc/apt/sources.list
RUN DEBIAN_FRONTEND=noninteractive apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install nodejs

# openhab bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git

# perl bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y perl libterm-readkey-perl libgd-perl libb-lint-perl libdata-dump-perl libperl-critic-perl libmodule-starter-perl libmodule-build-perl libdigest-hmac-perl

# python bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 pylint3 python3-pil python3-setuptools python3-opencv python3-numpy

# php bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y php-pear

# ruby bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y ruby gem2deb

# rust bindings
USER foobar
RUN wget https://sh.rustup.rs -O /tmp/rustup-init.sh
RUN bash /tmp/rustup-init.sh -y --default-toolchain nightly-2024-02-20 -c rustfmt-preview
USER root
RUN ln -s /home/foobar/.cargo/bin/* /usr/local/bin/

# shell bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y bash-completion

# user 2/2
USER foobar
RUN git config --global user.email "foobar@tinkerforge.com"
RUN git config --global user.name "foobar"
