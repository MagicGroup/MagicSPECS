%global oname hamcrest

Name:           hamcrest12
Version:        1.2
Release:        9%{?dist}
Epoch:          0
Summary:        Library of matchers for building test expressions
License:        BSD
URL:            http://code.google.com/p/hamcrest/
Source0:        http://hamcrest.googlecode.com/files/hamcrest-1.2.tgz
Source1:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-library/1.2/hamcrest-library-1.2.pom
Source2:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-generator/1.2/hamcrest-generator-1.2.pom
Source3:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-core/1.2/hamcrest-core-1.2.pom
Source4:        hamcrest-all-1.2.pom
Patch0:         hamcrest-1.1-build.patch
Patch1:         hamcrest-1.1-no-jarjar.patch
Patch2:         hamcrest-1.1-no-integration.patch
Patch3:         hamcrest1.2-build.patch
Requires:       easymock3
Requires:       qdox
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  zip
BuildRequires:  easymock3
BuildRequires:  junit
BuildRequires:  qdox
BuildRequires:  maven-local

Requires:       java-headless

BuildArch:      noarch

%description
Provides a library of matcher objects (also known as constraints or predicates)
allowing 'match' rules to be defined declaratively, to be used in other
frameworks. Typical scenarios include testing frameworks, mocking libraries and
UI validation rules.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{oname}-%{version}
find . -type f -name "*.jar" | xargs -t rm
ln -sf $(build-classpath qdox) lib/generator/
%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch3 -p1

%mvn_compat_version : 1.2

perl -pi -e 's/\r$//g' LICENSE.txt

%build
export CLASSPATH=$(build-classpath qdox):build/hamcrest-core-%{version}.jar
export OPT_JAR_LIST="junit ant/ant-junit"
ant -Dversion=%{version} clean core
ant -Dversion=%{version} generator
ant -Dversion=%{version} library bigjar javadoc

%mvn_artifact %{SOURCE1} build/%{oname}-library-%{version}.jar
%mvn_artifact %{SOURCE2} build/%{oname}-generator-%{version}.jar
%mvn_artifact %{SOURCE3} build/%{oname}-core-%{version}.jar
%mvn_artifact %{SOURCE4} build/%{oname}-all-%{version}.jar

%install
%mvn_install -J build/javadoc

%files -f .mfiles
%doc LICENSE.txt
%dir %{_javadir}/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Michael Simacek <msimacek@redhat.com> - 0:1.2-8
- Use mvn_install for installation
- Generate compat provides (resolves rhbz#1059216)
- Drop manifest (duplicate OSGi provides)
- Change R java to java-headless

* Thu Jul 25 2013 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-7
- Build against easymock3.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Andy Grimm <agrimm@gmail.com> 0:1.2-4
- Remove erroneous line breaks in manifest

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 16 2012 Andy Grimm <agrimm@gmail.com> 0:1.2-3
- package review fixes

* Mon Feb 13 2012 Andy Grimm <agrimm@gmail.com> 0:1.2-2
- disable integration, update POM files to 1.2

* Mon Feb 13 2012 Andy Grimm <agrimm@gmail.com> 0:1.2-1
- Initial 1.2 package, loosely based on Fedora hamcrest 1.1 package
