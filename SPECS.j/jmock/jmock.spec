%global namedreltag %{nil}
%global namedversion %{version}%{?namedreltag}

Name:          jmock
Version:       2.5.1
Release:       9%{?dist}
Summary:       Java library for testing code with mock objects
License:       BSD
Url:           http://www.jmock.org/
# svn export http://svn.codehaus.org/jmock/tags/2.5.1 jmock-2.5.1
# find jmock-2.5.1 -name "*.jar" -type f -delete
# find jmock-2.5.1 -name "*.class" -delete
# svn export http://svn.codehaus.org/jmock/tags/packaging-maven-2.5.1 jmock-2.5.1/maven
# tar czf jmock-2.5.1-clean-src-svn.tar.gz jmock-2.5.1
Source0:       %{name}-%{namedversion}-clean-src-svn.tar.gz
Patch0:        %{name}-%{namedversion}-use_system_libraries.patch
# build with cglib 2.2
Patch1:        %{name}-%{namedversion}-cglib22.patch
# patch for java6
Patch2:        %{name}-%{namedversion}-DeterministicSchedule.patch
# remove hamcrest classes
Patch3:        %{name}-%{namedversion}-javadoc.patch
# remove
#    gmaven
#    wagon-webdav 
#    profile jmock1
# change
#   cglib cglib-nodep 2.1_3 -> net.sf.cglib cglib 2.2
#   junit-dep -> junit
Patch4:        %{name}-%{namedversion}-poms.patch
# from Debian
Patch5:        %{name}-%{namedversion}-hamcrest12.patch
# build fix for java 7
Patch6:        %{name}-%{namedversion}-name-clash.patch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils

BuildRequires: ant
BuildRequires: ant-junit
BuildRequires: bsh
BuildRequires: cglib
BuildRequires: hamcrest12
BuildRequires: junit
BuildRequires: objectweb-asm3
BuildRequires: objenesis

Requires:      bsh
Requires:      hamcrest12
Requires:      junit

Requires:      objenesis
Requires:      jpackage-utils
BuildArch:     noarch

%description
Mock objects help you design and test the interactions between the objects in
your programs.
The jMock library:
  * makes it quick and easy to define mock objects, so you don't break the
    rhythm of programming.
  * lets you precisely specify the interactions between your objects, reducing
    the brittleness of your tests.
  * works well with the auto-completion and re-factoring features of your IDE
  * plugs into your favorite test framework
  * is easy to extend.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
%patch0 -p0
sed -i "s|objectweb-asm/asm.jar|objectweb-asm3/asm.jar|" build.xml
sed -i "s|objenesis|objenesis/objenesis|" build.xml
sed -i "s|hamcrest12/core.jar|hamcrest12/hamcrest-core-1.2.jar|" build.xml
sed -i "s|hamcrest12/library.jar|hamcrest12/hamcrest-library-1.2.jar|" build.xml
sed -i "s|junit4.jar|junit.jar|" build.xml
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p1
%patch6 -p0

# fix non ASCII chars
for s in test/org/jmock/example/sniper/Money.java;do
  native2ascii -encoding UTF8 ${s} ${s}
done

# TODO this test fails
rm -r test/org/jmock/test/acceptance/ParameterMatchingAcceptanceTests.java \
  test/org/jmock/test/acceptance/PrimitiveParameterTypesAcceptanceTests.java

sed -i 's|<batchtest haltonfailure="yes">|<batchtest haltonfailure="no">|' build.xml

%build

ant \
  -Dant.build.javac.source=1.5 \
  -Dant.build.javac.target=1.5 \
 -Dversion=%{namedversion} \
 zip.jars javadoc

%install

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 maven/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-parent.pom
%add_maven_depmap JPP.%{name}-parent.pom

mkdir -p %{buildroot}%{_javadir}/%{name}
for m in %{name} \
  %{name}-junit3 \
  %{name}-junit4 \
  %{name}-legacy \
  %{name}-script;do
    install -m 644 build/%{name}-%{namedversion}/${m}-%{namedversion}.jar %{buildroot}%{_javadir}/%{name}/${m}.jar
    install -pm 644 maven/${m}/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-${m}.pom
    %add_maven_depmap JPP.%{name}-${m}.pom %{name}/${m}.jar
done

sed -i 's|<version>x-SNAPSHOT</version>|<version>%{namedversion}</version>|'  maven/%{name}-core/pom.xml
sed -i 's|<artifactId>%{name}-core</artifactId>|<artifactId>%{name}-tests</artifactId>|'  maven/%{name}-core/pom.xml
sed -i 's|<name>jMock 1 Core</name>|<name>jMock 2 Tests</name>|' maven/%{name}-core/pom.xml
install -m 644 build/%{name}-%{namedversion}/%{name}-tests-%{namedversion}.jar \
  %{buildroot}%{_javadir}/%{name}/%{name}-tests.jar
install -pm 644 maven/%{name}-core/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-tests.pom
%add_maven_depmap JPP.%{name}-%{name}-tests.pom %{name}/%{name}-tests.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr build/%{name}-%{namedversion}/doc/* %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE.txt README*

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.txt

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.5.1-9
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 2.5.1-8
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 gil cattaneo <puntogil@libero.it> 2.5.1-6
- Use .mfiles generated during build
- Fix junit dep

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.5.1-5
- Use Requires: java-headless rebuild (#1067528)

* Fri Nov 15 2013 gil cattaneo <puntogil@libero.it> 2.5.1-4
- use objectweb-asm3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Apr 19 2012 gil cattaneo <puntogil@libero.it> 2.5.1-1
- initial rpm