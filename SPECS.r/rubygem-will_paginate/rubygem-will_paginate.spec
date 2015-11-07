%global gem_name will_paginate


Summary:       Most awesome pagination solution for Rails
Name:          rubygem-%{gem_name}
Version:       3.0.7
Release:       3%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://github.com/mislav/will_paginate
Source0:       http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(actionpack)
BuildRequires: rubygem(activerecord)
# apply_finder_options was deprecated in RoR, this might be possible to remove
# in the future.
# https://github.com/mislav/will_paginate/issues/322
BuildRequires: rubygem(activerecord-deprecated_finders)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(rspec)
# It seems that will_paginate is not compatible with Sequel 4.x.
# https://github.com/mislav/will_paginate/issues/333
# BuildRequires: rubygem(sequel)
BuildArch:     noarch

%description
The will_paginate library provides a simple, yet powerful and extensible API
for ActiveRecord pagination and rendering of pagination links in ActionView
templates.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
rspec spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/spec
%doc %{gem_docdir}
%exclude %{gem_cache}
%{gem_spec}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 3.0.7-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.0.7-2
- 为 Magic 3.0 重建

* Mon Jul 07 2014 Vít Ondruch <vondruch@redhat.com> - 3.0.7-1
- Update to will_paginate 3.0.7.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 02 2014 Vít Ondruch <vondruch@redhat.com> - 3.0.5-1
- Update to will_paginate 3.0.5 (fixes CVE-2013-6459).

* Wed Aug 21 2013 Vít Ondruch <vondruch@redhat.com> - 3.0.4-3
- Fix Ruby on Rails 4.0 compatibility.
- Disable Sequel test, since Sequel 4.x does not seem to be supported by
  will_paginate yet.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 12 2013 Vít Ondruch <vondruch@redhat.com> - 3.0.4-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to will_paginate 3.0.4.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.2-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Vít Ondruch <vondruch@redhat.com> - 3.0.2-1
- Update to will_paginate 3.0.2.

* Tue Jul 12 2011 Mo Morsi <mmorsi@redhat.com> - 3.0-0.1.pre2
- Update to 3.0.pre2 for Rails 3 compatability

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 08 2010 Michal Fojtik <mfojtik@redhat.com> - 2.3.14-1
- Version bump

* Wed May 19 2010 Michal Fojtik <mfojtik@redhat.com> - 2.3.12-2
- Fixed documents
- Fixed macros in changelog
- Added activesupport to requires

* Tue May 18 2010 Michal Fojtik <mfojtik@redhat.com> - 2.3.12-1
- Version bump
- Fixed BuildRequires


* Tue Dec 08 2009 Darryl Pierce <dpierce@redhat.com> - 2.3.11-2
- Replaced %%define with %%global.
- Fixed license.
- Replaced the source URL.

* Thu Nov 19 2009 Darryl Pierce <dpierce@redhat.com> - 2.3.11-1
- Initial package
