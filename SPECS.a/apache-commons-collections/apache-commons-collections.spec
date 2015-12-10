%global base_name       collections
%global short_name      commons-%{base_name}

Name:           apache-%{short_name}
Version:        3.2.1
Release:        21%{?dist}
Summary:        Provides new interfaces, implementations and utilities for Java Collections
License:        ASL 2.0
Group:          Development/Libraries
URL:            http://commons.apache.org/%{base_name}/
Source0:        http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source1:        commons-collections-testframework.pom

Patch0:         jakarta-%{short_name}-javadoc-nonet.patch
Patch4:         commons-collections-3.2-build_xml.patch

BuildArch:      noarch

BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: maven-local
BuildRequires: ant
BuildRequires: apache-commons-parent
Requires:      java-headless
Requires:      jpackage-utils

Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}-%{release}
Obsoletes:      %{name}-tomcat5 < %{version}-%{release}

%description
The introduction of the Collections API by Sun in JDK 1.2 has been a
boon to quick and effective Java programming. Ready access to powerful
data structures has accelerated development by reducing the need for
custom container classes around each core object. Most Java2 APIs are
significantly easier to use because of the Collections API.
However, there are certain holes left unfilled by Sun's
implementations, and the Jakarta-Commons Collections Component strives
to fulfill them. Among the features of this package are:
- special-purpose implementations of Lists and Maps for fast access
- adapter classes from Java1-style containers (arrays, enumerations) to
Java2-style collections.
- methods to test or create typical set-theory properties of collections
such as union, intersection, and closure.

%package testframework
Summary:        Testframework for %{name}
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Provides:       jakarta-%{short_name}-testframework = %{version}-%{release}
Obsoletes:      jakarta-%{short_name}-testframework < %{version}-%{release}

%description testframework
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
Provides:       jakarta-%{short_name}-javadoc = %{version}-%{release}
Obsoletes:      jakarta-%{short_name}-javadoc < %{version}-%{release}

%description javadoc
%{summary}.

%package testframework-javadoc
Summary:        Javadoc for %{name}-testframework
Group:          Documentation
Provides:       jakarta-%{short_name}-testframework-javadoc = %{version}-%{release}
Obsoletes:      jakarta-%{short_name}-testframework-javadoc < %{version}-%{release}

%description testframework-javadoc
%{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src

# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

%patch0 -p1
%patch4 -b .sav

# Fix file eof
%{__sed} -i 's/\r//' LICENSE.txt
%{__sed} -i 's/\r//' PROPOSAL.html
%{__sed} -i 's/\r//' RELEASE-NOTES.html
%{__sed} -i 's/\r//' README.txt
%{__sed} -i 's/\r//' NOTICE.txt

# Substitute version into testframework pom
cp -p %{SOURCE1} pom-testframework.xml
sed -i 's/@VERSION@/%{version}/' pom-testframework.xml

%build
%mvn_build

ant tf.javadoc

%install

# jars
install -Dm 644 target/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -Dm 644 target/%{short_name}-testframework-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-testframework.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *; do ln -sf ${jar} `echo $jar| sed  "s|apache-||g"`; done)


# poms
install -Dpm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{short_name}.pom
install -Dpm 644 pom-testframework.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{short_name}-testframework.pom


# fragments
%add_maven_depmap JPP-%{short_name}.pom %{short_name}.jar -a "org.apache.commons:%{short_name}"
%add_maven_depmap JPP-%{short_name}-testframework.pom %{short_name}-testframework.jar -f "testframework" -a "org.apache.commons:%{short_name}-testframework"


# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf target/site/apidocs


# testframework-javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testframework-%{version}
cp -pr build/docs/testframework/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testframework-%{version}
ln -s %{name}-testframework-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testframework 


%files
%doc PROPOSAL.html README.txt LICENSE.txt RELEASE-NOTES.html NOTICE.txt
%{_mavenpomdir}/JPP-%{short_name}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}.jar
%{_javadir}/%{short_name}.jar

%files testframework
%{_mavenpomdir}/JPP-%{short_name}-testframework.pom
%{_mavendepmapfragdir}/%{name}-testframework
%{_javadir}/%{name}-testframework.jar
%{_javadir}/%{short_name}-testframework.jar

%files javadoc
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files testframework-javadoc
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}-testframework-%{version}
%{_javadocdir}/%{name}-testframework


%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 3.2.1-21
- 为 Magic 3.0 重建

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.1-20
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 12 2013 Mat Booth <fedora@matbooth.co.uk> - 3.2.1-19
- Fix FTBFS rhbz #991965

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-17
- Remove unneeded BR: maven-idea-plugin

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.2.1-15
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 08 2012 Jaromir Capik <jcapik@redhat.com> 3.2.1-13
- saxon dependency removed - not needed
- minor spec file changes according to the latest guidelines

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 6 2011 Chris Spike <spike@fedoraproject.org> 3.2.1-11
- Added *-testframework depmap entries.

* Wed Mar 16 2011 Alexander Kurtakov <akurtako@redhat.com> 3.2.1-10
- Drop tomcat5 subpackage.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 8 2010 Alexander Kurtakov <akurtako@redhat.com> 3.2.1-8
- Add commons-collections:commons-collections depmap.

* Mon Oct 4 2010 Alexander Kurtakov <akurtako@redhat.com> 3.2.1-7
- Fix pom name.
- Use newer maven plugins names.

* Tue Aug 31 2010 Carl Green <carlgreen at gmail.com> - 3.2.1-6
- Change package to own files in directories, not the directories

* Mon Aug 30 2010 Carl Green <carlgreen at gmail.com> - 3.2.1-5
- Remove source and patches no longer needed for Maven
- Fix non-standard groups and remove empty sections
- Fix file permissions

* Sat Aug 28 2010 Carl Green <carlgreen at gmail.com> - 3.2.1-4
- Renamed from jakarta-commons-collections
- Updated to use maven2
- Replaced saxon:group instruction with xsl:for-each-group in pom-maven2jpp-newdepmap.xsl
