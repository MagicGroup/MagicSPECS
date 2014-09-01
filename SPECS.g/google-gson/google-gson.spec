
%global short_name   gson
%global group_id     com.google.code.gson

Name:             google-%{short_name}
Version:          2.2.4
Release:          7%{?dist}
Summary:          Java lib for conversion of Java objects into JSON representation
License:          ASL 2.0
Group:            Development/Libraries
URL:              http://code.google.com/p/%{name}
# request for tarball: http://code.google.com/p/google-gson/issues/detail?id=283
# svn export http://google-gson.googlecode.com/svn/tags/gson-%{version} google-gson-%{version}
# tar caf google-gson-%{version}.tar.xz google-gson-%{version}
Source0:          %{name}-%{version}.tar.xz

BuildArch:        noarch

BuildRequires:    java-devel
BuildRequires:    jpackage-utils
BuildRequires:    maven-local
BuildRequires:    maven-surefire-provider-junit
BuildRequires:    maven-plugin-cobertura
BuildRequires:    maven-enforcer-plugin
BuildRequires:    maven-install-plugin

Requires:         jpackage-utils

%description
Gson is a Java library that can be used to convert a Java object into its
JSON representation. It can also be used to convert a JSON string into an
equivalent Java object. Gson can work with arbitrary Java objects including
pre-existing objects that you do not have source-code of.

%package javadoc
Summary:          API documentation for %{name}
Group:            Documentation
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

# convert CR+LF to LF
sed -i 's/\r//g' LICENSE

%build
# LANG="C" or LANG="en_US.utf8" needed for the tests
%mvn_build -- -Dmaven.test.failure.ignore=true

%install
%mvn_install

%files -f .mfiles
%doc LICENSE README

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Fri Aug 15 2014 Liu Di <liudidi@gmail.com> - 2.2.4-7
- 为 Magic 3.0 重建

* Tue Jun 10 2014 Severin Gehwolf <sgehwolf@redhat.com> - 2.2.4-6
- Move to xmvn style packaging.
- Fix FTBFS. Resolves RHBZ#1106707.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.4-4
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 05 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.2.4-3
- Add BR maven-install-plugin, resolves RHBZ#992422.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Alexander Kurtakov <akurtako@redhat.com> 2.2.4-1
- Update to newer upstream release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.2-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Dec 19 2012 Severin Gehwolf <sgehwolf@redhat.com> 2.2.2-2
- Add BR for surefire junit provider.

* Wed Dec 19 2012 Severin Gehwolf <sgehwolf@redhat.com> 2.2.2-1
- Update to latest upstream release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 2 2012 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-2
- Add missing BR on maven-enforcer-plugin.
- Remove no longer needed parts of the spec.

* Mon Jul 2 2012 Krzysztof Daniel <kdaniel@redhat.com> 2.2.1-1
- Update to latest upstream 2.2.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 13 2011 Jaromir Capik <jcapik@redhat.com> - 1.7.1-3
- Removal of failing testInetAddressSerializationAndDeserialization

* Wed May 11 2011 Jaromir Capik <jcapik@redhat.com> - 1.7.1-2
- Conversion of CR+LF to LF in the license file

* Tue May 10 2011 Jaromir Capik <jcapik@redhat.com> - 1.7.1-1
- Initial version of the package
