Name:           joda-convert
Version:        1.7
Release:        2%{?dist}
Summary:        Java library for conversion to and from standard string formats
License:        ASL 2.0 
URL:            https://github.com/JodaOrg/joda-convert/
BuildArch:      noarch

Source0:        https://github.com/JodaOrg/joda-convert/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-checkstyle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)

%description
Java library to enable conversion to and from standard string formats.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package contains the %{summary}.

%prep
%setup -q
%mvn_file : %{name}
sed -i s/// *.txt

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Tue Aug 12 2014 Liu Di <liudidi@gmail.com> - 1.7-2
- 为 Magic 3.0 重建

* Tue Aug  5 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-1
- Update to upstream version 1.7

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-1
- Update to upstream version 1.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 14 2013 Mat Booth <fedora@matbooth.co.uk> - 1.3.1-1
- Update to latest upstream, fixes rhbz #919539
- Use XMvn macros

* Tue May 28 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.3-2
- Install NOTICE file with javadoc as well
- Use full URL for Source0

* Fri Feb 22 2013 Andy Grimm <agrimm@gmail.com> - 1.3-1
- Update to 1.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Andy Grimm <agrimm@gmail.com> - 1.2-1
- update to 1.2 and pull source tarball correctly

* Tue Oct 18 2011 Andy Grimm <agrimm@gmail.com> - 1.1-1
- Initial package
