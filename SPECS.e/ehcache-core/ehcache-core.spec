Name:          ehcache-core
Version:       2.6.7
Release:       5%{?dist}
Summary:       Easy Hibernate Cache
License:       ASL 2.0
URL:           http://ehcache.org/
# svn export http://svn.terracotta.org/svn/ehcache/tags/ehcache-core-2.6.7
# find ehcache-core-2.6.7 -name '*.jar' -delete
# ehcache-core-2.6.7/tools/maven-ant-tasks-2.0.7.jar
# ehcache-core-2.6.7/src/test/resources/resourceclassloader/private-classpath.jar
# find ehcache-core-2.6.7 -name '*.class' -delete
# tar czf ehcache-core-2.6.7-clean-src-svn.tar.gz ehcache-core-2.6.7
Source0:       %{name}-%{version}-clean-src-svn.tar.gz
Patch0:        %{name}-2.6.7-java8.patch

BuildRequires: ehcache-parent
BuildRequires: java-devel

BuildRequires: geronimo-jta
BuildRequires: hibernate3 >= 3.6.10-7
BuildRequires: ehcache-sizeof-agent
BuildRequires: slf4j
BuildRequires: tomcat-servlet-3.0-api
BuildRequires: mvn(org.slf4j:slf4j-jdk14)

# test
%if 0
BuildRequires: apache-commons-logging
BuildRequires: mvn(net.sf.hibernate:hibernate) >= 2.1.8
BuildRequires: mvn(org.hibernate:hibernate-ehcache)
BuildRequires: bsh
BuildRequires: btm
BuildRequires: derby
BuildRequires: dom4j
BuildRequires: hamcrest12
BuildRequires: javassist
BuildRequires: junit
BuildRequires: mockito
BuildRequires: xsom
%endif

BuildRequires: maven-local
BuildRequires: maven-source-plugin
BuildRequires: rmic-maven-plugin
BuildRequires: xml-maven-plugin
BuildRequires: plexus-resources

Requires:      ehcache-sizeof-agent
Requires:      geronimo-jta
Requires:      hibernate3 >= 3.6.10-7
Requires:      slf4j
Requires:      tomcat-servlet-3.0-api

BuildArch:     noarch

%description
Ehcache is a pure Java, in-process cache.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
%patch0 -p0

%pom_remove_plugin org.codehaus.gmaven:gmaven-plugin
%pom_remove_plugin org.eclipse.m2e:lifecycle-mapping
%pom_remove_plugin org.apache.maven.plugins:maven-checkstyle-plugin

# don't generate source archive
%pom_remove_plugin org.apache.maven.plugins:maven-assembly-plugin

# Make sure we require version '3' of Hibernate
%pom_xpath_remove "pom:dependencies/pom:dependency[pom:groupId = 'org.hibernate']/pom:version"
%pom_xpath_inject "pom:dependencies/pom:dependency[pom:groupId = 'org.hibernate']" "<version>3</version>"

# Don't use buildnumber-plugin, because jna is required (and currently broken)
%pom_xpath_remove "pom:profiles/pom:profile[pom:id = 'buildnumber-git']"

# circular deps
# org.hibernate hibernate-ehcache 3.3.2.GA
# unavailable deps
%pom_remove_dep net.sf.hibernate:hibernate
%pom_xpath_remove "pom:dependencies/pom:dependency[pom:scope = 'test']"

# disable embedded ehcache-sizeof-agent.jar copy
%pom_remove_plugin :maven-dependency-plugin

%build

%mvn_file :%{name} %{name}
%mvn_alias :%{name} net.sf.ehcache:ehcache
# tests skipped. cause: missing dependencies
%mvn_build -f -- -Dmaven.local.depmap.file="%{_mavendepmapfragdir}/tomcat-tomcat-servlet-api"

%install
%mvn_install

%files -f .mfiles
%doc src/assemble/EHCACHE-CORE-LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc src/assemble/EHCACHE-CORE-LICENSE.txt

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.6.7-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 gil cattaneo <puntogil@libero.it> - 2.6.7-2
- switch to XMvn
- minor changes to adapt to current guideline

* Fri May 24 2013 gil cattaneo <puntogil@libero.it> - 2.6.7-1
- update to 2.6.7

* Sun Apr 21 2013 gil cattaneo <puntogil@libero.it> - 2.6.6-1
- update to 2.6.6

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.6.0-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Nov 07 2012 Marek Goldmann <mgoldman@redhat.com> - 2.6.0-3
- Add support for new Maven compat version resolver (hibernate3)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 gil cattaneo <puntogil@libero.it> - 2.6.0-1
- update to 2.6.0

* Sat Apr 21 2012 gil cattaneo <puntogil@libero.it> - 2.5.2-1
- update to 2.5.2

* Mon Mar 12 2012 Andy Grimm <agrimm@gmail.com> - 2.5.1-1
- Initial packaging
