%global namedreltag .RELEASE
%global namedversion %{version}%{?namedreltag}

Name:          springframework
Version:       3.2.6
Release:       3%{?dist}
Summary:       Spring Java Application Framework
Epoch:         0
License:       ASL 2.0
URL:           http://projects.spring.io/spring-framework/

Source0:       https://github.com/spring-projects/spring-framework/archive/v%{namedversion}.tar.gz

Source101:     springframework-%{namedversion}.pom
Source102:     http://repo1.maven.org/maven2/org/%{name}/spring-core/%{namedversion}/spring-core-%{namedversion}.pom
Source103:     http://repo1.maven.org/maven2/org/%{name}/spring-expression/%{namedversion}/spring-expression-%{namedversion}.pom
Source104:     http://repo1.maven.org/maven2/org/%{name}/spring-context/%{namedversion}/spring-context-%{namedversion}.pom
Source105:     http://repo1.maven.org/maven2/org/%{name}/spring-aop/%{namedversion}/spring-aop-%{namedversion}.pom
Source106:     http://repo1.maven.org/maven2/org/%{name}/spring-instrument/%{namedversion}/spring-instrument-%{namedversion}.pom
Source107:     http://repo1.maven.org/maven2/org/%{name}/spring-beans/%{namedversion}/spring-beans-%{namedversion}.pom
Source108:     http://repo1.maven.org/maven2/org/%{name}/spring-orm/%{namedversion}/spring-orm-%{namedversion}.pom
Source109:     http://repo1.maven.org/maven2/org/%{name}/spring-test/%{namedversion}/spring-test-%{namedversion}.pom
Source110:     http://repo1.maven.org/maven2/org/%{name}/spring-context-support/%{namedversion}/spring-context-support-%{namedversion}.pom
Source111:     http://repo1.maven.org/maven2/org/%{name}/spring-instrument-tomcat/%{namedversion}/spring-instrument-tomcat-%{namedversion}.pom
Source112:     http://repo1.maven.org/maven2/org/%{name}/spring-jdbc/%{namedversion}/spring-jdbc-%{namedversion}.pom
Source113:     http://repo1.maven.org/maven2/org/%{name}/spring-jms/%{namedversion}/spring-jms-%{namedversion}.pom
Source114:     http://repo1.maven.org/maven2/org/%{name}/spring-tx/%{namedversion}/spring-tx-%{namedversion}.pom
Source115:     http://repo1.maven.org/maven2/org/%{name}/spring-web/%{namedversion}/spring-web-%{namedversion}.pom
Source116:     http://repo1.maven.org/maven2/org/%{name}/spring-oxm/%{namedversion}/spring-oxm-%{namedversion}.pom
Source117:     http://repo1.maven.org/maven2/org/%{name}/spring-struts/%{namedversion}/spring-struts-%{namedversion}.pom
Source118:     http://repo1.maven.org/maven2/org/%{name}/spring-webmvc/%{namedversion}/spring-webmvc-%{namedversion}.pom
Source119:     http://repo1.maven.org/maven2/org/%{name}/spring-webmvc-portlet/%{namedversion}/spring-webmvc-portlet-%{namedversion}.pom

Patch0:        springframework-3.2.6-java.io.IOException-is-never-thrown.patch
Patch1:        springframework-3.2.6-port-spring-jms-to-javax.resources-1.7.patch
Patch2:        springframework-3.2.6-port-spring-orm-to-javax.persistence-2.0.patch
Patch3:        springframework-3.2.6-port-spring-test-to-servlet-3.0.patch
Patch4:        springframework-3.2.6-port-spring-tx-to-javax.resources-1.7.patch
Patch5:        springframework-3.2.6-port-to-hibernate-validator-5.patch
# TODO: rebase the patch for 3.2.x
#Patch6:       springframework-3.1.4-osgi-support.patch

