# Copyright statement from JPackage this file is derived from:

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

Name:           xstream
Version:        1.4.7
Release:        9%{?dist}
Summary:        Java XML serialization library
License:        BSD
URL:            http://xstream.codehaus.org/
Source0:        https://nexus.codehaus.org/content/repositories/releases/com/thoughtworks/xstream/xstream-distribution/%{version}/xstream-distribution-%{version}-src.zip
BuildRequires: java-devel

BuildRequires:  maven-local
BuildRequires:  mvn(cglib:cglib)
BuildRequires:  mvn(commons-cli:commons-cli)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-lang:commons-lang)
BuildRequires:  mvn(dom4j:dom4j)
BuildRequires:  mvn(javassist:javassist)
BuildRequires:  mvn(joda-time:joda-time)
BuildRequires:  mvn(net.sf.kxml:kxml2)
BuildRequires:  mvn(net.sf.kxml:kxml2-min)
BuildRequires:  mvn(org.apache.maven.plugins:maven-release-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus:codehaus-parent:pom:)
BuildRequires:  mvn(org.codehaus.jettison:jettison)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.codehaus.woodstox:woodstox-core-asl)
BuildRequires:  mvn(org.hibernate:hibernate-core)
BuildRequires:  mvn(org.hibernate:hibernate-envers)
BuildRequires:  mvn(org.hsqldb:hsqldb)
BuildRequires:  mvn(org.jdom:jdom)
BuildRequires:  mvn(org.jdom:jdom2)
BuildRequires:  mvn(org.json:json)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
BuildRequires:  mvn(oro:oro)
BuildRequires:  mvn(stax:stax)
BuildRequires:  mvn(stax:stax-api)
BuildRequires:  mvn(xom:xom)
BuildRequires:  mvn(xpp3:xpp3_min)


BuildArch:     noarch

%description
XStream is a simple library to serialize objects to XML 
and back again. A high level facade is supplied that 
simplifies common use cases. Custom objects can be serialized 
without need for specifying mappings. Speed and low memory 
footprint are a crucial part of the design, making it suitable 
for large object graphs or systems with high message throughput. 
No information is duplicated that can be obtained via reflection. 
This results in XML that is easier to read for humans and more 
compact than native Java serialization. XStream serializes internal 
fields, including private and final. Supports non-public and inner 
classes. Classes are not required to have default constructor. 
Duplicate references encountered in the object-model will be 
maintained. Supports circular references. By implementing an 
interface, XStream can serialize directly to/from any tree 
structure (not just XML). Strategies can be registered allowing 
customization of how particular types are represented as XML. 
When an exception occurs due to malformed XML, detailed diagnostics 
are provided to help isolate and fix the problem.


%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
%{name} API documentation.

%package        hibernate
Summary:        hibernate module for %{name}
Requires:       %{name} = %{version}-%{release}

%description    hibernate
hibernate module for %{name}.

%package        benchmark
Summary:        benchmark module for %{name}
Requires:       %{name} = %{version}-%{release}

%description    benchmark
benchmark module for %{name}.

%package parent
Summary:        Parent POM for %{name}
Requires:       %{name} = %{version}-%{release}

%description parent
Parent POM for %{name}.


%prep
%setup -qn %{name}-%{version}
find . -name "*.class" -print -delete
find . -name "*.jar" -print -delete

# Remove org.apache.maven.wagon:wagon-webdav
%pom_xpath_remove "pom:project/pom:build/pom:extensions"
# Require org.codehaus.xsite:xsite-maven-plugin
%pom_disable_module xstream-distribution
%pom_remove_plugin :xsite-maven-plugin
%pom_remove_plugin :jxr-maven-plugin
# Unwanted
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-dependency-plugin

%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'org.codehaus.woodstox' ]/pom:artifactId" woodstox-core-asl xstream
%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'cglib' ]/pom:artifactId" cglib xstream
# Remove xmlpull classes provides by xpp3
%pom_remove_dep :xmlpull xstream
# Require unavailable proxytoys:proxytoys
%pom_remove_plugin :maven-dependency-plugin xstream

%pom_remove_plugin :maven-javadoc-plugin xstream

