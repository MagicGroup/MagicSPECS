Name:          jackson-databind
Version:       2.4.1.3
Release:       3%{?dist}
Summary:       General data-binding package for Jackson (2.x)
License:       ASL 2.0 and LGPLv2+
URL:           http://wiki.fasterxml.com/JacksonHome
Source0:       https://github.com/FasterXML/jackson-databind/archive/%{name}-%{version}.tar.gz
%if %{?fedora} > 20
BuildRequires: mvn(com.fasterxml.jackson:jackson-parent:pom:)
%else
BuildRequires: mvn(com.fasterxml.jackson:jackson-parent)
%endif
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-annotations) >= 2.4.1
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-core) >= 2.4.1
# test deps
BuildRequires: mvn(cglib:cglib)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.codehaus.groovy:groovy)

BuildRequires: maven-local
BuildRequires: replacer
# bundle-plugin Requires
#BuildRequires: mvn(org.sonatype.aether:aether)

Provides:      jackson2-databind = %{version}-%{release}
Obsoletes:     jackson2-databind < %{version}-%{release}

BuildArch:     noarch

%description
General data-binding functionality for Jackson:
works on core streaming API.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

cp -p src/main/resources/META-INF/LICENSE .
cp -p src/main/resources/META-INF/NOTICE .
sed -i 's/\r//' LICENSE NOTICE

# unavailable test deps
%pom_remove_dep org.hibernate:hibernate-cglib-repack
rm src/test/java/com/fasterxml/jackson/databind/interop/TestHibernate.java
# Off test that require connection with the web
rm src/test/java/com/fasterxml/jackson/databind/ser/TestJdkTypes.java \
 src/test/java/com/fasterxml/jackson/databind/deser/TestJdkTypes.java \
 src/test/java/com/fasterxml/jackson/databind/TestJDKSerialization.java

%build

%mvn_file : %{name}
%mvn_build -- -Dmaven.test.failure.ignore=true

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE README.md release-notes/*

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.4.1.3-3
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 2.4.1.3-2
- 为 Magic 3.0 重建

* Wed Jul 23 2014 gil cattaneo <puntogil@libero.it> 2.4.1.3-1
- update to 2.4.1.3

* Thu Jul 03 2014 gil cattaneo <puntogil@libero.it> 2.4.1.1-1
- update to 2.4.1.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.2-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 gil cattaneo <puntogil@libero.it> 2.2.2-2
- review fixes

* Tue Jul 16 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- 2.2.2
- renamed jackson-databind

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 2.2.1-1
- 2.2.1

* Wed Oct 24 2012 gil cattaneo <puntogil@libero.it> 2.1.0-1
- update to 2.1.0
- renamed jackson2-databind

* Thu Sep 13 2012 gil cattaneo <puntogil@libero.it> 2.0.6-1
- initial rpm
