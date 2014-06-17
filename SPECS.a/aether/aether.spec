%global vertag v20140518

Name:           aether
Epoch:          1
Version:        1.0.0
Release:        3%{?dist}
Summary:        Library to resolve, install and deploy artifacts the Maven way
License:        EPL
URL:            http://eclipse.org/aether
BuildArch:      noarch

Source0:        http://git.eclipse.org/c/%{name}/%{name}-core.git/snapshot/%{name}-%{version}.%{vertag}.tar.bz2

Patch1:         0001-Revert-Bug-433953-Remove-support-for-Plexus-IoC-fram.patch

BuildRequires:  maven-local
BuildRequires:  mvn(com.google.inject:guice::no_aop:)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin) >= 1.7
BuildRequires:  mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.hamcrest:hamcrest-library)
BuildRequires:  mvn(org.slf4j:jcl-over-slf4j)
BuildRequires:  mvn(org.slf4j:slf4j-api)

%description
Aether is a standalone library to resolve, install and deploy artifacts
the Maven way.

%package api
Summary: Aether API

%description api
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides application
programming interface for Aether repository system.

%package connector-basic
Summary: Aether Connector Basic

%description connector-basic
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides repository connector
implementation for repositories using URI-based layouts.

%package impl
Summary: Implementation of Aether repository system

%description impl
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides implementation of
Aether repository system.

%package spi
Summary: Aether SPI

%description spi
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package contains Aether service
provider interface (SPI) for repository system implementations and
repository connectors.

%package test-util
Summary: Aether test utilities

%description test-util
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides collection of utility
classes that ease testing of Aether repository system.

%package transport-classpath
Summary: Aether Transport Classpath

%description transport-classpath
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides a transport
implementation for repositories using classpath:// URLs.

%package transport-file
Summary: Aether Transport File
Obsoletes: %{name}-connector-file < %{epoch}:%{version}-%{release}

%description transport-file
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides a transport
implementation for repositories using file:// URLs.

%package transport-http
Summary: Aether Transport HTTP
Obsoletes: %{name}-connector-asynchttpclient < %{epoch}:%{version}-%{release}

%description transport-http
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides a transport
implementation for repositories using http:// and https:// URLs.

%package transport-wagon
Summary: Aether Transport Wagon
Obsoletes: %{name}-connector-wagon < %{epoch}:%{version}-%{release}

%description transport-wagon
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides a transport
implementation based on Maven Wagon.

%package util
Summary: Aether utilities

%description util
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides a collection of
utility classes to ease usage of Aether repository system.

%package javadoc
Summary: Java API documentation for Aether

%description javadoc
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides Java API documentation
for Aether.

%prep
%setup -q -n %{name}-%{version}.%{vertag}
%patch1 -p1

# Remove clirr plugin
%pom_remove_plugin :clirr-maven-plugin
%pom_remove_plugin :clirr-maven-plugin aether-api
%pom_remove_plugin :clirr-maven-plugin aether-util
%pom_remove_plugin :clirr-maven-plugin aether-spi

# Animal sniffer is not useful in Fedora
for module in . aether-api aether-connector-basic aether-impl   \
              aether-spi aether-test-util aether-transport-file \
              aether-transport-classpath aether-transport-http  \
              aether-transport-wagon aether-util; do
    %pom_remove_plugin :animal-sniffer-maven-plugin $module
done

# HTTP transport tests require Jetty 7 and networking.
rm -rf aether-transport-http/src/test
%pom_xpath_remove "pom:dependency[pom:scope='test']" aether-transport-http

%pom_remove_plugin :maven-enforcer-plugin

# Upstream uses Sisu 0.0.0.M4, but Fedora has 0.0.0.M5.  In M5 scope
# of Guice dependency was changed from "compile" to "provided".
%pom_add_dep com.google.inject:guice::provided . "<classifier>no_aop</classifier>"

%build
%mvn_build -s

%install
%mvn_install

%files -f .mfiles-%{name}
%doc README.md
%doc epl-v10.html notice.html

%files api -f .mfiles-%{name}-api
%doc README.md
%doc epl-v10.html notice.html
%dir %{_javadir}/%{name}

%files connector-basic -f .mfiles-%{name}-connector-basic
%files impl -f .mfiles-%{name}-impl
%files spi -f .mfiles-%{name}-spi
%files test-util -f .mfiles-%{name}-test-util
%files transport-classpath -f .mfiles-%{name}-transport-classpath
%files transport-file -f .mfiles-%{name}-transport-file
%files transport-http -f .mfiles-%{name}-transport-http
%files transport-wagon -f .mfiles-%{name}-transport-wagon
%files util -f .mfiles-%{name}-util
%files javadoc -f .mfiles-javadoc
%doc epl-v10.html notice.html

%changelog
* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1:1.0.0-3
- 为 Magic 3.0 重建

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0.0-2
- Bring back Plexus support

* Tue May 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0.0-1
- Update to upstream version 1.0.0

* Tue Apr  1 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.9.1-1
- Update to upstream version 0.9.1

* Thu Feb 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.9.0-1
- Update to upstream version 0.9.0

* Mon Jan  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.9.0-0.5.M4
- Update to upstream version 0.9.0.M4
- Remove workaround for rhbz#911365

* Wed Aug 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.9.0-0.4.M3
- Add missing Obsoletes: aether-connector-file
- Resolves: rhbz#996764

* Mon Aug 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.9.0-0.3.M3
- Update to upstream version 0.9.0.M3

* Thu Jul 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.9.0-0.2.M2
- Remove remains of Sonatype Aether
- Port from Sonatype Sisu to Eclipse Sisu, resolves: rhbz#985691

* Fri Jul 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.9.0-0.M2.1
- Switch upstream from Sonatype to Eclipse
- Update to upstream version 0.9.0.M2
- Install Sonatype Aether in pararell to Eclipse Aether

* Fri Jul 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-12
- Add symlinks to Sonatype Aether

* Wed Jun 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-11
- Install license files
- Resolves: rhbz#958116

* Fri May 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-10
- Conditionally build without AHC connector

* Thu May  2 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-9
- Install compat JAR symlinks
- Resolves: rhbz#958558

* Tue Apr 30 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-8
- Complete spec file rewrite
- Build with xmvn
- Split into multiple subpackages, resolves: rhbz#916142
- Update to current packaging guidelines

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-7
- Build with xmvn
- Disable animal sniffer
- Remove R on jboss-parent, resolves: rhbz#908583

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.13.1-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Aug 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-5
- Disable animal-sniffer on RHEL

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-3
- Replace pom.xml patches with pom macros

* Thu Apr 19 2012 Alexander Kurtakov <akurtako@redhat.com> 1.13.1-2
- Install aether-connector-asynchttpclient - it was build but not installed.

* Tue Jan 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.13.1-1
- Update to latest upstream
- Update spec to latest guidelines

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 8 2011 Alexander Kurtakov <akurtako@redhat.com> 1.11-3
- Build with maven 3.x.
- Do not require maven - not found in dependencies in poms.
- Guidelines fixes.

* Mon Feb 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.11-2
- Rebuild after bugfix update to plexus-containers (#675865)

* Fri Feb 25 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.11-1
- Update to latest version
- Add ASL 2.0 back as optional license

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.9-1
- License changed to EPL
- Add async-http-client to BR/R
- Update to latest version

* Wed Dec  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-3
- Make jars/javadocs versionless
- Remove buildroot and clean section

* Wed Oct 13 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-2
- Explained how to get tarball properly
- Removed noreplace on depmap fragment

* Mon Oct 11 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-1
- Initial Package
