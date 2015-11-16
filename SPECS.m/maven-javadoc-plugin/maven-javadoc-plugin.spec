Name:           maven-javadoc-plugin
Version:        2.10.3
Release:        2%{?dist}
Summary:        Maven Javadoc Plugin
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-javadoc-plugin
BuildArch:      noarch

Source0:        http://repo1.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

Patch0:         reduce-exceptions.patch
Patch1:         doxia-sitetools-1.6.patch

BuildRequires:  maven-local
BuildRequires:  apache-commons-io
BuildRequires:  apache-commons-lang
BuildRequires:  apache-commons-logging
BuildRequires:  httpcomponents-client
BuildRequires:  log4j
BuildRequires:  maven
BuildRequires:  maven-archiver
BuildRequires:  maven-common-artifact-filters
BuildRequires:  maven-doxia-sink-api
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-invoker
BuildRequires:  maven-plugin-annotations
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-plugins-pom
BuildRequires:  maven-reporting-api
BuildRequires:  maven-shade-plugin
BuildRequires:  maven-wagon-provider-api
BuildRequires:  modello
BuildRequires:  plexus-archiver
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-interactivity-api
BuildRequires:  plexus-utils
BuildRequires:  qdox

%description
The Maven Javadoc Plugin is a plugin that uses the javadoc tool for
generating javadocs for the specified project.
 
%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q 
%patch0
%patch1

# Remove test dependencies because tests are skipped anyways.
%pom_xpath_remove "pom:dependency[pom:scope[text()='test']]"

%pom_add_dep org.codehaus.plexus:plexus-interactivity-api pom.xml "
<exclusions>
    <exclusion>
        <groupId>org.codehaus.plexus</groupId>
        <artifactId>plexus-component-api</artifactId>
    </exclusion>
</exclusions>"

# Don't use maven2 modules
%pom_remove_dep :maven-project
%pom_remove_dep :maven-artifact-manager
%pom_remove_dep :maven-toolchain

sed -i -e "s|org.apache.maven.doxia.module.xhtml.decoration.render|org.apache.maven.doxia.siterenderer|g" src/main/java/org/apache/maven/plugin/javadoc/JavadocReport.java

# XXX remove javadoc:fix MOJO for now
# TODO: port to QDox 2.0
rm -f src/main/java/org/apache/maven/plugin/javadoc/*FixJavadocMojo.java
%pom_remove_dep :qdox

%build
%mvn_build -f -- -DmavenVersion=3.1.1

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE NOTICE 

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE 

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 10 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10.3-1
- Update to upstream version 2.10.3

* Wed Mar 18 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10.2-1
- Update to upstream version 2.10.2

* Wed Nov 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10.1-3
- Remove dependency on qdox

* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10.1-2
- Remove legacy Obsoletes/Provides for maven2 plugin

* Mon Sep 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10.1-1
- Update to upstream version 2.10.1

* Tue Sep 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10-1
- Update to upstream version 2.10

* Fri Jul 18 2014 Roland Grunberg <rgrunber@redhat.com> - 2.9.1-10
- Rebuild against maven-doxia-sitetools 1.6.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.9.1-8
- Use Requires: java-headless rebuild (#1067528)

* Fri Feb 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.1-7
- Fix BR on plexus-interactivity

* Thu Feb 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.1-6
- Migrate to Wagon subpackages

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.1-5
- Fix unowned directory

* Mon Jan 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.1-4
- Remove dependency on maven2

* Fri Jan 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9.1-3
- Update to current packaging guidelines
- Update to Maven 3.x

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 30 2013 Mat Booth <fedora@matbooth.co.uk> - 2.9.1-1
- Update to latest upstream, fixes rhbz #979577, works around CVE-2013-1571
- Remove dep on jakarta-commons-httpclient

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-6
- Remove test dependencies from POM

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.9-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-3
- Add missing requires
- Resolves: rhbz#893166

* Mon Nov 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.9-2
- Add LICENSE and NOTICE files to packages (#879605)
- Add dependency exclusion to make enforcer happy

* Tue Oct 23 2012 Alexander Kurtakov <akurtako@redhat.com> 2.9-1
- Update to latest upstream version.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Alexander Kurtakov <akurtako@redhat.com> 2.8.1-1
- Update to latest upstream version.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Tomas Radej <tradej@redhat.com> - 2.8-4
- Added maven-compat dep to pom.xml

* Mon Dec 12 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-3
- Add BR on modello.

* Tue Dec 6 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-2
- FIx build in pure maven 3 environment.

* Wed May 11 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-1
- Update to latest upstream version.
- Guidelines fixes.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 24 2010 Alexander Kurtakov <akurtako@redhat.com> 2.7-3
- Add missing invoker requires.

* Wed Jul 21 2010 Alexander Kurtakov <akurtako@redhat.com> 2.7-2
- Add missing invoker BR.

* Wed Jul 21 2010 Alexander Kurtakov <akurtako@redhat.com> 2.7-1
- Update to 2.7.

* Fri May  7 2010 Mary Ellen Foster <mefoster at gmail.com> - 2.4-2
- Add jpackage-utils requirements
- Update requirements of javadoc subpackage

* Thu May  6 2010 Mary Ellen Foster <mefoster at gmail.com> - 2.4-1
- Initial version, based on akurtakov's initial spec
