Name:           istack-commons
Version:        2.17
Release:        5%{?dist}
Summary:        Common code for some Glassfish projects
Group:          Development/Libraries
License:        CDDL and GPLv2 with exceptions
URL:            http://istack-commons.java.net

# svn export https://svn.java.net/svn/istack-commons~svn/tags/istack-commons-2.17/ istack-commons-2.17
# find istack-commons-2.17/ -name '*.class' -delete
# find istack-commons-2.17/ -name '*.jar' -delete
# tar -zcvf istack-commons-2.17.tar.gz istack-commons-2.17
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  args4j
BuildRequires:  bea-stax-api
BuildRequires:  codemodel >= 2.6-4
BuildRequires:  dom4j
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  jvnet-parent
BuildRequires:  junit
BuildRequires:  maven-local
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-plugin-build-helper
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-release-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-shared-file-management
BuildRequires:  plexus-archiver
BuildRequires:  plexus-io
BuildRequires:  testng

Requires:       jpackage-utils
Requires:       jvnet-parent


%description
Code shared between JAXP, JAXB, SAAJ, and JAX-WS projects.


%package -n maven-istack-commons-plugin
Summary:        istack-commons Maven Mojo
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       codemodel >= 2.6-4
Requires:       maven-shared-file-management
Requires:       plexus-archiver
Requires:       plexus-io


%description -n maven-istack-commons-plugin
This package contains the istack-commons Maven Mojo.


%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils


%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q
rm -rf test/lib/*.zip runtime/lib/*.zip

%pom_remove_plugin org.glassfish.copyright:glassfish-copyright-maven-plugin
%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin
%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin

%build

# The "-Pdefault-tools.jar" option is needed in order to make sure that the
# "tools.jar" file is added to the dependencies, otherwise it will not be added
# if the "java.vendor" property is "Oracle Corporation", which happens to be
# the value in JDK7:
mvn-rpmbuild \
  -Dproject.build.sourceEncoding=UTF-8 \
  -Pdefault-tools.jar \
  install \
  javadoc:aggregate


%install

install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_mavenpomdir}

# JAR
cp -p runtime/target/istack-commons-runtime-%{version}.jar %{buildroot}%{_javadir}/%{name}-runtime.jar
cp -p tools/target/istack-commons-tools-%{version}.jar %{buildroot}%{_javadir}/%{name}-tools.jar
cp -p test/target/istack-commons-test-%{version}.jar %{buildroot}%{_javadir}/%{name}-test.jar
cp -p buildtools/target/%{name}-buildtools-%{version}.jar %{buildroot}%{_javadir}/%{name}-buildtools.jar
cp -p maven-plugin/target/%{name}-maven-plugin-%{version}.jar %{buildroot}%{_javadir}/%{name}-maven-plugin.jar
cp -p soimp/target/%{name}-soimp-%{version}.jar %{buildroot}%{_javadir}/%{name}-soimp.jar

# JAVADOC
cp -rp target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

# POM
cp -p pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
cp -p runtime/pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}-runtime.pom
cp -p tools/pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}-tools.pom
cp -p test/pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}-test.pom
cp -p buildtools/pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}-buildtools.pom
cp -p maven-plugin/pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}-maven-plugin.pom
cp -p soimp/pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}-soimp.pom

# DEPMAP
%add_maven_depmap JPP-%{name}.pom
%add_maven_depmap JPP-%{name}-runtime.pom %{name}-runtime.jar
%add_maven_depmap JPP-%{name}-tools.pom %{name}-tools.jar
%add_maven_depmap JPP-%{name}-test.pom %{name}-test.jar
%add_maven_depmap JPP-%{name}-buildtools.pom %{name}-buildtools.jar
%add_maven_depmap JPP-%{name}-maven-plugin.pom %{name}-maven-plugin.jar -f maven-plugin
%add_maven_depmap JPP-%{name}-soimp.pom %{name}-soimp.jar

%files -f .mfiles
%doc Licence.txt

%files -n maven-istack-commons-plugin -f .mfiles-maven-plugin
%doc Licence.txt

%files javadoc
%{_javadocdir}/%{name}
%doc Licence.txt


%changelog
* Sun Aug 03 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 2.17-5
- Fix FTBFS due to F21 XMvn changes (#1106808)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.17-3
- Use Requires: java-headless rebuild (#1067528)

* Fri Jul 26 2013 Ade Lee <alee@rdhat.com> - 2.17-2
- Bugzilla BZ#988933 - Removed unneeded build dependencies.

* Thu May 16 2013 Tom Callaway <spot@fedoraproject.org> - 2.17-1
- update to 2.17

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.6.1-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Juan Hernandez <juan.hernandez@redhat.com> - 2.6.1-5
- Add maven-enforcer-plugin as build time dependency

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 31 2012 Gil Cattaneo <puntogil@libero.it> 2.6.1-3
- Rebuilt with codemodel support
- Enable maven-plugin, test and buildtools modules

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6.1-2
- Minor cleanups of the spec file

* Mon Jan 16 2012 Marek Goldmann <mgoldman@redhat.com> 2.6.1-1
- Initial packaging