BuildRequires:  maven-local
BuildRequires:  mvn(aopalliance:aopalliance)
BuildRequires:  mvn(c3p0:c3p0)
BuildRequires:  mvn(com.caucho:hessian)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:  mvn(com.h2database:h2)
BuildRequires:  mvn(com.jamonapi:jamon)
BuildRequires:  mvn(com.lowagie:itext)
BuildRequires:  mvn(commons-beanutils:commons-beanutils)
BuildRequires:  mvn(commons-fileupload:commons-fileupload)
BuildRequires:  mvn(commons-httpclient:commons-httpclient)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(commons-pool:commons-pool)
BuildRequires:  mvn(com.thoughtworks.xstream:xstream)
BuildRequires:  mvn(hsqldb:hsqldb:1)
BuildRequires:  mvn(jasperreports:jasperreports)
BuildRequires:  mvn(javax.ejb:ejb-api)
BuildRequires:  mvn(javax.el:el-api)
BuildRequires:  mvn(javax.faces:jsf-api)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(javax.jdo:jdo-api)
BuildRequires:  mvn(javax.mail:mail)
BuildRequires:  mvn(javax.portlet:portlet-api)
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(javax.servlet.jsp:jsp-api)
BuildRequires:  mvn(javax.servlet:jstl)
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(javax.xml:jaxrpc-api)
BuildRequires:  mvn(javax.xml.soap:saaj-api)
BuildRequires:  mvn(joda-time:joda-time)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(log4j:log4j)
BuildRequires:  mvn(net.sf.cglib:cglib)
BuildRequires:  mvn(net.sf.ehcache:ehcache-core)
BuildRequires:  mvn(net.sourceforge.jexcelapi:jxl)
BuildRequires:  mvn(org.apache.derby:derby)
BuildRequires:  mvn(org.apache.derby:derbyclient)
BuildRequires:  mvn(org.apache.geronimo.specs:geronimo-interceptor_3.0_spec)
BuildRequires:  mvn(org.apache.geronimo.specs:geronimo-jms_1.1_spec)
BuildRequires:  mvn(org.apache.geronimo.specs:geronimo-jta_1.1_spec)
BuildRequires:  mvn(org.apache.geronimo.specs:geronimo-validation_1.0_spec)
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  mvn(org.apache.openjpa:openjpa-lib)
BuildRequires:  mvn(org.apache.openjpa:openjpa-persistence)
BuildRequires:  mvn(org.apache.poi:poi)
BuildRequires:  mvn(org.apache.struts:struts-core)
BuildRequires:  mvn(org.apache.struts:struts-extras)
BuildRequires:  mvn(org.apache.struts:struts-tiles)
BuildRequires:  mvn(org.apache.tiles:tiles-api)
BuildRequires:  mvn(org.apache.tiles:tiles-core)
BuildRequires:  mvn(org.apache.tiles:tiles-el)
BuildRequires:  mvn(org.apache.tiles:tiles-jsp)
BuildRequires:  mvn(org.apache.tiles:tiles-servlet)
BuildRequires:  mvn(org.apache.tomcat:tomcat-catalina)
BuildRequires:  mvn(org.apache.tomcat:tomcat-el-api)
BuildRequires:  mvn(org.apache.tomcat:tomcat-jsp-api)
BuildRequires:  mvn(org.apache.tomcat:tomcat-servlet-api)
BuildRequires:  mvn(org.apache.xmlbeans:xmlbeans)
BuildRequires:  mvn(org.aspectj:aspectjweaver)
BuildRequires:  mvn(org.beanshell:bsh)
BuildRequires:  mvn(org.codehaus.castor:castor-xml)
BuildRequires:  mvn(org.codehaus.groovy:groovy)
BuildRequires:  mvn(org.codehaus.jackson:jackson-mapper-asl)
BuildRequires:  mvn(org.eclipse.jetty:jetty-server)
BuildRequires:  mvn(org.eclipse.jetty:jetty-servlet)
BuildRequires:  mvn(org.eclipse.persistence:org.eclipse.persistence.core)
BuildRequires:  mvn(org.freemarker:freemarker)
BuildRequires:  mvn(org.hamcrest:hamcrest-core)
BuildRequires:  mvn(org.hibernate:hibernate-core:3)
BuildRequires:  mvn(org.hibernate:hibernate-entitymanager:3)
BuildRequires:  mvn(org.hibernate:hibernate-validator)
BuildRequires:  mvn(org.hibernate.javax.persistence:hibernate-jpa-2.0-api)
BuildRequires:  mvn(org.jboss.spec.javax.resource:jboss-connector-api_1.7_spec)
BuildRequires:  mvn(org.jibx:jibx-run)
BuildRequires:  mvn(org.jruby.extras:bytelist)
BuildRequires:  mvn(org.jruby:jruby)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.quartz-scheduler:quartz-backward-compat)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.testng:testng)
BuildRequires:  mvn(rome:rome)
BuildRequires:  mvn(taglibs:standard)
BuildRequires:  mvn(toplink.essentials:toplink-essentials)
BuildRequires:  mvn(velocity-tools:velocity-tools-view)
BuildRequires:  mvn(velocity:velocity)
BuildRequires:  mvn(xmlunit:xmlunit)

