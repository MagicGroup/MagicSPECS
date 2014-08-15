Name:		mongo-java-driver
Version:	2.11.3
Release:	4%{?dist}
Summary:	A Java driver for MongoDB

Group:		Development/Libraries
BuildArch:	noarch
License:	ASL 2.0
URL:		http://www.mongodb.org/display/DOCS/Java+Language+Center
Source0:	https://github.com/mongodb/%{name}/archive/r%{version}.tar.gz

BuildRequires:	jpackage-utils
BuildRequires:	java-devel

BuildRequires:	ant
BuildRequires:	ant-contrib
BuildRequires:	testng
BuildRequires:	git

Requires:	jpackage-utils

%description
This is the Java driver for MongoDB.

%package bson
Summary:	A Java-based BSON implementation
Group:		Development/Libraries
Requires:	jpackage-utils

%description bson
This is the Java implementation of BSON that the Java driver for
MongoDB ships with.  It can be used separately by Java applications
that require BSON.
# Upstream has hinted that eventually, their bson implementation will
# be better separated out: http://bsonspec.org/#/implementation
# To make things easier for when that does happen, for now the jar
# and javadocs for this are in separate subpackages.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%package bson-javadoc
Summary:	Javadoc for %{name}-bson
Group:		Documentation
Requires:	jpackage-utils

%description bson-javadoc
This package contains the API documentation for %{name}-bson.

%prep
%setup -qn %{name}-r%{version}

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build
(
  ln -s $(build-classpath testng) lib/testng-6.3.1.jar
  ant -Dfile.encoding=UTF-8 -Denv.JAVA_HOME=/usr/lib/jvm/java -Dplatforms.JDK_1.5.home=/usr/lib/jvm/java jar javadocs
)
sed -i -e "s|@VERSION@|%{version}|g" maven/maven-bson.xml maven/maven-%{name}.xml

%install
# Jars
mkdir -p %{buildroot}%{_javadir}
cp -p mongo.jar %{buildroot}%{_javadir}/%{name}.jar
cp -p bson.jar %{buildroot}%{_javadir}/%{name}-bson.jar

# poms
install -Dpm 644 maven/maven-%{name}.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
install -Dpm 644 maven/maven-bson.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}-bson.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar
%add_maven_depmap -f bson JPP-%{name}-bson.pom %{name}-bson.jar

# Java-docs
mkdir -p %{buildroot}%{_javadocdir}
cp -rp docs/mongo-java-driver %{buildroot}%{_javadocdir}/%{name}
cp -rp docs/bson %{buildroot}%{_javadocdir}/%{name}-bson

%files -f .mfiles
%doc README.md LICENSE.txt

%files bson -f .mfiles-bson
%doc README.md LICENSE.txt

%files javadoc
%{_javadocdir}/%{name}
%doc README.md LICENSE.txt

%files bson-javadoc
%{_javadocdir}/%{name}-bson
%doc README.md LICENSE.txt

%changelog
* Tue Jun 10 2014 Severin Gehwolf <sgehwolf@redhat.com> - 2.11.3-4
- Fix FTBFS. Resolves RHBZ#1106228.
- Fix @VERSION@ substitution. Resolves RHBZ#1048200.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.11.3-2
- Use Requires: java-headless rebuild (#1067528)

* Tue Sep 24 2013 Severin Gehwolf <sgehwolf@redhat.com> - 2.11.3-1
- Update to latest upstream release.

* Thu Sep 05 2013 Omair Majid <omajid@redhat.com> - 2.11.2-2
- Do not require -bson subpackage. The classes are present in both jars.

* Fri Aug 30 2013 Omair Majid <omajid@redhat.com> - 2.11.2-1
- Update to 2.11.2
- Generate tarball from commit tag, according to packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Jon VanAlten <jon.vanalten@redhat.com> 2.7.3-1
- Bump to 2.7.3.

* Mon Jan 16 2012 Alexander Kurtakov <akurtako@redhat.com> 2.6.5-4
- Add depmap/pom.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Jon VanAlten <jon.vanalten@redhat.com> - 2.6.5-2
- Sources moved to lookaside cache where they belong

* Tue Nov 29 2011 Jon VanAlten <jon.vanalten@redhat.com> - 2.6.5-1
- Add missing BuildDep: git (git-hash is used during build)

* Tue Oct 11 2011 Jon VanAlten <jon.vanalten@redhat.com> - 2.6.5-1
- Initial packaging of mongo-java-driver for Fedora.
