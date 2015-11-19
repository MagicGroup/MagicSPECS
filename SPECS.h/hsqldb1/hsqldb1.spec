
%global cvs_version 1_8_1_3
%global majorversion 1
Name:          hsqldb1
Version:       1.8.1.3
Release:       8%{?dist}
Summary:       HyperSQL Database Engine
License:       BSD
URL:           http://hsqldb.sourceforge.net/
Source0:       http://downloads.sourceforge.net/hsqldb/hsqldb_%{cvs_version}.zip
Source1:       http://mirrors.ibiblio.org/pub/mirrors/maven2/hsqldb/hsqldb/1.8.0.10/hsqldb-1.8.0.10.pom
Patch0:        hsqldb-jdbc-4.1.patch
BuildRequires: ant
BuildRequires: jpackage-utils >= 0:1.5
BuildRequires: junit
BuildRequires: glassfish-servlet-api

Requires:      glassfish-servlet-api
Requires:      jpackage-utils
BuildArch:     noarch

%description
HSQLdb is a relational database engine written in JavaTM , with a JDBC
driver, supporting a subset of ANSI-92 SQL. It offers a small (about
100k), fast database engine which offers both in memory and disk based
tables. Embedded and server modes are available. Additionally, it
includes tools such as a minimal web server, in-memory query and
management tools (can be run as applets or servlets, too) and a number
of demonstration examples.
Downloaded code should be regarded as being of production quality. The
product is currently being used as a database and persistence engine in
many Open Source Software projects and even in commercial projects and
products! In it's current version it is extremely stable and reliable.
It is best known for its small size, ability to execute completely in
memory and its speed. Yet it is a completely functional relational
database management system that is completely free under the Modified
BSD License. Yes, that's right, completely free of cost or restrictions!

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n hsqldb

# set right permissions
find . -name "*.sh" -exec chmod 755 \{\} \;
# remove all _notes directories
for dir in `find . -name _notes`; do rm -rf $dir; done
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;
find . -name "*.war" -exec rm -f {} \;
# correct silly permissions
chmod -R go=u-w *

%patch0 -p1

cp %{SOURCE1} ./pom.xml

%build
export CLASSPATH=$(build-classpath glassfish-servlet-api junit)
pushd build
ant jar javadoc
popd

%install

# jar
mkdir -p %{buildroot}%{_javadir}
install -m 644 lib/hsqldb.jar %{buildroot}%{_javadir}/%{name}.jar

# Maven metadata
mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar -v "%{majorversion}"

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -r doc/src/* %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%license doc/hsqldb_lic.txt

%files javadoc
%{_javadocdir}/%{name}
%license doc/hsqldb_lic.txt

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Alexander Kurtakov <akurtako@redhat.com> 1.8.1.3-7
- Switch to glassfish servlet api from tomcat.

* Wed Mar 4 2015 Alexander Kurtakov <akurtako@redhat.com> 1.8.1.3-6
- Bump to tomcat servlet api 3.1.

* Thu Feb 05 2015 gil cattaneo <puntogil@libero.it> 1.8.1.3-5
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.8.1.3-3
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 gil cattaneo <puntogil@libero.it> 1.8.1.3-1
- initial rpm
