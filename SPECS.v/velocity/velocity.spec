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

Name:           velocity
Version:        1.7
Release:        15%{?dist}
Epoch:          0
Summary:        Java-based template engine
License:        ASL 2.0
URL:            http://velocity.apache.org/
Source0:        http://www.apache.org/dist/%{name}/engine/%{version}/%{name}-%{version}.tar.gz
Source1:        http://repo1.maven.org/maven2/org/apache/%{name}/%{name}/%{version}/%{name}-%{version}.pom
Patch0:         0001-Remove-avalon-logkit.patch
Patch1:         0004-Use-log4j-1.2.17.patch
Patch2:         0003-Use-system-jars.patch
Patch3:         0004-JDBC-41-compat.patch
Patch4:         0001-Don-t-use-Werken-XPath.patch
Patch5:         0006-Skip-Java-8-incompatible-test.patch
Requires:       apache-commons-collections
Requires:       apache-commons-logging
Requires:       apache-commons-lang
Requires:       servlet3
Requires:       jakarta-oro
Requires:       junit
Requires:       hsqldb
Requires:       jaxen
Requires:       jdom
Requires:       bcel
Requires:       log4j

BuildRequires:  javapackages-local
BuildRequires:  ant
BuildRequires:  antlr
BuildRequires:  junit
BuildRequires:	ant-junit
BuildRequires:  hsqldb
BuildRequires:  apache-commons-collections
BuildRequires:  apache-commons-logging
BuildRequires:  apache-commons-lang
BuildRequires:  servlet3
BuildRequires:  jakarta-oro
BuildRequires:  jaxen
BuildRequires:  jdom
BuildRequires:  bcel
BuildRequires:  log4j

# It fails one of the arithmetic test cases with gcj
BuildRequires:	java-devel >= 1:1.6.0
BuildArch:      noarch

%description
Velocity is a Java-based template engine. It permits anyone to use the
simple yet powerful template language to reference objects defined in
Java code.
When Velocity is used for web development, Web designers can work in
parallel with Java programmers to develop web sites according to the
Model-View-Controller (MVC) model, meaning that web page designers can
focus solely on creating a site that looks good, and programmers can
focus solely on writing top-notch code. Velocity separates Java code
from the web pages, making the web site more maintainable over the long
run and providing a viable alternative to Java Server Pages (JSPs) or
PHP.
Velocity's capabilities reach well beyond the realm of web sites; for
example, it can generate SQL and PostScript and XML (see Anakia for more
information on XML transformations) from templates. It can be used
either as a standalone utility for generating source code and reports,
or as an integrated component of other systems. Velocity also provides
template services for the Turbine web application framework.
Velocity+Turbine provides a template service that will allow web
applications to be developed according to a true MVC model.

%package        manual
Summary:        Manual for %{name}

%description    manual
Documentation for %{name}.

%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Demo for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}

# remove bundled libs/classes (except those used for testing)
find . -name '*.jar' -o -name '*.class' -not -path '*test*' -print -delete

# Remove dependency on avalon-logkit
rm -f src/java/org/apache/velocity/runtime/log/AvalonLogChute.java
rm -f src/java/org/apache/velocity/runtime/log/AvalonLogSystem.java
rm -f src/java/org/apache/velocity/runtime/log/VelocityFormatter.java

# need porting to new servlet API. We would just add a lot of empty functions
rm  src/test/org/apache/velocity/test/VelocityServletTestCase.java

# This test doesn't work with new hsqldb
rm src/test/org/apache/velocity/test/sql/DataSourceResourceLoaderTestCase.java

cp %{SOURCE1} ./pom.xml

# remove rest of avalon logkit refences
%patch0 -p1

# Use log4j 1.2.17
%patch1 -p1

# Use system jar files instead of downloading from net
%patch2 -p1

%patch3 -p1

# Use jdom instead of werken-xpath
%patch4 -p1
%pom_remove_dep werken-xpath:

# Skip Java 8 incompatible test
%patch5 -p1

# -----------------------------------------------------------------------------

%build
export CLASSPATH=$(build-classpath \
antlr \
apache-commons-collections \
commons-lang \
commons-logging \
tomcat-servlet-api \
junit \
jakarta-oro \
log4j:log4j:1.2.17 \
jaxen \
jdom \
bcel \
hsqldb \
junit)
ant \
  -buildfile build/build.xml \
  -Dbuild.sysclasspath=first \
  jar javadocs test

# fix line-endings in generated files
sed -i 's/\r//' docs/api/stylesheet.css docs/api/package-list

# -----------------------------------------------------------------------------

%install

# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 bin/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr docs/api/* %{buildroot}%{_javadocdir}/%{name}

# data
install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -pr examples test %{buildroot}%{_datadir}/%{name}

# Maven metadata
install -pD -T -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap -a "%{name}:%{name}"


%files -f .mfiles
%doc LICENSE NOTICE README.txt

