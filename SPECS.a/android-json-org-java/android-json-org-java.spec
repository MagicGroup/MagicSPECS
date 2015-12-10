%global namedreltag _r3.1
%global namedversion %{version}%{?namedreltag}
%global oname json
Name:          android-json-org-java
Version:       4.3
Release:       0.6.r3.1%{?dist}
Summary:       Androids rewrite of the evil licensed Json.org
License:       ASL 2.0
URL:           https://android.googlesource.com/platform/libcore/+/master/json
# git clone https://android.googlesource.com/platform/libcore/ android-json-org-java
# (cd android-json-org-java/json/ && git archive --format=tar --prefix=android-json-org-java-4.3_r3.1/ android-4.3_r3.1 | xz > ../../android-json-org-java-4.3_r3.1-src-git.tar.xz)
Source0:       %{name}-%{namedversion}-src-git.tar.xz
Source1:       %{name}-template.pom
# android-json-org-java package don't include the license file
Source2:       http://www.apache.org/licenses/LICENSE-2.0.txt

Patch0:        %{name}-20130122-ignore_failing_junit_test.patch

BuildRequires: java-devel
BuildRequires: geronimo-parent-poms

BuildRequires: maven-local
BuildRequires: maven-surefire-provider-junit

BuildArch:     noarch

%description
Json.org is a popular java library to parse and
create json string from the author of the json
standard Douglas Crockford. His implementation
however is not free software.
Therefor the Android team did a clean-room
re-implementation of a json library to
be used in-place of the original one.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}
%patch0 -p0
cp -p %{SOURCE1} pom.xml
sed -i "s|<version>@version@|<version>%{namedversion}|" pom.xml
cp -p %{SOURCE2} .
sed -i 's/\r//' LICENSE-2.0.txt

# empty file
rm -rf MODULE_LICENSE_BSD_LIKE

%build

%mvn_file :%{oname} %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE-2.0.txt

%changelog
* Thu Nov 19 2015 Liu Di <liudidi@gmail.com> - 4.3-0.6.r3.1
- 为 Magic 3.0 重建

* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 4.3-0.5.r3.1
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 4.3-0.4.r3.1
- 为 Magic 3.0 重建

* Wed Aug 13 2014 Liu Di <liudidi@gmail.com> - 4.3-0.3.r3.1
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-0.2.r3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 28 2013 gil cattaneo <puntogil@libero.it> 4.3-0.1.r3.1
- update to 4.3_r3.1

* Mon Sep 16 2013 gil cattaneo <puntogil@libero.it> 4.2.2-0.2.r1.2
- fix license tag

* Mon Jan 14 2013 gil cattaneo <puntogil@libero.it> 4.2.2-0.1.r1.2
- initial rpm