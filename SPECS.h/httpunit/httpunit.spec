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

Name:           httpunit
Version:        1.7
Release:        19%{?dist}
Epoch:          0
Summary:        Automated web site testing toolkit
License:        MIT and ASL 2.0
# ./create-tarball.sh %%{version}
Source0:        httpunit-1.7-clean.tar.gz
Source1:        http://repo1.maven.org/maven2/httpunit/httpunit/1.7/httpunit-1.7.pom
# replacement for non-free XML DTD files
Source2:        https://raw.github.com/apache/tomcat/TOMCAT_7_0_42/java/javax/servlet/resources/web-app_2_2.dtd
Source3:        https://raw.github.com/apache/tomcat/TOMCAT_7_0_42/java/javax/servlet/resources/web-app_2_3.dtd
Source4:        https://raw.github.com/apache/tomcat/TOMCAT_7_0_42/java/javax/servlet/resources/web-app_2_4.xsd
# sources 2-4 are licensed under ASL 2.0
Source5:        http://www.apache.org/licenses/LICENSE-2.0.txt
Patch1:         %{name}-rhino-1.7.7.patch
Patch2:         %{name}-servlettest.patch
Patch3:         %{name}-servlet31.patch
Patch4:         junit4.patch
URL:            http://httpunit.sourceforge.net/
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  nekohtml
BuildRequires:  jtidy
BuildRequires:  junit >= 0:3.8
BuildRequires:  tomcat-servlet-3.1-api
BuildRequires:  javamail >= 0:1.3
BuildRequires:  rhino
BuildRequires:  java-devel >= 1:1.6.0

Requires:       junit >= 0:3.8
Requires:       tomcat-servlet-3.1-api
# As of 1.5, requires either nekohtml or jtidy, and prefers nekohtml.
Requires:       nekohtml
Requires:       rhino

BuildArch:      noarch

Obsoletes:      %{name}-demo < %{epoch}:%{version}

%description
HttpUnit emulates the relevant portions of browser behavior, including form
submission, JavaScript, basic http authentication, cookies and automatic page
redirection, and allows Java test code to examine returned pages either as
text, an XML DOM, or containers of forms, tables, and links.
A companion framework, ServletUnit is included in the package.

%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
Javadoc for %{name}

%package        doc
Summary:        Documentation for %{name}
Requires:       %{name}-javadoc

%description    doc
Documentation for %{name}

%prep
%setup -q
# patch to work with rhino 1.7.7
%patch1 -p1
# add META-INF
%patch2
%patch3 -p1
%patch4

sed -i -e 's|destdir|encoding="iso-8859-1" destdir|g' build.xml

sed -i -e 's|setCharEncoding( org.w3c.tidy.Configuration.UTF8 )|setInputEncoding("UTF-8")|g' src/com/meterware/httpunit/parsing/JTidyHTMLParser.java

# remove all binary libs and javadocs
find . -name "*.jar" -exec rm -f {} \;
rm -rf doc/api

ln -s \
  %{_javadir}/junit.jar \
  %{_javadir}/jtidy.jar \
  %{_javadir}/nekohtml.jar \
  %{_javadir}/tomcat-servlet-api.jar \
  %{_javadir}/js.jar \
  %{_javadir}/xerces-j2.jar \
  jars

mv %{SOURCE1} pom.xml
mv %{SOURCE2} META-INF/
mv %{SOURCE3} META-INF/
mv %{SOURCE4} META-INF/
mv %{SOURCE5} LICENSE-ASL


%build
export CLASSPATH=$(build-classpath javamail)
export ANT_OPTS="-Dfile.encoding=iso-8859-1"
ant -Dbuild.compiler=modern -Dbuild.sysclasspath=last \
  jar javadocs test servlettest 

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# Javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# POM
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar


# Avoid having api in doc
rm -rf doc/api

# Fix link between doc and javadoc
pushd doc
ln -sf %{_javadocdir}/%{name} api
popd

%files -f .mfiles
%doc LICENSE-ASL

