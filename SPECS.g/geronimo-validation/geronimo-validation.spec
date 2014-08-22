%global spec_ver 1.0
%global spec_name geronimo-validation_%{spec_ver}_spec

Name:           geronimo-validation
Version:        1.1
Release:        12%{?dist}
Summary:        Geronimo implementation of JSR 303
License:        ASL 2.0
# should be http://geronimo.apache.org/
URL:            http://apache.org/
# svn export https://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-validation_1.0_spec-1.1/
# tar caf geronimo-validation_1.0_spec-1.1.tar.xz geronimo-validation_1.0_spec-1.1
Source0:        %{spec_name}-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  geronimo-parent-poms
BuildRequires:  geronimo-osgi-support

%description
This is the Geronimo implementation of JSR-303, the Bean
Validation API specification.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{spec_name}-%{version}
%pom_xpath_set "pom:project/pom:parent/pom:groupId" org.apache.geronimo.specs
%pom_xpath_set "pom:project/pom:parent/pom:artifactId" specs
%pom_xpath_set "pom:project/pom:parent/pom:version" 1.4
%pom_xpath_inject "pom:project/pom:parent" "<relativePath>../pom.xml</relativePath>"
%pom_xpath_set "pom:project/pom:packaging" jar

%build
%mvn_file : %{name}
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 1.1-12
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep 11 2013 Marek Goldmann <mgoldman@redhat.com> - 1.1-10
- Removed javax.validation:validation-api alias, bean-validation-api is the RI

* Sat Aug 17 2013 gil cattaneo <puntogil@libero.it> 1.1-9
- fix rhbz#992345
- use pom macros
- minor changes to adapt to current guideline

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Andy Grimm <agrimm@gmail.com> 1.1-3
- add jpackage-utils dep for javadoc subpackage

* Tue Oct 18 2011 Andy Grimm <agrimm@gmail.com> 1.1-2
- add maven fragment mapping for javax.validation

* Mon Oct 17 2011 Andy Grimm <agrimm@gmail.com> 1.1-1
- Initial Build
