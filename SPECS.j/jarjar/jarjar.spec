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

Name:           jarjar
Version:        1.4
Release:        13%{?dist}
Summary:        Jar Jar Links
License:        ASL 2.0
URL:            http://code.google.com/p/jarjar/
Source0:        http://jarjar.googlecode.com/files/jarjar-src-1.4.zip
Source1:        jarjar.pom
Source2:        jarjar-util.pom
Patch0:         fix-maven-plugin.patch

BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  objectweb-asm
BuildRequires:  javapackages-local
BuildRequires:  maven
BuildRequires:  xmvn-install
Requires:       objectweb-asm

BuildArch:      noarch

%description
Jar Jar Links is a utility that makes it easy to repackage Java 
libraries and embed them into your own distribution. This is 
useful for two reasons:
You can easily ship a single jar file with no external dependencies. 
You can avoid problems where your library depends on a specific 
version of a library, which may conflict with the dependencies of 
another library.

%package maven-plugin
Summary:        Maven plugin for %{name}
Requires:       maven
Requires:       %{name} = %{version}-%{release}
Obsoletes: %{name}-maven2-plugin <= 1.0
Provides: %{name}-maven2-plugin = %{version}-%{release}

%description maven-plugin
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 -b.orig

# remove all binary libs
rm -f lib/*.jar

%mvn_package :jarjar-plugin %{name}-maven-plugin

%build
pushd lib
ln -sf $(build-classpath objectweb-asm/asm) asm-4.0.jar
ln -sf $(build-classpath objectweb-asm/asm-commons) asm-commons-4.0.jar
ln -sf $(build-classpath maven/maven-plugin-api) maven-plugin-api.jar
popd
export CLASSPATH=$(build-classpath ant)
ant jar jar-util javadoc mojo test

sed -i -e s/@VERSION@/%{version}/g maven/pom.xml

# request maven artifact installation
%mvn_artifact %{SOURCE1} dist/jarjar-%{version}.jar
%mvn_artifact %{SOURCE2} dist/jarjar-util-%{version}.jar
%mvn_artifact maven/pom.xml dist/jarjar-plugin-%{version}.jar
%mvn_alias tonic:jarjar jarjar:jarjar com.tonicsystems:jarjar com.googlecode.jarjar:jarjar
%mvn_alias tonic:jarjar-util jarjar:jarjar-util com.tonicsystems:jarjar-util
%mvn_alias com.tonicsystems.jarjar:jarjar-plugin jarjar:jarjar-plugin tonic:jarjar-plugin com.tonicsystems:jarjar-plugin

%install
%mvn_install

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr dist/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files -f .mfiles
%doc COPYING
%dir %{_javadir}/%{name}

%files maven-plugin -f .mfiles-%{name}-maven-plugin
%doc COPYING

%files javadoc
%doc COPYING
%{_javadocdir}/%{name}

%changelog
* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.4-13
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.4-12
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.4-11
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.4-10
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Mat Booth <mat.booth@redhat.com> - 1.4-9
- Fix BR on asm and install with maven

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-7
- Use .mfiles generated during build

* Fri Oct 25 2013 Vít Ondruch <vondruch@redhat.com> - 1.4-6
- Fix alias to com.googlecode.jarjar:jarjar.

* Thu Oct 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-5
- Add alias for com.googlecode:jarjar

* Sun Sep 15 2013 Mat Booth <fedora@matbooth.co.uk> - 1.4-4
- Fix contents of maven plugin jar, rhbz #1006568

* Thu Aug 08 2013 Mat Booth <fedora@matbooth.co.uk> - 1.4-3
- Update for newer guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 02 2013 Mat Booth <fedora@matbooth.co.uk> - 1.4-1
- Update to latest upstream version.
- Drop no longer needed patches.
- Drop unneeded BR/R on gnu-regexp.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Sep 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-7
- Install COPYING file with javadoc package
- Update to current packaging guidelines
- Remove rpm bug workaround

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-4
- Do not require maven2.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Mat Booth <fedora@matbooth.co.uk> 1.0-2
- Fix pom names RHBZ #655805.
- Drop versioned jars/javadocs.

* Wed Sep 29 2010 Mary Ellen Foster <mefoster@gmail.com> 1.0-1
- Update to 1.0
- Change project URLs
- Fix FTBFS
- Remove gcj stuff

* Fri Feb  5 2010 Mary Ellen Foster <mefoster at gmail.com> 0.9-5
- Make javadoc noarch

* Tue Nov 17 2009 Mary Ellen Foster <mefoster at gmail.com> 0.9-4
- Re-add GCJ bits
- Require jpackage-utils (for directories)
- Link javadoc dir

* Sun Nov  1 2009 Mary Ellen Foster <mefoster at gmail.com> 0.9-3
- Initial package, based on jpackage jarjar-0.9-2