%files javadoc
%doc LICENSE-ASL
%{_javadocdir}/%{name}

%files doc
%doc doc/*

%changelog
* Wed Sep 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-19
- Port to Rhino 1.7.7
- Resolves: rhbz#1263627

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 09 2015 Michal Srb <msrb@redhat.com> - 0:1.7-17
- Port to servlet 3.1

* Thu Mar 5 2015 Alexander Kurtakov <akurtako@redhat.com> 0:1.7-16
- Rebuild for servlet 3.1.

* Fri Jun 27 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 0:1.7-15
- Fix FTBFS due to xmvn changes (#1106777)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep 18 2013 Michal Srb <msrb@redhat.com> - 0:1.7-13
- Replace non-free XML DTD files
- Drop group tag
- Fix R/BR
- bump spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7-10
- BR/R new tomcat servlet

* Tue Aug 21 2012 Tomas Radej <tradej@redhat.com> - 0:1.7-9
- Added POM File
- Added Requires on jpackage-utils to javadoc package

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.7-7
- Fix build against junit 4.x.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 6 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.7-5
- Fix build.
- Adapt to current guidelines.

* Mon Mar 7 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.7-4
- Adopt to current guidelines.
- Fix various rpmlint errors/warnings.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 21 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.7-2
- BR java 1.6.0.
- Remove jaf from exported classpath.

* Wed Oct 20 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.7-1
- Update to 1.7.
- Drop demo subpackage - it was never upstream.
- Use default permissions.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.6.2-2
- drop repotag

* Wed Feb 14 2007 Permaine Cheung <pcheung@redhat.com> - 0:1.6.2-1jpp.1
- Fixed buildroot, release
- Renamed manual subpackage to doc subpackage as per fedora packaging guideline
- Got rid of Vendor and Distribution tags.

* Mon May 08 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.6.2-1jpp
- Upgrade to 1.6.2
- First JPP-1.7 release

* Sat Nov 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6-1jpp
- Update to 1.6.
- Require Servlet API 2.3, ServletUnit doesn't work with 2.4.
- Fix classpath construction during build; now works also with classpathx-mail.
- Apply upstream patch to build with Java 1.5 (built with 1.4.2 though).
- Patch to fix class path in servlet tests during build.

* Wed Sep 22 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.5.4-3jpp
- Patched JavaScript.java to not handle  NotAFunctionException,
  as in Rhino-1.5-R5 this now is deprecated, not thrown any more
  and extends Error; also not to handle PropertyException not thrown
  any more in that try block 

* Wed Aug 25 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.5.4-2jpp
- Build with ant-1.6.2

* Thu Aug 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.5.4-1jpp
- Update to 1.5.4.
- Save .spec in UTF-8.

* Mon May  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.5.3-2jpp
- Fix non-versioned javadoc symlinking.

* Mon Apr 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.5.3-1jpp
- Update to 1.5.3 and JPackage 1.5.
- Include non-versioned javadoc symlink.

* Tue Mar  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 1.5.2-1jpp
- Update to 1.5.2.
- Run unit tests during build.

* Wed Dec 18 2002 Ville Skyttä <ville.skytta at iki.fi> - 1.5.1-1jpp
- Update to 1.5.1.

* Mon Nov  4 2002 Ville Skyttä <ville.skytta at iki.fi> 1.5-1jpp
- Update to 1.5.

* Thu Oct  3 2002 Ville Skyttä <ville.skytta at iki.fi> 1.4.6-1jpp
- Update to 1.4.6.

* Fri Sep  6 2002 Ville Skyttä <ville.skytta at iki.fi> 1.4.5-0.cvs20020906.1jpp
- Update to 1.4.5 (CVS 2002-09-06, CVS version needed since we have JUnit 3.8).
- Add requirements.
- Add rhino and xerces to build requirements.
- Fix/add Distribution, License, Vendor tags.
- Use sed instead of bash2 extension when symlinking jars during build.
- s/Copyright/License/

* Tue Jul 16 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.4.1-1jpp
- first jpp release
