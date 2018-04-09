Name:          prometheus-java-simpleclient
Version:       0.3.0
Release:       1%{?dist}
Summary:       Prometheus instrumentation library for JVM applications
License:       ASL 2.0 and CC0
URL:           https://github.com/yaacov/client_java/
Source0:       https://github.com/yaacov/client_java/archive/parent-%{version}.tar.gz
BuildArch:     noarch

Patch0: https://raw.githubusercontent.com/yaacov/client_java/master/base-0.3.0.patch

BuildRequires: maven-local
BuildRequires: maven-plugin-bundle
BuildRequires: mockito
BuildRequires: assertj-core
BuildRequires: jetty8-servlet
BuildRequires: jboss-servlet-3.0-api
BuildRequires: sonatype-oss-parent

%description
Prometheus JVM Client supports Java, Clojure, Scala,
JRuby, and anything else that runs on the JVM.

%package parent
Summary:       Prometheus Java Suite Parent POM

%description parent
Prometheus Java Suite Parent POM.

%package common
Summary:       Prometheus Java Simpleclient Common

%description common
Common code used by various modules of the Simpleclient.

%package servlet
Summary:       Prometheus Java Simpleclient Servlet

%description servlet
HTTP servlet exporter for the simpleclient.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n client_java-parent-%{version}

%pom_disable_module simpleclient_caffeine
%pom_disable_module simpleclient_dropwizard
%pom_disable_module simpleclient_graphite_bridge
%pom_disable_module simpleclient_hibernate
%pom_disable_module simpleclient_guava
%pom_disable_module simpleclient_hotspot
%pom_disable_module simpleclient_httpserver
%pom_disable_module simpleclient_log4j
%pom_disable_module simpleclient_log4j2
%pom_disable_module simpleclient_logback
%pom_disable_module simpleclient_pushgateway
%pom_disable_module simpleclient_spring_web
%pom_disable_module simpleclient_spring_boot
%pom_disable_module simpleclient_jetty
%pom_disable_module simpleclient_jetty_jdk8
%pom_disable_module simpleclient_vertx
%pom_disable_module benchmark

%pom_remove_plugin :maven-deploy-plugin
%pom_remove_plugin :maven-release-plugin

%patch0 -p0

%build
%mvn_build -s

%install
%mvn_install

%files -f .mfiles-simpleclient
%doc README.md
%license LICENSE NOTICE

%files parent -f .mfiles-parent
%license LICENSE NOTICE

%files common -f .mfiles-simpleclient_common
%license LICENSE NOTICE

%files servlet -f .mfiles-simpleclient_servlet
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Mon Apr 2 2018 Yaacov Zamir <yzamir@redhat.com> - 0.3.0-1
- Initial packaging
