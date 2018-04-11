# jetty8 is a compat package and as such it shouldn't have any OSGi provides
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^osgi\\(

%global addver v20150415

Name:           jetty8
Version:        8.1.17
Release:        5%{?dist}
Summary:        Java Webserver and Servlet Container
# Jetty is dual licensed under both ASL 2.0 and EPL 1.0, see NOTICE.txt
# some MIT-licensed code (from Utf8Appendable) is used too
License:        (ASL 2.0 or EPL) and MIT
URL:            http://www.eclipse.org/jetty
BuildArch:      noarch

Source0:        http://git.eclipse.org/c/jetty/org.eclipse.jetty.project.git/snapshot/org.eclipse.jetty.project-jetty-%{version}.%{addver}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.eclipse.jetty:jetty-parent:pom:)
BuildRequires:  mvn(org.eclipse.jetty.toolchain:jetty-artifact-remote-resources)
BuildRequires:  mvn(org.eclipse.jetty.toolchain:jetty-assembly-descriptors)
BuildRequires:  mvn(org.eclipse.jetty.toolchain:jetty-build-support)
BuildRequires:  mvn(org.eclipse.jetty.toolchain:jetty-version-maven-plugin)
BuildRequires:  mvn(org.eclipse.jetty.toolchain:jetty-test-policy)
BuildRequires:  mvn(org.jboss.spec.javax.servlet:jboss-servlet-api_3.0_spec)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-jdk14)

Requires:       %{name}-rewrite = %{version}-%{release}
Requires:       %{name}-client = %{version}-%{release}
Requires:       %{name}-xml = %{version}-%{release}
Requires:       %{name}-websocket = %{version}-%{release}
Requires:       %{name}-webapp = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}
Requires:       %{name}-servlet = %{version}-%{release}
Requires:       %{name}-server = %{version}-%{release}
Requires:       %{name}-security = %{version}-%{release}
Requires:       %{name}-jmx = %{version}-%{release}
Requires:       %{name}-io = %{version}-%{release}
Requires:       %{name}-http = %{version}-%{release}
Requires:       %{name}-continuation = %{version}-%{release}

%description
Jetty is a 100% Java HTTP Server and Servlet Container. This means that you
do not need to configure and run a separate web server (like Apache) in order
to use Java, servlets and JSPs to generate dynamic content. Jetty is a fully
featured web server for static and dynamic content. Unlike separate
server/container solutions, this means that your web server and web
application run in the same process, without interconnection overheads
and complications. Furthermore, as a pure java component, Jetty can be simply
included in your application for demonstration, distribution or deployment.
Jetty is available on all Java supported platforms.

%package        rewrite
Summary:        Jetty rewrite handler
%description    rewrite
This package contains %{summary}.

%package        client
Summary:        Jetty asynchronous HTTP client
%description    client
This package contains %{summary}.

%package        xml
Summary:        Jetty XML utilities
%description    xml
This package contains %{summary}.

%package        websocket
Summary:        Jetty websocket
%description    websocket
This package contains %{summary}.

%package        webapp
Summary:        Jetty web application support
%description    webapp
This package contains %{summary}.

%package        util
Summary:        Jetty utility classes
%description    util
This package contains %{summary}.

%package        servlet
Summary:        Jetty servlet container
%description    servlet
This package contains %{summary}.

%package        server
Summary:        Jetty server artifact
%description    server
This package contains %{summary}.

%package        security
Summary:        Jetty security infrastructure
%description    security
This package contains %{summary}.

%package        jmx
Summary:        Jetty JMX management artifact
%description    jmx
This package contains %{summary}.

%package        io
Summary:        Jetty IO utility
%description    io
This package contains %{summary}.

%package        http
Summary:        Jetty HTTP utility
%description    http
This package contains %{summary}.

%package        continuation
Summary:        Jetty asynchronous API
%description    continuation
This package contains %{summary}.

%package        deploy
Summary:        Jetty deployers
%description    deploy
This package contains %{summary}.

%package        servlets
Summary:        Jetty utility servlets and filters
%description    servlets
This package contains %{summary}.

%package        javadoc
Summary:        API documentation for %{name}

%description    javadoc
This package provides %{summary}.

%prep
%setup -q -n jetty-%{version}.%{addver}
find -name "*.jar" -delete
find -name "*.war" -delete
find -name "*.class" -delete

%mvn_compat_version : 8.1 %{version}.%{addver} 8.1.14.v20131031

# aggregating POM belongs to main package
%mvn_package :jetty-project::pom

