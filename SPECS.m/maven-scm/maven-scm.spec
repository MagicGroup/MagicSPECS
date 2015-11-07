# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           maven-scm
Version:        1.9.1
Release:        3%{?dist}
Summary:        Common API for doing SCM operations
License:        ASL 2.0
URL:            http://maven.apache.org/scm

Source0:        http://repo1.maven.org/maven2/org/apache/maven/scm/%{name}/%{version}/%{name}-%{version}-source-release.zip

# Patch to migrate to new plexus default container
# This has been sent upstream: http://jira.codehaus.org/browse/SCM-731
Patch6:         0001-port-maven-scm-to-latest-version-of-plexus-default-c.patch
# Workaround upstream's workaround for a modello bug, see: http://jira.codehaus.org/browse/SCM-518
Patch7:         vss-modello-config.patch

BuildArch:      noarch

BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  maven-local
BuildRequires:  modello
BuildRequires:  plexus-utils >= 1.5.6
BuildRequires:  maven-invoker-plugin
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  bzr
BuildRequires:  subversion
BuildRequires:  plexus-containers-component-metadata
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-classworlds
BuildRequires:  jgit

%description
Maven SCM supports Maven plugins (e.g. maven-release-plugin) and other
tools (e.g. Continuum) in providing them a common API for doing SCM operations.

%package test
Summary:        Tests for %{name}
Requires:       maven-scm = %{version}-%{release}

%description test
Tests for %{name}.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch6 -p1 -b.orig
%patch7 -p0 -b.orig

# Remove unnecessary animal sniffer
%pom_remove_plugin org.codehaus.mojo:animal-sniffer-maven-plugin

# Remove providers-integrity from build (we don't have mks-api)
%pom_remove_dep org.apache.maven.scm:maven-scm-provider-integrity maven-scm-providers/maven-scm-providers-standard
%pom_disable_module maven-scm-provider-integrity maven-scm-providers

# Partially remove cvs support for removal of netbeans-cvsclient
# It still works with cvsexe provider
%pom_remove_dep org.apache.maven.scm:maven-scm-provider-cvsjava maven-scm-client
%pom_remove_dep org.apache.maven.scm:maven-scm-provider-cvsjava maven-scm-providers/maven-scm-providers-standard
%pom_disable_module maven-scm-provider-cvsjava maven-scm-providers/maven-scm-providers-cvs
sed -i s/cvsjava.CvsJava/cvsexe.CvsExe/ maven-scm-client/src/main/resources/META-INF/plexus/components.xml

# Tests are skipped anyways, so remove dependency on mockito.
%pom_remove_dep org.mockito: maven-scm-providers/maven-scm-provider-jazz
%pom_remove_dep org.mockito: maven-scm-providers/maven-scm-provider-accurev

# Put TCK tests into a separate sub-package
%mvn_package :%{name}-provider-cvstest test
%mvn_package :%{name}-provider-gittest test
%mvn_package :%{name}-provider-svntest test
%mvn_package :%{name}-test test

%build
# Don't build and unit run tests because
# * accurev tests need porting to a newer hamcrest
# * vss tests fail with the version of junit in fedora
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE
%dir %{_javadir}/%{name}

%files test -f .mfiles-test
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.9.1-3
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 1.9.1-2
- 为 Magic 3.0 重建

