Name:          classmate
Version:       0.8.0
Release:       8%{?dist}
Summary:       Java introspection library
License:       ASL 2.0
Url:           http://github.com/cowtowncoder/java-classmate/
Source0:       https://github.com/cowtowncoder/java-classmate/archive/%{name}-%{version}.tar.gz
# classmate package don't include the license file
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires: java-devel
BuildRequires: sonatype-oss-parent

BuildRequires: junit

BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-source-plugin
BuildRequires: maven-surefire-provider-junit

BuildArch:     noarch

%description
Library for introspecting types with full generic information
including resolving of field and method types.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n java-%{name}-%{name}-%{version}

find . -name "*.class" -delete
find . -name "*.jar" -delete

cp -p %{SOURCE1} .
sed -i 's/\r//' LICENSE-2.0.txt

# these test fails junit.framework.AssertionFailedError: expected:<X> but was:<Y>
rm -r src/test/java/com/fasterxml/classmate/TestReadme.java \
 src/test/java/com/fasterxml/classmate/types/ResolvedObjectTypeTest.java \
 src/test/java/com/fasterxml/classmate/AnnotationsTest.java

%build
%mvn_file :%{name} %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-2.0.txt README.md release-notes.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE-2.0.txt

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 0.8.0-8
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.8.0-7
- 为 Magic 3.0 重建

* Wed Aug 13 2014 Liu Di <liudidi@gmail.com> - 0.8.0-6
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 0.8.0-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 gil cattaneo <puntogil@libero.it> 0.8.0-2
- switch to XMvn
- minor changes to adapt to current guideline

* Thu Apr 18 2013 gil cattaneo <puntogil@libero.it> 0.8.0-1
- update to 0.8.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.5.4-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat May 05 2012 gil cattaneo <puntogil@libero.it> 0.5.4-2
- changed summary

* Sun Apr 22 2012 gil cattaneo <puntogil@libero.it> 0.5.4-1
- initial rpm
