Name:           javapackages-tools
Version:        3.5.0
Release:        5%{?dist}

Summary:        Macros and scripts for Java packaging support

License:        BSD
URL:            https://fedorahosted.org/javapackages/
Source0:        https://fedorahosted.org/released/javapackages/javapackages-%{version}.tar.xz

# Add support for installing Maven artifacts with .hpi extension
Patch0:         0001-Add-support-for-installing-hpi.patch

Patch1:         0001-depgenerators-Switch-to-require-java-headless-instea.patch
Patch2:         0002-test-Fix-testsuite-for-java-headless-change.patch

BuildArch:      noarch

BuildRequires:  jpackage-utils
BuildRequires:  asciidoc
BuildRequires:  xmlto
BuildRequires:  python-lxml
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-formencode
BuildRequires:  scl-utils-build
BuildRequires:  python-nose

Requires:       coreutils
Requires:       libxslt
Requires:       lua
Requires:       python
Requires:       python-javapackages = %{version}-%{release}

Provides:       jpackage-utils = %{version}-%{release}
Obsoletes:      jpackage-utils < %{version}-%{release}

%description
This package provides macros and scripts to support Java packaging.

%package -n maven-local
Summary:        Macros and scripts for Maven packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       maven
Requires:       xmvn >= 1.0.0-0.1
# POM files needed by maven itself
Requires:       apache-commons-parent
Requires:       apache-parent
Requires:       geronimo-parent-poms
Requires:       httpcomponents-project
Requires:       jboss-parent
Requires:       jvnet-parent
Requires:       maven-parent
Requires:       maven-plugins-pom
Requires:       mojo-parent
Requires:       objectweb-pom
Requires:       plexus-components-pom
Requires:       plexus-pom
Requires:       plexus-tools-pom
Requires:       sonatype-oss-parent
Requires:       weld-parent
# Common Maven plugins required by almost every build. It wouldn't make
# sense to explicitly require them in every package built with Maven.
Requires:       maven-assembly-plugin
Requires:       maven-compiler-plugin
Requires:       maven-enforcer-plugin
Requires:       maven-jar-plugin
Requires:       maven-javadoc-plugin
Requires:       maven-resources-plugin
Requires:       maven-surefire-plugin
# Tests based on JUnit are very common and JUnit itself is small.
# Include JUnit provider for Surefire just for convenience.
Requires:       maven-surefire-provider-junit
# testng is quite common as well
Requires:       maven-surefire-provider-testng

%description -n maven-local
This package provides macros and scripts to support packaging Maven artifacts.

%package -n ivy-local
Summary:        Local mode for Apache Ivy
Requires:       %{name} = %{version}-%{release}
Requires:       apache-ivy >= 2.3.0-8
Requires:       guava
Requires:       maven
Requires:       plexus-classworlds
Requires:       plexus-containers-container-default
Requires:       plexus-utils
Requires:       xbean
Requires:       xmvn >= 1.5

%description -n ivy-local
This package implements local mode fow Apache Ivy, which allows
artifact resolution using XMvn resolver.

%package -n python-javapackages
Summary:        Module for handling various files for Java packaging
Requires:       python-lxml

%description -n python-javapackages
Module for handling, querying and manipulating of various files for Java
packaging in Linux distributions

%package -n fedora-review-plugin-java
Summary:        fedora-review plugin for checking Java packaging guidelines
License:        GPLv2+
Requires:       fedora-review

%description -n fedora-review-plugin-java
%{summary}.



%prep
%setup -q -n javapackages-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure
./build
pushd python
%{__python} setup.py build
popd

%install
./install
sed -e 's/.[17]$/&.gz/' -e 's/.py$/&*/' -i files-*

pushd python
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd

%check
./check



%files -f files-common
%doc LICENSE

%files -n maven-local -f files-maven

%files -n ivy-local -f files-ivy

%files -n python-javapackages
%doc LICENSE
%{python_sitelib}/javapackages*

