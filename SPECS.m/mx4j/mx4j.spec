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

Name:           mx4j
Version:        3.0.1
Release:        18%{?dist}
Epoch:          1
Summary:        Open source implementation of JMX Java API
License:        ASL 1.1
Group:          Development/Libraries
Source0:        %{name}-%{version}-src.tar.gz
Source1:        %{name}-build.policy
Source2:        CatalogManager.properties

Source3:        http://repo1.maven.org/maven2/mx4j/mx4j/%{version}/mx4j-%{version}.pom
Source4:        http://repo1.maven.org/maven2/mx4j/mx4j-jmx/%{version}/mx4j-jmx-%{version}.pom
Source5:        http://repo1.maven.org/maven2/mx4j/mx4j-jmx-remote/%{version}/mx4j-jmx-remote-%{version}.pom
Source6:        http://repo1.maven.org/maven2/mx4j/mx4j-remote/%{version}/mx4j-remote-%{version}.pom
Source7:        http://repo1.maven.org/maven2/mx4j/mx4j-tools/%{version}/mx4j-tools-%{version}.pom
# not available
Source8:        http://repo1.maven.org/maven2/mx4j/mx4j-impl/2.1.1/mx4j-impl-2.1.1.pom
Source9:        http://repo1.maven.org/maven2/mx4j/mx4j-rimpl/2.1.1/mx4j-rimpl-2.1.1.pom
Source10:       http://repo1.maven.org/maven2/mx4j/mx4j-rjmx/2.1.1/mx4j-rjmx-2.1.1.pom

Patch0:         mx4j-javaxssl.patch
Patch1:         mx4j-%{version}.patch
Patch2:         mx4j-build.patch
Patch3:         mx4j-docbook.patch
Patch5:         mx4j-caucho-build.patch
Patch6:         mx4j-no-iiop.patch
URL:            http://mx4j.sourceforge.net/
BuildRequires:  jpackage-utils > 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-apache-resolver
BuildRequires:  javamail >= 0:1.2-5jpp
BuildRequires:  log4j >= 0:1.2.7
BuildRequires:  apache-commons-logging >= 0:1.0.1
BuildRequires:  xml-commons-apis
BuildRequires:  bcel >= 0:5.0
BuildRequires:  coreutils
BuildRequires:  axis >= 0:1.1
BuildRequires:  wsdl4j
BuildRequires:  apache-commons-discovery
BuildRequires:  docbook-dtds >= 0:1.0
BuildRequires:  docbook-style-xsl >= 0:1.61
BuildRequires:  xml-commons-resolver
BuildRequires:  xml-commons
BuildRequires:  xerces-j2
BuildRequires:  dos2unix
BuildArch:      noarch
Requires(pre):  /bin/rm
Requires(post):       %{_sbindir}/update-alternatives
Requires(postun):       %{_sbindir}/update-alternatives
Requires:       javamail >= 0:1.2-5jpp
Requires:       log4j >= 0:1.2.7
Requires:       apache-commons-logging >= 0:1.0.1
Requires:       xml-commons-apis
Requires:       bcel >= 0:5.0
Requires:       axis >= 0:1.1
Requires:       xml-commons-resolver
Requires:       xml-commons

%description
OpenJMX is an open source implementation of the
Java(TM) Management Extensions (JMX).

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%package manual
Group:          Development/Libraries
Summary:        Documentation for %{name}

%description    manual
Documentation for %{name}.

%prep
%setup -q

# FIXME To enable iiop when rmic becomes available
# turn off patch6 and turn on patch4
# Patch4 is a backport of upstream changes (MX4J) and may go
# away on future releases
%patch0 -p1
%patch1 -p0
%patch2 -b .sav
%patch3 -p1
%patch5 -p1
%patch6 -p1

cp %{SOURCE1} build
cp %{_sourcedir}/CatalogManager.properties %{_builddir}/%{name}-%{version}/build/

cp %{SOURCE8} %{name}-impl-%{version}.pom
cp %{SOURCE9} %{name}-rimpl-%{version}.pom
cp %{SOURCE10} %{name}-rjmx-%{version}.pom
sed -i "s|<version>2.1.1</version>|<version>%{version}</version>|" %{name}-*-%{version}.pom

