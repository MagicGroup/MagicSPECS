Name:    mchange-commons
Version: 0.2.7
Release: 1%{?dist}
Summary: A collection of general purpose utilities for c3p0
License: LGPLv2 or EPL
URL:     https://github.com/swaldman/mchange-commons-java
Group:   Development/Libraries

BuildRequires: sbt
BuildRequires: ivy-local
BuildRequires: maven-local
BuildRequires: log4j12
BuildRequires: slf4j
BuildRequires: typesafe-config

Source0: https://github.com/swaldman/mchange-commons-java/archive/mchange-commons-java-%{version}-final.tar.gz
Source1: https://raw.github.com/willb/climbing-nemesis/master/climbing-nemesis.py

# There is a missing dep in Fedora so cannot build tests
Patch0:  mchange-no-tests.patch

BuildArch: noarch

%description
Originally part of c3p0, mchange-commons is a set of general purpose
utilities.

%package javadoc
Summary:       API documentation for %{name}
Group:         Documentation

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-java-%{name}-java-%{version}-final

%patch0

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

cp %{SOURCE1} .

cp -pr /usr/share/sbt/ivy-local .

%build
# XXX: This jar has changed location, which breaks sbt -- this is a temp workaround
rm ivy-local/org.fusesource.hawtjni/hawtjni-runtime/1.8/hawtjni-runtime-1.8.jar
ln -s /usr/lib/java/hawtjni/hawtjni-runtime.jar ivy-local/org.fusesource.hawtjni/hawtjni-runtime/1.8/hawtjni-runtime-1.8.jar

# XXX: Link deps, I understand this is a temp measure until sbt gains real xmvn integration
python climbing-nemesis.py com.typesafe config ivy-local --version 1.0.0
# XXX: Have to specify exact pom here in case log4j2's compat api gets resolved instead
python climbing-nemesis.py log4j log4j ivy-local --version 1.2.14 --pom /usr/share/maven-poms/log4j12-*.pom --ignore ant --ignore junit --ignore sun.jdk
python climbing-nemesis.py org.slf4j slf4j-api ivy-local --version 1.7.5

export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local
sbt package make-pom doc

%mvn_artifact target/mchange-commons-java-%{version}.pom target/mchange-commons-java-%{version}.jar

%install
%mvn_install

install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/api/* %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc LICENSE*
%dir %{_javadir}/%{name}

%files javadoc
%doc LICENSE*
%{_javadocdir}/%{name}

%changelog
* Sun Jun 08 2014 Mat Booth <mat.booth@redhat.com> - 0.2.7-1
- Update to latest upstream version
- Drop patches
- Build with sbt and install with maven

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Mat Booth <fedora@matbooth.co.uk> - 0.2.3.4-4
- Require java-headless, rhbz #1068404

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 02 2013 Mat Booth <fedora@matbooth.co.uk> - 0.2.3.4-2
- Include pom file
- Update project URL

* Thu Mar 28 2013 Mat Booth <fedora@matbooth.co.uk> - 0.2.3.4-1
- Update to latest upstream release
- License change to "LGPLv2 or EPL"

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.8.20110130hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.2-0.7.20110130hg
- Fix file permissions
- Update to current packaging guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.6.20110130hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 25 2012 Deepak Bhole <dbhole@redhat.com> - 0.2-0.5.20110130hg
- Added patch to build with JDBC 4.1/Java 7
- Added patch to disable one of the tests that is not always guaranteed to pass

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.4.20110130hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 31 2011 Mat Booth <fedora@matbooth.co.uk> 0.2-0.3.20110130hg
- Add build dep on ant-junit.
- Build and install javadoc.

* Sun Jan 30 2011 Mat Booth <fedora@matbooth.co.uk> 0.2-0.2.20110130hg
- Update for guideline compliance.

* Fri Oct 8 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.2-0.1.20101008hg
- initial package
