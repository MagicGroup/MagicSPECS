Name:             maven-checkstyle-plugin
Version:          2.12
Release:          3%{?dist}
Summary:          Plugin that generates a report regarding the code style used by the developers
Group:            Development/Libraries
License:          ASL 2.0
URL:              http://maven.apache.org/plugins/%{name}

Source0:          http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

Patch0:           %{name}-maven-core-dep.patch

BuildArch:        noarch

BuildRequires:    java-devel >= 1:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    maven-local
BuildRequires:    maven-plugin-plugin >= 2.5.1
BuildRequires:    plexus-containers-component-metadata >= 1.5.1
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-resources-plugin
BuildRequires:    maven-compiler-plugin >= 2.0.2
BuildRequires:    maven-jar-plugin >= 2.2
BuildRequires:    maven-install-plugin >= 2.2
BuildRequires:    checkstyle >= 5.6
BuildRequires:    plexus-cli >= 1.2
BuildRequires:    maven-artifact-manager 
BuildRequires:    plexus-resources
BuildRequires:    maven-doxia-sitetools
BuildRequires:    maven-doxia-sink-api

Provides:         maven2-plugin-checkstyle = %{version}-%{release}
Obsoletes:        maven2-plugin-checkstyle <= 0:2.0.8

%description
Generates a report on violations of code style and optionally fails the build
if violations are detected.

%package javadoc
Group:            Documentation
Summary:          Javadoc for %{name}
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
%patch0 

%build
%mvn_build -f -- -DmavenVersion=3.2.1

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Tue Aug 12 2014 Liu Di <liudidi@gmail.com> - 2.12-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.12-1
- Update to upstream version 2.12
- Update to current packaging guidelines
- Use Maven 3.x APIs

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.10-3
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 23 2013 Mat Booth <fedora@matbooth.co.uk> - 2.10-1
- Update to 2.10, require checkstyle 5.6, rhbz #915219

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.9.1-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan 02 2013 Michal Srb <msrb@redhat.com> - 2.9.1-4
- Migrated from maven-doxia to doxia subpackages (Resolves: #889144)

* Mon Nov 26 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.1-3
- Install NOTICE files
- Resolves: rhbz#880265

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 5 2012 Alexander Kurtakov <akurtako@redhat.com> 2.9.1-1
- Update to 2.9.1.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 2 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-1
- Update to 2.8.

* Thu Sep 15 2011 Tomas Radej <tradej@redhat.com> - 2.7-1
- Updated to 2.7
- Guideline fixes

* Thu Jun 9 2011 Alexander Kurtakov <akurtako@redhat.com> 2.6-5
- Fix checkstyle groupId.

* Thu Jun 9 2011 Alexander Kurtakov <akurtako@redhat.com> 2.6-4
- Build with maven 3.x.
- Guideline fixes.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 5 2010 Chris Spike <chris.spike@arcor.de> 2.6-2
- Changed BR from 'commons-collections' to 'apache-commons-collections'

* Sat Oct 2 2010 Chris Spike <chris.spike@arcor.de> 2.6-1
- Updated to latest upstream version

* Mon Jul 19 2010 Chris Spike <chris.spike@arcor.de> 2.5-3
- Eventually really fixed Requires for plexus-containers-container-default and 
  plexus-resources (#616202)

* Mon Jul 19 2010 Chris Spike <chris.spike@arcor.de> 2.5-2
- Removed BuildArch from javadoc subpackage
- Fixed Requires for plexus-containers-container-default and 
  plexus-resources (#616202)

* Thu Jul 15 2010 Chris Spike <chris.spike@arcor.de> 2.5-1
- Initial version of the package
