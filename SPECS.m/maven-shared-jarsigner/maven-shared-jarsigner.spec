Name:             maven-shared-jarsigner
Version:          1.3.2
Release:          4%{?dist}
Summary:          Component to assist in signing Java archives
License:          ASL 2.0
URL:              http://maven.apache.org/shared/maven-jarsigner/
BuildArch:        noarch

Source0:          http://repo1.maven.org/maven2/org/apache/maven/shared/maven-jarsigner/%{version}/maven-jarsigner-%{version}-source-release.zip

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-utils) >= 0.6
BuildRequires:  mvn(org.apache.maven:maven-toolchain)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)

%description
Apache Maven Jarsigner is a component which provides utilities to sign
and verify Java archive and other files in your Maven MOJOs.

%package javadoc
Summary:          API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -qn maven-jarsigner-%{version}
find -name \*.jar -delete

%build
# Tests require bundled JARs, which are removed.
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE README.TXT

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.3.2-4
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 1.3.2-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 24 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.2-1
- Update to upstream version 1.3.2

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.3.1-2
- Use Requires: java-headless rebuild (#1067528)

* Tue Jan  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.1-1
- Update to upstream version 1.3.1

* Mon Jan  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-2
- Remove bundled JARs and skip tests

* Thu Jan  2 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-1
- Initial packaging
