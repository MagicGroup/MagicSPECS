Name:          ehcache-core
Version:       2.6.11
Release:       1%{?dist}
Summary:       Easy Hibernate Cache
License:       ASL 2.0
URL:           http://ehcache.org/
# svn export http://svn.terracotta.org/svn/ehcache/tags/ehcache-core-2.6.11
# find ehcache-core-2.6.11 -name '*.jar' -delete
# tools/maven-ant-tasks-2.0.7.jar
# src/test/resources/resourceclassloader/private-classpath.jar
# find ehcache-core-2.6.11 -name '*.class' -delete
# tar cJf ehcache-core-2.6.11.tar.xz ehcache-core-2.6.11
Source0:       %{name}-%{version}.tar.xz
Patch0:        %{name}-2.6.7-java8.patch

BuildRequires: maven-local
BuildRequires: mvn(javax.servlet:javax.servlet-api)
BuildRequires: mvn(javax.transaction:jta)
BuildRequires: mvn(net.sf.ehcache:ehcache-parent:pom:)
BuildRequires: mvn(net.sf.ehcache:sizeof-agent)
BuildRequires: mvn(org.codehaus.mojo:rmic-maven-plugin)
BuildRequires: mvn(org.codehaus.mojo:xml-maven-plugin)
BuildRequires: mvn(org.codehaus.plexus:plexus-resources)
BuildRequires: mvn(org.hibernate:hibernate-core:3)
BuildRequires: mvn(org.slf4j:slf4j-api)
BuildRequires: mvn(org.slf4j:slf4j-jdk14)

# test
%if 0
BuildRequires: mvn(com.sun.xsom:xsom)
BuildRequires: mvn(commons-logging:commons-logging)
BuildRequires: mvn(dom4j:dom4j)
BuildRequires: mvn(javassist:javassist)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(net.sf.hibernate:hibernate:2.1.8)
BuildRequires: mvn(org.apache.derby:derby)
BuildRequires: mvn(org.beanshell:bsh:1.3.0)
BuildRequires: mvn(org.codehaus.btm:btm)
BuildRequires: mvn(org.hamcrest:hamcrest-core:1.2)
BuildRequires: mvn(org.hamcrest:hamcrest-library:1.2)
BuildRequires: mvn(org.hibernate:hibernate-ehcache:3.3.2.GA)
BuildRequires: mvn(org.mockito:mockito-core)
%endif

Requires:      hibernate3 >= 3.6.10-7

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
# Use net.sf.ehcache:ehcache-parent:2.5
# Remove its support because it breaks build during javadoc task
%pom_remove_parent
# disable doclint
%pom_remove_plugin :maven-javadoc-plugin
%pom_xpath_inject "pom:project" "<groupId>net.sf.ehcache</groupId>"

%pom_remove_plugin :gmaven-plugin
%pom_remove_plugin :lifecycle-mapping
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :maven-source-plugin

# don't generate source archive
%pom_remove_plugin :maven-assembly-plugin

# Make sure we require version '3' of Hibernate
%pom_xpath_set "pom:dependency[pom:groupId = 'org.hibernate']/pom:version" 3

%pom_change_dep :servlet-api :javax.servlet-api:3.1.0

# Don't use buildnumber-plugin, because jna is required (and currently broken)
%pom_xpath_remove "pom:profiles/pom:profile[pom:id = 'buildnumber-git']"

# circular deps
# org.hibernate hibernate-ehcache 3.3.2.GA
# unavailable deps
%pom_remove_dep net.sf.hibernate:hibernate
%pom_xpath_remove "pom:dependency[pom:scope = 'test']"

%pom_xpath_remove "pom:dependency/pom:scope"

# disable embedded ehcache-sizeof-agent.jar copy
%pom_remove_plugin :maven-dependency-plugin

%mvn_file :%{name} %{name}
%mvn_alias :%{name} net.sf.ehcache:ehcache

%build

# tests skipped. cause: missing dependencies
%mvn_build -f -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%license src/assemble/EHCACHE-CORE-LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license src/assemble/EHCACHE-CORE-LICENSE.txt

%changelog
* Sun Jul 26 2015 gil cattaneo <puntogil@libero.it> 2.6.11-1
- update to 2.6.11

* Thu Jun 18 2015 gil cattaneo <puntogil@libero.it> 2.6.7-9
- disable doclint in javadoc

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 04 2015 gil cattaneo <puntogil@libero.it> 2.6.7-7
- use servlet api 3.1

* Sun Feb 01 2015 gil cattaneo <puntogil@libero.it> 2.6.7-6
- introduce license macro

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
