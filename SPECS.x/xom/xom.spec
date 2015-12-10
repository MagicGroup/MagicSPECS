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

# To build with dom4j issue rpmbuild --with dom4j xom.spec

%define with_dom4j %{?_with_dom4j:1}%{!?_with_dom4j:0}
%define without_dom4j %{!?_with_dom4j:1}%{?_with_dom4j:0}

Summary:        XML Object Model
Name:           xom
Version:        1.0
Release:        19%{?dist}
Epoch:          0
License:        LGPLv2
URL:            http://www.xom.nu
Group:          Development/Libraries
Source0:        http://www.cafeconleche.org/XOM/xom-1.0.tar.gz
Source1:        http://central.maven.org/maven2/xom/xom/1.0/xom-1.0.pom

# Evidently gjdoc doesn't know about the noqualifier option; also, it
# must do linkoffline and not link
Patch0:         %{name}-gjdocissues.patch
# FIXME:  file this
# I don't know if this is a libgcj bug or if this is a legitimate typo
# in build.xml
Patch1:         %{name}-betterdocclasspath.patch
# Replace icu4j by java.text from JDK to reduce dependency chain
Patch2:         %{name}-Replace-icu4j-with-JDK.patch

BuildRequires:  ant >= 0:1.6, jpackage-utils >= 0:1.6
BuildRequires:  junit
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
%if %{with_dom4j}
BuildRequires:  dom4j
%endif
BuildRequires:  xml-commons-apis

BuildRequires:  tagsoup
# Use JAXP implementation in JDK
BuildRequires:  java-devel
BuildRequires:  xml-commons-resolver
BuildRequires:  servlet

Requires:  xalan-j2
Requires:  xerces-j2
Requires:  xml-commons-apis
BuildArch: noarch

%description
XOM is a new XML object model. It is an open source (LGPL),
tree-based API for processing XML with Java that strives
for correctness, simplicity, and performance, in that order.
XOM is designed to be easy to learn and easy to use. It
works very straight-forwardly, and has a very shallow
learning curve. Assuming you're already familiar with XML,
you should be able to get up and running with XOM very quickly.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%package demo
Summary:        Samples for %{name}
Requires:       %{name} = %{version}-%{release}

%description demo
This package provides %{summary}.

%prep
%setup -q -n XOM
%patch0
%patch1
%patch2 -p1
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# disable tests that require icu4j
rm -f src/nu/xom/tests/{Encoding,Verifier}Test.java

cp %{SOURCE1} pom.xml
# remove it from pom.xml since it's not needed anymore
%pom_remove_dep com.ibm.icu:icu4j


%build
pushd lib
ln -sf $(build-classpath junit) junit.jar
ln -sf $(build-classpath xerces-j2) xercesImpl.jar
ln -sf $(build-classpath xalan-j2) xalan.jar
ln -sf $(build-classpath xml-commons-apis) xmlParserAPIs.jar
popd
mkdir lib2
pushd lib2
ln -sf $(build-classpath tagsoup) tagsoup-1.0rc1.jar
ln -sf $(build-classpath xml-commons-resolver) resolver.jar

%if %{with_dom4j}
ln -sf $(build-classpath dom4j) dom4j.jar
%endif

ln -sf $(build-classpath servlet) servlet.jar
popd

ant jar samples betterdoc

# Fix encoding
sed -i 's/\r//g' LICENSE.txt
pushd apidocs
for f in `find -name \*.css -o -name \*.html`; do
  sed -i 's/\r//g' $f
done
popd

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 build/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}/

# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 644 build/xom-samples.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/

# POM
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -m 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

# Workaround for RPM bug #646523 - can't change symlink to directory
# TODO: Remove this in F-23
%pretrans javadoc -p <lua>
dir = "%{_javadocdir}/%{name}"
dummy = posix.readlink(dir) and os.remove(dir)

%files -f .mfiles
%doc overview.html
%doc README.txt
%doc LICENSE.txt
%doc Todo.txt
%doc lgpl.txt
%doc %{name}.graffle

%files javadoc
%{_javadocdir}/*

%files demo
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/xom-samples.jar

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 0:1.0-19
- 为 Magic 3.0 重建

* Sun Oct 25 2015 Liu Di <liudidi@gmail.com> - 0:1.0-18
- 为 Magic 3.0 重建

* Wed Aug 13 2014 Liu Di <liudidi@gmail.com> - 0:1.0-17
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 23 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-15
- Update to current packaging guidelines
- Remove versioned JARs, resolves: rhbz#1022173
- Add workaround for rhbz#646523

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-13
- Replace BR on libgcj with generic java-devel

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-11
- Remove icu4j dependency from pom.xml

* Mon Oct  8 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-10
- Replace icu4j Normalizer with java.text.Normalizer from JDK

* Fri Aug 10 2012 Andy Grimm <agrimm@gmail.com> - 0:1.0-9
- add POM

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-8.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-7.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-6.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Mar 11 2010 Peter Lemenkov <lemenkov@gmail.com> - 0:1.0-5.6
- Added missing Requires: jpackage-utils (%%{_javadir} and %%{_javadocdir})

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-5.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-4.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-3.5
- drop repotag
- fix license tag

* Mon Mar 26 2007 Nuno Santos <nsantos@redhat.com> 0:1.0-3jpp.4.fc7
- Apply patch from bugs.michael@gmx.net to fix unowned directory

* Mon Mar 12 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.0-3jpp.3.fc7
- Make build with dom4j optional (off by default)

* Mon Mar 12 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.0-3jpp.2.fc7
- Remove BR on classpathx-jaxp since libgcj includes the required bits

* Wed Feb 14 2007 Andrew Overholt <overholt@redhat.com> 0:1.0-3jpp.1
- Update for Fedora review
- Remov Vendor & Distribution tags
- Add .1%%{?dist} to release
- Remove bad javadoc symlinking and %%post{,un}
- Fixe buildroot
- Use %%doc for doc files
- Change group to Development/Libraries
- Remove running of tests; should perhaps move to %%check
- Fix encoding of LICENSE.txt and generated javadocs
- Remove BR: saxon

* Tue Feb 28 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-3jpp
- Remove dependency on clover10 (non-free)

* Sun Feb 26 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-2jpp
- First JPP 1.7 release

* Wed Aug 17 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0-1jpp
- First JPP release
