Name:           maven-verifier
Version:        1.5
Release:        7%{?dist}
Summary:        Maven verifier
License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-verifier
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-utils)

Obsoletes:      maven-shared-verifier < %{version}-%{release}
Provides:       maven-shared-verifier = %{version}-%{release}

%description
Provides a test harness for Maven integration tests.

This is a replacement package for maven-shared-verifier

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
    
%description javadoc
API documentation for %{name}.


%prep
%setup -q

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 1.5-7
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.5-6
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 1.5-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5-3
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5-2
- Fix unowned directory

* Mon Dec 09 2013 Michal Srb <msrb@redhat.com> - 1.5-1
- Update to upstream version 1.5

* Thu Oct  3 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-6
- Add missing BR: maven-shared

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-4
- Update to maven-shared-utils 0.3

* Fri Feb 08 2013 Tomas Radej <tradej@redhat.com> - 1.4-3
- Building the new way

* Thu Jan 24 2013 Tomas Radej <tradej@redhat.com> - 1.4-2
- Added BuildRequires on maven-shared-utils

* Wed Jan 16 2013 Tomas Radej <tradej@redhat.com> - 1.4-1
- Initial version

