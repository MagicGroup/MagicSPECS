%global spec_ver 1.3
%global spec_name geronimo-saaj_%{spec_ver}_spec

Name:             geronimo-saaj
Version:          1.1
Release:          18%{?dist}
Summary:          Java EE: SOAP with Attachments API Package v1.3
License:          ASL 2.0 and W3C

URL:              http://geronimo.apache.org/
Source0:          http://repo2.maven.org/maven2/org/apache/geronimo/specs/%{spec_name}/%{version}/%{spec_name}-%{version}-source-release.tar.gz
BuildArch:        noarch

BuildRequires:    java-devel >= 1:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    maven-local
BuildRequires:    geronimo-parent-poms
BuildRequires:    maven-resources-plugin
BuildRequires:    geronimo-osgi-locator

Provides:         saaj_api = %{spec_ver}


%description
Provides the API for creating and building SOAP messages.

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{spec_name}-%{version}
iconv -f iso8859-1 -t utf-8 LICENSE > LICENSE.conv && mv -f LICENSE.conv LICENSE
sed -i 's/\r//' LICENSE NOTICE
# Use parent pom files instead of unavailable 'genesis-java5-flava'
%pom_set_parent org.apache.geronimo.specs:specs:1.4
%pom_remove_dep :geronimo-activation_1.1_spec

%mvn_alias : org.apache.geronimo.specs:geronimo-saaj_1.1_spec
%mvn_alias : javax.xml.soap:saaj-api

%mvn_file : %{name}

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.1-18
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.1-17
- 为 Magic 3.0 重建

* Tue Aug 12 2014 Liu Di <liudidi@gmail.com> - 1.1-16
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-14
- Use Requires: java-headless rebuild (#1067528)

* Thu Aug  8 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-13
- Update to latest packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-11
- Replace local depmap with POM macro
- Resolves: rhbz#914030

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1-9
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Aug 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-8
- Fix license tag
- Remove dangling symlink
- Update to current guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Alexander Kurtakov <akurtako@redhat.com> 1.1-5
- Build with Maven 3.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 4 2010 Chris Spike <chris.spike@arcor.de> 1.1-3
- Added 'org.apache.geronimo.specs:geronimo-saaj_1.1_spec' to maven depmap

* Mon Aug 2 2010 Chris Spike <chris.spike@arcor.de> 1.1-2
- Consistently using 'rm' now
- Removed W3C from 'License:' field (XMLSchema.dtd not existent)

* Thu Jul 22 2010 Chris Spike <chris.spike@arcor.de> 1.1-1
- Initial version of the package
