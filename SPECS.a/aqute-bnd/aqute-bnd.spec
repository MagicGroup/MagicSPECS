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

Name:           aqute-bnd
Version:        0.0.363
Release:        16%{?dist}
Summary:        BND Tool
License:        ASL 2.0
URL:            http://www.aQute.biz/Code/Bnd

# NOTE : sources for 0.0.363 are no longer available
# The following links would work for 0.0.370-0.0.401 version range, but
# we need to stay by 0.0.363 to minimize problems during the 1.43.0 introduction
Source0:        http://www.aqute.biz/repo/biz/aQute/bnd/%{version}/bnd-%{version}.jar
Source1:        http://www.aqute.biz/repo/biz/aQute/bnd/%{version}/bnd-%{version}.pom
Source2:        aqute-service.tar.gz

# from Debian, add source compatibility with ant 1.9
Patch0:         %{name}-%{version}-ant19.patch
# fixing base64 class ambiguity
Patch1:         %{name}-%{version}-ambiguous-base64.patch


BuildArch:      noarch

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  ant
BuildRequires:  felix-osgi-compendium
BuildRequires:  felix-osgi-core
BuildRequires:  junit

Requires:       java-headless

%description
The bnd tool helps you create and diagnose OSGi R4 bundles.
The key functions are:
- Show the manifest and JAR contents of a bundle
- Wrap a JAR so that it becomes a bundle
- Create a Bundle from a specification and a class path
- Verify the validity of the manifest entries
The tool is capable of acting as:
- Command line tool
- File format
- Directives
- Use of macros

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c

mkdir -p target/site/apidocs/
mkdir -p target/classes/
mkdir -p src/main/
mv OSGI-OPT/src src/main/java
pushd src/main/java
tar xfs %{SOURCE2}
popd
sed -i "s|import aQute.lib.filter.*;||g" src/main/java/aQute/bnd/make/ComponentDef.java
sed -i "s|import aQute.lib.filter.*;||g" src/main/java/aQute/bnd/make/ServiceComponent.java

# get rid of eclipse plugins which are not usable anyway and complicate
# things
rm -rf src/main/java/aQute/bnd/annotation/Test.java \
       src/main/java/aQute/bnd/{classpath,jareditor,junit,launch,plugin} \
       aQute/bnd/classpath/messages.properties

# remove bundled stuff
find aQute/ -type f -name "*.class" -delete

%patch0 -p1 -b .ant19
%patch1 -p1 -b .base64

# Convert CR+LF to LF
sed -i "s|\r||g" LICENSE
mkdir temp
(
cd temp
mkdir -p target/classes/
mkdir -p src/main/
%jar -xf ../aQute/bnd/test/aQute.runtime.jar
mv OSGI-OPT/src src/main/java
find aQute -type f -name "*.class" -delete
)
rm -rf aQute/bnd/test/aQute.runtime.jar

%build
export LANG=en_US.utf8


(
cd temp
%{javac} -d target/classes -target 1.5 -source 1.5 -classpath $(build-classpath junit felix/org.osgi.core felix/org.osgi.compendium) $(find src/main/java -type f -name "*.java")
for f in $(find aQute/ -type f -not -name "*.class"); do
    cp -p $f target/classes/$f
done
  (
   cd target/classes
   %jar cmf ../../META-INF/MANIFEST.MF ../../../aQute/bnd/test/aQute.runtime.jar *
  )
)
rm -r temp
export OPT_JAR_LIST=:
export CLASSPATH=$(build-classpath ant)

%{javac} -d target/classes -target 1.5 -source 1.5 $(find src/main/java -type f -name "*.java")
%{javadoc} -d target/site/apidocs -sourcepath src/main/java aQute.lib.header aQute.lib.osgi aQute.lib.qtokens aQute.lib.filter
cp -p LICENSE maven-dependencies.txt plugin.xml pom.xml target/classes
for f in $(find aQute/ -type f -not -name "*.class"); do
    cp -p $f target/classes/$f
done
pushd target/classes
%{jar} cmf ../../META-INF/MANIFEST.MF ../%{name}-%{version}.jar *
popd

%install
# jars
install -Dpm 644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -Dm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%add_maven_depmap

%files -f .mfiles
%doc LICENSE

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.0.363-16
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 0.0.363-15
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-13
- Use .mfiles generated during build

* Fri May 09 2014 Jaromir Capik <jcapik@redhat.com> - 0.0.363-12
- Fixing ambiguous base64 class

* Fri May 09 2014 Gil Cattaneo <puntogil@libero.it> 0.0.363-11
- fix rhbz#991985
- add source compatibility with ant 1.9
- remove and rebuild from source aQute.runtime.jar
- update to current packaging guidelines

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.0.363-10
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.0.363-6
- Get rid of unusable eclipse plugins to simplify dependencies

* Fri Mar 02 2012 Jaromir Capik <jcapik@redhat.com> - 0.0.363-5
- Fixing build failures on f16 and later

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Jaromir Capik <jcapik@redhat.com> - 0.0.363-3
- Resurrection of bundled non-class files

* Thu Sep 22 2011 Jaromir Capik <jcapik@redhat.com> - 0.0.363-2
- Bundled classes removed
- jpackage-utils dependency added to the javadoc subpackage

* Wed Sep 21 2011 Jaromir Capik <jcapik@redhat.com> - 0.0.363-1
- Initial version (cloned from aqute-bndlib 0.0.363)