%files -n fedora-review-plugin-java
%{_datadir}/fedora-review/plugins/*


%changelog
* Mon Feb 24 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.5.0-5
- Backport java-headless patches

* Mon Feb 10 2014 Michal Srb <msrb@redhat.com> - 3.5.0-4
- Add support for installing Maven artifacts with .hpi extension

* Fri Jan 17 2014 Michael Simacek <msimacek@redhat.com> - 3.5.0-3
- Use upstream method of running tests (nosetests)

* Thu Jan 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.0-2
- Add version requirements on xmvn and ivy

* Thu Jan 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.0-1
- Update to upstream version 3.5.0
- Add ivy-local subpackage

* Tue Jan  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.2-3
- Update patch for ZIP files

* Tue Jan  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.2-2
- Allow ZIP files in %{_javadir}

* Thu Dec 05 2013 Michal Srb <msrb@redhat.com> - 3.4.2-1
- Update to upstream bugfix release 3.4.2

* Wed Dec  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.1-3
- Add Requires on objectweb-pom

* Tue Nov 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4.1-2
- Do not create parent dirs for pom.properties
- Resolves: rhbz#1031769

* Tue Nov 05 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4.1-1
- Update to upstream bugfix release 3.4.1

* Mon Oct 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-3
- Fix XMvn configuration for native JNI repos
- Resolves: rhbz#1021608

* Mon Oct 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-2
- Require exact version of python-javapackages

* Mon Oct 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4.0-1
- Update to upstream version 3.4.0

* Wed Oct  2 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-1
- Update to upstream version 3.3.1
- Remove workaround for sisu-guice no_aop

* Tue Oct 01 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.3.0-1
- Update to upstream version 3.3.0

* Wed Sep 25 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.4-2
- Fix installation of artifacts with classifier

* Tue Sep 24 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.4-1
- Update to upstream version 3.2.4

* Tue Sep 24 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.3-1
- Update to upstream version 3.2.3

* Fri Sep 20 2013 Michal Srb <msrb@redhat.com> - 3.2.2-1
- Update to upstream version 3.2.2

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-1
- Update to upstream version 3.2.1

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.0-1
- Update to upstream version 3.2.0

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-1
- Update to upstream version 3.1.2

* Thu Sep 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.1-1
- Update to upstream version 3.1.1

* Thu Sep 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.0-1
- Update to upstream version 3.1.0

* Mon Sep 16 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-2
- Add depmap for sun.jdk:jconsole

* Fri Sep 13 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-1
- Update to upstream version 3.0.4

* Wed Sep 11 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-1
- Update to upstream version 3.0.3

* Tue Sep 10 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.2-3
- Fix a typo in temporary depmap

* Tue Sep 10 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.2-2
- Make sure we do not provide google guice mapping

* Tue Sep 10 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> 3.0.2-1
- Update to upstream version 3.0.2
- Add separate python-javapackages subpackage
- Add separate fedora-review-plugin-java subpackage
- Enable part of unit tests

* Tue Sep  3 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> 3.0.0-0.2
- Fix javadoc directory override

* Tue Sep  3 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> 3.0.0-0.1
- Update to upstream pre-release version 3.0.0

* Fri Jul 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.1-1
- Update to upstream version 2.0.1
- Fix creation of artifact aliases, resolves: rhbz#988462

* Thu Jul 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-2
- Require maven-resources-plugin by maven-local

* Thu Jul 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-1
- Update to upstream version 2.0.0
- Merge functionality of jpackage-utils
- Provide and obsolete jpackage-utils
- %%add_maven_depmap macro now injects pom.properties to every JAR
- %%add_to_maven_depmap and %%update_maven_depmap macros were removed
- maven2jpp-mapdeps.xsl template has been removed
- Macros related to installation of icons and desktop files were removed
- 14 new manual pages were added
- Documentation specific to JPackage was removed
- Add BuildRequires: asciidoc, xmlto

* Mon Jul  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.15.0-2
- Add R: jvnet-parent

* Wed Jun  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.15.0-1
- Update to upstream version 0.15.0
- Added depmap for tools.jar
- Added support for versioned autorequires
- New plugin metadata from Maven Central

* Tue Jun  4 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.14.1-2
- Add several maven plugins to maven-local requires

* Wed May 29 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.14.1-1
- Update to upstream version 0.14.1 with disabled debugging

* Tue Apr 09 2013 Michal Srb <msrb@redhat.com> - 0.14.0-1
- Update to upstream version 0.14.0

* Mon Apr  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.7-2
- Add R: maven-surefire-provider-junit4 to maven-local

* Fri Mar 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.7-1
- Update to upstream version 0.13.7

* Wed Mar 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.6-4
- Add geronimo-parent-poms to common POMs

* Wed Mar 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.6-3
- Add weld-parent to common POMs

* Wed Mar 20 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.13.6-2
- Fix conditional macro to evaluate properly when fedora is not defined

* Mon Mar 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.6-1
- Update to upstream version 0.13.6

* Wed Mar 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.5-1
- Update to upstream version 0.13.5

* Wed Mar 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.4-1
- Update to upstream version 0.13.4

* Tue Mar 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.3-1
- Update to upstream version 0.13.3

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.2-1
- Update to upstream version 0.13.2

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.1-1
- Update to upstream version 0.13.1

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.0-1
- Update to upstream version 0.13.0

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.13.0-0.1.git2f13366
- Upate to upstream pre-release snapshot 2f13366

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.6-1
- Update to upstream version 0.12.6
- Resolves: rhbz#917618 (remove jetty orbit provides)
- Resolves: rhbz#917647 (system.bundle into autogenerated deps)

* Fri Mar  1 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.12.5-1
- Update to upstream version 0.12.5
- Resolves problems with compat package provides and automatic requires

* Wed Feb 27 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.4-2
- Don't mark RPM macro files as configuration

* Mon Feb 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.4-1
- Update to upstream version 0.12.4
- Resolves: rhbz#913630 (versioned requires between subpackages)

* Fri Feb 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.3-1
- Update to upstream version 0.12.3
- Resolves: rhbz#913694 (No plugin found for prefix 'X')

* Wed Feb 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.2-1
- Update to upstream version 0.12.2
- Resolves: rhbz#913120 (MAVEN_OPTS are not passed to Maven)

* Mon Feb 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.1-1
- Update to upstream version 0.12.1
- Resolves: rhbz#912333 (M2_HOME is not exported)

* Fri Feb 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.12.0-1
- Update to upstream version 0.12.0
- Implement new pom macros: xpath_replace and xpath_set
- Remove Support-local-depmaps.patch (accepted upstream)

* Fri Feb 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-6
- Support local depmaps

* Thu Feb 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-5
- Add some maven-local Requires for convenience

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-4
- Add missing R: httpcomponents-project

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-3
- Add missing R: jboss-patent

* Wed Feb  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-2
- Don't install mvn-local and mvn-rpmbuild on F18

* Wed Jan 30 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.2-1
- Update to upstream version 0.11.2

* Wed Jan 30 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.1-1
- Update to upstream version 0.11.1

* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.11.0-1
- Update to upstream version 0.11.0
- Add mvn-local and mvn-rpmbuild scripts

* Mon Jan 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10.1-1
- Update to upstream version 0.10.1

* Mon Jan  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10.0-1
- Update to upstream version 0.10.0
- Implement %%xmvn_alias, %%xmvn_file and %%xmvn_package macros
- Fix regex in osgi.attr
- Add support for pre- and post-goals in mvn-build script

* Mon Dec 10 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.9.1-1
- Update to upstream version 0.9.1
- Resolves: rhbz#885636

* Thu Dec  6 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.9.0-1
- Update to latest upstream version
- Enable maven requires generator for xmvn packages
- Enable requires generator for javadoc packages

* Wed Dec  5 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.3-1
- Update to upstream version 0.8.3
- Fix maven provides generator for new XML valid fragments

* Fri Nov 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.2-1
- Update to upstream version 0.8.2

* Fri Nov 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.1-1
- Update to upstream version 0.8.1

* Wed Nov 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.0-1
- Update to upstream version 0.8.0
- Add xmvn macros

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.5-3
- Add BR: jpackage-utils

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.5-2
- Add maven-local subpackage

* Thu Nov 08 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.5-1
- Fix versioned pom installation by quoting _jpath

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.4-1
- Shorten maven filelist filenames

* Wed Oct 31 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.3-1
- Update to upstream version 0.7.3

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.2-1
- Make sure add_maven_depmap fails when python tracebacks

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.1-1
- Fix problem with exception in default add_maven_depmap invocation

* Tue Oct 30 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.0-1
- Update to latest upstream
- Full support for compat depmap generation
- Generate maven-files-%%{name} with a list of files to package
- Add support for maven repo generation (alpha version)

* Mon Jul 30 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.6.0-1
- Update to upstream version 0.6.0
- Make maven provides versioned
- Add additional pom_ macros to simplify additional pom editing

* Wed Jul 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.5.0-1
- Update to upstream version 0.5.0 - add support for add_maven_depmap -v

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.1-1
- Update to upstream version 0.4.1
- Fixes #837203

* Wed Jun 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.0-1
- Update to upstream version 0.4.0

* Tue Mar  6 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.1-1
- Create maven provides from fragments instead of poms

* Thu Feb 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.0-3
- Fix maven_depmap installation

* Wed Feb 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.0-2
- Add conflicts with older jpackage-utils

* Wed Feb 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.0-1
- Initial version split from jpackage-utils
