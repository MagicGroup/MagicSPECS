Name:           cobertura
Version:        1.9.4.1
Release:        14%{?dist}
Summary:        Java tool that calculates the percentage of code accessed by tests

# ASL 2.0: src/net/sourceforge/cobertura/webapp/web.xml
# GPL+: src/net/sourceforge/cobertura/reporting/html/files/sortabletable.js
#       src/net/sourceforge/cobertura/reporting/html/files/stringbuilder.js
# MPL 1.1, GPLv2+, LGPLv2+: some files in src/net/sourceforge/cobertura/javancss/ccl/
# rest is mix of GPLv2+ and ASL 1.1
License:        ASL 1.1 and GPLv2+ and MPL and ASL 2.0 and GPL+
URL:            http://cobertura.sourceforge.net/

# ./create-tarball.sh %%{version}
Source0:        %{name}-%{version}-clean.tar.gz
# POMs based from those available from the Maven repository
Source1:        http://repo1.maven.org/maven2/net/sourceforge/%{name}/%{name}/%{version}/%{name}-%{version}.pom
Source2:        http://repo1.maven.org/maven2/net/sourceforge/%{name}/%{name}-runtime/%{version}/%{name}-runtime-%{version}.pom
Source3:        http://www.apache.org/licenses/LICENSE-1.1.txt
Source4:        http://www.apache.org/licenses/LICENSE-2.0.txt
Source5:        create-tarball.sh

Patch0:         %{name}-unmappable-characters.patch

BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  antlr
BuildRequires:  apache-commons-cli
BuildRequires:  groovy
BuildRequires:  java-devel
BuildRequires:  jakarta-oro
BuildRequires:  jaxen
BuildRequires:  jdom
BuildRequires:  junit
BuildRequires:  log4j
BuildRequires:  objectweb-asm3
BuildRequires:  tomcat-servlet-3.0-api
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-jaxp-1.3-apis

Requires:       ant
Requires:       java-headless
Requires:       jakarta-oro
Requires:       junit
Requires:       log4j
Requires:       objectweb-asm3

BuildArch:      noarch

%description
Cobertura is a free Java tool that calculates the percentage of code
accessed by tests. It can be used to identify which parts of your
Java program are lacking test coverage.

%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
%patch0 -p1

cp %{SOURCE3} LICENSE-ASL-1.1
cp %{SOURCE4} LICENSE-ASL-2.0

sed -i 's/\r//' ChangeLog COPYING COPYRIGHT README

%build
pushd lib
  ln -s $(build-classpath jaxen) .
  ln -s $(build-classpath jdom) .
  ln -s $(build-classpath junit) .
  ln -s $(build-classpath log4j) .
  ln -s $(build-classpath objectweb-asm3/asm-all) .
  ln -s $(build-classpath oro) .
  ln -s $(build-classpath xalan-j2) .
  ln -s $(build-classpath tomcat-servlet-3.0-api) servlet-api.jar
  ln -s $(build-classpath apache-commons-cli) commons-cli.jar
  pushd xerces
    ln -s $(build-classpath xalan-j2) .
    ln -s $(build-classpath xml-commons-jaxp-1.3-apis) .
  popd
popd

pushd antLibrary/common
  ln -s $(build-classpath groovy) .
popd

export CLASSPATH=$(build-classpath objectweb-asm3/asm-all commons-cli antlr junit)
%ant -Djetty.dir=. -Dlib.dir=. compile test jar javadoc

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 %{name}.jar %{buildroot}%{_javadir}/%{name}.jar
(cd %{buildroot}%{_javadir} && ln -s %{name}.jar %{name}-runtime.jar)

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
install -p -m 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/JPP-%{name}-runtime.pom

# depmap
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "%{name}:%{name}"
%add_maven_depmap JPP-%{name}-runtime.pom %{name}-runtime.jar -a "%{name}:%{name}-runtime"

# ant config
install -d -m 755  %{buildroot}%{_sysconfdir}/ant.d
cat > %{buildroot}%{_sysconfdir}/ant.d/%{name} << EOF
ant cobertura junit log4j oro xerces-j2
EOF

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -rp build/api/* %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc ChangeLog COPYING COPYRIGHT README LICENSE-ASL-1.1 LICENSE-ASL-2.0
%config %{_sysconfdir}/ant.d/%{name}

%files javadoc
%doc COPYING COPYRIGHT LICENSE-ASL-1.1 LICENSE-ASL-2.0
%{_javadocdir}/%{name}

%changelog
* Tue Aug 12 2014 Liu Di <liudidi@gmail.com> - 1.9.4.1-14
- 为 Magic 3.0 重建

* Wed May 21 2014 Orion Poplawski <orion@cora.nwra.com> - 1.9.4.1-13
- Use junit instead of junit4

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9.4.1-12
- Use .mfiles generated during build

* Thu Mar 06 2014 Michal Srb <msrb@redhat.com> - 1.9.4.1-11
- Switch to asm3

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.9.4.1-10
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Michal Srb <msrb@redhat.com> - 1.9.4.1-8
- Add create-tarball.sh script to SRPM

* Mon Jul 22 2013 Michal Srb <msrb@redhat.com> - 1.9.4.1-7
- Fix license tag
- Add ASL 2.0 license text
- Remove unneeded files licensed under questionable license

* Fri Jul 19 2013 Michal Srb <msrb@redhat.com> - 1.9.4.1-6
- Provide URL for Source1 and Source2

* Wed Jul 17 2013 Michal Srb <msrb@redhat.com> - 1.9.4.1-5
- Build from clean tarball

* Wed Jul 03 2013 Michal Srb <msrb@redhat.com> - 1.9.4.1-4
- Replace servlet 2.5 with servlet 3.0 (Resolves: #979499)
- Install ASL 1.1 license file
- Spec file clean up

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Tomas Radej <tradej@redhat.com> - 1.9.4.1-2
- Added MPL to licence field

* Sun Oct 14 2012 Mat Booth <fedora@matbooth.co.uk> - 1.9.4.1-1
- Update for latest guidelines.
- Update to latest upstream version, bug 848871.
- Fix directory ownership, bug 850004.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Tomas Radej <tradej@redhat.com> - 1.9.3-5
- Fixed unmappable characters

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.9.3-2
- Fix objectweb-asm groupId in pom files
- Use simple ln -s and build-classpath to symlink jars
- Versionless jars

* Mon Jun 21 2010 Victor G. Vasilyev <victor.vasilyev@sun.com> 1.9.3-1
- Release 1.9.3

* Wed Aug 19 2009 Victor G. Vasilyev <victor.vasilyev@sun.com> 1.9-3
- Fix B(R) according to guidelines
- Use the  lnSysJAR macro
- Prevent brp-java-repack-jars from being run

* Sun Aug 09 2009 Victor G. Vasilyev <victor.vasilyev@sun.com> 1.9-2
- The license tag is changed according to http://cobertura.sourceforge.net/license.html

* Fri Jun 19 2009 Victor G. Vasilyev <victor.vasilyev@sun.com> 1.9-1
- release 1.9
