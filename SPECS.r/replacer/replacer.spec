Name:          replacer
Version:       1.5.3
Release:       4%{?dist}
Summary:       Replacer Maven Mojo
License:       MIT
URL:           http://code.google.com/p/maven-replacer-plugin/
# svn export http://maven-replacer-plugin.googlecode.com/svn/tags/replacer-1.5.3/trunk/ replacer-1.5.3
# tar cJf replacer-1.5.3.tar.xz replacer-1.5.3
Source0:       %{name}-%{version}.tar.xz
BuildRequires: mvn(commons-io:commons-io)
BuildRequires: mvn(commons-lang:commons-lang)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(org.apache.maven:maven-plugin-api)
%if %{?fedora} > 20
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)
%else
BuildRequires: mvn(org.sonatype.oss:oss-parent)
%endif
BuildRequires: mvn(xerces:xercesImpl)

# test deps
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.hamcrest:hamcrest-all)
BuildRequires: mvn(org.mockito:mockito-all)
BuildRequires: mvn(xml-apis:xml-apis)

BuildRequires: maven-local
BuildRequires: maven-plugin-plugin

BuildArch:     noarch

%description
Maven plugin to replace tokens in a given file with a value.

This plugin is also used to automatically generating PackageVersion.java
in the FasterXML.com project.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

%pom_remove_plugin :dashboard-maven-plugin
# NoClassDefFoundError: org/w3c/dom/ElementTraversal
%pom_add_dep xml-apis:xml-apis::test

sed -i.hamcrest '/startsWith/d' src/test/java/com/google/code/maven_replacer_plugin/file/FileUtilsTest.java
sed -i 's/\r//' LICENSE.txt

%mvn_file :%{name} %{name}
%mvn_alias :%{name} com.google.code.maven-replacer-plugin:maven-replacer-plugin

%build

%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.5.3-4
- 为 Magic 3.0 重建

* Sat Sep 12 2015 Liu Di <liudidi@gmail.com> - 1.5.3-3
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 1.5.3-2
- 为 Magic 3.0 重建

* Thu Jul 03 2014 gil cattaneo <puntogil@libero.it> 1.5.3-1
- update to 1.5.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.5.2-4
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 03 2013 gil cattaneo <puntogil@libero.it> 1.5.2-2
- switch to XMvn
- minor changes to adapt to current guideline

* Sun May 26 2013 gil cattaneo <puntogil@libero.it> 1.5.2-1
- initial rpm
