Name: rngom
Version: 201103
Release: 0.13.20120119svn%{?dist}
Summary: Java library for parsing RELAX NG grammars
Group: Development/Libraries
License: MIT
URL: https://rngom.dev.java.net

# svn export -r 70 https://svn.java.net/svn/rngom~svn/trunk/rngom rngom-201103
# find rngom-201103/ -name '*.class' -delete
# find rngom-201103/ -name '*.jar' -delete
# tar czf rngom-201103.tar.gz rngom-201103
Source0: %{name}-%{version}.tar.gz
Patch0: %{name}-%{version}-pom.patch

BuildRequires: bsf
BuildRequires: bsh
BuildRequires: stax2-api
BuildRequires: javacc
BuildRequires: javacc-maven-plugin
BuildRequires: jpackage-utils
BuildRequires: junit
BuildRequires: maven-local
BuildRequires: maven-clean-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-enforcer
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: msv-xsdlib
BuildRequires: relaxngDatatype
BuildRequires: sonatype-oss-parent
BuildRequires: xmlunit

Requires: stax2-api
Requires: jpackage-utils
Requires: msv-xsdlib
Requires: relaxngDatatype

BuildArch: noarch


%description
RNGOM is an open-source Java library for parsing RELAX NG grammars.

In particular, RNGOM can:
* parse the XML syntax
* parse the compact syntax
* check all the semantic restrictions as specified in the specification
* parse RELAX NG into application-defined data structures
* build a default data structure based around the binarized simple syntax or
  another data structure that preserves more of the parsed information
* parse foreign elements/attributes in a schema
* parse comments in a schema


%package javadoc
Group: Documentation
Summary: Javadoc for %{name}
Requires: jpackage-utils


%description javadoc
This package contains javadoc for %{name}.


%prep
%setup -q
%patch0 -p1


%build
mvn-rpmbuild install javadoc:aggregate


%install

# Jar files:
install -d -m 755 %{buildroot}%{_javadir}
cp -p target/rngom-%{version}-SNAPSHOT.jar %{buildroot}%{_javadir}/%{name}.jar

# POM files:
install -d -m 755 %{buildroot}%{_mavenpomdir}
cp -p pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# Javadoc files:
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/.

# Dependencies map:
%add_maven_depmap JPP-%{name}.pom %{name}.jar


%files -f .mfiles


%files javadoc
%{_javadocdir}/*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 201103-0.13.20120119svn
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 201103-0.12.20120119svn
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 201103-0.11.20120119svn
- 为 Magic 3.0 重建

* Mon Aug 04 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 201103-0.10.20120119svn
- Fix FTBFS due to F21 XMvn changes (#1107027)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 201103-0.9.20120119svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 201103-0.8.20120119svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 201103-0.7.20120119svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 201103-0.6.20120119svn
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 201103-0.5.20120119svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 23 2012 Juan Hernandez <juan.hernandez@redhat.com> 201103-0.4.20120119svn
- Make explicit the checked out revision number in the comments

* Sat Feb 18 2012 Juan Hernandez <juan.hernandez@redhat.com> 201103-0.3.20120119svn
- Remove the binary file lic.jar from the source tarball

* Fri Feb 17 2012 Juan Hernandez <juan.hernandez@redhat.com> 201103-0.2.20120119svn
- Cleanup of the spec file

* Sat Jan 21 2012 Marek Goldmann <mgoldman@redhat.com> 201103-0.1.20120119svn
- Initial packaging

