%global tag a594629

Name:           sonatype-plugins-parent
Version:        8
Release:        6%{?dist}
Summary:        Sonatype Plugins Parent POM
BuildArch:      noarch
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/sonatype/oss-parents
Source:         https://github.com/sonatype/oss-parents/tarball/plugins-parent-%{version}#/%{name}-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires:  maven-local
BuildRequires:  forge-parent

%description
This package provides Sonatype plugins parent POM used by other Sonatype
packages.

%prep
%setup -q -n sonatype-oss-parents-%{tag}
cp -p %{SOURCE1} LICENSE

%build
cd ./plugins-parent
%mvn_build

%install
cd ./plugins-parent
%mvn_install

%files -f plugins-parent/.mfiles
%doc LICENSE

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 8-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 8-3
- Build with xmvn

* Wed Dec 12 2012 Michal Srb <msrb@redhat.com> - 8-2
- Added license (Resolves: #884637)

* Wed Aug  8 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8-1
- Initial packaging