pushd lib
   ln -sf $(build-classpath xml-commons-apis) xml-apis.jar
   ln -sf $(build-classpath xerces-j2) xercesImpl.jar
   ln -sf $(build-classpath xalan-j2) xalan.jar
   ln -sf $(build-classpath commons-logging) .
   ln -sf $(build-classpath log4j) .
   ln -sf $(build-classpath bcel) .
   ln -sf $(build-classpath axis/axis) .
   ln -sf $(build-classpath axis/jaxrpc) .
   ln -sf $(build-classpath axis/saaj) .
   ln -sf $(build-classpath wsdl4j) .
   ln -sf $(build-classpath commons-discovery) .
   ln -sf $(build-classpath servlet25) servlet.jar
   ln -sf $(build-classpath javamail/mail) .
   ln -sf $(build-classpath xml-commons-resolver) .
popd

%build

export OPT_JAR_LIST="ant/ant-junit junit xmlunit jaxp_transform_impl ant/ant-apache-resolver xml-commons-resolver xalan-j2-serializer"

cd build
ant -Dbuild.sysclasspath=first compile.jmx compile.rjmx compile.tools javadocs docs

%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 644 dist/lib/%{name}-impl.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-impl.jar
install -m 644 dist/lib/%{name}-jmx.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-jmx.jar
install -m 644 dist/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}.jar
install -m 644 dist/lib/%{name}-tools.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tools.jar
install -m 644 dist/lib/%{name}-rjmx.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-rjmx.jar
install -m 644 dist/lib/%{name}-rimpl.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-rimpl.jar
install -m 644 dist/lib/%{name}-remote.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-remote.jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}/boa
install -m 644 dist/lib/boa/%{name}-rjmx-boa.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/boa/%{name}-rjmx-boa.jar
install -m 644 dist/lib/boa/%{name}-rimpl-boa.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/boa/%{name}-rimpl-boa.jar
install -m 644 dist/lib/boa/%{name}-remote-boa.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/boa/%{name}-remote-boa.jar

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 %{SOURCE3} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}.pom
%add_maven_depmap JPP.%{name}-%{name}.pom %{name}/%{name}.jar
install -pm 644 %{SOURCE4} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-jmx.pom
%add_maven_depmap JPP.%{name}-%{name}-jmx.pom %{name}/%{name}-jmx.jar
install -pm 644 %{SOURCE6} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-remote.pom
%add_maven_depmap JPP.%{name}-%{name}-remote.pom %{name}/%{name}-remote.jar
install -pm 644 %{SOURCE7} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-tools.pom
%add_maven_depmap JPP.%{name}-%{name}-tools.pom %{name}/%{name}-tools.jar

install -pm 644 %{name}-impl-%{version}.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-impl.pom
%add_maven_depmap JPP.%{name}-%{name}-impl.pom %{name}/%{name}-impl.jar
install -pm 644 %{name}-rimpl-%{version}.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-rimpl.pom
%add_maven_depmap JPP.%{name}-%{name}-rimpl.pom %{name}/%{name}-rimpl.jar
install -pm 644 %{name}-rjmx-%{version}.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-rjmx.pom
%add_maven_depmap JPP.%{name}-%{name}-rjmx.pom %{name}/%{name}-rjmx.jar

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
dos2unix dist/docs/styles.css README.txt LICENSE.txt
cp -r dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%pre
rm -f %{_javadir}/%{name}.jar

%post
%{_sbindir}/update-alternatives --install %{_javadir}/jmxri.jar jmxri %{_javadir}/%{name}/%{name}-jmx.jar 0

%postun
if [ "$1" = "0" ]; then
  %{_sbindir}/update-alternatives --remove jmxri %{_javadir}/%{name}/%{name}-jmx.jar
fi

%files
%{_javadir}/%{name}
%{_mavenpomdir}/JPP.%{name}-*.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE.txt
%doc README.txt

%files javadoc
%{_javadocdir}/%{name}

