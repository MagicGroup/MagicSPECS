# Copyright (c) 2000-2007, JPackage Project
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

%{?scl:%scl_package icu4j}
%{!?scl:%global pkg_name %{name}}
%{!?scl:%global _scl_root %{nil}}


%global with_eclipse 1

%if 0%{?rhel}
%global with_eclipse 0
%endif

%global eclipse_base            `more %{_bindir}/eclipse-pdebuild  | grep datadir= | sed -e "s/datadir=//"`/eclipse
# Note:  this next section looks weird having an arch specified in a
# noarch specfile but the parts of the build
# All arches line up between Eclipse and Linux kernel names except i386 -> x86
%ifarch %{ix86}
%global eclipse_arch    x86
%else
%global eclipse_arch   %{_arch}
%endif

Name:           %{?scl_prefix}icu4j
Version:        52.1
Release:        2%{?dist}
Epoch:          1
Summary:        International Components for Unicode for Java
License:        MIT and EPL 
URL:            http://site.icu-project.org/
Group:          Development/Libraries
#CAUTION
#to create a tarball use following procedure
#svn co http://source.icu-project.org/repos/icu/icu4j/tags/release-52-eclipse-20140218 icu4j-<version>
#tar caf icu4j-<version>.tar.xz icu4j-<version>/
Source0:        icu4j-%{version}.tar.xz
Source1:        %{pkg_name}-%{version}.pom

Patch0:         %{pkg_name}-crosslink.patch
BuildRequires:  ant >= 1.7.0
# FIXME:  is this necessary or is it just adding strings in the hrefs in
# the docs?
BuildRequires:  java-javadoc >= 1:1.6.0
# This is to ensure we get OpenJDK and not GCJ
BuildRequires:  java-devel >= 1:1.7.0
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  zip
Requires:       jpackage-utils
%{?scl:Requires: %scl_runtime}
# This is to ensure we get OpenJDK and not GCJ
Requires:       java-headless >= 1:1.6.0
%if %{with_eclipse}
BuildRequires:  %{?scl_prefix}eclipse-pde >= 0:3.2.1
%global         debug_package %{nil}
%endif

BuildArch:      noarch


%description
The International Components for Unicode (ICU) library provides robust and
full-featured Unicode services on a wide variety of platforms. ICU supports
the most current version of the Unicode standard, and provides support for
supplementary characters (needed for GB 18030 repertoire support).

Java provides a very strong foundation for global programs, and IBM and the
ICU team played a key role in providing globalization technology into Sun's
Java. But because of its long release schedule, Java cannot always keep
up-to-date with evolving standards. The ICU team continues to extend Java's
Unicode and internationalization support, focusing on improving
performance, keeping current with the Unicode standard, and providing
richer APIs, while remaining as compatible as possible with the original
Java text and internationalization API design.

%package charset
Summary:        Charset sublibrary of %{pkg_name}
Group:          Development/Libraries
Requires:       jpackage-utils

%description charset
Charset sublibrary of %{pkg_name}.

%package javadoc
Summary:        Javadoc for %{pkg_name}
Group:          Documentation
Requires:       jpackage-utils
Requires:       java-javadoc >= 1:1.6.0

%description javadoc
Javadoc for %{pkg_name}.

%if %{with_eclipse}
%package eclipse
Summary:        Eclipse plugin for %{pkg_name}
Group:          Development/Libraries
Requires:       jpackage-utils

%description eclipse
Eclipse plugin support for %{pkg_name}.

%endif

%prep
%setup -q -n %{pkg_name}-%{version}
#%patch0 -p0

cp %{SOURCE1} .

%{__sed} -i 's/\r//' APIChangeReport.html
%{__sed} -i 's/\r//' readme.html

sed --in-place "s/ .*bootclasspath=.*//g" build.xml
sed --in-place "s/<date datetime=.*when=\"after\"\/>//" build.xml
sed --in-place "/javac1.3/d" build.xml
sed --in-place "s:/usr/lib:%{_datadir}:g" build.xml

