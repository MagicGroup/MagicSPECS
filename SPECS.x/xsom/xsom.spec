%global checkout 20110809

Name: xsom
Version: 0
Release: 14.%{checkout}svn%{?dist}
Summary: XML Schema Object Model (XSOM)
Group: Development/Libraries
License: CDDL or GPLv2 with exceptions
URL: http://xsom.java.net

# svn export https://svn.java.net/svn/xsom~sources/tags/xsom-20110809 xsom-20110809svn
# find xsom-20110809svn/ -name '*.class' -delete
# find xsom-20110809svn/ -name '*.class' -delete
# tar czf xsom-20110809svn.tar.gz xsom-20110809svn
Source0: %{name}-%{checkout}svn.tar.gz

# We need this because one of the original tests tries to download
# it from the website, but that doesn't work in Koji:
Source1: http://docs.oasis-open.org/regrep/v3.0/schema/lcm.xsd

Patch0: %{name}-%{checkout}svn-pom.patch

BuildRequires: jpackage-utils
BuildRequires: junit
BuildRequires: maven-local
BuildRequires: maven-antrun-plugin
BuildRequires: maven-plugin-build-helper
BuildRequires: maven-compiler-plugin
BuildRequires: maven-enforcer
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-shared
BuildRequires: relaxngDatatype
BuildRequires: relaxngcc
BuildRequires: sonatype-oss-parent
BuildRequires: forge-parent

Requires: jpackage-utils
Requires: relaxngDatatype
BuildArch: noarch


%description
XML Schema Object Model (XSOM) is a Java library that allows applications to
easily parse XML Schema documents and inspect information in them. It is
expected to be useful for applications that need to take XML Schema as an
input.  The library is a straight-forward implement of "schema components" as
defined in the XML Schema spec part 1.  Refer to this specification of how this
object model works. 


%package javadoc
Group: Development/Libraries
Summary: Javadoc for %{name}
Requires: jpackage-utils


%description javadoc
This package contains javadoc for %{name}.


%prep
%setup -q -n %{name}-%{checkout}svn
%patch0 -p1

# Replace the URL of the XSD file used by the tests with its
# absolute filesystem location:
sed -i \
  's|http://docs.oasis-open.org/regrep/v3.0/schema/lcm.xsd|file://%{SOURCE1}|' \
  test/XSOMParserTest.java

pushd lib
  ln -sf $(build-classpath relaxngcc) relaxngcc.jar
popd


%build

mvn-rpmbuild \
  -Dproject.build.sourceEncoding=UTF-8 \
  install \
  javadoc:aggregate


%install

# Jar files:
install -d -m 755 %{buildroot}%{_javadir}
cp -p target/xsom-%{checkout}.jar %{buildroot}%{_javadir}/%{name}.jar

# POM files:
install -d -m 755 %{buildroot}%{_mavenpomdir}
cp -p pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# Javadoc files:
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

# Dependencies map:
%add_maven_depmap JPP-%{name}.pom %{name}.jar


%files -f .mfiles
%doc license.txt


%files javadoc
%{_javadocdir}/*
%doc license.txt


%changelog
* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 0-14.20110809svn
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 0-13.20110809svn
- 为 Magic 3.0 重建

* Mon Aug 04 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 0-12.20110809svn
- Fix junit BRs (#1107359)
- Fix FTBFS due to F21 XMvn changes

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-11.20110809svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-10.20110809svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 22 2013 Juan Hernandez <juan.hernandez@redhat.com> - 0-9.20110809svn
- Add build dependency on maven-shared (rhbz 914590)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-8.20110809svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0-7.20110809svn
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-6.20110809svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 23 2012 Juan Hernandez <juan.hernandez@redhat.com> 0-5.20110809svn
- Update the release tag

* Thu Feb 23 2012 Juan Hernandez <juan.hernandez@redhat.com> 0-4.20110809svn
- Avoid downloading XSD files during the build process

* Wed Feb 22 2012 Juan Hernandez <juan.hernandez@redhat.com> 0-3.20110809svn
- Put the date tag in the release instead of in the version

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 0-2.20110809svn
- Cleanup of the spec file

* Sat Jan 21 2012 Marek Goldmann <mgoldman@redhat.com> 0-1.20110809svn
- Initial packaging