%pom_change_dep -r org.eclipse.jetty.orbit:javax.servlet org.jboss.spec.javax.servlet:jboss-servlet-api_3.0_spec

# Disable unneeded modules. This is a compat package and only a
# minimal set of modules are being built.
%pom_xpath_remove "pom:modules"
%pom_xpath_inject "pom:project" "<modules/>"
for mod in continuation deploy http io jmx security server servlet servlets util webapp websocket xml client rewrite; do
  %pom_xpath_inject pom:modules "<module>jetty-$mod</module>"
  %pom_xpath_inject 'pom:plugin[pom:artifactId="maven-bundle-plugin"]/pom:executions/pom:execution' '
     <phase>process-classes</phase>' jetty-$mod
done

# PMD plugin is not useful in Fedora.
%pom_remove_plugin -r :maven-pmd-plugin

%pom_remove_plugin -r :maven-license-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
%pom_remove_plugin -r :maven-release-plugin
%pom_remove_plugin -r :maven-source-plugin
%pom_remove_plugin -r :maven-site-plugin

# this needs jetty6 things, so just remove it
# shouldn't cause any trouble since it handled only in loadClass elsewhere
%pom_remove_dep org.mortbay.jetty:jetty-util jetty-continuation
rm jetty-continuation/src/main/java/org/eclipse/jetty/continuation/Jetty6Continuation.java

# Disable default-jar executions of maven-jar-plugin in certain Jetty
# modules, which define their own executions of the plugin.  This
# avoids problems with version 3.0.0 of the plugin.
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-jar-plugin']/pom:executions" "
      <execution>
        <id>default-jar</id>
        <phase>skip</phase>
      </execution>" \
    jetty-continuation \
    jetty-http \
    jetty-io \
    jetty-server \
    jetty-websocket \

# CCLAs and CLAs, we don't want to install these
rm -Rf LICENSE-CONTRIBUTOR/

%build
# Tests disabled because of missing dependencies
%mvn_build -f -s

%install
%mvn_install

%files -f .mfiles-jetty-project
%{!?_licensedir:%global license %%doc}
%license NOTICE.txt README.txt VERSION.txt LICENSE*

%files rewrite -f .mfiles-jetty-rewrite
%files client -f .mfiles-jetty-client
%files deploy -f .mfiles-jetty-deploy
%files xml -f .mfiles-jetty-xml
%files websocket -f .mfiles-jetty-websocket
%files webapp -f .mfiles-jetty-webapp
%files util -f .mfiles-jetty-util
%license NOTICE.txt LICENSE*
%files servlet -f .mfiles-jetty-servlet
%files servlets -f .mfiles-jetty-servlets
%files server -f .mfiles-jetty-server
%files security -f .mfiles-jetty-security
%files jmx -f .mfiles-jetty-jmx
%files io -f .mfiles-jetty-io
%files http -f .mfiles-jetty-http
%files continuation -f .mfiles-jetty-continuation

%files javadoc -f .mfiles-javadoc
%license NOTICE.txt LICENSE*

%changelog
* Tue May 31 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.17-5
- Fix build issue with maven-jar-plugin 3.0.0

* Thu Mar 24 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.17-4
- Enable deploy and servlets modules

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 04 2015 Michael Simacek <msimacek@redhat.com> - 8.1.17-2
- Adjust bundle-plugin configuration

* Fri Jul 03 2015 Michal Srb <msrb@redhat.com> - 8.1.17-1
- Update to upstream release 8.1.17

* Fri Jul 03 2015 Michal Srb <msrb@redhat.com> - 8.1.14-11
- Move artifacts into subpackages

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 30 2015 Michael Simacek <msimacek@redhat.com> - 8.1.14-9
- Use jboss-servlet-3.0-api as tomcat no longer provides 3.0

* Mon Jul 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.14-8
- Don't generate OSGi provides
- Resolves: rhbz#1079675

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Timothy St. Clair <tstclair@redhat.com> - 8.1.14-6
- Rebuild for metadata change from xmvn

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.14-5
- Use Requires: java-headless rebuild (#1067528)

* Tue Feb 4 2014 Peter MacKinnon <pmackinn@redhat.com> - 8.1.14-4
- Add maven-dependency-plugin, jetty-test-policy deps

* Tue Feb 4 2014 Peter MacKinnon <pmackinn@redhat.com> - 8.1.14-3
- Enable rewrite, client modules

* Fri Jan 31 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.14-2
- Enable websocket module

* Mon Jan 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.14-1
- Initial packaging
