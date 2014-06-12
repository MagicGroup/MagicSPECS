Name:           maven-surefire
Version:        2.17
Release:        3%{?dist}
Epoch:          0
Summary:        Test framework project
License:        ASL 2.0 and CPL
URL:            http://maven.apache.org/surefire/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/surefire/surefire/%{version}/surefire-%{version}-source-release.zip
Source2:        http://junit.sourceforge.net/cpl-v10.html
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-core)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-decoration-model)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-impl)
BuildRequires:  mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-utils)
BuildRequires:  mvn(org.apache.maven.shared:maven-verifier)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-parent)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-plugin-descriptor)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.apache.maven:maven-toolchain)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.testng:testng)

BuildRequires:  maven-invoker-plugin
BuildRequires:  maven-plugin-annotations
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-shade-plugin
BuildRequires:  maven-shared-utils
BuildRequires:  maven-shared-verifier
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-failsafe-plugin
BuildRequires:  maven-surefire-plugin >= 0:2.12-1
BuildRequires:  maven-toolchain
BuildRequires:  maven-project
BuildRequires:  maven-shared-common-artifact-filters
BuildRequires:  modello
BuildRequires:  plexus-containers-component-api >= 1.0-0.a34
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  javacc-maven-plugin

Obsoletes:      maven-surefire-booter <= 0:1.5.3
Provides:       maven-surefire-booter = %{epoch}:%{version}-%{release}

%description
Surefire is a test framework project.

%package plugin
Summary:                Surefire plugin for maven
Obsoletes:              maven2-plugin-surefire <= 0:2.0.4
Provides:               maven2-plugin-surefire = %{epoch}:%{version}-%{release}
Obsoletes:              maven-surefire-maven-plugin < 0:2.6
Provides:               maven-surefire-maven-plugin = %{epoch}:%{version}-%{release}

%description plugin
Maven surefire plugin for running tests via the surefire framework.

%package report-plugin
Summary:                Surefire reports plugin for maven
Obsoletes:              maven2-plugin-surefire-report <= 0:2.0.4
Provides:               maven2-plugin-surefire-report = %{epoch}:%{version}-%{release}
Obsoletes:              maven-surefire-report-maven-plugin < 0:2.6
Provides:               maven-surefire-report-maven-plugin = %{epoch}:%{version}-%{release}

%description report-plugin
Plugin for generating reports from surefire test runs.


%package provider-junit
Summary:                JUnit provider for Maven Surefire
Obsoletes:              maven2-plugin-surefire-report <= 0:2.0.4O
Provides:               maven2-plugin-surefire-report = %{epoch}:%{version}-%{release}

%description provider-junit
JUnit provider for Maven Surefire.

%package provider-testng
Summary:                TestNG provider for Maven Surefire

%description provider-testng
TestNG provider for Maven Surefire.

%package report-parser
Summary:                Parses report output files from surefire

%description report-parser
Plugin for parsing report output files from surefire.

%package -n maven-failsafe-plugin
Summary:                Maven plugin for running integration tests

%description -n maven-failsafe-plugin
The Failsafe Plugin is designed to run integration tests while the
Surefire Plugins is designed to run unit. The name (failsafe) was
chosen both because it is a synonym of surefire and because it implies
that when it fails, it does so in a safe way.

If you use the Surefire Plugin for running tests, then when you have a
test failure, the build will stop at the integration-test phase and
your integration test environment will not have been torn down
correctly.

The Failsafe Plugin is used during the integration-test and verify
phases of the build lifecycle to execute the integration tests of an
application. The Failsafe Plugin will not fail the build during the
integration-test phase thus enabling the post-integration-test phase
to execute.

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n surefire-%{version}
cp -p %{SOURCE2} .
%pom_disable_module surefire-shadefire

for module in maven-failsafe-plugin maven-surefire-common \
        maven-surefire-plugin surefire-api surefire-booter \
        surefire-grouper surefire-providers \
        surefire-setup-integration-tests \
        surefire-report-parser; do
    %pom_remove_dep org.apache.maven.surefire:surefire-shadefire $module
done

# Help plugin is needed only to evaluate effective Maven settings.
# For building RPM package default settings will suffice.
%pom_remove_plugin :maven-help-plugin surefire-setup-integration-tests

%build
%mvn_package ":*{surefire-plugin,report-plugin}*" @1
%mvn_package ":*{junit,testng,failsafe-plugin,report-parser}*"  @1
%mvn_package ":*tests*" __noinstall
# tests turned off because they need jmock
%mvn_build -f

%install
%mvn_install


%files -f .mfiles
%doc README.TXT
%doc LICENSE NOTICE cpl-v10.html
%dir %{_javadir}/maven-surefire

%files plugin -f .mfiles-surefire-plugin
%files report-plugin -f .mfiles-report-plugin
%files report-parser -f .mfiles-report-parser
%files provider-junit -f .mfiles-junit
%files provider-testng -f .mfiles-testng
%files -n maven-failsafe-plugin -f .mfiles-failsafe-plugin

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE cpl-v10.html

%changelog
* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.17-3
- Rebuild to regenerate file lists

* Thu May 22 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.17-2
- Drop junit4 virtual provide

