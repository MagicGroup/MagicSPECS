Name:    c3p0
Version: 0.9.5
Release: 0.1.pre8%{?dist}
Summary: JDBC DataSources/Resource Pools
License: LGPLv2 or EPL
URL:     https://github.com/swaldman/c3p0
Group:   Development/Libraries

BuildRequires: javapackages-local
BuildRequires: ant
BuildRequires: mchange-commons >= 0.2.7

Requires: mchange-commons >= 0.2.7

Source0: https://github.com/swaldman/c3p0/archive/c3p0-%{version}-pre8.tar.gz

BuildArch: noarch

%description
c3p0 is an easy-to-use library for augmenting traditional JDBC drivers with
JNDI-bindable DataSources, including DataSources that implement Connection
and Statement Pooling, as described by the jdbc3 spec and jdbc2 standard
extension.

%package  javadoc
Summary:  API documentation for %{name}
Group:    Documentation

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{name}-%{version}-pre8

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

# remove manifest classpath
sed -i -e "/Class-Path/d" build.xml

%build
ant \
  -Dbuild.sysclasspath=first \
  -Dmchange-commons-java.jar.file=$(build-classpath mchange-commons-java) \
  jar javadoc

sed -i -e "s|@c3p0.version.maven@|%{version}|g" \
  -e "s|@mchange-commons-java.version.maven@|0.2.7|g" \
  src/maven/pom.xml

%mvn_artifact src/maven/pom.xml build/c3p0-%{version}-pre8.jar
%mvn_alias : c3p0:c3p0

%install
%mvn_install

install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc src/dist-static/LICENSE*
%doc src/dist-static/RELEASE*
%doc src/dist-static/CHANGELOG
%doc src/dist-static/README
%doc src/doc/index.html
%dir %{_javadir}/%{name}

%files javadoc
%doc src/dist-static/LICENSE*
%{_javadocdir}/%{name}

%changelog
* Wed Jun 11 2014 Mat Booth <mat.booth@redhat.com> - 0.9.5-0.1.pre8
- Update to latest upstream release
- Drop upstreamed patches
- Install with maven

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Mat Booth <fedora@matbooth.co.uk> - 0.9.2.1-5
- Require java-headless, rhbz #1067993

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Mat Booth <fedora@matbooth.co.uk> - 0.9.2.1-3
- Add legacy c3p0:c3p0 mapping, fixes rhbz #983533

* Tue Apr 02 2013 Mat Booth <fedora@matbooth.co.uk> - 0.9.2.1-2
- Use included pom file
- Update project URL

* Thu Mar 28 2013 Mat Booth <fedora@matbooth.co.uk> - 0.9.2.1-1
- Update to latest upstream release
- License change to "LGPLv2 or EPL"

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-0.10.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.9.2-0.9.pre1
- Fix file permissions

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-0.8.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Deepak Bhole <dbhole@redhat.com> 0.9.2-0.7.pre1
- Added patch for building with JDBC 4.1/Java 7

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-0.6.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 28 2011 Mat Booth <fedora@matbooth.co.uk> 0.9.2-0.5.pre1
- Update for latest guidelines.

* Sat Jun 11 2011 Mat Booth <fedora@matbooth.co.uk> 0.9.2-0.4.pre1
- Drop redundant clean steps.
- Req(post/postun) jpackage-utils

* Mon Apr 25 2011 Mat Booth <fedora@matbooth.co.uk> 0.9.2-0.3.pre1
- Add a POM and Maven depmap.

* Thu Feb 3 2011 Mat Booth <fedora@matbooth.co.uk> 0.9.2-0.2.pre1
- Patch to build with Java 1.6 (thanks to mcrawford for contributing a chunk
  of this.)
- Other guideline mis-compliances fixed.

* Fri Oct 8 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.2-0.1.pre1
- initial package
