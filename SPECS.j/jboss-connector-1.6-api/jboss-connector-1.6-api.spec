%global namedreltag .20120310git9dc9a5
%global namedversion %{version}%{?namedreltag}

Name:             jboss-connector-1.6-api
Version:          1.0.1
Release:          0.9%{namedreltag}%{?dist}
Summary:          Connector Architecture 1.6 API
Group:            Development/Libraries
License:          CDDL or GPLv2 with exceptions
URL:              http://www.jboss.org

# git clone git://github.com/jboss/jboss-connector-api_spec.git jboss-connector-1.6-api
# cd jboss-connector-1.6-api/ && git archive --format=tar --prefix=jboss-connector-1.6-api/ 9dc9a58fb8672609790db93abcaac3875901243c | xz > jboss-connector-1.6-api-1.0.1.20120310git9dc9a5.tar.xz

Source0:          %{name}-%{namedversion}.tar.xz

BuildRequires:    java-devel
BuildRequires:    jboss-specs-parent
BuildRequires:    jpackage-utils
BuildRequires:    maven-local
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-enforcer-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    jboss-transaction-1.1-api

Requires:         java
Requires:         jboss-transaction-1.1-api
Requires:         jpackage-utils

BuildArch:        noarch

%description
Java EE Connector Architecture 1.6 API classes

%package javadoc
Summary:          Javadocs for %{name}
Group:            Documentation
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}

%build
mvn-rpmbuild install javadoc:aggregate

%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# JAR
install -pm 644 target/jboss-connector-api_1.6_spec-%{version}-SNAPSHOT.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# POM
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

# DEPMAP
%add_maven_depmap JPP-%{name}.pom %{name}.jar

# APIDOCS
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/*
%{_datadir}/maven-metadata/jboss-connector-1.6-api.xml
#%{_mavendepmapfragdir}/*
%doc README LICENSE

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.0.1-0.9.20120310git9dc9a5
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.0.1-0.8.20120310git9dc9a5
- 为 Magic 3.0 重建

* Fri Aug 15 2014 Liu Di <liudidi@gmail.com> - 1.0.1-0.7.20120310git9dc9a5
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.6.20120310git9dc9a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.5.20120310git9dc9a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.1-0.4.20120310git9dc9a5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Aug 6 2012 Ricardo Arguello <ricardo@fedoraproject.org> - 1.0.1-0.3.20120310git9dc9a5
- Added BR: maven-enforcer-plugin

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.2.20120310git9dc9a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Ricardo Arguello <ricardo@fedoraproject.org> 1.0.1-0.1.20120310git9dc9a5
- Packaging after license cleanup upstream

* Thu Mar 8 2012 Ricardo Arguello <ricardo@fedoraproject.org> 1.0.0-2
- Cleanup of the spec file

* Mon Nov 21 2011 Marek Goldmann <mgoldman@redhat.com> 1.0.0-1
- Initial packaging