BuildArch:     noarch

%description
Spring is a layered Java/J2EE application framework, based on code published in
Expert One-on-One J2EE Design and Development by Rod Johnson (Wrox, 2002). 

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%package aop
Summary:       Spring Aspect Oriented Framework

%description aop
Spring AOP is an enabling technology that allows the implementation of custom
aspects and provides declarative transaction management without EJB.

%package beans
Summary:       Spring Bean Factory

%description beans
The Spring Bean Factory provides an advanced configuration mechanism capable of
managing beans of any nature, using potentially any kind of storage facility.

%package context
Summary:       Spring Application Context

%description context
The Spring Application Context is a complete superset of a bean factory, and
adds enhanced capabilities to it, some of them more J2EE and
enterprise-centric.

%package context-support
Summary:       Spring Context Support

%description context-support
This package provide Quartz/CommonJ scheduling,
UI templating, mail and caching.

%package expression
Summary:       Spring Expression Language (SpEL)

%description expression
The Spring Expression Language (SpEL for short) is a powerful expression
language that supports querying and manipulating an object graph at runtime.

%package instrument
Summary:       Spring Instrumentation

%description instrument
The Spring Instrumentation Framework exposes performance and
resource utilization metrics for the Spring container and
gives you runtime control of the container.

%package instrument-tomcat
Summary:       Spring Instrument Tomcat Weaver

%description instrument-tomcat
Extension of Tomcat's default class loader which
adds instrumentation to loaded classes without the
need to use a VM-wide agent.

%package jdbc
Summary:       Spring JDBC

%description jdbc
Spring JDBC takes care of all the low-level details associated to the
development with JDBC.

%package jms
Summary:       Spring jms

%description jms
This package provide Java Message Service 1.0.2/1.1 support.

%package orm
Summary:       Spring ORM

%description orm
This package provide JDO support, JPA support, Hibernate
support, TopLink support.

%package oxm
Summary:       Spring OXM

%description oxm
This package provide marshaling and unmarshalling
for XML with JAXB context and JiBX binding factories.

%package struts
Summary:       Spring Web Struts

%description struts
This package provide integrate a Struts
application with Spring

%package test
Summary:       Spring test context framework

%description test
Spring's test context framework. Also includes common Servlet and
Portlet API mocks.

%package tx
Summary:       Spring Transaction Management

%description tx
Spring provides a consistent abstraction for transaction management that
provides a consistent programming model across different transaction APIs,
supports declarative transaction management, provides a simpler API for
programmatic transaction management and integrates with Spring's various data
access abstractions.

%package web
Summary:       Spring Web

%description web
This package provide web application context, multipart
resolver, HTTP-based remoting support.

%package webmvc
Summary:       Spring Web Servlet

%description webmvc
This package provide framework servlets, web MVC framework,
web controllers, web views for JSP, Velocity, Tiles,
iText and POI.

