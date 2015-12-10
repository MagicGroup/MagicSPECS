Name:           apache-parent
Version:        14
Release:        5%{?dist}
Summary:        Parent pom file for Apache projects
Group:          Development/Libraries
License:        ASL 2.0
URL:            http://apache.org/
Source0:        http://svn.apache.org/repos/asf/maven/pom/tags/apache-%{version}/pom.xml#/%{name}-%{version}.pom
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  jpackage-utils
BuildRequires:  apache-resource-bundles
BuildRequires:  maven-remote-resources-plugin

Requires:       apache-resource-bundles

%description
This package contains the parent pom file for apache projects.


%prep
%setup -n %{name}-%{version} -Tc
cp %{SOURCE0} pom.xml
cp %{SOURCE1} LICENSE

%pom_remove_plugin :maven-site-plugin pom.xml

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 14-5
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 14-4
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 14-3
- 为 Magic 3.0 重建

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 14-2
- Rebuild to regenerate Maven auto-requires

* Mon Mar 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 14-1
- Update to upstream version 14

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 10-15
- Remove maven-site-plugin from dependencies

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 10-14
- Rebuild to regenerate Maven provides

* Thu Aug 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 10-13
- Add missing R: apache-resource-bundles

* Mon Aug 26 2013 Michal Srb <msrb@redhat.com> - 10-12
- Migrate away from mvn-rpmbuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 10-9
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Dec 18 2012 Michal Srb <msrb@redhat.com> - 10-8
- Added license (Resolves: #888287)

* Wed Nov 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 10-7
- Install patched pom not the original

* Fri Nov  2 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 10-6
- Add missing R: maven-remote-resources-plugin, apache-resource-bundles
- Add %%check to verify dependencies during build

* Thu Jul 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 10-5
- Make sure we generate 1.5 version bytecode

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 13 2011 Andy Grimm <agrimm@gmail.com> 10-2
- Follow suggestions in BZ #736069

* Mon Aug 29 2011 Andy Grimm <agrimm@gmail.com> 10-1
- Initial Build