%files manual
%doc dist/docs/*

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 gil cattaneo <puntogil@libero.it> 1:3.0.1-16
- Add maven POMs

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.0.1-14
- Drop a lot of ancient things.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 7 2010 Alexander Kurtakov <akurtako@redhat.com> 1:3.0.1-11
- Drop jaf R. It is part of Java 5+.

* Wed Oct 6 2010 Alexander Kurtakov <akurtako@redhat.com> 1:3.0.1-10
- Fix build.

* Fri Jan 08 2010 Andrew Overholt <overholt@redhat.com> 1:3.0.1-9.11
- Add dos2unix BR.

* Fri Jan 08 2010 Andrew Overholt <overholt@redhat.com> 1:3.0.1-9.10
- Remove gcj support
- Add cleaning of buildroot to beginning of %%install
- Remove old unversioned Obsoletes/Provides
- Remove touching of RPM_BUILD_ROOT in %%prep
- Fix Groups
- Fix line endings in styles.css, README.txt, and LICENSE.txt
- Add %%doc files to main package
- Fix mixed tabs and spaces

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.1-9.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.1-8.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 21 2008 David Walluck <dwalluck@redhat.com> 1:3.0.1-7.9
- fix file permissions
- own directories

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 1:3.0.1-7.8
- add %%{_javadocdir}/%%{name} to file list

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 1:3.0.1-7.7
- own %%{_libdir}/gcj/%%{name}
- add %%{_javadocdir}/%%{name} to file list
- remove javadoc scriptlets
- replace /usr/sbin with %%{_sbindir}

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.0.1-7.6
- really fix license tag

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.0.1-7.5
- drop repotag
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:3.0.1-7jpp.4
- Autorebuild for GCC 4.3

* Wed Aug 30 2006 Deepak Bhole <dbhole@redhat.com> 3.0.1-6jpp.4
- Rebuilding.

* Fri Aug 25 2006 Deepak Bhole <dbhole@redhat.com> 0:3.0.1-6jpp.3
- Fixed broken deps.

* Fri Aug 25 2006 Deepak Bhole <dbhole@redhat.com> 0:3.0.1-6jpp.2
- Make tests conditional
- Add missing requirements

* Fri Aug 18 2006 Fernando Nasser <fnasser@redhat.com> 0:3.0.1-6jpp.1
- Merge with upstream
- Fixed build file to correctly resolve dtds.

* Fri Aug 18 2006 Fernando Nasser <fnasser@redhat.com> 0:3.0.1-6jpp
- Rebuild
  
* Wed Jul 26 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:3.0.1-4jpp_8fc
- Unstub docs.

* Mon Jul 24 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:3.0.1-4jpp_7fc
- Require xerces-j2.

* Mon Jul 24 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:3.0.1-4jpp_6fc
- Build using interpreted ant.

* Sun Jul 23 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:3.0.1-4jpp_5fc
- Stub docs.

* Sun Jul 23 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:3.0.1-4jpp_4fc
- Bump release number. (dist-fc6-java)

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:3.0.1-4jpp_3fc
- Rebuilt

* Wed Jul 19 2006 Fernando Nasser <fnasser@redhat.com> 0:3.0.1-4jpp_2fc
- Add x86_64 to the build

* Wed Jul 19 2006 Fernando Nasser <fnasser@redhat.com> 0:3.0.1-4jpp_1fc
- Merge with upstream
- Do not use jython as it is not available on FC6
- Do not use jetty4 as it is not available on FC6
- Do not run tests as xmlunit not available on FC6 (FIXME)
  so do not BR junit as well

* Tue Jul 18 2006 Fernando Nasser <fnasser@redhat.com> 0:3.0.1-4jpp
- Remove duplicate macros
- Use unversioned burlap and hessian
- Don't use jetty4 as it is not yet available on JPP 1.7
- Re-add Epoch to the versions required
- Split patch for removal of poa
- Add AOT bits

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:3.0.1-1jpp_10fc
- rebuild

* Tue Mar 14 2006 Fernando Nasser <fnasser@redhat.com> 0:3.0.1-3jpp
- Remove dependencies on non-free JXM packages by building MX4J's own
- Add (re-add?) "java.naming.corba.orb" patch, needed by JOnAS

* Fri Mar 10 2006 Ralph Apel <r.apel@r-apel.de> 0:3.0.1-2jpp
- Activate burlap and hessian support
- Most unit tests now pass with java-1.4.2-sun-1.4.2.10-1jpp

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:3.0.1-1jpp_9fc
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:3.0.1-1jpp_8fc
- rebuilt for new gcc4.1 snapshot and glibc changes
- remove dep on jonathan-rmi

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> 0:3.0.1-1jpp_6fc
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Jul 22 2005 Gary Benson <gbenson@redhat.com> 0:3.0.1-1jpp_5fc
- Remove workarounds for #163689.

* Tue Jul 19 2005 Gary Benson <gbenson@redhat.com> 0:3.0.1-1jpp_4fc
- Build on ia64, ppc64, s390 and s390x.
- Remove explicit references to jacorb and jonathan-rmi.
- Switch to aot-compile-rpm (also BC-compiles tools).

* Mon Jun 27 2005 Gary Benson <gbenson@redhat.com> 0:3.0.1-1jpp_3fc
- Also BC-compile the combined remote jarfile.

* Fri Jun 24 2005 Gary Benson <gbenson@redhat.com> 0:3.0.1-1jpp_2fc
- Compile JRMP stubs.

* Mon Jun 20 2005 Gary Benson <gbenson@redhat.com> 0:3.0.1-1jpp_1fc
- Upgrade to 3.0.1-1jpp.
- Add missing build dependency on ant-junit.
- Build stuff that requires axis and xdoclet now that we ship them.
- Pick up CORBA and javax.rmi classes from jacorb and jonathan-rmi.

* Fri May 27 2005 Gary Benson <gbenson@redhat.com> 0:2.1.0-1jpp_9fc
- Rearrange how BC-compiled stuff is built and installed.
- Add missing epochs to dependencies.

* Mon May 23 2005 Gary Benson <gbenson@redhat.com> 0:2.1.0-1jpp_8fc
- Add alpha to the list of build architectures (#157522).
- Use absolute paths for rebuild-gcj-db.

* Fri May  6 2005 Gary Benson <gbenson@redhat.com> 0:2.1.0-1jpp_7fc
- Fix ownership in %%{_javadir}.

* Thu May  5 2005 Gary Benson <gbenson@redhat.com> 0:2.1.0-1jpp_6fc
- Add dependencies for %%post and %%postun scriptlets (#156901).

* Fri Apr 29 2005 Gary Benson <gbenson@redhat.com> 0:2.1.0-1jpp_5fc
- BC-compile the combined jarfile.

* Fri Apr 22 2005 Fernando Nasser <fnasser@redhat.com> 0:3.0.1-1jpp
- Upgrade to 3.0.1

* Thu Apr 21 2005 Gary Benson <gbenson@redhat.com> 0:2.1.0-1jpp_4fc
- Revert my previous two changes.

* Thu Apr 21 2005 Gary Benson <gbenson@redhat.com> 0:2.1.0-1jpp_3fc
- Bump priority of alternative to avoid problems on upgrade.

* Wed Apr 20 2005 Fernando Nasser <fnasser@redhat.com> 0:2.1.0-1jpp
- Upgrade to 2.1.0
- Do not build caucho part because of version incompatibilities
  From Andrew Overholt <overholt@redhat.com>
- add coreutils BuildRequires

* Mon Mar 14 2005 Gary Benson <gbenson@redhat.com> 0:2.1.0-1jpp_2fc
- Install mx4j.jar as the jmxri.jar alternative instead of
  mx4j-jmx.jar.  From Anthony Green <green@redhat.com>.

* Tue Mar 08 2005 Ralph Apel <r.apel at r-apel.de> 0:2.0.1-3jpp
- Drop spurious Requires: junit

* Mon Mar  7 2005 Gary Benson <gbenson@redhat.com> 0:2.1.0-1jpp_1fc
- Build into Fedora.

* Fri Sep 24 2004 Ralph Apel <r.apel at r-apel.de> 0:2.0.1-2jpp
- Require xml-commons (jpackage), not xml-common (linux)
- Activate jython- and jetty-related classes
- Activate unit tests, therefore BuildReq xmlunit
- Include compliance test, therefore BuildReq jmx, jmxremote
- Define essential runtime requires
- Use security manager and relaxed policy

* Fri Jun 25 2004 Aizaz Ahmed <aahmed@redhat.com> 1:2.0.1-1jpp
- Updated to use mx4j-2.0.1
- Rebuilt with Ant 1.6.2

* Mon Mar 24 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 1.1.1-4jpp
- jmxri alternative

* Mon Mar 24 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 1.1.1-3jpp
- use own dir
- For jpackage-utils 1.5

* Thu Feb 20 2003 Henri Gomez <hgomez@users.sourceforge.net> 1.1.1-1jpp
- mx4j 1.1.1
- grabed from CVS TAG MX4J_1_1_1

* Wed Sep 18 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.1-3jpp
- added missing xsl/jython resources in mx4j-tools.jar
- correct the build.xml to have correct contents for mx4.jar and mx4j-tools.jar

* Tue Jul 02 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1-2jpp
- bzipped additional sources
- section macro
- ant already requires jaxp_parser
- fixed source perms
- fixed compilation with jsse and javamail
- buildrequires jsse >= 1.0.2-6jpp
- buildrequires javamail >= 1.2-5jpp

* Mon Jun 10 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.1-1jpp
- mx4j 1.1 
- set correct jpackage tags
- add provide jmxri

* Mon Mar 04 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.0b3-1jpp
- mx4j 1.0b3 (previous name was openjmx)

* Fri Jan 18 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.0b1-1jpp
- first JPackage release