%build
%ant -Dicu4j.javac.source=1.5 -Dicu4j.javac.target=1.5 -Dj2se.apidoc=%{_javadocdir}/java jar docs
%if %{with_eclipse}
ECLIPSE_BASE=%{eclipse_base}
pushd eclipse-build
  %ant -Dj2se.apidoc=%{_javadocdir}/java -Declipse.home=${ECLIPSE_BASE} \
    -Djava.rt=%{_jvmdir}/jre/lib/rt.jar \
    -Declipse.basews=gtk -Declipse.baseos=linux \
    -Declipse.pde.dir=${ECLIPSE_BASE}/dropins/sdk/plugins/`ls ${ECLIPSE_BASE}/dropins/sdk/plugins/|grep org.eclipse.pde.build_`
popd
%endif
  
%install

# jars
%__mkdir_p %{buildroot}%{_javadir}
%__cp -ap %{pkg_name}.jar %{buildroot}%{_javadir}/%{pkg_name}.jar
%__cp -ap %{pkg_name}-charset.jar %{buildroot}%{_javadir}/%{pkg_name}-charset.jar

# javadoc
%__mkdir_p %{buildroot}%{_javadocdir}/%{pkg_name}
%__cp -pr doc/* %{buildroot}%{_javadocdir}/%{pkg_name}

%if %{with_eclipse}
# eclipse
install -d -m755 %{buildroot}%{_javadir}/icu4j-eclipse

unzip -qq -d %{buildroot}%{_javadir}/icu4j-eclipse eclipse-build/out/projects/ICU4J.com.ibm.icu/com.ibm.icu-com.ibm.icu.zip
%endif

# maven stuff
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
cp %{pkg_name}-%{version}.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{pkg_name}.pom
%add_maven_depmap JPP-%{pkg_name}.pom %{pkg_name}.jar

%files
%doc readme.html APIChangeReport.html
%{_javadir}/%{pkg_name}.jar
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/*.pom

%files charset
%{_javadir}/%{pkg_name}-charset.jar

%files javadoc
%doc %{_javadocdir}/*

%if %{with_eclipse}
%files eclipse
%dir %{_javadir}/icu4j-eclipse/
%dir %{_javadir}/icu4j-eclipse/features
%dir %{_javadir}/icu4j-eclipse/plugins
%{_javadir}/icu4j-eclipse/features/*
%{_javadir}/icu4j-eclipse/plugins/*
%doc readme.html
%endif

%changelog
* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1:52.1-2
- Use Requires: java-headless rebuild (#1067528)

* Tue Mar 18 2014 Michael Simacek <msimacek@redhat.com> - 1:52.1-1
- Update to upstream version 52.1
- Require java-headless

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:50.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.1-1
- Update to latest upstream.

* Fri Mar 22 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-7
- Build sclized version using SCLized Eclipse.

* Thu Feb 21 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-6
- RHBZ#913369 Provide icu4j-charset library

* Tue Feb 12 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-5
- SCLize.

* Mon Feb 11 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-4
- Revert a hardcoded path.

* Mon Feb 11 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-3
- Complete the removal.

* Mon Feb 11 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-2
- Remove the main jar manifest.

* Thu Feb 7 2013 Krzysztof Daniel <kdaniel@redhat.com> 1:50.1.0-1
- Update to latest upstream. 

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.4.2.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.2.2-12
- Don't build icu4j-eclipse for rhel.

* Thu Feb 16 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.4.2.2-11
- Make the package noarch.

* Wed Feb  1 2012 Daniel Mach <dmach@redhat.com> 1:4.4.2.2-10
- Tweak with_eclipse macro for rhel and non-intel architectures.

* Fri Jan 27 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.4.2.2-9
- Getting back to 4 digit version

* Thu Jan 26 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.4.2-8
- Proper sources uploaded

* Thu Jan 26 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.4.2-7
- Better versioning consistent with previous releases

* Mon Jan 16 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.4.2.2-6
- Update to 4.4.2.2.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.2-4
- Add proper manifest to the jar in the main package.

* Fri Sep 16 2011 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.2-3
- Adapt to current guidelines.

* Mon May 9 2011 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.2-2
- Use proper tarball.
- Fix build.

* Tue Apr 05 2011 Chris Aniszczyk <zx@redhat.com> 1:4.4.2-1
- Update to 4.4.2.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 8 2010 Alexander Kurtakov <akurtako@redhat.com> 1:4.2.1-1
- Update to 4.2.1.

* Fri Feb  5 2010 Mary Ellen Foster <mefoster at gmail.com> 1:4.0.1-5
- Add maven pom and depmap fragment

* Tue Sep 29 2009 Alexander Kurtakov <akurtako@redhat.com> 1:4.0.1-4
- Simplify with_eclipse conditional.

* Mon Aug 10 2009 Alexander Kurtakov <akurtako@redhat.com> 1:4.0.1-3
- Update qualifier to the Eclipse 3.5.0 release.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 8 2009 Alexander Kurtakov <akurtako@redhat.com> 1:4.0.1-1
- Update to 4.0.1.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct  8 2008 Ville Skyttä <ville.skytta at iki.fi> - 0:3.8.1-4
- Disable debuginfo package when built with Eclipse support, change to
  noarch when built without it (#464017).

* Mon Aug 11 2008 Andrew Overholt <overholt@redhat.com> 3.8.1-3
- Get rid of eclipse_name macro
- Rebuild with Eclipse 3.4 and put into Eclipse stuff into
  %%{_libdir}/eclipse
- Remove now-unnecessary OSGi configuration dir patch
- Add patch to point to PDE Build location

* Fri Jul 11 2008 Andrew Overholt <overholt@redhat.com> 0:3.8.1-2
- Remove GCJ support due to
  com.sun.tools.doclets.internal.toolkit.taglets.* import (not in gjdoc)

* Fri Jul 11 2008 Andrew Overholt <overholt@redhat.com> 0:3.8.1-1
- 3.8.1

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:3.6.1-3
- drop repotag
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:3.6.1-2jpp.6
- Autorebuild for GCC 4.3

* Tue Nov 13 2007 Andrew Overholt <overholt@redhat.com> 3.6.1-1jpp.6
- Bump release and change updatetimestamp patch to have DOS
  line-endings.

* Tue Nov 13 2007 Andrew Overholt <overholt@redhat.com> 3.6.1-1jpp.5
- Bump release.

* Fri Sep 28 2007 Andrew Overholt <overholt@redhat.com> 3.6.1-1jpp.4
- Update timestamp to match Eclipse 3.3.1 release.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.6.1-1jpp.3
- Rebuild for selinux ppc32 issue.

* Wed Jun 27 2007 Ben Konrath <bkonrath@redhat.com> - 0:3.6.1-1jpp.2
- Remove requires eclipse-rcp in eclipse sub-package.

* Thu Jun 07 2007 Ben Konrath <bkonrath@redhat.com> - 0:3.6.1-1jpp.1
- 3.6.1.
- Enable eclipse sub-package.

* Fri Mar 16 2007 Jeff Johnston <jjohnstn@redhat.com> - 0:3.4.5-2jpp.2
- Disable eclipse plugin support temporarily until build problems
  can be worked out.  Plugin is still being built as part of
  eclipse platform.
- BuildRequire sinjdoc.

* Mon Feb 12 2007 Matt Wringe <mwringe@redhat.com> - 0:3.4.5-2jpp.1
- Fix some rpmlint issues
- Make use of buildroot more consistent
- Remove javadoc post and postun sections as per new jpp standard
- Change license section to 'MIT style' license from 'MIT' license.
  This was done since the source package calls the license the 
  "X license" (see readme.html in src jar).
- Install eclipse plugin into /usr/share/eclipse

* Mon Jan 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.4.5-2jpp.1
- Merge with upstream

* Mon Jan 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.4.5-2jpp
- Add optional eclipse subpackage, created by
  Jeff Johnston  <jjohnstn@rdhat.com> :
- Add eclipse sub-package to create plugins.

* Mon Jan 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.4.5-1jpp
- Upgrade to 3.4.5 with merge
- Re-enable javadoc

* Mon Sep 04 2006 Ben Konrath <bkonrath@redhat.com> 0:3.4.5-1jpp_1fc
- 3.4.5.
- Add GCJ support with spec-convert-gcj-1.6.

* Mon Jul 17 2006 Ben Konrath <bkonrath@redhat.com> 0:3.4.4-1jpp_1fc
- 3.4.4.
- Add disable javadocs patch.

* Tue Feb 28 2006 Fernando Nasser <fnasser@redhat.com> - 0:3.2-2jpp_1rh
- First Red Hat build

* Mon Feb 27 2006 Fernando Nasser <fnasser@redhat.com> - 0:3.2-2jpp
- First JPP 1.7 build

* Sun Jan 29 2005 David Walluck <david@jpackage.org> 0:3.2-1jpp
- release (contributed by Mary Ellen Foster <mefoster at gmail.com>)
