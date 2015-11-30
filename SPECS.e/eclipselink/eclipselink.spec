%global reltag .v20140319-9ad6abd
%global namedversion %{version}%{?reltag}

%global core org.eclipse.persistence.core
%global dbws org.eclipse.persistence.dbws
%global jpa org.eclipse.persistence.jpa
%global jpql org.eclipse.persistence.jpa.jpql
%global modelgen org.eclipse.persistence.jpa.modelgen.processor
%global moxy org.eclipse.persistence.moxy
%global sdo org.eclipse.persistence.sdo

Name:          eclipselink
Version:       2.5.2
Release:       1%{?dist}
Summary:       Eclipse Persistence Services Project
License:       EPL and BSD
Url:           http://www.eclipse.org/eclipselink/
Source0:       http://www.mirrorservice.org/sites/download.eclipse.org/eclipseMirror/rt/%{name}/releases/%{version}/%{name}-src-%{namedversion}.zip
Source1:       %{name}-2.4.2-build.properties
Source2:       %{name}-2.5.2-build.xml
# http://git.eclipse.org/c/eclipselink/eclipselink.runtime
#Source3:       http://maven.eclipse.org/nexus/content/repositories/build/org/eclipse/persistence/eclipselink/2.4.2/eclipselink-2.4.2.pom

Source3:       http://repo1.maven.org/maven2/org/eclipse/persistence/%{name}/%{version}/%{name}-%{version}.pom
Source4:       http://repo1.maven.org/maven2/org/eclipse/persistence/%{core}/%{version}/%{core}-%{version}.pom
Source5:       http://repo1.maven.org/maven2/org/eclipse/persistence/%{dbws}/%{version}/%{dbws}-%{version}.pom
Source6:       http://repo1.maven.org/maven2/org/eclipse/persistence/%{jpa}/%{version}/%{jpa}-%{version}.pom
Source7:       http://repo1.maven.org/maven2/org/eclipse/persistence/%{jpql}/%{version}/%{jpql}-%{version}.pom
Source8:       http://repo1.maven.org/maven2/org/eclipse/persistence/%{modelgen}/%{version}/%{modelgen}-%{version}.pom
Source9:       http://repo1.maven.org/maven2/org/eclipse/persistence/%{moxy}/%{version}/%{moxy}-%{version}.pom
Source10:      http://repo1.maven.org/maven2/org/eclipse/persistence/%{sdo}/%{version}/%{sdo}-%{version}.pom

# thanks to Andrew Ross ubuntu[at]rossfamily.co.uk
# build fix for openjdk https://bugs.eclipse.org/bugs/show_bug.cgi?id=413186
Patch0:        %{name}-2.5.2-openjdk.patch
# use system libraries asm3 and antlr3
Patch1:        %{name}-2.5.2-use-system-libraries.patch

BuildRequires: ant
#BuildRequires: ant-antlr3
BuildRequires: antlr3-java
BuildRequires: antlr3-tool
BuildRequires: aqute-bnd
BuildRequires: cdi-api
BuildRequires: eclipse-equinox-osgi
BuildRequires: eclipselink-persistence-api
BuildRequires: geronimo-jms
BuildRequires: geronimo-validation
BuildRequires: glassfish-jaxb-api
BuildRequires: glassfish-jaxb-codemodel
BuildRequires: glassfish-jaxb-core
BuildRequires: glassfish-jaxb-jxc
BuildRequires: glassfish-servlet-api
BuildRequires: java-devel
BuildRequires: java-javadoc
BuildRequires: javamail
BuildRequires: javapackages-local
BuildRequires: jboss-connector-1.7-api
BuildRequires: jboss-transaction-1.2-api
BuildRequires: jsr-311
BuildRequires: objectweb-asm3
BuildRequires: stringtemplate4
BuildRequires: tuscany-sdo-java
BuildRequires: wsdl4j

BuildArch:     noarch

%description
Eclipse Persistence Services Project, more commonly known as EclipseLink,
is a Java comprehensive persistence framework delivering a set of persistence
services based around standards. This lets you rapidly build applications
that combine the best aspects of object technology and the specific data
source.

EclipseLink was started by a donation of the full source code and
test suites of Oracle's TopLink product.

