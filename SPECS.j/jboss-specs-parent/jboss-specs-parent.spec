%global namedreltag .Beta2
%global namedversion %{version}%{?namedreltag}

Name:             jboss-specs-parent
Version:          1.0.0
Release:          0.14%{namedreltag}%{?dist}
Summary:          JBoss Specification API Parent POM
Group:            Development/Libraries
# The license is not included because it's not a part of this tag. License file
# was pushed to trunk and no new tag will be created for this change.
# http://anonsvn.jboss.org/repos/jbossas/projects/specs/trunk/jboss-specs-parent/LICENSE-2.0.txt
License:          ASL 2.0
Url:              http://www.jboss.org/

# svn export http://anonsvn.jboss.org/repos/jbossas/projects/specs/tags/jboss-specs-parent-1.0.0.Beta2/
# tar czf jboss-specs-parent-1.0.0.Beta2-src-svn.tar.gz jboss-specs-parent-1.0.0.Beta2
Source0:          %{name}-%{namedversion}-src-svn.tar.gz

BuildRequires:    jpackage-utils

Requires:         jboss-parent
Requires:         maven-compiler-plugin
Requires:         maven-release-plugin
Requires:         jpackage-utils
BuildArch:        noarch

%description
Parent POM that allows building all specification projects at once.

%prep
%setup -q -n %{name}-%{namedversion}

%build

%install
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.jboss-%{name}.pom

%add_maven_depmap JPP.jboss-%{name}.pom

%files -f .mfiles

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.0.0-0.14.Beta2
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.0.0-0.13.Beta2
- 为 Magic 3.0 重建

* Fri Aug 15 2014 Liu Di <liudidi@gmail.com> - 1.0.0-0.12.Beta2
- 为 Magic 3.0 重建

* Sun Aug 03 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.0.0-0.11.Beta2
- Fix FTBFS due to XMvn changes in F21 (#1106901)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.10.Beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun  2 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.0-0.9.Beta2
- Fix dist tag

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.0.0-0.8.Beta2
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.7.Beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.6.Beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.5.Beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.4.Beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Marek Goldmann <mgoldman@redhat.com> 1.0.0-0.3.Beta2
- Cleared license status

* Fri Oct 07 2011 Marek Goldmann <mgoldman@redhat.com> 1.0.0-0.2.Beta2
- Updated license

* Thu Aug 11 2011 Marek Goldmann <mgoldman@redhat.com> 1.0.0-0.1.Beta2
- Initial packaging