%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'cglib' ]/pom:artifactId" cglib xstream-hibernate
%pom_xpath_inject "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'junit' ]" "<scope>test</scope>" xstream-hibernate
%pom_remove_plugin :maven-dependency-plugin xstream-hibernate
%pom_remove_plugin :maven-javadoc-plugin xstream-hibernate

%pom_xpath_inject "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'junit' ]" "<scope>test</scope>" xstream-benchmark
%pom_remove_plugin :maven-javadoc-plugin xstream-benchmark

%mvn_file :%{name} %{name}/%{name} %{name}
%mvn_file :%{name}-benchmark %{name}/%{name}-benchmark %{name}-benchmark

%mvn_package :%{name}

%build
# test skipped for unavailable test deps (com.megginson.sax:xml-writer)
%mvn_build -f -s

%install
%mvn_install

# Workaround for RPM bug #646523 - can't change symlink to directory
# TODO: Remove this in F-22
%pretrans javadoc -p <lua>
dir = "%{_javadocdir}/%{name}"
dummy = posix.readlink(dir) and os.remove(dir)

%files -f .mfiles
%doc LICENSE.txt README.txt
%dir %{_javadir}/%{name}
%files parent -f .mfiles-%{name}-parent
%files hibernate -f .mfiles-%{name}-hibernate
%files benchmark -f .mfiles-%{name}-benchmark

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 1.4.7-9
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.4.7-8
- 为 Magic 3.0 重建

* Tue Aug 12 2014 Liu Di <liudidi@gmail.com> - 1.4.7-7
- 为 Magic 3.0 重建

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.7-6
- Fix build-requires on codehaus-parent

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 07 2014 Michael Simacek <msimacek@redhat.com> - 1.4.7-4
- Split into subpackages

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.7-3
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Michal Srb <msrb@redhat.com> - 1.4.7-2
- Spec file cleanup
- Fix BR
- Build with kxml2 and json

* Mon Feb 10 2014 Michal Srb <msrb@redhat.com> - 1.4.7-1
- Update to latest upstream release 1.4.7

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 1.4.6-1
- Update to upstream release 1.4.6

* Thu Oct 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.5-3
- Rebuild to move arch-independant JARs out of %%_jnidir

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.5-2
- Rebuild to regenerate broken POM files
- Related: rhbz#1021484

* Sun Oct 20 2013 Matt Spaulding <mspaulding06@gmail.com> 1.4.5-1
- update to 1.4.5

* Tue Aug 20 2013 gil cattaneo <puntogil@libero.it> 1.4.4-1
- update to 1.4.4
- switch to XMvn

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.1-7
- Update to current packaging guidelines

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.1-6
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jun 14 2010 Alexander Kurtakov <akurtako@redhat.com> 1.3.1-1
- Update to 1.3.1.
- Install maven pom and depmap.

* Wed Dec 02 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.2.2-4
- Cosmetic fixes

* Fri Nov 27 2009 Lubomir Rintel <lkundrak@v3.sk> - 0:1.2.2-3
- Drop gcj (suggested by Jochen Schmitt), we seem to need OpenJDK anyway
- Fix -javadoc Require
- Drop epoch

* Sun Nov 01 2009 Lubomir Rintel <lkundrak@v3.sk> - 0:1.2.2-2
- Greatly simplify for Fedora
- Disable tests, we don't have all that's required to run them
- Remove maven build

* Fri Jul 20 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.2.2-1jpp
- Upgrade to 1.2.2
- Build with maven2 by default
- Add poms and depmap frags

* Tue May 23 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3-1jpp
- Upgrade to 1.1.3
- Patched to work with bea

* Mon Sep 13 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0.2-2jpp
- Drop saxpath requirement
- Require jaxen >= 0:1.1

* Mon Aug 30 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0.2-1jpp
- Upgrade to 1.0.2
- Delete included binary jars
- Change -Dbuild.sysclasspath "from only" to "first" (DynamicProxyTest)
- Relax some versioned dependencies
- Build with ant-1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0.1-2jpp
- Upgrade to ant-1.6.X

* Tue Jun 01 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0.1-1jpp
- Upgrade to 1.0.1

* Fri Feb 13 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.3-1jpp
- Upgrade to 0.3
- Add manual subpackage

* Mon Jan 19 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.2-1jpp
- First JPackage release
