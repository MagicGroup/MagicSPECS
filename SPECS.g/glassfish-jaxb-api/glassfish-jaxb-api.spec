%global oname jaxb-api
Name:          glassfish-jaxb-api
Version:       2.2.9
Release:       6%{?dist}
Summary:       Java Architecture for XML Binding
License:       CDDL or GPLv2 with exception
URL:           http://jaxb.java.net/
# jaxb api and impl have different version
# svn export https://svn.java.net/svn/jaxb~version2/tags/jaxb-2_2_6/tools/lib/redist/jaxb-api-src.zip

Source0:       http://repo1.maven.org/maven2/javax/xml/bind/%{oname}/%{version}/%{oname}-%{version}-sources.jar
Source1:       http://repo1.maven.org/maven2/javax/xml/bind/%{oname}/%{version}/%{oname}-%{version}.pom

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: java-javadoc
BuildRequires: jvnet-parent

BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-resources-plugin
BuildRequires: maven-shared-osgi
Requires:      jvnet-parent
BuildArch:     noarch

# The Fedora Packaging Committee granted openjdk a bundling exception to carry JAXP and
# JAX-WS (glassfish doesn't need one, since it is the upstream for these files).
# Reference: https://fedorahosted.org/fpc/ticket/292

%description
Glassfish - JAXB (JSR 222) API.

%package javadoc
Summary:       Javadoc for %{oname}
Requires:      %{name} = %{version}-%{release} 

%description javadoc
Glassfish - JAXB (JSR 222) API.

This package contains javadoc for %{name}.

%prep
%setup -T -q -c

# fixing incomplete source directory structure
mkdir -p src/main/java

(
  cd src/main/java
  unzip -qq %{SOURCE0}
  rm -rf META-INF
)

cp -p %{SOURCE1} pom.xml

sed -i 's|<location>${basedir}/offline-javadoc</location>|<location>%{_javadocdir}/java</location>|' pom.xml

%build

%mvn_file :%{oname} %{oname}
%mvn_build

%install
%mvn_install

mv %{buildroot}%{_javadocdir}/%{name} \
 %{buildroot}%{_javadocdir}/%{oname}

%files -f .mfiles

%files javadoc
%{_javadocdir}/%{oname}

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.9-5
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 gil cattaneo <puntogil@libero.it> 2.2.9-3
- switch to XMvn
- minor changes to adapt to current guideline

* Mon Jun 10 2013 Orion Poplawski <orion@cora.nwra.com> 2.2.9-2
- Add requires jvnet-parent

* Thu May 02 2013 gil cattaneo <puntogil@libero.it> 2.2.9-1
- update to 2.2.9

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.7-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Aug 04 2012 gil cattaneo <puntogil@libero.it> 2.2.7-1
- update to 2.2.7

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 gil cattaneo <puntogil@libero.it> 2.2.6-1
- update to 2.2.6
- remove Build/Requires: bea-stax-api

* Tue Jan 24 2012 gil cattaneo <puntogil@libero.it> 2.2.3-2
- revert to 2.2.3 (stable release)
- fix License field

* Fri Jul 22 2011 gil cattaneo <puntogil@libero.it> 2.2.3-1
- initial rpm
