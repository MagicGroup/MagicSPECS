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
#    distributio4.3n.
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

Name:           tagsoup
Version:        1.2.1
Release:        8%{?dist}
Epoch:          0
Summary:        A SAX-compliant HTML parser written in Java 
# AFL/GPLv2+ license for src/java/org/ccil/cowan/tagsoup/PYXScanner.java is
# likely mixup of upstream but needs to be cleared up
License:        ASL 2.0 and (GPLv2+ or AFL)
Source0:        http://home.ccil.org/~cowan/XML/tagsoup/tagsoup-1.2.1-src.zip
URL:            http://home.ccil.org/~cowan/XML/tagsoup/
Group:          Text Processing/Markup/XML
Source1:        http://repo1.maven.org/maven2/org/ccil/cowan/tagsoup/tagsoup/%{version}/tagsoup-%{version}.pom
# fix version
Patch0:         tagsoup-1.2.1-man.patch
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant
BuildRequires:  ant-apache-xalan2
BuildRequires:  bash
BuildRequires:  xalan-j2
Requires:       jpackage-utils >= 0:1.6
BuildArch:      noarch

%description
TagSoup is a SAX-compliant parser written in Java that, instead of
parsing well-formed or valid XML, parses HTML as it is found in the wild: nasty
and brutish, though quite often far from short. TagSoup is designed for people
who have to process this stuff using some semblance of a rational application
design. By providing a SAX interface, it allows standard XML tools to be
applied to even the worst HTML.

%package javadoc
Summary:       Javadoc for %{name}
Group:         Documentation
Requires:      jpackage-utils >= 0:1.6

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

find . -name '*.class' -delete
find . -name "*.jar" -delete
%patch0 -p0

%build

export CLASSPATH=$(build-classpath xalan-j2-serializer xalan-j2)
ant \
  -Dtagsoup.version=%{version} \
  -Dj2se.apiurl=%{_javadocdir}/java \
  dist docs-api

%install

mkdir -p %{buildroot}%{_javadir}
install -m 644 dist/lib/%{name}-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr docs/api/* %{buildroot}%{_javadocdir}/%{name}

mkdir -p %{buildroot}%{_mandir}/man1
install -m 644 %{name}.1 %{buildroot}%{_mandir}/man1/

%files -f .mfiles
%{_mandir}/man1/%{name}.1.gz
%doc CHANGES LICENSE README TODO %{name}.txt

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.1-7
- Use .mfiles generated during build

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.1-4
- Remove ppc64 ExcludeArch
- Resolves: rhbz#502328

* Thu Nov 08 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.1-3
- Upstream relicensed to ASL 2.0, but likely accidentally left some things

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 09 2012 gil cattaneo <puntogil@libero.it> 0:1.2.1-1
- Upgraded to 1.2.1
- remove ant-nodeps reference
- changed group in javadoc sub package (from Development/Documentation in Documentation)
- add maven metadata
- add manual
- Adapt to current guidelines.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0.1-7
- BR ant-apache-xalan2.

* Tue Dec 21 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0.1-6
- BR java 6.

* Tue Dec 21 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0.1-5
- Fix FTBFS.
- Drop gcj.
- Adapt to current guidelines.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0.1-4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 24 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0:1.0.1-3.3
- Fix FTBFS: disabled ppc64 build

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0.1-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0.1-2.2
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.0.1-2jpp.1
- Autorebuild for GCC 4.3

* Mon Feb 12 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.0.1-1jpp.1.fc7
- rpmlint fixes
- Use fedora approved naming convention
- Fix buildroot to conform to Fedora packaging guidelines
- Add LICENSE to the rpm and label as doc
- Remove Vendor and Distribution tags
- Minor formatting fixes
- Use proper javaoc handling
- Add requires and requires(x) on jpackage-utils
- Add GCJ support
- BR on ant-trax and xalan-j2

* Sun Jan 20 2007 Sebastiano Vigna <vigna@dsi.unimi.it> 0:1.0.1-1jpp
- Upgraded to 1.0.1

* Mon Feb 27 2006 Fernando Nasser <fnasser@redhat.com> 0:1.0rc-2jpp
- First JPP 1.7 version

* Fri Jan 28 2005 Sebastiano Vigna <vigna@acm.org> 0:1.0rc-1jpp
- First JPackage version
