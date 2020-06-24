#!/bin/sh

# https://maven.apache.org/plugins/maven-toolchains-plugin/index.html

version=3.0.0

rm maven-toolchains-plugin-${version}-source-release.zip
wget https://downloads.apache.org/maven/plugins/maven-toolchains-plugin-${version}-source-release.zip

rm -rf maven-toolchains-plugin-${version}
unzip maven-toolchains-plugin-${version}-source-release.zip
cp -r debian maven-toolchains-plugin-${version}

pushd maven-toolchains-plugin-${version}

JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 dpkg-buildpackage --no-sign

popd

lintian libmaven-toolchains-plugin-java_${version}_all.deb
