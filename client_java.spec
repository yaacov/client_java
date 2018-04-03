Name:          prometheus-java-simpleclient
Version:       0.3.0
Release:       1%{?dist}
Summary:       Prometheus instrumentation library for JVM applications
License:       ASL 2.0 and CC0
URL:           https://github.com/yaacov/client_java/
Source0:       https://github.com/yaacov/client_java/archive/parent-%{version}.tar.gz
BuildArch:     noarch

BuildRequires: maven-local
BuildRequires: maven-plugin-bundle
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-assembly-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: jetty8-servlet
BuildRequires: jetty8-http
BuildRequires: glassfish-servlet-api
BuildRequires: sonatype-oss-parent

%description
Prometheus JVM Client supports Java, Clojure, Scala,
JRuby, and anything else that runs on the JVM.

%package common
Summary:       Prometheus Java Simpleclient Common

%description common
Common code used by various modules of the Simpleclient.

%package parent
Summary:       Prometheus Java Suite Parent POM

%description parent
Prometheus Java Suite Parent POM.

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
#%pom_disable_module simpleclient_servlet
%pom_disable_module simpleclient_spring_web
%pom_disable_module simpleclient_spring_boot
%pom_disable_module simpleclient_jetty
%pom_disable_module simpleclient_jetty_jdk8
%pom_disable_module simpleclient_vertx
%pom_disable_module benchmark

%pom_remove_plugin :maven-deploy-plugin
%pom_remove_plugin :maven-release-plugin

%build
%mvn_build -s

%install
%mvn_install

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%files parent -f .mfiles-parent
%license LICENSE NOTICE

%files -f .mfiles-simpleclient
%doc README.md
%doc LICENSE NOTICE
%dir %{_javadir}/%{name}

%files common -f .mfiles-simpleclient_common

%files servlet -f .mfiles-simpleclient_servlet

%changelog
* Mon Apr 2 2018 Yaacov Zamir <yzamir@redhat.com> - 0.3.0-1
- Initial packaging
