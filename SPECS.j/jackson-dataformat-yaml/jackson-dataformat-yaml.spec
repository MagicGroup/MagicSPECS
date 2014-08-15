Name:          jackson-dataformat-yaml
Version:       2.4.1
Release:       1%{?dist}
Summary:       Jackson module to add YAML back-end (parser/generator adapters)
License:       ASL 2.0
URL:           http://wiki.fasterxml.com/JacksonExtensionYAML
Source0:       https://github.com/FasterXML/jackson-dataformat-yaml/archive/%{name}-%{version}.tar.gz
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-core)
%if %{?fedora} > 20
BuildRequires: mvn(com.fasterxml.jackson:jackson-parent:pom:)
%else
BuildRequires: mvn(com.fasterxml.jackson:jackson-parent)
%endif
BuildRequires: mvn(org.yaml:snakeyaml)
# Test deps
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-annotations)
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires: mvn(junit:junit)

BuildRequires: maven-local
BuildRequires: mvn(com.google.code.maven-replacer-plugin:replacer)
BuildArch:     noarch

%description
Support for reading and writing YAML-encoded data via Jackson
abstractions.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

cp -p %{SOURCE1} .
cp -p src/main/resources/META-INF/{LICENSE,NOTICE} .
sed -i 's/\r//' LICENSE NOTICE LICENSE-2.0.txt

%pom_remove_plugin :maven-shade-plugin

%build

%mvn_file : %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE LICENSE-2.0.txt NOTICE README.md release-notes/*

%files javadoc -f .mfiles-javadoc
%doc LICENSE LICENSE-2.0.txt NOTICE

%changelog
* Fri Jul 04 2014 gil cattaneo <puntogil@libero.it> 2.4.1-1
- update to 2.4.1

* Mon Nov 25 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- initial rpm