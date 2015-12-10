Name:           forge-parent
Version:        38
Release:        4%{?dist}
Summary:        Sonatype Forge Parent Pom
License:        ASL 2.0
URL:            https://docs.sonatype.org/display/FORGE/Index
Source0:        http://repo1.maven.org/maven2/org/sonatype/forge/%{name}/%{version}/%{name}-%{version}.pom
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
BuildArch:      noarch
BuildRequires:  maven-local

%description
Sonatype Forge is an open-source community dedicated to the creation of the 
next-generation of development tools and technologies.

%prep
%setup -qcT
cp -p %{SOURCE0} pom.xml
cp -p %{SOURCE1} LICENSE
# We don't have nexus-staging-maven-plugin in Fedora
%pom_remove_plugin :nexus-staging-maven-plugin

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 38-4
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 38-3
- 为 Magic 3.0 重建

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 38-2
- Rebuild to regenerate Maven auto-requires

* Mon Nov 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 38-1
- Update to upstream version 38

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 31-1
- Update to upstream version 31
- Install missing LICENSE file
- Build with xmvn

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 20 2010 Weinan Li <weli@redhat.com> - 5-5
- Rebuild for dist-f14-maven221

* Thu May 20 2010 Weinan Li <weli@redhat.com> - 5-4
- Change JPP.%{name}.pom to JPP-%{name}.pom

* Fri May 14 2010 Weinan Li <weli@redhat.com> - 5-3
- Each package must consistently use macros, use rm instead of all %{_rm}
- Add Requires: jpackage-utils

* Thu May 13 2010 Weinan Li <weli@redhat.com> - 5-2
- Add the license source note
- Cleanup the svn metadata in source
- Add the full instructions for creating the tar in the comment 

* Wed May 12 2010 Weinan Li <weli@redhat.com> - 5-1
- Initial version
