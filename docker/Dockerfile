FROM debian:stretch

# apt
RUN echo "deb http://deb.debian.org/debian stretch-backports main" >> /etc/apt/sources.list
RUN echo "deb http://deb.debian.org/debian stretch-backports-sloppy main" >> /etc/apt/sources.list
RUN DEBIAN_FRONTEND=noninteractive apt-get clean
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports apt-utils apt-transport-https debconf-utils
COPY debconf.conf debconf.conf
RUN debconf-set-selections < debconf.conf

# locales
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports locales locales-all
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# user 1/2
RUN adduser --disabled-password --gecos '' foobar

# zip
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports zip

# debian package
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports debhelper dh-golang dh-python dh-systemd lintian

# c bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports build-essential mingw-w64 clang libgd-dev

# csharp bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports mono-complete mono-reference-assemblies-2.0 mono-reference-assemblies-4.0 wget
RUN wget https://packages.microsoft.com/config/debian/10/packages-microsoft-prod.deb -O /tmp/packages-microsoft-prod.deb
RUN DEBIAN_FRONTEND=noninteractive dpkg -i /tmp/packages-microsoft-prod.deb
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports dotnet-sdk-6.0
ENV DOTNET_CLI_TELEMETRY_OPTOUT 1

# delphi bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports fpc

# go bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports golang-any

# java bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports default-jdk default-jdk-doc openjdk-8-jdk-headless maven maven-debian-helper libmaven-javadoc-plugin-java

# FIXME: maven-debian-helper 2.1.3 in Debian Stretch is broken, install 2.3.2 manually instead
RUN wget http://ftp.de.debian.org/debian/pool/main/m/maven-debian-helper/maven-debian-helper_2.3.2_all.deb -O /tmp/maven-debian-helper_2.3.2_all.deb
RUN DEBIAN_FRONTEND=noninteractive dpkg -i /tmp/maven-debian-helper_2.3.2_all.deb

# javascript bindings
RUN wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add -
RUN echo "deb https://deb.nodesource.com/node_10.x stretch main" >> /etc/apt/sources.list
RUN DEBIAN_FRONTEND=noninteractive apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install nodejs

# openhab bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports git

# perl bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports perl libterm-readkey-perl libgd-perl libb-lint-perl libdata-dump-perl libperl-critic-perl libmodule-starter-perl libmodule-build-perl

# FIXME: libb-lint-perl 1.20 in Debian Stretch is broken, install 1.22 manually instead
RUN wget http://ftp.de.debian.org/debian/pool/main/libb/libb-lint-perl/libb-lint-perl_1.22-1_all.deb -O /tmp/libb-lint-perl_1.22-1_all.deb
RUN DEBIAN_FRONTEND=noninteractive dpkg -i /tmp/libb-lint-perl_1.22-1_all.deb

# python bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports python python3 pylint pylint3 python-pil python3-pil python-setuptools python3-setuptools

# php bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports php-pear

# ruby bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports ruby gem2deb
COPY gem2deb-sha256.patch /tmp/gem2deb-sha256.patch
RUN patch -p1 < /tmp/gem2deb-sha256.patch

# rust bindings
USER foobar
RUN wget https://sh.rustup.rs -O /tmp/rustup-init.sh
RUN bash /tmp/rustup-init.sh -y --default-toolchain nightly-2020-10-24 -c rustfmt-preview
USER root
RUN ln -s /home/foobar/.cargo/bin/* /usr/local/bin/

# vbnet bindings
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -t stretch-backports mono-vbnc

# user 2/2
USER foobar
RUN git config --global user.email "foobar@tinkerforge.com"
RUN git config --global user.name "foobar"
