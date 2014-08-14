Name:           mojo-parent
Version:        33
Release:        4%{?dist}
Summary:        Codehaus MOJO parent project pom file

License:        ASL 2.0
URL:            http://mojo.codehaus.org/
Source0:        http://repo1.maven.org/maven2/org/codehaus/mojo/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  codehaus-parent
BuildRequires:  maven-enforcer-plugin

%description
Codehaus MOJO parent project pom file

%prep
%setup -q
# Cobertura plugin is executed only during clean Maven phase.
%pom_remove_plugin :cobertura-maven-plugin
# wagon-webdav-jackrabbit is not available in Fedora
%pom_xpath_remove "pom:extension[pom:artifactId[text()='wagon-webdav-jackrabbit']]"

cp %SOURCE1 .

%build
%mvn_alias : org.codehaus.mojo:mojo
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-2.0.txt

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 33-3
- Rebuild to regenerate Maven auto-requires

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 33-2
- Regenerate requires

* Mon Mar 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 33-1
- Update to upstream version 33

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 32-3
- Add ASL 2.0 license text to rpms

* Mon Apr 22 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 32-2
- Update to latest upstream (#948704)

* Fri Feb  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 31-1
- Update to upstream version 31

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 30-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 17 2013 Michal Srb <msrb@redhat.com> - 30-4
- Build with xmvn

* Fri Jan  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 30-3
- Disable maven-plugin-cobertura

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 30-2
- Install additional depmap
- Resolves: rhbz#880619

* Mon Jul 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 30-1
- Update to upstream version 30

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 7 2011 Alexander Kurtakov <akurtako@redhat.com> 29-1
- Update to latest upstream.

* Tue Mar  8 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 28-2
- Remove parent from pom.xml (no codehaus-parent in Fedora now)

* Mon Mar  7 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 28-1
- Update to latest upstream

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 16 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 24-5
- Add component-javadoc to R

* Thu Sep 16 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 24-4
- Add forgotten jpackage-utils BR

* Tue Sep 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 24-3
- Change to license used by upstream (ASL 2.0)

* Mon Sep  6 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 24-2
- Removed %%build section and BRs (not really needed)

* Mon Sep  6 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 24-1
- Initial version of the package
