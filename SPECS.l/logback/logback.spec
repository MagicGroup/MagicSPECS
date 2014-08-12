Name:           logback
Version:        1.1.1
Release:        2%{?dist}
Summary:        A Java logging library
License:        LGPLv2 or EPL
URL:            http://logback.qos.ch/
Source0:        http://logback.qos.ch/dist/%{name}-%{version}.tar.gz
# use antrun-plugin instead of gmaven
Patch0:         %{name}-1.0.10-antrunplugin.patch

# Java dependencies
BuildRequires: java-devel >= 1:1.6.0

# Required libraries
BuildRequires: mvn(javax.mail:mail)
BuildRequires: mvn(log4j:log4j:1.2.17)
BuildRequires: mvn(org.apache.geronimo.specs:geronimo-jms_1.1_spec)
BuildRequires: mvn(org.apache.tomcat:tomcat-catalina)
BuildRequires: mvn(org.apache.tomcat:tomcat-servlet-api)
# require groovy 2.0.7
BuildRequires: mvn(org.codehaus.groovy:groovy)
BuildRequires: mvn(org.codehaus.janino:janino)
BuildRequires: mvn(org.eclipse.jetty:jetty-server)
BuildRequires: mvn(org.fusesource:fusesource-pom:pom:)
BuildRequires: mvn(org.fusesource.jansi:jansi)
BuildRequires: mvn(org.slf4j:slf4j-api)
BuildRequires: mvn(org.slf4j:slf4j-ext)

# groovy-all embedded libraries
BuildRequires: mvn(antlr:antlr)
BuildRequires: mvn(asm:asm-all)
BuildRequires: mvn(commons-cli:commons-cli)
BuildRequires: mvn(org.slf4j:slf4j-nop)

# test deps
%if 0
BuildRequires: mvn(com.h2database:h2:1.2.132)
BuildRequires: mvn(dom4j:dom4j:1.6.1)
BuildRequires: mvn(hsqldb:hsqldb:1.8.0.7)
BuildRequires: mvn(mysql:mysql-connector-java:5.1.9)
BuildRequires: mvn(postgresql:postgresql:8.4-701.jdbc4)
BuildRequires: mvn(org.easytesting:fest-assert:1.2)
BuildRequires: mvn(org.mockito:mockito-core:1.9.0)
BuildRequires: mvn(org.slf4j:integration:1.7.5)
BuildRequires: mvn(org.slf4j:jul-to-slf4j:1.7.5)
BuildRequires: mvn(org.slf4j:log4j-over-slf4j:1.7.5)
BuildRequires: mvn(org.slf4j:slf4j-api:1.7.5:test-jar)
BuildRequires: mvn(org.slf4j:slf4j-ext:1.7.5)
BuildRequires: mvn(com.icegreen:greenmail:1.3)
BuildRequires: mvn(org.subethamail:subethasmtp:2.1.0)
# mvn(ch.qos.logback:logback-core:%%{version}:test-jar)
%endif

# antrun plugin deps
BuildRequires: mvn(org.apache.ant:ant-junit)
BuildRequires: mvn(org.apache.felix:org.apache.felix.main)
BuildRequires: mvn(junit:junit)

BuildRequires: maven-local
BuildRequires: maven-antrun-plugin
BuildRequires: maven-plugin-build-helper
BuildRequires: maven-plugin-bundle
#BuildRequires: maven-source-plugin

BuildArch:     noarch

%description
Logback is intended as a successor to the popular log4j project. At present
time, logback is divided into three modules, logback-core, logback-classic
and logback-access.

The logback-core module lays the groundwork for the other two modules. The
logback-classic module can be assimilated to a significantly improved
version of log4j. Moreover, logback-classic natively implements the SLF4J
API so that you can readily switch back and forth between logback and other
logging frameworks such as log4j or java.util.logging (JUL).

The logback-access module integrates with Servlet containers, such as
Tomcat and Jetty, to provide HTTP-access log functionality. Note that you
could easily build your own module on top of logback-core.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
API documentation for the Logback library

%package access
Summary:       Logback-access module for Servlet integration

%description access
The logback-access module integrates with Servlet containers, such as Tomcat
and Jetty, to provide HTTP-access log functionality. Note that you could
easily build your own module on top of logback-core. 

%package examples
Summary:       Logback Examples Module

%description examples
logback-examples module.

%prep
%setup -q
# Clean up
find . -name "*.class" -delete
find . -name "*.cmd" -delete
find . -name "*.jar" -delete

%patch0 -p0

%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :gmaven-plugin %{name}-classic