%files manual
%doc LICENSE NOTICE
%doc docs/*

%files javadoc
%doc LICENSE NOTICE
%{_javadocdir}/%{name}

%files demo
%doc LICENSE NOTICE
%{_datadir}/%{name}

%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0:1.7-15
- 为 Magic 3.0 重建

* Wed Jun 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-14
- Apply patch for log4j 1.2.17

* Wed Jun 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-13
- Use log4j 1.2 compat package
- Skip Java 8 incompatible test

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-11
- Use .mfiles generated during build

* Sat Sep 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-10
- Port from werken-xpath to jdom
- Resolves: rhbz#875817

* Mon Aug 05 2013 Michal Srb <msrb@redhat.com> - 0:1.7-9
- Fix FTBFS (Resolves: #992852)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-6
- Install NOTICE files
- Resolves: rhbz#879021

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 05 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7-4
- Use new tomcat-servlet-api
- Update to latest guidelines

* Fri Feb 17 2012 Deepak Bhole <dbhole@redhat.com> - 0:1.7-3
- Resolved rhbz#791045
- Added patch from Omaid Majid <omajid@redhat.com> to fix build with Java 7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 21 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7-1
- Update to latest version
- Drop old patches

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.6.4-2
- Add compatibility depmap

* Wed Nov  3 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.6.4-1
- Rebase to latest upstream
- Fix problems from bz#226525

* Thu Oct 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.6.3-5
- Use apache-commons-collections instead of jakarta name
- Use tomcat6 for dependency instead of tomcat5 (bz#640660)

* Mon Jun 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.6.3-4
- Fix BR/R for jakarta-commons-rename.

* Sat Feb 13 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.6.3-3
- Get (Build)Requires right

* Sat Feb 13 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.6.3-2
- Require all of the packages in the POM
- Add dist to version

* Fri Jan 15 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.6.3-1
- Update to 1.6.3
- Remove dependency on avalon-logkit
- Add maven metadata and pom

* Sun Jan 10 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4-10.5
- Drop gcj_support.
- Fix groups and url.
- Use upstream tarball.

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 0:1.4-10.4
- Convert specfile to UTF-8.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-9.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 24 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0:1.4-8.4
- Fix FTBFS: added velocity-enum.patch (enum is a reserved keyword in java >= 1.5)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-8.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.4-7.3
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.4-7jpp.2
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.4-7jpp.1
- Autorebuild for GCC 4.3

* Tue Aug 08 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.4-6jpp.1
- Resync with latest from JPP.
- Partially adopt new naming convention.

* Sat Jul 22 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.4-5jpp_2fc
- Rebuilt

* Sat Jul 22 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.4-5jpp_1fc
- Merge with latest from JPP.
- Remove fileversion and my_version macros.
- Remove notexentests patch and replace with a patch to disable
- failure on tests.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.4-3jpp_8fc
- Rebuilt

* Tue Jul 18 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.4-3jpp_7fc
- Build on all archs.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.4-3jpp_6fc
- rebuild

* Wed Mar  8 2006 Rafael Schloming <rafaels@redhat.com> - 0:1.4-3jpp_5fc
- excluded s390[x] and ppc64 due to eclipse

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:1.4-3jpp_4fc
- stop scriptlet spew

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> - 0:1.4-3jpp_3fc
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 0:1.4-3jpp_2fc
- rebuilt

* Tue Nov  8 2005 Vadim Nasardinov <vadimn@redhat.com> - 0:1.4-3jpp_1fc
- Converted from ISO-8859-1 to UTF-8

* Wed Jun 15 2005 Gary Benson <gbenson@redhat.com> 0:1.4-3jpp_1fc
- Build into Fedora.

* Thu Jun  9 2005 Gary Benson <gbenson@redhat.com>
- Remove jarfiles from the tarball.

* Mon Jun  6 2005 Gary Benson <gbenson@redhat.com>
- Build with servletapi5.
- Add NOTICE file as per Apache License version 2.0.
- Skip some failing tests.

* Mon Oct 18 2004 Fernando Nasser <fnasser@redhat.com> 0:1.4-3jpp_1rh
- First Red Hat build

* Thu Sep 23 2004 Ralph Apel <r.apel at r-apel.de> 0:1.4-3jpp
- Adapt to jdom-1.0-1 replacing org.jdom.input.DefaultJDOMFactory
  by org.jdom.DefaultJDOMFactory in AnakiaJDOMFactory.java
  as well as using org.jdom.output.Format in AnakiaTask.java
- Therefore require jdom >= 0:1.0-1

* Thu Sep 02 2004 Ralph Apel <r.apel at r-apel.de> 0:1.4-2jpp
- Build with ant-1.6.2

* Mon Jun 07 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.4-1jpp
- 1.4 final
- Patch #0 is unnecessary (upstream)
- We have to build velocity against servletapi3

* Wed Feb 18 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.4-0.rc1.2jpp
- Fix a few jpackage related .spec typos, oops.

* Wed Feb 18 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.4-0.rc1.1jpp
- Added Patch #0 (velocity-1.4-rc1-ServletTest.patch) from CVS which fixes
  build problems.

* Sun May 25 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:1.3.1-2jpp
- Add Epochs to dependencies.
- Add explicit defattrs.
- Add non-versioned javadoc symlinks.
- Use sed instead of bash 2 extension when symlinking jars during build.
- Use full URL in Source.
- Fix -javadoc Group tag.
- Drop patch in favour of ant options.
- BuildRequire jpackage-utils and antlr (latter needed for Anakia tests).

* Sat May 24 2003 Richard Bullington-McGuire <rbulling@pkrinternet.com> 1.3.1-1jpp
- 1.3.1 stable release

* Fri May 23 2003 Richard Bullington-McGuire <rbulling@pkrinternet.com> 1.3-1jpp
- 1.3 stable release
- Updated for JPackage 1.5
- Run JUnit regression tests as part of the build process
- Added patch file to fix test case classpath for JUnit standard locations

* Mon May 06 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.3-0.rc1.1jpp
- 1.3.0rc1
- dropped patch
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- stricter dependency for demo package

* Wed Dec 12 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-1jpp
- 1.2
- regenerated patch and corrected manifest
- requires and buildrequires jdom >= 1.0-0.b7.1

* Wed Dec 5 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1-4jpp
- javadoc into javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.1-3jpp
- removed packager tag
- new jpp extension

* Thu Nov 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1-2jpp
- first unified release
- s/jPackage/JPackage

* Fri Sep 14 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1-1jpp
- first Mandrake release
