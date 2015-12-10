%global artifactId plexus-component-factories

Name:		plexus-component-factories-pom
Version:	1.0
Release:	0.11.alpha11%{?dist}
Summary:	Plexus Component Factories POM
BuildArch:	noarch
Group:		Development/Libraries
License:	ASL 2.0
URL:		https://github.com/codehaus-plexus/plexus-component-factories
Source0:	http://repo1.maven.org/maven2/org/codehaus/plexus/%{artifactId}/%{version}-alpha-11/%{artifactId}-%{version}-alpha-11.pom
Source1:	http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires:	maven-local


%description
This package provides Plexus Component Factories parent POM used by different
Plexus packages.

%prep
%setup -cT
cp -p %{SOURCE0} pom.xml
cp -p %{SOURCE1} LICENSE

%pom_xpath_remove pom:modules

%build
%mvn_alias : plexus:
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE

%changelog
* Fri Nov 27 2015 Liu Di <liudidi@gmail.com> - 1.0-0.11.alpha11
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.10.alpha11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.9.alpha11
- Update upstream URL

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.8.alpha11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.7.alpha11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.6.alpha11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-0.5.alpha11
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.4.alpha11
- Build with xmvn

* Thu Dec 13 2012 Michal Srb <msrb@redhat.com> - 1.0-0.3.alpha11
- Fixed artifactId

* Tue Dec 11 2012 Michal Srb <msrb@redhat.com> - 1.0-0.2.alpha11
- Use direct link in Source0
- Improved prep/setup section
- mvn-rpmbuild verify is now in check section
- More specific files section
- add_maven_depmap macro now with -a option

* Mon Dec 10 2012 Michal Srb <msrb@redhat.com> - 1.0-0.1.alpha11
- Initial packaging

