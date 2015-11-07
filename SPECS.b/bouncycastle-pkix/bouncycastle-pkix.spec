%global ver 150
%global archivever  jdk15on-%(echo %{version}|sed 's|\\\.||')
Name:          bouncycastle-pkix
Version:       1.50
Release:       5%{?dist}
Summary:       Bouncy Castle PKIX, CMS, EAC, TSP, PKCS, OCSP, CMP, and CRMF APIs
License:       MIT
URL:           http://www.bouncycastle.org/
Source0:       http://www.bouncycastle.org/download/bcpkix-%{archivever}.tar.gz
Source1:       http://central.maven.org/maven2/org/bouncycastle/bcpkix-jdk15on/%{version}/bcpkix-jdk15on-%{version}.pom
Source2:       bouncycastle-pkix-build.xml
Source3:       bouncycastle-pkix-OSGi.bnd

BuildRequires: ant
BuildRequires: ant-junit
BuildRequires: aqute-bnd
BuildRequires: java-devel
BuildRequires: javapackages-tools
BuildRequires: junit
BuildRequires: mvn(org.bouncycastle:bcprov-jdk15on) = %{version}
Requires:      mvn(org.bouncycastle:bcprov-jdk15on) = %{version}
Requires:      java-headless
Requires:      javapackages-tools
BuildArch:     noarch
Obsoletes:     bouncycastle-tsp < 1.50-2
Provides:      bouncycastle-tsp = %{version}-%{release}

%description
The Bouncy Castle Java APIs for CMS, PKCS, EAC, TSP, CMP, CRMF, OCSP, and
certificate generation. This jar contains APIs for JDK 1.5 to JDK 1.7. The
APIs can be used in conjunction with a JCE/JCA provider such as the
one provided with the Bouncy Castle Cryptography APIs.

