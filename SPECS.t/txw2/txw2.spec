Name: txw2
Version: 20110809
Release: 11%{?dist}
Summary: Typed XML writer for Java
Group: Development/Libraries
License: CDDL and GPLv2 with exceptions
URL: https://txw.dev.java.net

# svn export https://svn.java.net/svn/jaxb~version2/tags/txw2-project-20110809/ txw2-20110809
# tar -zcvf txw2-20110809.tar.gz txw2-20110809
Source0: %{name}-%{version}.tar.gz

# Remove the reference to the parent net.java:jvnet-parent, as no package
# contains that artifact:
Patch0: %{name}-%{version}-pom.patch

# Update to use the version of args4j available in the distribution:
Patch1: %{name}-%{version}-args4j.patch

BuildArch: noarch

BuildRequires: jpackage-utils
BuildRequires: java-devel
BuildRequires: maven-local

BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-release-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-shared
BuildRequires: args4j
BuildRequires: xsom
BuildRequires: rngom
BuildRequires: codemodel

Requires: jpackage-utils
Requires: args4j
Requires: xsom
Requires: rngom
Requires: codemodel


%description
Typed XML writer for Java.


%package javadoc
Summary: Javadocs for %{name}
Group: Documentation
Requires: jpackage-utils


%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build
mvn-rpmbuild \
  -Dproject.build.sourceEncoding=UTF-8 \
  install \
  javadoc:aggregate


%install

# Jar files:
install -d -m 755 %{buildroot}%{_javadir}
cp -p runtime/target/txw2-%{version}.jar %{buildroot}%{_javadir}/txw2.jar
cp -p compiler/target/txwc2-%{version}.jar %{buildroot}%{_javadir}/txwc2.jar

# POM files:
install -d -m 755 %{buildroot}%{_mavenpomdir}
cp -p pom.xml %{buildroot}%{_mavenpomdir}/JPP-txw2-project.pom
cp -p runtime/pom.xml %{buildroot}%{_mavenpomdir}/JPP-txw2.pom
cp -p compiler/pom.xml %{buildroot}%{_mavenpomdir}/JPP-txwc2.pom

# Dependencies map:
%add_maven_depmap JPP-txw2-project.pom
%add_maven_depmap JPP-txw2.pom txw2.jar
%add_maven_depmap JPP-txwc2.pom txwc2.jar

# Javadoc files:
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}


%files -f .mfiles
%doc license.txt


%files javadoc
%{_javadocdir}/%{name}
%doc license.txt


%changelog
* Mon Aug 04 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 20110809-11
- Fix FTBFS due to F21 XMvn changes (#1107468)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110809-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 20110809-9
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110809-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 22 2013 Juan Hernandez <juan.hernandez@redhat.com> - 20110809-7
- Add build dependency on maven-shared (rhbz 914555)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110809-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 20110809-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110809-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 2 2012 Juan Hernandez <juan.hernandez@redhat.com> 20110809-3
- Use the jar names from upstream
- Add comments describing the patches

* Fri Feb 17 2012 Juan Hernandez <juan.hernandez@redhat.com> 20110809-2
- Cleanup of the spec file

* Mon Jan 16 2012 Marek Goldmann <mgoldman@redhat.com> 20110809-1
- Initial packaging
