# Eclipse does not yet export virtual maven provides, so filter out the requires
%global __requires_exclude mvn\\(org\\.eclipse\\.core:resources\\)

Name:           maven-eclipse-plugin
Version:        2.9
Release:        11%{?dist}
Summary:        Maven Eclipse Plugin

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-eclipse-plugin/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
Patch0:         %{name}-compat.patch
Patch1:         %{name}-exception.patch
Patch2:         %{name}-ioexception.patch

%if 0%{?rhel} >= 6
ExclusiveArch: %{ix86} x86_64
%else
BuildArch: noarch
%endif

# Basic stuff
BuildRequires: jpackage-utils
BuildRequires: java-devel >= 1:1.6.0

# Maven and its dependencies
BuildRequires: maven-local
BuildRequires: maven-test-tools
BuildRequires: maven-plugin-testing-tools
# Others
BuildRequires: apache-commons-io
BuildRequires: xmlunit
BuildRequires: eclipse-platform
BuildRequires: plexus-resources
BuildRequires: bsf
BuildRequires: jaxen
BuildRequires: dom4j
BuildRequires: xom
BuildRequires: saxpath

Provides:       maven2-plugin-eclipse = 0:%{version}-%{release}
Obsoletes:      maven2-plugin-eclipse <= 0:2.0.8

%description
The Eclipse Plugin is used to generate Eclipse IDE files (.project, .classpath 
and the .settings folder) from a POM.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.


%prep
%setup -q 
%patch0 -p1
%patch1 -p1
%patch2 -p1

sed -i -e "s|3.3.0-v20070604|3.7.100.v20110510-0712|g" pom.xml

# Remove easymock dependency (tests are skipped)
%pom_remove_dep easymock:

%build
# Create a local repo for the eclipse dependency because eclipse
# does not yet export virtual mvn provides or ship pom files
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
CORE_FAKE_VERSION="3.7.100.v20110510-0712"
CORE_PLUGIN_DIR=$MAVEN_REPO_LOCAL/org/eclipse/core/resources/$CORE_FAKE_VERSION

mkdir -p $CORE_PLUGIN_DIR
plugin_file=`ls /usr/lib{,64}/eclipse/plugins/org.eclipse.core.resources_*jar || :`

ln -s "$plugin_file" $CORE_PLUGIN_DIR/resources-$CORE_FAKE_VERSION.jar

# Skip tests because they do not compile
%mvn_build -- -Dmaven.test.skip=true -Dmaven.repo.local=$MAVEN_REPO_LOCAL

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE DEPENDENCIES README-testing.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 2.9-11
- 为 Magic 3.0 重建

* Fri Aug 15 2014 Liu Di <liudidi@gmail.com> - 2.9-10
- 为 Magic 3.0 重建

* Thu Aug 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-9
- Don't use %%_libdir in noarch package

* Thu Aug 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-8
- Remove dependency on easymock
- Resolves: rhbz#1002477

* Sun Aug 18 2013 Mat Booth <fedora@matbooth.co.uk> - 2.9-7
- Update for newer guidelines rhbz #992186
- Install license files

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Weinan Li <weli@redhat.com> - 2.9-5
- Remove unneeded dependencies on maven-doxia

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.9-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Tomas Radej <tradej@redhat.com> - 2.9-1
- Updated to the upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 9 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-7
- Add exclusive arch for rhel.

* Mon Dec 5 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-6
- Fix build in pure maven 3 environment.

* Fri Jun 17 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-5
- Build with maven 3.x.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 09 2010 Weinan Li <weli@redhat.com> - 2.8-3
- Remove version from BR eclipse-platform

* Fri Jun 25 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.8-2
- Update R/BRs, make eclipse.core.resources path dynamic

* Fri Jun 11 2010 Weinan Li <weli@redhat.com> - 2.8-1
- Initial Package
