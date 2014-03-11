# Copyright (c) 2000-2008, JPackage Project
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

Name:           junit
Version:        4.10
Release:        6%{?dist}
Epoch:          0
Summary:        Java regression test package
License:        CPL
URL:            http://www.junit.org/
Group:          Development/Tools
BuildArch:      noarch

# git clone --bare git://github.com/KentBeck/junit.git junit.git 
# mkdir junit-4.10
# git --git-dir=junit.git --work-tree=junit-4.10 checkout r4.10
# tar cjf junit-4.10.tar.xz junit-4.10/
Source0:        %{name}-%{version}.tar.xz
Source1:        http://search.maven.org/remotecontent?filepath=%{name}/%{name}/%{version}/%{name}-%{version}.pom
Source2:        junit-OSGi-MANIFEST.MF
Patch0:         %{name}-removed-test.patch

BuildRequires:  ant
BuildRequires:  ant-contrib
BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  hamcrest
BuildRequires:  perl-MD5

Requires:       hamcrest
Requires:       java >= 1:1.6.0

Provides:       junit4 = %{epoch}:%{version}-%{release}
Obsoletes:      junit4 < %{epoch}:%{version}-%{release}

%description
JUnit is a regression testing framework written by Erich Gamma and Kent Beck. 
It is used by the developer who implements unit tests in Java. JUnit is Open
Source Software, released under the Common Public License Version 1.0 and 
JUnit is Open Source Software, released under the IBM Public License and
hosted on SourceForge.

%package manual
Group:          Documentation
Summary:        Manual for %{name}
Provides:       junit4-manual = %{epoch}:%{version}-%{release}
Obsoletes:      junit4-manual < %{epoch}:%{version}-%{release}

%description manual
Documentation for %{name}.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils
Provides:       junit4-javadoc = %{epoch}:%{version}-%{release}
Obsoletes:      junit4-javadoc < %{epoch}:%{version}-%{release}

%description javadoc
Javadoc for %{name}.

%package demo
Group:          Development/Libraries
Summary:        Demos for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}
Provides:       junit4-demo = %{epoch}:%{version}-%{release}
Obsoletes:      junit4-demo < %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q 
%patch0 -p1
cp %{SOURCE1} pom.xml
find -iname '*.class' -o -iname '*.jar' -delete
ln -s $(build-classpath hamcrest/core) lib/hamcrest-core-1.1.jar

%build
ant dist

# inject OSGi manifest
mkdir -p META-INF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}%{version}/%{name}-%{version}.jar META-INF/MANIFEST.MF

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 %{name}%{version}/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
# Many packages still use the junit4.jar directly
ln -s %{_javadir}/%{name}.jar %{buildroot}%{_javadir}/%{name}4.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr %{name}%{version}/javadoc/* %{buildroot}%{_javadocdir}/%{name}

# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}/demo/%{name} 

cp -pr %{name}%{version}/%{name}/* %{buildroot}%{_datadir}/%{name}/demo/%{name}


%files
%doc cpl-v10.html README.html
%{_javadir}/%{name}.jar
%{_javadir}/%{name}4.jar
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files demo
%doc cpl-v10.html
%{_datadir}/%{name}

%files javadoc
%doc cpl-v10.html
%doc %{_javadocdir}/%{name}

%files manual
%doc cpl-v10.html
%doc junit%{version}/doc/*

%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:4.10-5
- Update OSGi metadata to match 4.10.0 release.

* Thu Feb 09 2012 Harald Hoyer <harald@redhat.com> 4.10-4
- removed Conflicts with itsself

* Thu Jan 26 2012 Roland Grunberg <rgrunber@redhat.com> 0:4.8.2-3
- Add OSGi metadata to junit.jar manifest.

* Thu Jan 26 2012 Tomas Radej <tradej@redhat.com> - 0:4.10-2
- Fixed versioning

* Wed Jan 25 2012 Tomas Radej <tradej@redhat.com> - 0:4.10-1
- Updated to upstream 4.10
- Obsoleted junit4
- Epoch added

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 7 2010 Alexander Kurtakov <akurtako@redhat.com> 3.8.2-7
- Drop gcj support.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-6.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-5.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.8.2-4.4
- drop repotag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.8.2-4jpp.3
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> - 3.8.2-3jpp.3
- Fix location of stylesheet for javadocs

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> - 3.8.2-3jpp.2
- Rebuild for ppc32 execmem issue and new build-id

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1.fc7
- Add dist tag

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1
- Committed on behalf of Tania Bento <tbento@redhat.com>
- Update per Fedora review process
- Resolves rhbz#225954

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-3jpp.1
- Added missing requirements.

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 0:3.8.2-2jpp_3fc
- Require(post/postun): coreutils

* Sun Jun 23 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_2fc
- Rebuilt.

* Sat Jun 22 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_1fc
- Upgrade to 3.8.2
- Added conditional native compilation.
- Fix path where demo is located.

* Mon Mar 03 2006 Ralph Apel <r.apel at r-apel.de> - 0:3.8.2-1jpp
- First JPP-1.7 release

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:3.8.1-4jpp
- Rebuild with ant-1.6.2
* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:3.8.1-3jpp
- update for JPackage 1.5

* Fri Mar 21 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 3.8.1-2jpp
- For jpackage-utils 1.5

* Fri Sep 06 2002 Henri Gomez <hgomez@users.sourceforge.net> 3.8.1-1jpp
- 3.8.1

* Sun Sep 01 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-2jpp 
- used original zip file

* Thu Aug 29 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-1jpp 
- 3.8
- group, vendor and distribution tags

* Sat Jan 19 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-6jpp
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- stricter dependency for demo package
- additional sources in individual archives
- section macro

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-5jpp
- javadoc in javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-4jpp
- fixed previous releases ...grrr

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-3jpp
- added jpp extension
- removed packager tag

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-2jpp
- first unified release
- s/jPackage/JPackage

* Mon Sep 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-1mdk
- 3.7
- vendor tag
- packager tag
- s/Copyright/License/
- truncated description to 72 columns in spec
- spec cleanup
- used versioned jar
- moved demo files to %%{_datadir}/%%{name}

* Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 3.5-1mdk
- first Mandrake release
