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

Name:           maven-jxr
Version:        2.4
Release:        5%{?dist}
Epoch:          0
Summary:        Source cross referencing tool
# BSD: maven-jxr/src/main/java/org/apache/maven/jxr/JavaCodeTransform.java
License:        ASL 2.0 and BSD
URL:            http://maven.apache.org/doxia/

Source0:        http://repo2.maven.org/maven2/org/apache/maven/jxr/jxr/%{version}/jxr-%{version}-source-release.zip
# taken from maven-jxr/src/main/java/org/apache/maven/jxr/JavaCodeTransform.java
Source1:        LICENSE-BSD

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-lang:commons-lang)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-impl)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.apache.velocity:velocity)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(oro:oro)
BuildRequires:  mvn(xalan:xalan)
BuildRequires:  mvn(xml-apis:xml-apis)

%description
Maven JXR is a source cross referencing tool.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%package -n maven-plugin-jxr
Summary:        Maven plugin for JXR
Requires:       %{name} = %{version}-%{release}

%description -n maven-plugin-jxr
Maven plugin for JXR.

%prep
%setup -q -n jxr-%{version}

cp %{SOURCE1} .

# Missing dependency
%pom_add_dep oro:oro maven-jxr

%mvn_package :maven-jxr-plugin maven-plugin-jxr

# maven-core has scope "provided" in Plugin Testing Harness, so we
# need to provide it or tests will fail to compile.  This works for
# upstream because upstream uses a different version of Plugin Testing
# Harness in which scope of maven-core dependency is "compile".
%pom_xpath_inject pom:project "<dependencies/>"
%pom_add_dep org.apache.maven:maven-core::test

%build
# The test failures seem to have something to do with:
# http://jira.codehaus.org/browse/MCHANGES-88
# We can investigate when we upgrade to 2.2.x to see if they still occur.
# Update: Seems that tests fail because they are trying to access
# plexus component descriptors which seem to be different?
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE LICENSE-BSD NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE LICENSE-BSD NOTICE

%files -n maven-plugin-jxr -f .mfiles-maven-plugin-jxr

%changelog
* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 0:2.4-5
- 为 Magic 3.0 重建

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-4
- Fix build-requires on parent POM

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.4-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Dec 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-1
- Update to upstream version 2.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Michal Srb <msrb@redhat.com> - 0:2.3-8
- Build with XMvn
- Add BSD license text
- Drop group tag
- Replace patch with %%pom_ macro
- Fix BR

* Mon Mar 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.3-7
- Add maven-core to test dependencies
- Resolves: rhbz#914171

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:2.3-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Nov 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.3-4
- Install license files and add BSD to license tag (#876984)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-1
- Update to upstream 2.3. release.

* Sun Mar 13 2011 Mat Booth <fedora@matbooth.co.uk> 0:2.2-3
- Maven plug-in sub-package should require the core package.
- Use _mavenpomdir macro.
- Don't install versioned javadocs.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.2-1
- Update to upstream 2.2.
- Adapt to current guidelines.

* Tue Sep  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.1-7
- Fix build bug (javadoc:aggregate)

* Sat Sep 12 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-6
- Install maven-jxr parent pom.

* Sat Sep 12 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-5
- Fix jxr plugin pom name.

* Fri Sep 11 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-4
- Add BR for maven2-plugin.site.
- BR tomcat5-servlet-api.
- BR tomcat5.eclipse-subclipse - update to 1.6.16 in both rawhide and F-14
- BR maven-surefire-provider-junit.
- BR maven-plugin-plugin.
- BR maven-shared-plugin-testing-harness.

* Fri Sep 11 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-3
- Add BR for doxia-sitetools.

* Fri Sep 11 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-2
- Fix depmap for the plugin.

* Thu Sep 10 2009 Andrew Overholt <overholt@redhat.com> 2.1-1
- 2.1
- Add maven-plugin-jxr.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-4.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-3.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 13 2008 Deepak Bhole <dbhole@redhat.com> 1.0-2.8
- Build for ppc64

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-2.7
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-2jpp.6
- fix license tag

* Thu Feb 28 2008 Deepak Bhole <dbhole@redhat.com> 1.0-2jpp.5
- Rebuild

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 1.0-2jpp.4
- Build without maven
- ExcludeArch ppc64

* Fri Aug 31 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-2jpp.3
- Build without maven (for initial ppc build)

* Tue Mar 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-2jpp.2
- Build with maven

* Tue Feb 27 2007 Tania Bento <tbento@redhat.com> 0:1.0-2jpp.1
- Fixed %%Release.
- Fixed %%BuildRoot.
- Removed period from %%Summary.
- Removed %%Vendor.
- Removed %%Distribution.
- Removed %%post and %%postun sections for javadoc.
- Added gcj support option.
- Fixed instructions on how to generate source drops.

* Tue Oct 17 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.0-2jpp
- Update for maven 9jpp.

* Fri Jun 16 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.0-1jpp
- Initial build