* Mon Mar 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.17-1
- Update to upstream version 2.17

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.16-3
- Use Requires: java-headless rebuild (#1067528)

* Fri Feb 21 2014 Michal Srb <msrb@redhat.com> - 0:2.16-2
- Remove dep on maven-compat

* Mon Aug 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.16-1
- Update to upstream version 2.16

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Michal Srb <msrb@redhat.com> - 0:2.15-1
- Update to upstream version 2.15

* Thu May  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.14.1-2
- Remove unneeded BR
- Resolves: rhbz#961467

* Mon Apr 15 2013 Michal Srb <msrb@redhat.com> - 0:2.14.1-1
- Update to upstream version 2.14.1

* Fri Apr 05 2013 Michal Srb <msrb@redhat.com> - 0:2.14-3
- Remove unnecessary dependency on mockito

* Fri Mar 15 2013 Michal Srb <msrb@redhat.com> - 0:2.14-2
- Remove unneeded dependencies

* Fri Mar 15 2013 Michal Srb <msrb@redhat.com> - 0:2.14-1
- Update to upstream version 2.14

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.13-4
- Add missing BR: mockito

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:2.13-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.13-2
- Get rid of custom depmap

* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.13-1
- Update to upstream version 2.13

* Fri Dec 21 2012 Michal Srb <msrb@redhat.com> - 0:2.12.4-8
- Migrated from maven-doxia to doxia subpackages (Resolves: #889149)

* Fri Dec 14 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-7
- Fix Provides: maven-surefire-provider-junit4

* Fri Dec 14 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-6
- Merge junit3 and junit4 providers
- Disable dependency on shadefire

* Mon Dec 10 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-5
- Enable xmvn auto-requires

* Thu Nov 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-4
- Build with xmvn

* Thu Nov 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-3
- Add CPL license

* Mon Oct 22 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-2
- Add maven depmap for org.beanshell:bsh

* Fri Oct  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-1
- Update to upstream version 2.12.4

* Tue Sep 25 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.3-1
- Update to upstream version 2.12.3

* Mon Aug 13 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.2-1
- Update to upstream version 2.12.2

* Fri Aug  3 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.1-1
- Update to upstream version 2.12.1
- Install LICENSE and NOTICE files
- Remove RPM bug workaround

* Fri Jul 27 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.12-5
- Fix build problem and rebuild with target 1.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Jaromir Capik <jcapik@redhat.com> - 0:2.12-3
- Removing bootstrap condition for Patch1 inclusion (always needed in SRPM)

* Thu Mar 01 2012 Jaromir Capik <jcapik@redhat.com> - 0:2.12-2
- Update to 2.12

* Thu Mar 01 2012 Jaromir Capik <jcapik@redhat.com> - 0:2.12-1
- Bootstrap for 2.12

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.10-4
- Move poms and depmaps to respective sub-packages
- Add requires on junit provider to maven-plugin

* Wed Oct  5 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.10-3
- Fix junit4 depmap provider macro
- Remove unused patches

* Sun Oct 2 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.10-2
- BR maven-enforcer-plugin.

* Sun Oct 2 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.10-1
- Update to latest upstream - 2.10.
- Use new maven macro.

* Mon Jun 27 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.9-1
- Update to latest upstream (2.9)
- Fix up Requires for juni4 provider

* Tue May 24 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.8.1-4
- Fix up providers artifact and report plugin groupid

* Tue May 24 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.8.1-3
- Fix maven-surefire-plugin group in the depmap.

* Fri May 13 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.8.1-2
- Install testng-utils jar and pom

* Mon Apr 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.8.1-1
- Update to latest upstream version (2.8.1)

* Tue Mar 29 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.8-1
- Update to latest upstream version (2.8)

* Mon Mar  7 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.7.2-1
- Update to latest version (2.7.2)
- Add common-junit* jars to distribution
- Versionless javadocs
- Use maven 3 to build

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 3 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.7.1-2
- Fix junit3 depmap.

* Wed Dec 29 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.7.1-1
- Update to 2.7.1.

* Wed Dec  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-3
- Add proper Requires on junit/junit4/testng to providers

* Fri Oct 29 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-2
- Add main pom.xml

* Mon Aug 30 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-1
- Rename subpackages to not repeat "maven" twice
- Update to latest upstream version
- Add common jar to files
- Introduce maven-failsafe-plugin sub-package
- Cleanups

* Mon Aug 31 2009 Andrew Overholt <overholt@redhat.com> 0:2.3-7.7
- Bump release to rebuild

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.6
- Really remove maven2-plugin-surefire BR.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.5
- Revert previous change.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.4
- Disable not needed BRs.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.3
- Install JPP.maven2.plugins-surefire-plugin.pom now that we have maven 2.0.8.

* Wed Aug 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.2
- Don't install JPP.maven2.plugins-surefire-plugin.pom to fix conflict with maven2 2.0.4.

* Tue Aug 18 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.1
- Update to 2.3 - sync with jpackage.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.3-4.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.3-3.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 13 2008 Deepak Bhole <dbhole@redhat.com> 1.5.3-2.8
- Build for ppc64

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.3-2.7
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.3-2jpp.6
- fix license tag

* Thu Feb 28 2008 Deepak Bhole <dbhole@redhat.com> 1.5.3-2jpp.5
- Rebuild

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 1.5.3-2jpp.4
- Build with maven
- ExcludeArch ppc64

* Fri Aug 31 2007 Deepak Bhole <dbhole@redhat.com> 0:1.5.3-2jpp.3
- Build without maven (for initial ppc build)

* Tue Mar 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.5.3-2jpp.2
- Build with maven

* Mon Feb 26 2007 Tania Bento <tbento@redhat.com> 0:1.5.3-2jpp.1
- Fixed %%Release.
- Fixed %%BuildRoot.
- Removed %%Vendor.
- Removed %%Distribution.
- Removed period at the end of %%Summary.
- Removed %%post and %%postun sections for javadoc.
- Removed %%post and %%postun sections for booter-javadoc.
- Added gcj support option.
- Fixed instructions on how to generate source drop.

* Tue Oct 17 2006 Deepak Bhole <dbhole@redhat.com> 1.5.3-2jpp
- Update for maven2 9jpp

* Mon Jun 19 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.5.3-1jpp
- Initial build
