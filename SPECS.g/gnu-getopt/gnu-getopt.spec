# Copyright (c) 2000-2009, JPackage Project
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

Name:           gnu-getopt
Version:        1.0.14
Release:        9%{?dist}
Epoch:          0
Summary:        Java getopt implementation
License:        LGPLv2+
URL:            http://www.urbanophile.com/arenn/hacking/download.html
Source0:        http://www.urbanophile.com/arenn/hacking/getopt/java-getopt-%{version}.tar.gz
Source2:        gnu-getopt-%{version}.pom
Group:          Development/Libraries
Provides:       gnu.getopt = %{epoch}:%{version}-%{release}
Obsoletes:      gnu.getopt < %{epoch}:%{version}-%{release}
BuildArch:      noarch
BuildRequires:  ant
BuildRequires:  jpackage-utils
Requires:       java-headless
Requires:       jpackage-utils


%description
The GNU Java getopt classes support short and long argument parsing in
a manner 100% compatible with the version of GNU getopt in glibc 2.0.6
with a mostly compatible programmer's interface as well. Note that this
is a port, not a new implementation. I am currently unaware of any bugs
in this software, but there certainly could be some lying about. I would
appreciate bug reports as well as hearing about positive experiences.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation
Requires:       jpackage-utils
Provides:       gnu.getopt-javadoc = %{epoch}:%{version}-%{release}
Obsoletes:      gnu.getopt-javadoc < %{epoch}:%{version}-%{release}

%description javadoc
%{summary}.

%prep
%setup -q -c
mv gnu/getopt/buildx.xml build.xml

%build
ant jar javadoc

%install
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}

install -p -m 644 build/lib/gnu.getopt.jar %{buildroot}%{_javadir}/%{name}.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/gnu.getopt.jar

install -p -m 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap -a urbanophile:java-getopt,gnu.getopt:java-getopt

cp -pr build/api/* %{buildroot}%{_javadocdir}/%{name}

%pre javadoc
# workaround for rpm bug, can be removed in F-22
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files -f .mfiles
%doc gnu/getopt/COPYING.LIB gnu/getopt/README
%{_javadir}/gnu.getopt.jar

%files javadoc
%doc gnu/getopt/COPYING.LIB
%{_javadocdir}/%{name}

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0:1.0.14-9
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 0:1.0.14-8
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0.14-6
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0.14-5
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 04 2013 Marek Goldmann <mgoldman@redhat.com> - 0:1.0.14-3
- Added gnu.getopt:java-getopt mapping

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0.14-1
- Update to upstream version 1.0.14

* Thu Sep  6 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0.13-7
- Install license file with javadoc package
- Add missing R: java, jpackage-utils
- Convert versioned names to versionless
- Add rpm bug workaround
- Update to current packaging guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0.13-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0.13-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0.13-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 08 2009 David Walluck <dwalluck@redhat.com> 0:1.0.13-3.1
- remove repolib

* Tue Sep 08 2009 David Walluck <dwalluck@redhat.com> 0:1.0.13-3
- fix maven depmap install
- add compat symlinks for javadoc
- add depmap entry for urbanophile:java-getopt

* Thu Jul 30 2009 Yong Yang <yyang@redhat.com> 0:1.0.13-2
- Merge changes from JPP5 1.0.12-3 to 1.0.12-6 

* Wed Jul 29 2009 Yong Yang <yyang@redhat.com> 0:1.0.13-1
- 1.0.13

* Wed Aug 20 2008 David Walluck <dwalluck@redhat.com> 0:1.0.12-6
- call %%update_maven_depmap

* Wed Aug 20 2008 David Walluck <dwalluck@redhat.com> 0:1.0.12-5
- add pom
- fix component-info.xml

* Wed Aug 13 2008 David Walluck <dwalluck@redhat.com> 0:1.0.12-4
- bump release
- don't duplicate repolib in main package
- own repolib dirs
- fix repolib permissions

* Thu May 29 2008 Permaine Cheung <pcheung@redhat.com> 0:1.0.12-2
- First JPP 5 build

* Tue Mar 13 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.0.12-1jpp.ep1.2
- Fix repolib location

* Tue Mar 13 2007 Fernando Nasser <fnasser@redhat.com> 0:1.0.12-1jpp.ep1.1
- New repolib location

* Mon Feb 19 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.0.12-1jpp.el4ep1.2
- Add -brew suffix

* Fri Feb 16 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.0.12-1jpp.el4ep1.1
- Add repolib support

* Tue May 23 2006 Fernando Nasser <fnasser@redhat.com> 0:1.0.12-1jpp_1rh
- First Red Hat build with new name

* Thu May 04 2006 Ralph Apel <r.apel at r-apel.de> 0:1.0.12-1jpp
- 1.0.12
- Change name to gnu-getopt, Provide/Obsolete gnu.getopt
- Still provide gnu.getopt.jar as symlink

* Tue Dec 07 2004 David Walluck <david@jpackage.org> 0:1.0.10-1jpp
- 1.0.10

* Mon Aug 23 2004 Ralph Apel <r.apel at r-apel.de> 0:1.0.9-5jpp
- Build with ant-1.6.2

* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:1.0.9-4jpp
- fix groups

* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:1.0.9-3jpp
- update for JPackage 1.5

* Wed Mar 26 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 1.0.9-2jpp
- For jpackage-utils 1.5

* Sat Feb 16 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0.9-1jpp
- 1.0.9
- build script merged upstream

* Sat Jan 19 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0.8-2jpp
- versioned dir for javadoc
- no dependencies for javadoc package
- additional sources in individual archives
- section macro

* Sat Dec 8 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0.8-1jpp
- first JPackage release