# Clean up the documentation
sed -i 's/\r//' LICENSE.txt README.txt docs/*.* docs/*/*.* docs/*/*/*.*
sed -i 's#"apidocs#"%{_javadocdir}/%{name}#g' docs/*.html
rm -rf docs/apidocs docs/project-reports docs/testapidocs docs/project-reports.html
rm -f docs/manual/.htaccess docs/css/site.css # Zero-length file

sed -i 's#<artifactId>groovy-all</artifactId#<artifactId>groovy</artifactId#' $(find . -name "pom.xml")

# force tomcat apis
sed -i 's#<groupId>javax.servlet#<groupId>org.apache.tomcat#' $(find . -name "pom.xml")
sed -i 's#<artifactId>servlet-api#<artifactId>tomcat-servlet-api#' $(find . -name "pom.xml")
sed -i 's#javax.servlet.*;version="2.5"#javax.servlet.*;version="3.0"#' %{name}-access/pom.xml
sed -i 's#<version>2.5</version>#<version>${tomcat.version}</version>#' pom.xml

sed -i 's#<version>1.2.14</version>#<version>1.2.17</version>#' %{name}-examples/pom.xml

rm -r %{name}-*/src/test/java/*
# remove test deps
# ch.qos.logback:logback-core:test-jar
%pom_xpath_remove "pom:project/pom:dependencyManagement/pom:dependencies/pom:dependency[pom:type = 'test-jar']"

while read f
do

%pom_xpath_remove "pom:project/pom:dependencies/pom:dependency[pom:type = 'test-jar']" ${f}

done << EOF
%{name}-access/pom.xml
%{name}-classic/pom.xml
EOF

while read f
do

%pom_xpath_remove "pom:project/pom:dependencies/pom:dependency[pom:scope = 'test']" ${f}

done << EOF
pom.xml
%{name}-access/pom.xml
%{name}-classic/pom.xml
%{name}-core/pom.xml
EOF

# bundle-test-jar
%pom_xpath_remove "pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-jar-plugin']/pom:executions" %{name}-access
%pom_xpath_remove "pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-jar-plugin']/pom:executions" %{name}-classic
%pom_xpath_remove "pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-jar-plugin']/pom:executions" %{name}-core

# com.oracle:ojdbc14:10.2.0.1 com.microsoft.sqlserver:sqljdbc4:2.0
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id = 'host-orion']" %{name}-access
%pom_xpath_remove "pom:project/pom:profiles" %{name}-classic

%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id = 'javadocjar']"

# disable for now
%pom_disable_module logback-site

%pom_xpath_remove "pom:build/pom:extensions"

%build

%mvn_package ":%{name}-access" access
%mvn_package ":%{name}-examples" examples
# unavailable test dep maven-scala-plugin
# slf4jJAR and org.apache.felix.main are required by logback-examples modules for maven-antrun-plugin
%mvn_build -f -- \
  -Dslf4jJAR=$(build-classpath slf4j/api) \
  -Dorg.apache.felix:org.apache.felix.main:jar=$(build-classpath felix/org.apache.felix.main)

%install
%mvn_install

install -d -m 755 %{buildroot}%{_datadir}/%{name}-%{version}/examples
cp -r %{name}-examples/pom.xml %{name}-examples/src %{buildroot}%{_datadir}/%{name}-%{version}/examples

%files -f .mfiles
%doc LICENSE.txt README.txt docs/*
%dir %{_javadir}/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%files access -f .mfiles-access
%doc LICENSE.txt

%files examples -f .mfiles-examples
%doc LICENSE.txt
%{_datadir}/%{name}-%{version}

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Orion Poplawski <orion@cora.nwra.com> - 1.1.1-1
- Update to 1.1.1

* Wed Jan 29 2014 gil cattaneo <puntogil@libero.it> - 1.1.0-1
- Update to 1.1.0

* Sun Aug 04 2013 gil cattaneo <puntogil@libero.it> - 1.0.13-1
- Update to 1.0.13

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 gil cattaneo <puntogil@libero.it> - 1.0.10-2
- switch to XMvn
- minor changes to adapt to current guideline

* Tue Mar 19 2013 gil cattaneo <puntogil@libero.it> - 1.0.10-1
- Update to 1.0.10

* Thu Mar 14 2013 gil cattaneo <puntogil@libero.it> - 1.0.9-4
- Use Maven build
- Removed un{used,available} plugin

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Mary Ellen Foster <mefoster@gmail.com> - 1.0.9-2
- Remove F16 backward compatibility since it's EOL soon

* Sat Dec 08 2012 gil cattaneo <puntogil@libero.it> - 1.0.9-1
- Update to 1.0.9
- Preserved timestamp in pom files
- Applied changes to build against older jetty on F16, thanks to Mary Ellen F.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Orion Poplawski <orion@nwra.com> - 1.0.6-2
- Split off access module into sub-package (bug 663198)
- Change BR/R from servlet25 to tomcat-servlet-3.0-api (bug 819552)
- Update build.xml to include jetty jars, drop setting CLASSPATH

* Wed Jul 11 2012 gil cattaneo <puntogil@libero.it> - 1.0.6-1
- Update to 1.0.6

* Tue Mar 20 2012 Mary Ellen Foster <mefoster at gmail.com> - 1.0.1-1
- Update to 1.0.1
- Prepare for re-review

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.9.18-5
- Make jars and javadoc versionless
- Fix pom filenames (#655813)
- Remove gcj bits
- Other packaging cleanups/fixes

* Wed Jan 13 2010 Mary Ellen Foster <mefoster at gmail.com> - 0.9.18-4
- Change (Build)Requirement from geronimo-specs to jms

* Wed Jan 13 2010 Mary Ellen Foster <mefoster at gmail.com> - 0.9.18-3
- Add some missing (Build)Requirements

* Tue Jan 12 2010 Mary Ellen Foster <mefoster at gmail.com> - 0.9.18-2
- Add maven2 BuildRequirements
- Remove requirement for specific slf4j version

* Mon Jan 11 2010 Mary Ellen Foster <mefoster at gmail.com> - 0.9.18-1
- Update to new upstream version -- many bugfixes, see
  http://qos.ch/pipermail/announce/2009/000068.html
- Include new license tag
- Add all referenced dependencies to the Requires list
- Specify which bits of tomcat are actually used, instead of requiring
  all of it
- Don't remove hsqldb from poms any more; Maven metadata has been added

* Wed Jan  6 2010 Mary Ellen Foster <mefoster at gmail.com> - 0.9.17-3
- Manually add the Maven metadata for geronimo-specs-jms

* Wed Dec  2 2009 Mary Ellen Foster <mefoster at gmail.com> - 0.9.17-2
- Use Maven build instead (with all that entails), and include POMs
- Add -examples subpackage
- Depend on javamail 1.4

* Wed Nov 18 2009 Mary Ellen Foster <mefoster at gmail.com> - 0.9.17-1
- Initial package (using build.xml from Debian)
