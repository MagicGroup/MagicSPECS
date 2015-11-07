%global bundle org.apache.felix.gogo.command

%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package felix-gogo-command}

Name:           %{?scl_prefix}felix-gogo-command
Version:        0.14.0
Release:        3%{?dist}
Summary:        Apache Felix Gogo Command

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://felix.apache.org
Source0:        http://www.apache.org/dist/felix/%{bundle}-%{version}-project.tar.gz

Patch0:         felix-gogo-command-pom.xml.patch
Patch1:         java7compatibility.patch

BuildArch:      noarch

BuildRequires:  java
# This is to ensure we get OpenJDK and not GCJ
BuildRequires:  java-devel >= 1:1.7.0
BuildRequires:  maven-local
BuildRequires:  maven-dependency-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-install-plugin
BuildRequires:  mockito

BuildRequires:  felix-osgi-core
BuildRequires:  felix-framework
BuildRequires:  felix-osgi-compendium
BuildRequires:  %{?scl_prefix}felix-gogo-runtime >= 0.12.0
BuildRequires:  %{?scl_prefix}felix-gogo-parent
BuildRequires:  mvn(org.apache.felix:org.apache.felix.bundlerepository)
%{?scl:BuildRequires:	  %{?scl_prefix}build}

Requires:       felix-framework
Requires:       felix-osgi-compendium
Requires:       %{?scl_prefix}felix-gogo-runtime >= 0.12.0
Requires:       mvn(org.apache.felix:org.apache.felix.bundlerepository)
%{?scl:Requires: %scl_runtime}

%description
Provides basic shell commands for Gogo.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{bundle}-%{version} 
%patch0 -p1
%patch1 -p1

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 0.14.0-3
- 为 Magic 3.0 重建

* Thu Jul 03 2014 Mat Booth <mat.booth@redhat.com> - 0.14.0-2
- BR/R: gogo-runtime >= 0.12.0

* Thu Jul 3 2014 Alexander Kurtakov <akurtako@redhat.com> 0.14.0-1
- Update to 0.14.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Alexander Kurtakov <akurtako@redhat.com> 0.12.0-10
- Start using mvn_build/install.

* Mon Aug 5 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-9
- Fix FTBS.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-7
- Initial SCLization.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.12.0-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-3
- Dependency to Java 7 added.
- Sources are patched to compile with OpenJDK 7.

* Tue Jan 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-2
- description formatting removed
- jar_repack removed
- license added to the javadoc

* Tue Jan 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-1
- Release 0.12.0