EclipseLink's services currently include object-relational with JPA,
object-XML binding in MOXy (with support for JAXB), a Service Data Objects
(SDO) implementation and support for another technologies like: Database Web
Services (DWS), XML-Relational (XRM) and Non-Relational (EIS via JCA).

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -c

%patch0 -p1
%patch1 -p1
rm -rf org/eclipse/persistence/internal/libraries/*
# temporary fix for antlr 3.5.2
sed -i "s|Token.EOF_TOKEN|Token.EOF|" \
 org/eclipse/persistence/internal/jpa/parsing/jpql/JPQLParser.java


%if 0
sed -i "s|org.eclipse.persistence.internal.libraries.antlr|org.antlr|" \
 org/eclipse/persistence/internal/jpa/parsing/jpql/CaseInsensitiveANTLRStringStream.java \
 org/eclipse/persistence/internal/jpa/parsing/jpql/CaseInsensitiveJPQLLexer.java \
 org/eclipse/persistence/internal/jpa/parsing/jpql/InvalidIdentifierException.java \
 org/eclipse/persistence/internal/jpa/parsing/jpql/InvalidIdentifierStartException.java \
 org/eclipse/persistence/internal/jpa/parsing/jpql/JPQLParser.java \
 org/eclipse/persistence/internal/jpa/parsing/jpql/antlr/JPQLLexer.java \
 org/eclipse/persistence/internal/jpa/parsing/jpql/antlr/JPQLParser.java \
 org/eclipse/persistence/internal/jpa/parsing/jpql/antlr/JPQLParserBuilder.java \
 org/eclipse/persistence/internal/oxm/record/json/JSONLexer.java \
 org/eclipse/persistence/internal/oxm/record/json/JSONParser.java \
 org/eclipse/persistence/internal/oxm/record/json/JSONReader.java

sed -i "s|org.eclipse.persistence.internal.libraries.asm|org.objectweb.asm|" \
 org/eclipse/persistence/dynamic/DynamicClassWriter.java \
 org/eclipse/persistence/internal/dbws/SOAPResponseClassLoader.java \
 org/eclipse/persistence/internal/jpa/metadata/MetadataDynamicClassWriter.java \
 org/eclipse/persistence/internal/jpa/metadata/accessors/objects/MetadataAsmFactory.java \
 org/eclipse/persistence/internal/jpa/metadata/accessors/objects/MetadataClass.java \
 org/eclipse/persistence/internal/jpa/weaving/AttributeDetails.java \
 org/eclipse/persistence/internal/jpa/weaving/ClassWeaver.java \
 org/eclipse/persistence/internal/jpa/weaving/ComputeClassWriter.java \
 org/eclipse/persistence/internal/jpa/weaving/MethodWeaver.java \
 org/eclipse/persistence/internal/jpa/weaving/PersistenceWeaver.java \
 org/eclipse/persistence/internal/jpa/weaving/RestAdapterClassWriter.java \
 org/eclipse/persistence/internal/jpa/weaving/TransformerFactory.java \
 org/eclipse/persistence/internal/xr/XRClassWriter.java \
 org/eclipse/persistence/jaxb/compiler/AnnotationsProcessor.java \
 org/eclipse/persistence/jaxb/compiler/MappingsGenerator.java \
 org/eclipse/persistence/sdo/helper/DynamicClassWriter.java \
%endif

cp -p %{SOURCE1} build.properties
cp -p %{SOURCE2} build.xml

cp -p %{SOURCE3} pom.xml
%pom_change_dep org.eclipse.persistence:commonj.sdo org.apache.tuscany.sdo:tuscany-sdo-api-r2.1:1.1.1

cp -p %{SOURCE4} core-pom.xml
%pom_change_dep org.eclipse.persistence:org.eclipse.persistence.asm asm:asm:3.3.1 core-pom.xml
%pom_add_dep asm:asm-commons:3.3.1:compile core-pom.xml
%pom_add_dep asm:asm-tree:3.3.1:compile core-pom.xml
%pom_add_dep asm:asm-tree:3.3.1:compile core-pom.xml
%pom_add_dep asm:asm-util:3.3.1:compile core-pom.xml
%pom_add_dep asm:asm-xml:3.3.1:compile core-pom.xml

cp -p %{SOURCE6} jpa-pom.xml
%pom_change_dep org.eclipse.persistence:org.eclipse.persistence.antlr org.antlr:antlr-runtime:3.5.2 jpa-pom.xml
#%% pom_add_dep org.antlr:antlr:3.5.2:compile jpa-pom.xml
%pom_change_dep org.eclipse.persistence:org.eclipse.persistence.asm asm:asm:3.3.1 jpa-pom.xml
%pom_add_dep asm:asm:3.3.1:compile jpa-pom.xml
%pom_add_dep asm:asm-commons:3.3.1:compile jpa-pom.xml
%pom_add_dep asm:asm-tree:3.3.1:compile jpa-pom.xml
%pom_add_dep asm:asm-tree:3.3.1:compile jpa-pom.xml
%pom_add_dep asm:asm-util:3.3.1:compile jpa-pom.xml
%pom_add_dep asm:asm-xml:3.3.1:compile jpa-pom.xml

cp -p %{SOURCE9} moxy-pom.xml
%pom_change_dep org.eclipse.persistence:org.eclipse.persistence.antlr org.antlr:antlr-runtime:3.5.2 moxy-pom.xml
#%% pom_add_dep org.antlr:antlr:3.5.2:compile moxy-pom.xml

cp -p %{SOURCE10} sdo-pom.xml
%pom_change_dep org.eclipse.persistence:commonj.sdo org.apache.tuscany.sdo:tuscany-sdo-api-r2.1:1.1.1 sdo-pom.xml

# fix non ASCII chars
for s in org/eclipse/persistence/internal/jpa/transaction/JTATransactionWrapper.java \
  org/eclipse/persistence/jpa/jpql/parser/AbstractExpression.java \
  org/eclipse/persistence/jpa/jpql/tools/DefaultGrammarValidator.java \
  org/eclipse/persistence/jpa/jpql/tools/model/IScalarExpressionStateObjectBuilder.java \
  org/eclipse/persistence/platform/database/HANAPlatform.java \
  org/eclipse/persistence/platform/database/MaxDBPlatform.java;do
  native2ascii -encoding UTF8 ${s} ${s}
done

%build

(
 cd org/eclipse/persistence/internal/oxm/record/json/
 antlr3 JSON.g
)

(
 cd org/eclipse/persistence/internal/jpa/parsing/jpql/antlr/
# error: variable node is already defined in method subselectIdentificationVariableDeclaration(List)
 sed -i '/Object node = null;/d' JPQL.g
 antlr3 JPQL.g
)

ant

%install
%mvn_artifact pom.xml target/%{name}.jar
%mvn_artifact core-pom.xml target/%{core}-%{version}.jar
%mvn_artifact %{SOURCE5} target/%{dbws}-%{version}.jar
%mvn_artifact jpa-pom.xml target/%{jpa}-%{version}.jar
%mvn_artifact %{SOURCE7} target/%{jpql}-%{version}.jar
%mvn_artifact %{SOURCE8} target/%{modelgen}-%{version}.jar
%mvn_artifact moxy-pom.xml target/%{moxy}-%{version}.jar
%mvn_artifact sdo-pom.xml target/%{sdo}-%{version}.jar
%mvn_install -J target/api

%files -f .mfiles
%doc about.html readme.html
%license license.html

%files javadoc -f .mfiles-javadoc
%license license.html

%changelog
* Sat Oct 31 2015 gil cattaneo <puntogil@libero.it> 2.5.2-1
- update to 2.5.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 gil cattaneo <puntogil@libero.it> 2.4.2-9
- use tomcat-servlet-3.1-api

* Mon Feb 02 2015 gil cattaneo <puntogil@libero.it> 2.4.2-8
- add antlr 3.5.2 support

* Sun Feb 01 2015 gil cattaneo <puntogil@libero.it> 2.4.2-7
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.4.2-5
- Use Requires: java-headless rebuild (#1067528)

* Mon Jan 20 2014 Michal Srb <msrb@redhat.com> - 2.4.2-4
- Provide org.eclipse.persistence:org.eclipse.persistence.jpa

* Fri Dec 06 2013 gil cattaneo <puntogil@libero.it> 2.4.2-3
- use objectweb-asm3

* Sat Sep 28 2013 gil cattaneo <puntogil@libero.it> 2.4.2-2
- fix some problems with missing explicit casts

* Tue Jul 16 2013 gil cattaneo <puntogil@libero.it> 2.4.2-1
- update to 2.4.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Apr 03 2012 gil cattaneo <puntogil@libero.it> 2.3.2-1
- initial rpm
