%global bundle org.apache.felix.main

Name:    felix-main
Version: 4.4.0
Release: 4%{?dist}
Summary: Apache Felix Main
Group:   Development/Libraries
License: ASL 2.0
URL:     http://felix.apache.org
Source0: http://www.apache.org/dist/felix/%{bundle}-%{version}-source-release.tar.gz

BuildArch: noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils
BuildRequires: felix-bundlerepository
BuildRequires: felix-gogo-command
BuildRequires: felix-gogo-runtime
BuildRequires: felix-gogo-shell
BuildRequires: felix-osgi-compendium
BuildRequires: felix-osgi-core
BuildRequires: felix-parent
BuildRequires: felix-framework >= 4.2.0
BuildRequires: maven-local
BuildRequires: maven-dependency-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: mockito

Requires: felix-bundlerepository
Requires: felix-gogo-command
Requires: felix-gogo-runtime
Requires: felix-gogo-shell
Requires: felix-osgi-compendium
Requires: felix-osgi-core
Requires: felix-framework >= 4.2.0

%description
Apache Felix Main Classes.

%package javadoc
Group:          Documentation
Summary:        API documentation for %{name}

%description javadoc
This package contains API documentation for %{name}.

%prep
%setup -q -n %{bundle}-%{version}

%mvn_file :%{bundle} "felix/%{bundle}"

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE DEPENDENCIES

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 4.4.0-4
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 4.4.0-3
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 4.4.0-2
- 为 Magic 3.0 重建

* Tue Jun 10 2014 Alexander Kurtakov <akurtako@redhat.com> 4.4.0-1
- Update to upstream 4.4.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 4.2.0-5
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 05 2013 Mat Booth <fedora@matbooth.co.uk> - 4.2.0-4
- Update for latest guidelines

* Sat Aug 03 2013 Mat Booth <fedora@matbooth.co.uk> - 4.2.0-3
- Add missing BRs

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 21 2013 Mat Booth <fedora@matbooth.co.uk> - 4.2.0-1
- Update to latest upstream version.
- Update spec to newer guidelines rhbz #810215.
- Fix FTBFS following mass rebuild.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0.5-6
- Fix pom filename (Resolves rhbz#655799)
- Fix BR of surefire-plugin
- Fix various packaging things according to new guidelines

* Mon Jul 26 2010 Victor G. Vasilyev <victor.vasilyev@sun.com> 2.0.5-5
- Remove R: felix-parent

* Mon Jul 26 2010 Victor G. Vasilyev <victor.vasilyev@sun.com> 2.0.5-4
- Use felix-parent https://bugzilla.redhat.com/show_bug.cgi?id=615868
- Remove demap file option from mvn-jpp command

* Sat Jul 24 2010 Victor G. Vasilyev <victor.vasilyev@sun.com> 2.0.5-3
- Add TODOs for uncompleted activities against maven packages
- Use new names of the maven plgins
- Add license file to independent subpackage javadoc
- Remove unneeded demap file

* Tue Jul 13 2010 Victor G. Vasilyev <victor.vasilyev@sun.com> 2.0.5-2
- Use maven instead of ant

* Tue Jun 22 2010 Victor G. Vasilyev <victor.vasilyev@sun.com> 2.0.5-1
- Release 2.0.5
