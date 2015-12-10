%global gem_name deltacloud-client

Summary: Deltacloud REST Client
Name: rubygem-%{gem_name}
Version: 1.1.2
Release: 9%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://www.deltacloud.org
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(rest-client) >= 1.4.0
Requires: rubygem(nokogiri)
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Deltacloud REST Client for API

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Modify the gemspec if necessary with a patch or sed
# Also apply patches to code if necessary
# %patch0 -p1

%build

# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# gem install compiles any C extensions and installs into a directory
# We set that to be a local directory so that we can move it into the
# buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.yardoc
%{gem_spec}
%doc %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/tests
%{gem_instdir}/NOTICE

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.1.2-9
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.1.2-8
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.2-7
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.2-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Mar 18 2013 Michal Fojtik <mfojtik@redhat.com> - 1.1.2-2
- Fixed tests directory

* Mon Mar 18 2013 Michal Fojtik <mfojtik@redhat.com> - 1.1.2-1
- Release 1.1.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Michal Fojtik <mfojtik@redhat.com> - 1.0.4-1
- Release 1.0.4

* Mon Sep 17 2012 Michal Fojtik <mfojtik@redhat.com> - 1.0.3-1
- Release 1.0.3

* Wed Aug 15 2012 Michal Fojtik <mfojtik@redhat.com> - 1.0.0-2
- Revamped spec file to be FPG compliant

* Wed Aug 15 2012 Michal Fojtik <mfojtik@redhat.com> - 1.0.0-1
- Version 1.0.0 bump

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Michal Fojtik <mfojtik@redhat.com> - 0.5.0-3
- Fixed the install section

* Thu Apr 19 2012 Michal Fojtik <mfojtik@redhat.com> - 0.5.0-2
- Fixed typo in geminst macro

* Thu Apr 19 2012 Michal Fojtik <mfojtik@redhat.com> - 0.5.0-1
- Updated to 0.5.0 official release

* Mon Feb 06 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.5.0-2.rc1
- Rebuilt for Ruby 1.9.3.

* Wed Jan 11 2012 Michal Fojtik <mfojtik@redhat.com> - 0.5.0-1.rc1
- Version bump 0.5.0-rc1

* Mon Sep 19 2011 Michal Fojtik <mfojtik@redhat.com> - 0.4.0-1
- Version bump
- Added patch to fix incorrect hardware properties handling for architecture property

* Thu Jun 16 2011 Michal Fojtik <mfojtik@redhat.com> - 0.3.1-1
- Version bump

* Thu May 05 2011 Michal Fojtik <mfojtik@redhat.com> - 0.3.0-1
- Version bump

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Michal Fojtik <mfojtik@redhat.com> - 0.1.1-1
- Version bump

* Thu Oct 14 2010 Michal Fojtik <mfojtik@redhat.com> - 0.1.0-2
- Fixed rest-client versioning

* Thu Oct 14 2010 Michal Fojtik <mfojtik@redhat.com> - 0.1.0-1
- Version bump

* Thu Oct 14 2010 Michal Fojtik <mfojtik@redhat.com> - 0.0.9.8-1
- Initial package
