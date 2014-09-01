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
Name:          janino
Version:       2.6.1
Release:       21%{?dist}
Summary:       An embedded Java compiler
License:       BSD
URL:           http://docs.codehaus.org/display/JANINO/Home
Source0:       http://dist.codehaus.org/%{name}/%{name}-%{version}.zip
Source1:       http://repo1.maven.org/maven2/org/codehaus/%{name}/%{name}-parent/%{version}/%{name}-parent-%{version}.pom
Source2:       http://repo1.maven.org/maven2/org/codehaus/%{name}/commons-compiler/%{version}/commons-compiler-%{version}.pom
Source3:       http://repo1.maven.org/maven2/org/codehaus/%{name}/commons-compiler-jdk/%{version}/commons-compiler-jdk-%{version}.pom
Source4:       http://repo1.maven.org/maven2/org/codehaus/%{name}/%{name}/%{version}/%{name}-%{version}.pom
# remove org.codehaus.mojo findbugs-maven-plugin 1.1.1, javancss-maven-plugin 2.0, jdepend-maven-plugin 2.0-beta-2
# change artifactId ant-nodeps in ant
Patch0:        %{name}-%{version}-poms.patch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: codehaus-parent

BuildRequires: ant
BuildRequires: junit

#BuildRequires: buildnumber-maven-plugin
BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-source-plugin
BuildRequires: maven-surefire-provider-junit

BuildArch:     noarch

%description
Janino is a super-small, super-fast Java compiler. Not only can it compile
a set of source files to a set of class files like the JAVAC tool, but also
can it compile a Java expression, block, class body or source file in
memory, load the bytecode and execute it directly in the same JVM. Janino
is not intended to be a development tool, but an embedded compiler for
run-time compilation purposes, e.g. expression evaluators or "server pages"
engines like JSP.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

find . -name "*.jar" -delete
find . -name "*.class" -delete

for m in commons-compiler \
  commons-compiler-jdk \
  %{name};do
  mkdir -p ${m}/src
  (
    cd ${m}/src/
    unzip -qq  ../../${m}-src.zip
    if [ -f org.codehaus.commons.compiler.properties ]; then
      mkdir -p main/resources
      mv org.codehaus.commons.compiler.properties main/resources
    fi
  )
done

cp -p %{SOURCE1} pom.xml
cp -p %{SOURCE2} commons-compiler/pom.xml
cp -p %{SOURCE3} commons-compiler-jdk/pom.xml
cp -p %{SOURCE4} %{name}/pom.xml

# RHBZ #842604
sed -i 's#<source>1.2</source>#<source>1.5</source>#' pom.xml
sed -i 's#<target>1.1</target>#<target>1.5</target>#' pom.xml

%patch0 -p1

perl -pi -e 's/\r$//g' new_bsd_license.txt README.txt

# Cannot run program "svn"
%pom_remove_plugin :buildnumber-maven-plugin

%build

%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc new_bsd_license.txt README.txt

%files javadoc -f .mfiles-javadoc
%doc new_bsd_license.txt

%changelog
* Wed Aug 13 2014 Liu Di <liudidi@gmail.com> - 2.6.1-21
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.6.1-19
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 gil cattaneo <puntogil@libero.it> 2.6.1-17
- switch to XMvn
- minor changes to adapt to current guideline

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.6.1-15
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jul 24 2012 gil cattaneo <puntogil@libero.it> 2.6.1-14
- Rebuilt RHBZ #842604 (compile with -target 1.5 or greater)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 gil cattaneo <puntogil@libero.it> 2.6.1-12
- add codehaus-parent to BR

* Thu Apr 19 2012 gil cattaneo <puntogil@libero.it> 2.6.1-11
- Remove janino-parent as a BuildRequirement

* Wed Apr 18 2012 gil cattaneo <puntogil@libero.it> 2.6.1-10
- moved all of the jar files into janino subdirectory

* Wed Apr 18 2012 gil cattaneo <puntogil@libero.it> 2.6.1-9
- merged commons-compiler, commons-compiler-jdk and janino-parent in main package

* Wed Apr 18 2012 gil cattaneo <puntogil@libero.it> 2.6.1-8
- add janino-parent

* Mon Apr 16 2012 gil cattaneo <puntogil@libero.it> 2.6.1-7
- Remove commons-compiler as a BuildRequirement
- Add janino-parent as a Requirement

* Fri Apr 13 2012 gil cattaneo <puntogil@libero.it> 2.6.1-6
- removed BR unzip

* Fri Apr 13 2012 gil cattaneo <puntogil@libero.it> 2.6.1-5
- commons-compiler spec file merged

* Fri Apr 13 2012 gil cattaneo <puntogil@libero.it> 2.6.1-4
- added missing BR maven-surefire-provider-junit4 for prevent mock build failure

* Tue Apr 10 2012 gil cattaneo <puntogil@libero.it> 2.6.1-3
- removed janino-parent commons-compiler modules.

* Sun Mar 25 2012 gil cattaneo <puntogil@libero.it> 2.6.1-2
- janino janino-parent commons-compiler spec file merged

* Tue Mar 20 2012 Mary Ellen Foster <mefoster at gmail.com> - 2.6.1-1
- Update to 2.6.1, with new build system and all
- Prepare for re-review

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 27 2009 Mary Ellen Foster <mefoster at gmail.com> - 2.5.15-3
- Changed group tag on main package and sub-package
- Fixed default attribute on files section

* Mon Oct 26 2009 Mary Ellen Foster <mefoster at gmail.com> - 2.5.15-2
- Removed gcj bits

* Sun Oct 25 2009 Mary Ellen Foster <mefoster at gmail.com> - 2.5.15-1
- Initial package, based on Alexander Kurtakov's JPackage and Mandriva package