* Mon Jul 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9.1-1
- Update to upstream version 1.9.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Michael Simacek <msimacek@redhat.com> - 1.9-3
- Drop manual requires

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.9-2
- Use Requires: java-headless rebuild (#1067528)

* Wed Jan  8 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-1
- Update to upstream version 1.9

* Tue Aug 27 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.1-2
- Remove BR: mockito

* Sun Aug 25 2013 Mat Booth <fedora@matbooth.co.uk> - 1.8.1-1
- Fix removal of cvs java provider, rhbz #962273
- Update to latest upstream
- Drop upstreamed patches

* Sat Aug 24 2013 Mat Booth <fedora@matbooth.co.uk> - 1.7-10
- Remove use of deprecated macros, rhbz #992204
- Don't ship test jars in main package
- Install NOTICE file

* Sat Aug 24 2013 Mat Booth <fedora@matbooth.co.uk> - 1.7-9
- Add patch to build against newer plexus default container, rhbz #996199
- Drop unneeded BRs

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-7
- Remove BR: maven2-common-poms

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-7
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.7-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Nov 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-4
- Install LICENSE file

* Tue Aug 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-3
- Remove unneeded mockito build dependency
- Use new pom_ macros instead of patches

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Tomas Radej <tradej@redhat.com> - 1.7-1
- Updated to latest upstream version
- plexus-maven-plugin -> plexus-component-metadata

* Mon Apr 23 2012 Guido Grazioli <guido.grazioli@gmail.com> - 1.6-3
- Fix typo

* Mon Apr 23 2012 Guido Grazioli <guido.grazioli@gmail.com> - 1.6-2
- Remove -client-with-dependencies jar to get rid of duplicate libraries
- Switch off maven execution debug output

* Mon Apr 09 2012 Guido Grazioli <guido.grazioli@gmail.com> - 1.6-1
- Update to 1.6 release
- Fix typo in description
- Remove unused patches 001 (mockito now available), 004 and 006
- Update patch 007 (plexus-containers-component-metadata)
- Move source encoding setting to separate patch

* Fri Feb  3 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5-5
- Remove cvsjava provider to get rid of netbeans-cvsclient dep

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Bruno Wolff III <bruno@wolff.to> 1.5-3
- Fix issue with bad requires by maven-scm-test

* Tue Nov 15 2011 Jaromir Capik <jcapik@redhat.com> 1.5-2
- Migration from plexus-maven-plugin to plexus-containers-component-metadata

* Tue Apr 5 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.5-1
- Update to upstream 1.5 release.
- Build with maven 3.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-5
- Drop buildroot definition
- Use mavenpomdir macro
- Make jars versionless (for real)

* Mon Jan 3 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.4-4
- Drop tomcat BRs.
- No more versioned jar and javadoc.

* Wed Sep 08 2010 Guido Grazioli <guido.grazioli@gmail.com> 0:1.4-2
- Fix BR
- Remove unused patch

* Tue Sep 07 2010 Guido Grazioli <guido.grazioli@gmail.com> 0:1.4-1
- Update to upstream 1.4 (#626455)
- Require netbeans-cvsclient instead of netbeans-ide (#572165)

* Mon May 10 2010 Guido Grazioli <guido.grazioli@gmail.com> 0:1.2-6
- Link netbeans-lib-cvsclient jar in the right place.
- Switch to xz compression.
- Sanitize files owned.
- Use %%global.

* Mon Feb 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-5
- Fix BR/Rs for netbeans-ide[version] to netbeans-ide rename.

* Thu Sep 17 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-4
- Fix maven-scm-plugin depmap.

* Sat Sep 12 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-3
- BR maven-surefire-provider-junit.
- BR plexus-maven-plugin.
- BR maven2-plugin-assembly.

* Sat Sep 12 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-2
- Add doxia-sitetools BR.

* Sat Sep 12 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-1
- Update to upstream 1.2.

* Tue Sep 01 2009 Andrew Overholt <overholt@redhat.com> 1.0-0.5.rc1.2
- Bump release

* Tue Sep 01 2009 Andrew Overholt <overholt@redhat.com> 1.0-0.5.rc1.1
- Add tomcat5, tomcat5-servlet-2.4-api,
  maven-shared-plugin-testing-harness, and tomcat5-jsp-2.0-api BRs

* Mon Aug 31 2009 Andrew Overholt <overholt@redhat.com> 1.0-0.5.rc1
- 1.0 RC1 (courtesy Deepak Bhole)
- Remove gcj support
- Add netbeans-ide11 requirement
- Change name on surefire plugin BR

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.4.b3.1.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 23 2009 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.3.b3.1.7
- Remove ppc64 arch exclusion

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.b3.1.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-0.2.b3.1.6
- drop repotag

* Thu Jun 26 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.b3.1jpp.5
- Fix mapping for the scm plugin

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-0.2.b3.1jpp.4
- fix license tag

* Thu Feb 28 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.b3.1jpp.3
- Rebuild

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-0.1.b3.2jpp.2
- Rebuild with excludearch for ppc64

* Tue Feb 27 2007 Tania Bento <tbento@redhat.com> 0:1.0-0.1.b3.2jpp.1
- Fixed %%Release.
- Fixed %%BuildRoot.
- Removed %%Vendor.
- Removed %%Distribution.
- Removed %%post and %%postun sections for javadoc.
- Fixed instructions on how to generate source drop.
- Marked documentation files as %%doc in %%files section.
- Fixed %%Summary.
- Fixed %%description.

* Tue Oct 17 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.b3.2jpp
- Update for maven 9jpp.

* Tue Sep 18 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.b3.1jpp
- Initial build
