%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Name:             jboss-connector-1.6-api
Version:          1.0.1
Release:          2%{?dist}
Summary:          Connector Architecture 1.6 API
Group:            Development/Libraries
License:          CDDL or GPLv2 with exceptions
URL:              http://www.jboss.org

Source0:          https://github.com/jboss/jboss-connector-api_spec/archive/jboss-connector-api_1.6_spec-%{namedversion}.tar.gz

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

BuildArch:        noarch

%description
Java EE Connector Architecture 1.6 API classes

%package javadoc
Summary:          Javadocs for %{name}
Group:            Documentation

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n jboss-connector-api_spec-jboss-connector-api_1.6_spec-%{namedversion}

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc README LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Marek Goldmann <mgoldman@redhat.com> - 1.0.1-1
- Upstream release 1.0.1.Final
- Switch to xmvn

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.7.20120310git9dc9a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

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
