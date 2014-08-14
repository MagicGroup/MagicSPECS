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

Name:           javacc
Version:        5.0
Release:        12%{?dist}
Epoch:          0
Summary:        A parser/scanner generator for java
License:        BSD
Source0:        http://java.net/projects/%{name}/downloads/download/%{name}-%{version}src.tar.gz
Source1:        javacc.sh
Source2:        jjdoc
Source3:        jjtree
Patch0:         0001-Add-javadoc-target-to-build.xml.patch
URL:            http://javacc.java.net/
Requires:       java-headless
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  junit
BuildRequires:  javacc
BuildRequires:  java-devel

BuildArch:      noarch

%description 
Java Compiler Compiler (JavaCC) is the most popular parser generator for use
with Java applications. A parser generator is a tool that reads a grammar
specification and converts it to a Java program that can recognize matches to
the grammar. In addition to the parser generator itself, JavaCC provides other
standard capabilities related to parser generation such as tree building (via
a tool called JJTree included with JavaCC), actions, debugging, etc.

%package manual
Summary:        Manual for %{name}

%description manual
Manual for %{name}.

%package demo
Summary:        Examples for %{name}
Requires:       %{name} = %{version}-%{release}

%description demo
Examples for %{name}.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}

%patch0 -p1

# Remove binary information in the source tar
find . -name "*.jar" -delete
find . -name "*.class" -delete

find ./examples -type f -exec sed -i 's/\r//' {} \;

ln -s `build-classpath javacc` bootstrap/javacc.jar

sed -i 's/source="1.4"/source="1.5"/g' src/org/javacc/{parser,jjdoc,jjtree}/build.xml

%build
# Use the bootstrap javacc.jar to generate some required
# source java files. After these source files are generated we
# remove the bootstrap jar and build the binary from source.
ant -f src/org/javacc/parser/build.xml parser-files
ant -f src/org/javacc/jjtree/build.xml tree-files
find . -name "*.jar" -delete
ant jar javadoc

%install
# jar
install -Dpm 644 bin/lib/%{name}.jar %{buildroot}%{_javadir}/%{name}.jar

# bin
install -Dp -T -m 755 %{SOURCE1} %{buildroot}/%{_bindir}/javacc.sh
install -Dp -T -m 755 %{SOURCE2} %{buildroot}/%{_bindir}/jjdoc
install -Dp -T -m 755 %{SOURCE3} %{buildroot}/%{_bindir}/jjtree

# javadoc
install -d -p 755 %{buildroot}/%{_javadocdir}/%{name}
cp -rp api/* %{buildroot}/%{_javadocdir}/%{name}

# pom
install -Dpm 644 pom.xml %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar


%files -f .mfiles
%{_javadir}/*.jar
%doc LICENSE README
%{_bindir}/*

%files manual
%doc LICENSE README
%doc www/*

%files demo
%doc examples

%files javadoc
%doc LICENSE README
%{_javadocdir}/%{name}

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:5.0-11
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:5.0-10
- Use Requires: java-headless rebuild (#1067528)

* Tue Jul 30 2013 Michal Srb <msrb@redhat.com> - 0:5.0-9
- Generate javadoc
- Drop group tag

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Jaromir Capik <jcapik@redhat.com> 0:5.0-6
- Fixing #835786 - javacc: Invalid upstream URL
- Minor spec file changes according to the latest guidelines

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:5.0-3
- Fix examples line endings.

* Fri Jun 4 2010 Alexander Kurtakov <akurtako@redhat.com> 0:5.0-2
- Apply changes requested in review bug (rhbz#225940).

* Thu Feb 11 2010 Alexander Kurtakov <akurtako@redhat.com> 0:5.0-1
- Update to upstream 5.0 release.

* Tue Nov 24 2009 Alexander Kurtakov <akurtako@redhat.com> 0:4.1-0.6
- Use standard permissions and fix unowned directories.

* Tue Nov 24 2009 Alexander Kurtakov <akurtako@redhat.com> 0:4.1-0.5
- Fix rpmlint warnings.
- Drop gcj support.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 03 2008 Matt Wringe <mwringe@redhat.com> - 0:4.1-0.2
- Update to remove packaged jars in source tar
- Build with bootstrap jar so that required java source 
  files get generated

* Wed Oct 22 2008 Jerry James <loganjerry@gmail.com> - 0:4.1-0.1
- Update to 4.1
- Also ship the jjrun script
- Own the appropriate gcj directory
- Minor spec file changes to comply with latest Fedora guidelines
- Include the top-level index.html file in the manual

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:4.0-4.5
- drop repotag

* Fri Feb 22 2008 Matt Wringe <mwringe at redhat.com> - 0:4.0-4jpp.4
- Rename javacc script file to javacc.sh as this confuses the makefile

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:4.0-4jpp.3
- Autorebuild for GCC 4.3

* Thu Aug 10 2006 Matt Wringe <mwringe at redhat.com> - 0:4.0-3jpp.3
- Rebuilt with new naming convention

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:4.0-3jpp_2fc
- Rebuilt

* Tue Jul 18 2006 Matthew Wringe <mwringe at redhat.com> - 0:4.0-3jpp_1fc
- Merged with upstream version
- Changed directory locations to rpm macros
- Added conditional native compiling

* Thu Apr 20 2006 Fernando Nasser <fnasser@redhat.com> - 0:4.0-2jpp
- First JPP 1.7 build

* Fri Mar 31 2006 Sebastiano Vigna <vigna at acm.org> - 0:4.0-1jpp
- Updated to 4.0

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:3.2-2jpp
- Rebuild with ant-1.6.2

* Fri Jan 30 2004 Sebastiano Vigna <vigna at acm.org> 0:3.2-1jpp
- First JPackage version
