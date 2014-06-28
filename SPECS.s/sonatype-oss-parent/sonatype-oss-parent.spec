Name:           sonatype-oss-parent
Version:        7
Release:        10%{?dist}
Summary:        Sonatype OSS Parent

License:        ASL 2.0
URL:            https://github.com/sonatype/oss-parents
# git clone git://github.com/sonatype/oss-parents.git
# (cd ./oss-parents; git archive --prefix %{name}-%{version}/ oss-parent-%{version}) | gzip >%{name}-%{version}.tar.gz
Source:         %{name}-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildArch: noarch

BuildRequires:  maven-local


%description
Sonatype OSS parent pom used by other sonatype packages.

%prep
%setup -q
cp -p %{SOURCE1} LICENSE
%pom_remove_plugin org.apache.maven.plugins:maven-enforcer-plugin

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE

%changelog
* Sun Jun 22 2014 Liu Di <liudidi@gmail.com> - 7-10
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 7-8
- Rebuild to regenerate Maven auto-requires

* Thu Feb 20 2014 Michal Srb <msrb@redhat.com> - 7-7
- Rebuild to get provides with "pom" extension
- Small spec file cleanup

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 7-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 17 2013 Michal Srb <msrb@redhat.com> - 7-3
- Build with xmvn

* Wed Nov 21 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 7-2
- Install LICENSE file
- Resolves: rhbz#879013

* Mon Aug  6 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 7-1
- Update to upstream version 7

* Thu Jul 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 6-5
- Cleanup spec according to latest guidelines
- Use pom macro to remove enforcer plugin from pom

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 6-1
- Update to latest version that includes the license header

* Wed Dec  1 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 5-1
- Initial version of the package