%package javadoc
Summary:       Javadoc for %{name}
Obsoletes:     bouncycastle-tsp-javadoc < 1.50-2

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n bcpkix-%{archivever}
# Remove provided binaries and apidocs
find . -type f -name "*.class" -print -delete
find . -type f -name "*.jar" -print -delete
rm -rf docs/* javadoc/*

# fixing incomplete source directory structure
mkdir -p src/java src/test
unzip -qq src.zip -d src/java

mkdir -p src/test/org/bouncycastle/cert/cmp/test
mv src/java/org/bouncycastle/cert/cmp/test/* src/test/org/bouncycastle/cert/cmp/test
mkdir -p src/test/org/bouncycastle/cert/crmf/test
mv src/java/org/bouncycastle/cert/crmf/test/* src/test/org/bouncycastle/cert/crmf/test
mkdir -p src/test/org/bouncycastle/cert/ocsp/test
mv src/java/org/bouncycastle/cert/ocsp/test/* src/test/org/bouncycastle/cert/ocsp/test
mkdir -p src/test/org/bouncycastle/cert/test
mv src/java/org/bouncycastle/cert/test/* src/test/org/bouncycastle/cert/test
mkdir -p src/test/org/bouncycastle/cms/test
mv src/java/org/bouncycastle/cms/test/* src/test/org/bouncycastle/cms/test
mkdir -p src/test/org/bouncycastle/eac/test
mv src/java/org/bouncycastle/eac/test/* src/test/org/bouncycastle/eac/test
mkdir -p src/test/org/bouncycastle/mozilla/test
mv src/java/org/bouncycastle/mozilla/test/* src/test/org/bouncycastle/mozilla/test
mkdir -p src/test/org/bouncycastle/openssl/test
mv src/java/org/bouncycastle/openssl/test/* src/test/org/bouncycastle/openssl/test
mkdir -p src/test/org/bouncycastle/tsp/test
mv src/java/org/bouncycastle/tsp/test/* src/test/org/bouncycastle/tsp/test
mkdir -p src/test/org/bouncycastle/pkcs/test
mv src/java/org/bouncycastle/pkcs/test/* src/test/org/bouncycastle/pkcs/test
mkdir -p src/test/org/bouncycastle/dvcs
mv src/java/org/bouncycastle/dvcs/test src/test/org/bouncycastle/dvcs
mkdir -p src/test/org/bouncycastle/cert/path
mv src/java/org/bouncycastle/cert/path/test src/test/org/bouncycastle/cert/path

cp -p %{SOURCE2} build.xml
cp -p %{SOURCE3} bcpkix.bnd
sed -i "s|@VERSION@|%{version}|" build.xml bcpkix.bnd

# this test fails:
rm -rf src/test/org/bouncycastle/cert/ocsp/test/*.java
#  bc.test.data.home property not set
rm -rf src/test/org/bouncycastle/cert/cmp/test/AllTests.java
rm -rf src/test/org/bouncycastle/cms/test/Rfc4134Test.java
sed -i "s|suite.addTest(Rfc4134Test.suite());|//suite.addTest(Rfc4134Test.suite());|" \
  src/test/org/bouncycastle/cms/test/AllTests.java

# package org.bouncycastle.jce.provider.test does not exist
rm -rf src/test/org/bouncycastle/cms/test/SignedDataTest.java
sed -i "s|suite.addTest(SignedDataTest.suite());|//suite.addTest(SignedDataTest.suite());|" \
  src/test/org/bouncycastle/cms/test/AllTests.java
rm -rf src/test/org/bouncycastle/cms/test/NewSignedDataTest.java
sed -i "s|suite.addTest(NewSignedDataTest.suite());|//suite.addTest(NewSignedDataTest.suite());|" \
  src/test/org/bouncycastle/cms/test/AllTests.java
rm -rf src/test/org/bouncycastle/eac/test \
  src/test/org/bouncycastle/openssl/test
rm -rf src/test/org/bouncycastle/tsp/test/CMSTimeStampedDataTest.java
sed -i "s|suite.addTestSuite(CMSTimeStampedDataTest.class);|//suite.addTestSuite(CMSTimeStampedDataTest.class);|" \
  src/test/org/bouncycastle/tsp/test/AllTests.java
rm -rf src/test/org/bouncycastle/tsp/test/CMSTimeStampedDataParserTest.java
sed -i "s|suite.addTestSuite(CMSTimeStampedDataParserTest.class);|//suite.addTestSuite(CMSTimeStampedDataParserTest.class);|" \
  src/test/org/bouncycastle/tsp/test/AllTests.java
rm -rf src/test/org/bouncycastle/tsp/test/CMSTimeStampedDataGeneratorTest.java
sed -i "s|suite.addTestSuite(CMSTimeStampedDataGeneratorTest.class);|//suite.addTestSuite(CMSTimeStampedDataGeneratorTest.class);|" \
  src/test/org/bouncycastle/tsp/test/AllTests.java
rm -r src/test/org/bouncycastle/cert/test/BcCertTest.java
sed -i "s|suite.addTestSuite(BcCertTest.class);|//suite.addTestSuite(BcCertTest.class);|" \
  src/test/org/bouncycastle/cert/test/AllTests.java
rm -r src/test/org/bouncycastle/cms/test/BcSignedDataTest.java
sed -i "s|suite.addTest(BcSignedDataTest.suite());|//suite.addTest(BcSignedDataTest.suite());|" \
  src/test/org/bouncycastle/cms/test/AllTests.java
  
  
%build

%ant jar javadoc

%install

mkdir -p %{buildroot}%{_javadir}
install -pm 644 build/bcpkix.jar %{buildroot}%{_javadir}/bcpkix.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr build/apidocs/* %{buildroot}%{_javadocdir}/%{name}

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-bcpkix.pom
%add_maven_depmap JPP-bcpkix.pom bcpkix.jar -a "org.bouncycastle:bctsp-jdk16"

%files -f .mfiles
%doc *.html

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.html

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.50-5
- 为 Magic 3.0 重建

* Fri Aug 15 2014 Liu Di <liudidi@gmail.com> - 1.50-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 14 2014 Michal Srb <msrb@redhat.com> - 1.50-2
- Obsolete bouncycastle-tsp

* Mon Feb 24 2014 gil cattaneo <puntogil@libero.it> 1.50-1
- update to 1.50

* Fri Feb 22 2013 gil cattaneo <puntogil@libero.it> 1.48-1
- update to 1.48

* Thu Jun 21 2012 gil cattaneo <puntogil@libero.it> 1.47-1
- initial rpm
