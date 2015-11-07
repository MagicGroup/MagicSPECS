%global registry geronimo-osgi-registry
%global locator geronimo-osgi-locator

Name:             geronimo-osgi-support
Version:          1.0
Release:          18%{?dist}
Summary:          OSGI spec bundle support
License:          ASL 2.0 and W3C
URL:              http://geronimo.apache.org/

Source0:          http://repo2.maven.org/maven2/org/apache/geronimo/specs/%{name}/%{version}/%{name}-%{version}-source-release.tar.gz
BuildArch:        noarch

BuildRequires:    java-devel >= 1:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    maven-local
BuildRequires:    felix-osgi-core
BuildRequires:    felix-osgi-compendium
BuildRequires:    geronimo-parent-poms
BuildRequires:    maven-resources-plugin


Provides:         geronimo-osgi-locator = %{version}-%{release}
Provides:         geronimo-osgi-registry = %{version}-%{release}

%description
This project is a set of bundles and integration tests for implementing
OSGi-specific lookup in the Geronimo spec projects.


%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
iconv -f iso8859-1 -t utf-8 LICENSE > LICENSE.conv && mv -f LICENSE.conv LICENSE
sed -i 's/\r//' LICENSE NOTICE
# Use parent pom files instead of unavailable 'genesis-java5-flava'
%pom_set_parent org.apache.geronimo.specs:specs:1.4

# Remove itests due to unavailable dependencies
%pom_disable_module geronimo-osgi-itesta
%pom_disable_module geronimo-osgi-itestb
%pom_disable_module geronimo-osgi-registry-itests
%pom_disable_module geronimo-osgi-locator-itests

%pom_xpath_inject "pom:plugin[pom:artifactId[text()='maven-bundle-plugin']]
                       /pom:configuration/pom:instructions" "
    <Export-Package>!*</Export-Package>" geronimo-osgi-locator

# preserve compatibility locations for jars
%mvn_file ':{*}' @1

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.0-18
- 为 Magic 3.0 重建

* Tue Aug 12 2014 Liu Di <liudidi@gmail.com> - 1.0-17
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-15
- Use Requires: java-headless rebuild (#1067528)

* Thu Aug 08 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-14
- Update to latest packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-11
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Dec 07 2012 Jaromir Capik <jcapik@redhat.com> 1.0-10
- Depmap removed (not needed anymore)
- Removing EOL whitespaces in the spec file

* Thu Aug 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-9
- Fix license tag
- Install NOTICE files

* Mon Aug  6 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-8
- Add explicit OSGi export, resolves 812827

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-5
- Build with maven 3 - site-plugin no longer works with maven2.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 2 2010 Chris Spike <chris.spike@arcor.de> 1.0-3
- Removed W3C from 'License:' field (XMLSchema.dtd not existent)

* Thu Jul 29 2010 Chris Spike <chris.spike@arcor.de> 1.0-2
- Fixed wrong EOL encoding in LICENSE
- Fixed LICENSE file-not-utf8
- Added W3C to 'License:' field
- Added patch explanations

* Mon Jul 26 2010 Chris Spike <chris.spike@arcor.de> 1.0-1
- Initial version of the package
