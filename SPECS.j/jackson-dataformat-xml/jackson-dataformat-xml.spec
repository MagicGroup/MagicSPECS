Name:          jackson-dataformat-xml
Version:       2.4.1
Release:       2%{?dist}
Summary:       XML data binding extension for Jackson
License:       ASL 2.0
URL:           http://wiki.fasterxml.com/JacksonExtensionXmlDataBinding
Source0:       https://github.com/FasterXML/jackson-dataformat-xml/archive/%{name}-%{version}.tar.gz

%if %{?fedora} > 20
BuildRequires: mvn(com.fasterxml.jackson:jackson-parent:pom:)
%else
BuildRequires: mvn(com.fasterxml.jackson:jackson-parent)
%endif
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-annotations)
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-core)
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires: mvn(com.fasterxml.jackson.module:jackson-module-jaxb-annotations)
BuildRequires: mvn(javax.xml.stream:stax-api)
BuildRequires: mvn(org.codehaus.woodstox:stax2-api)

# test deps
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.codehaus.woodstox:woodstox-core-asl)

BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-plugin-build-helper
BuildRequires: maven-site-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: replacer

BuildArch:     noarch

%description
Data format extension for Jackson (http://jackson.codehaus.org)
to offer alternative support for serializing POJOs as XML and
deserializing XML as POJOs. Support implemented on top of Stax API
(javax.xml.stream), by implementing core Jackson Streaming API types
like JsonGenerator, JsonParser and JsonFactory. Some data-binding types
overridden as well (ObjectMapper sub-classed as XmlMapper).

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

cp -p src/main/resources/META-INF/LICENSE .
cp -p src/main/resources/META-INF/NOTICE .
sed -i 's/\r//' LICENSE NOTICE

%build

# see https://github.com/FasterXML/jackson-jaxrs-providers/issues/20
%mvn_file : %{name}
%mvn_build -- -Dmaven.test.failure.ignore=true

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE README.md release-notes/*

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Fri Aug 15 2014 Liu Di <liudidi@gmail.com> - 2.4.1-2
- 为 Magic 3.0 重建

* Fri Jul 04 2014 gil cattaneo <puntogil@libero.it> 2.4.1-1
- update to 2.4.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.2-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Sep 07 2013 gil cattaneo <puntogil@libero.it> 2.2.2-3
- remove sub-package doc

* Thu Aug 15 2013 gil cattaneo <puntogil@libero.it> 2.2.2-2
- add sub-package doc

* Wed Jul 17 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- initial rpm