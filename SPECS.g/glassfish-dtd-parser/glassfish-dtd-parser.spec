Name:          glassfish-dtd-parser
Version:       1.2
Release:       0.11.20120120svn%{?dist}
Summary:       Library for parsing XML DTDs
License:       CDDL 1.1 and GPLv2 with exceptions
Url:           http://java.net/projects/dtd-parser
# svn export https://svn.java.net/svn/dtd-parser~svn/trunk/dtd-parser glassfish-dtd-parser-1.2-SNAPSHOT
# find glassfish-dtd-parser-1.2-SNAPSHOT/ -name '*.jar' -delete
# tar czf glassfish-dtd-parser-1.2-SNAPSHOT-src-svn.tar.gz glassfish-dtd-parser-1.2-SNAPSHOT
Source0:       %{name}-%{version}-SNAPSHOT-src-svn.tar.gz
BuildRequires: java-devel
BuildRequires: bsf
BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: sonatype-oss-parent

BuildArch:     noarch

%description
Library for parsing XML DTDs.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}-SNAPSHOT

%build

%mvn_file :dtd-parser %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 1.2-0.11.20120120svn
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.10.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.2-0.9.20120120svn
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 1.2-0.8.20120120svn
- rebuilt rhbz#992383
- swith to Xmvn
- adapt to new guideline

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.7.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.6.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2-0.5.20120120svn
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.4.20120120svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.2-0.3.20120120svn
- Fixed the release number

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.2-0.2.20120120svn
- Updated license reference

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.2-0.1.20120120svn
- Initial packaging