%package webmvc-portlet
Summary:       Spring Web Portlet

%description webmvc-portlet
This package provide support development of Portlet
applications with Spring.

%prep
%setup -q -n spring-framework-%{namedversion}
find -name "*.class" -delete
find -name "*.jar" -print -delete

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
#%%patch6 -p1


cp %{SOURCE101} pom.xml
cp %{SOURCE102} spring-core/pom.xml
cp %{SOURCE103} spring-expression/pom.xml
cp %{SOURCE104} spring-context/pom.xml
cp %{SOURCE105} spring-aop/pom.xml
cp %{SOURCE106} spring-instrument/pom.xml
cp %{SOURCE107} spring-beans/pom.xml
cp %{SOURCE108} spring-orm/pom.xml
cp %{SOURCE109} spring-test/pom.xml
cp %{SOURCE110} spring-context-support/pom.xml
cp %{SOURCE111} spring-instrument-tomcat/pom.xml
cp %{SOURCE112} spring-jdbc/pom.xml
cp %{SOURCE113} spring-jms/pom.xml
cp %{SOURCE114} spring-tx/pom.xml
cp %{SOURCE115} spring-web/pom.xml
cp %{SOURCE116} spring-oxm/pom.xml
cp %{SOURCE117} spring-struts/pom.xml
cp %{SOURCE118} spring-webmvc/pom.xml
cp %{SOURCE119} spring-webmvc-portlet/pom.xml


# do not generate R on hiberante4, we use version 3
%pom_remove_dep :hibernate-entitymanager spring-orm
%pom_add_dep org.hibernate:hibernate-entitymanager:3 spring-orm

# missing dep
%pom_remove_dep com.jayway.jsonpath:json-path spring-test

# looks like older jstl 1.1 works just fine (upstream uses 1.2)
%pom_remove_dep javax.servlet:jstl spring-test
%pom_add_dep taglibs:standard spring-test

%pom_remove_dep struts:struts spring-struts
%pom_add_dep org.apache.struts:struts-core spring-struts
%pom_add_dep org.apache.struts:struts-extras spring-struts
%pom_add_dep org.apache.struts:struts-tiles spring-struts

# remove optional/missing deps
%pom_remove_dep org.apache.tiles:tiles-extras spring-webmvc
%pom_remove_dep org.apache.tiles:tiles-request-api spring-webmvc

# build against connector-api 1.7 instead of 1.5
%pom_remove_dep javax.resource:connector-api spring-tx
%pom_add_dep org.jboss.spec.javax.resource:jboss-connector-api_1.7_spec spring-tx

# Remove the dependency on WebSphere UOW as it is not open source and we will
# never be able to build it:
%pom_remove_dep com.ibm.websphere:uow spring-tx
rm spring-tx/src/main/java/org/springframework/transaction/jta/WebSphereUowTransactionManager.java \
 spring-tx/src/test/java/org/springframework/transaction/jta/WebSphereUowTransactionManagerTests.java

# hiberante3 is a compat package
%pom_remove_dep :hibernate-annotations spring-orm
%pom_remove_dep :hibernate-core spring-orm
%pom_add_dep org.hibernate:hibernate-core:3 spring-orm

# missing dep ibatis
rm -rf spring-orm/src/main/java/org/springframework/orm/ibatis/*
%pom_remove_dep :ibatis-sqlmap spring-orm

%pom_remove_dep :openjpa spring-orm
%pom_add_dep org.apache.openjpa:openjpa-lib spring-orm

%pom_remove_dep :org.eclipse.persistence.jpa spring-orm
%pom_add_dep org.apache.openjpa:openjpa-persistence spring-orm

# build against connector-api 1.7 instead of 1.5
%pom_remove_dep javax.resource:connector-api spring-jms
%pom_add_dep org.jboss.spec.javax.resource:jboss-connector-api_1.7_spec spring-jms

# hsqldb1 is a compat package, fix version
%pom_remove_dep hsqldb:hsqldb spring-jdbc
%pom_add_dep hsqldb:hsqldb:1 spring-jdbc

# use tomcat 7 lib
%pom_remove_dep org.apache.tomcat:catalina spring-instrument-tomcat
%pom_add_dep org.apache.tomcat:tomcat-catalina spring-instrument-tomcat

# missing dep jcache
rm -Rf spring-context-support/src/main/java/org/springframework/cache/jcache/
%pom_remove_dep javax.cache:cache-api spring-context-support

# missing dep commonj
rm -Rf spring-context-support/src/main/java/org/springframework/scheduling/
%pom_remove_dep org.codehaus.fabric3.api:commonj spring-context-support

# build against quartz compat artifact
%pom_remove_dep opensymphony:quartz spring-context-support
%pom_add_dep org.quartz-scheduler:quartz-backward-compat spring-context-support

# replace javax deps
%pom_remove_dep :el-api spring-beans
%pom_add_dep org.apache.tomcat:tomcat-el-api spring-beans

%pom_remove_dep :persistence-api spring-context
%pom_add_dep org.hibernate.javax.persistence:hibernate-jpa-2.0-api spring-context
%pom_remove_dep :validation-api spring-context
%pom_add_dep org.apache.geronimo.specs:geronimo-validation_1.0_spec spring-context

%pom_add_dep org.apache.geronimo.specs:geronimo-interceptor_3.0_spec spring-context
%pom_add_dep org.jruby.extras:bytelist spring-context

%pom_remove_dep :persistence-api spring-orm
%pom_add_dep org.hibernate.javax.persistence:hibernate-jpa-2.0-api spring-context
%pom_remove_dep javax.servlet:servlet-api spring-orm
%pom_add_dep org.apache.tomcat:tomcat-servlet-api spring-context

%pom_remove_dep :persistence-api spring-test
%pom_add_dep org.apache.tomcat:tomcat-el-api spring-test
%pom_remove_dep javax.servlet.jsp:jsp-api spring-test
%pom_add_dep org.apache.tomcat:tomcat-jsp-api spring-test

# Disable part of Derby support, require derby 10.5
# unavailable method purgeDatabase in org.apache.derby.impl.io.VFMemoryStorageFactory
rm -r spring-jdbc/src/main/java/org/springframework/jdbc/datasource/embedded/DerbyEmbeddedDatabaseConfigurer.java
sed -i "s|case DERBY:||" \
 spring-jdbc/src/main/java/org/springframework/jdbc/datasource/embedded/EmbeddedDatabaseConfigurerFactory.java
sed -i "s|return DerbyEmbeddedDatabaseConfigurer.getInstance();||" \
 spring-jdbc/src/main/java/org/springframework/jdbc/datasource/embedded/EmbeddedDatabaseConfigurerFactory.java

# ERROR: XThis is not public in Bsh
rm spring-context/src/main/java/org/springframework/scripting/bsh/BshScriptFactory.java
rm spring-context/src/main/java/org/springframework/scripting/bsh/BshScriptUtils.java

%pom_remove_dep :jopt-simple spring-core
rm -r spring-core/src/main/java/org/springframework/core/env/JOptCommandLinePropertySource.java

# Don't depend on backport-util-concurrent (upstream dropped this dep in 4.x)
%pom_remove_dep :backport-util-concurrent spring-context

# TODO: missing deps in upstream poms?
%pom_add_dep org.ow2.asm:asm spring-core
%pom_add_dep net.sf.cglib:cglib:4.2 spring-core

%pom_xpath_set "pom:dependencies/pom:dependency[pom:groupId = 'org.codehaus.groovy']/pom:artifactId" groovy spring-context

find ./ -name "*.java" -exec sed -i "s/org.springframework.asm/org.objectweb.asm/g" {} +
find ./ -name "*.java" -exec sed -i "s/org.springframework.cglib/net.sf.cglib/g" {} +
find ./ -name "*.java" -exec sed -i "/edu.emory.mathcs.backport/d" {} +

rm spring-context/src/main/java/org/springframework/scheduling/backportconcurrent/*

# copy license and notice file
cp -p src/dist/* .

%mvn_package ":spring-core" %{name}
%mvn_package :spring-project __noinstall

%build
# Build without the tests, as they bring a lot of dependecies that are not
# available in the distribution at the moment:
%mvn_build -X -f -s -- -Dproject.build.sourceEncoding=ISO-8859-1

%install
%mvn_install

%files -f .mfiles-%{name}
%dir %{_javadir}/%{name}
%doc license.txt notice.txt README.md
%files javadoc -f .mfiles-javadoc
%doc license.txt  notice.txt
%files aop -f .mfiles-spring-aop
%files beans -f .mfiles-spring-beans
%files context -f .mfiles-spring-context
%files context-support -f .mfiles-spring-context-support
%files expression -f .mfiles-spring-expression
%files instrument -f .mfiles-spring-instrument
%doc license.txt  notice.txt
%files instrument-tomcat -f .mfiles-spring-instrument-tomcat
%doc license.txt  notice.txt
%files jdbc -f .mfiles-spring-jdbc
%files jms -f .mfiles-spring-jms
%files orm -f .mfiles-spring-orm
%files oxm -f .mfiles-spring-oxm
%files struts -f .mfiles-spring-struts
%files test -f .mfiles-spring-test
%files tx -f .mfiles-spring-tx
%files web -f .mfiles-spring-web
%files webmvc -f .mfiles-spring-webmvc
%files webmvc-portlet -f .mfiles-spring-webmvc-portlet


%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 20 2014 Michal Srb <msrb@redhat.com> - 0:3.2.6-2
- Update to 3.2.6
- Fix BR

* Fri Jan 17 2014 Michal Srb <msrb@redhat.com> - 0:3.2.5-1
- Update to 3.2.5

* Fri Dec 06 2013 gil cattaneo <puntogil@libero.it> 0:3.1.4-2
- fix for rhbz: 993376, 953977
- switch to XMvn
- disable derby (partial), and jopt-simple support
- enable castor and jruby support

* Thu Dec 5 2013 Orion Poplawski <orion@cora.nwra.com> - 0:3.1.4-1
- Update to 3.1.4
- Add BR xmlunit
- Change wstx-asl to woodstox-core-asl

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:3.1.1-13
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1.1-12
- Don't depend on backport-util-concurrent

* Wed Nov 07 2012 Marek Goldmann <mgoldman@redhat.com> - 0:3.1.1-11
- Add support for new Maven compat version resolver (hibernate3)

* Thu Aug  9 2012 Andy Grimm <agrimm@gmail.com> 0:3.1.1-10
- Enable ehcache and quartz in context-support module

* Thu Aug  2 2012 Andy Grimm <agrimm@gmail.com> 0:3.1.1-9
- Fix broken Requires line in struts subpackage

* Tue Jul 31 2012 gil cattaneo <puntogil@libero.it> 0:3.1.1-8
- Enable new modules:  
- spring-context-support, spring-oxm, spring-web,
- spring-jms, spring-orm, spring-webmvc,
- spring-webmvc-portlet, spring-struts

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 9 2012 Juan Hernandez <juan.hernandez@redhat.com> 0:3.1.1-6
- Don't own the maven fragments directory (rhbz#819804)
- Add requirement on jpackage-utils

* Tue May 8 2012 Juan Hernandez <juan.hernandez@redhat.com> 0:3.1.1-5
- Move the maven fragments to the subpackages (rhbz#819804)

* Sat Apr 21 2012 Juan Hernandez <juan.hernandez@redhat.com> 0:3.1.1-3
- Own the /usr/share/java/springframework directory (rhbz#814934)
- Remove patch used to deal with missing tomcat POM files

* Thu Mar 15 2012 Juan Hernandez <juan.hernandez@redhat.com> 0:3.1.1-2
- Cleanup of the spec file

* Thu Mar 1 2012 Andy Grimm <agrimm@gmail.com> 0:3.1.1-1
- Initial build
