# Generated from mixlib-config-1.0.9.gem by gem2rpm -*- rpm-spec -*-
%global gem_name mixlib-config

# EPEL6 lacks rubygems-devel package that provides these macros
%if %{?el6}0
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_libdir %{gem_instdir}/lib
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%endif

%if %{?el6}0 || %{?fc16}0
%global rubyabi 1.8
%else
%global rubyabi 1.9.1
%endif

Summary: Simple Ruby config mix-in
Name: rubygem-%{gem_name}
Version: 2.1.0
Release: 6%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: https://github.com/opscode/mixlib-config
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(rubygems)

%if 0%{?fedora} >= 19
Requires: ruby(release)
BuildRequires: ruby(release)
%else
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(abi) = %{rubyabi}
%endif

# Needed to run checks:
%{!?el6:BuildRequires: rubygem(rspec)}
%{!?el6:BuildRequires: rubygems-devel}
# Needed for check:
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A class-based config mixin, similar to the one found in Chef.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

%if 0%{?fedora} >= 19
%gem_install -n %{SOURCE0}
%else
mkdir -p .%{gem_dir}
gem install -V \
  --local \
  --install-dir $(pwd)/%{gem_dir} \
  --force --rdoc \
  %{SOURCE0}
%endif

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

%check
%if %{?el6}0 || %{?fc16}0
# spec is too old; need RSpec2
%else
pushd .%{gem_instdir}
rspec
popd
%endif

%files
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/NOTICE
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.1.0-6
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.1.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.1.0-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec 20 2013 Julian C. Dunn <jdunn@aquezada.com> - 2.1.0-1
- Upgrade to 2.1.0 (bz#1038984)

* Sun Sep 15 2013 Julian C. Dunn <jdunn@aquezada.com> - 2.0.0-1
- Upgrade to 2.0.0 (bz#1012369)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Josef Stribny <jstribny@redhat.com> - 1.1.2-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 Julian C. Dunn <jdunn@aquezada.com> - 1.1.2-3
- Disable %check on F16/EL6; rspec is too old.

* Sun Dec 23 2012 Julian C. Dunn <jdunn@aquezada.com> - 1.1.2-2
- Silence tests & unify spec between Fedora/EPEL.

* Mon Apr 30 2012 Jonas Courteau <rpm@courteau.org> - 1.1.2-1
- Repackaged for fc17
- Call tests directly, eliminating need for patch, Rakefile modification
- New upstream version

* Wed Jun 9 2010 Matthew Kent <mkent@magoazul.com> - 1.1.0-4
- New patch to enable check again.

* Tue Jun 8 2010 Matthew Kent <mkent@magoazul.com> - 1.1.0-3
- Disable check for now.

* Tue Mar 23 2010 Matthew Kent <mkent@magoazul.com> - 1.1.0-2
- New upstream version - moves to jeweler for gem creation.

* Mon Oct 5 2009 Matthew Kent <mkent@magoazul.com> - 1.0.12-2
- Missing complete source url (#526180).
- Remove unused ruby_sitelib macro (#526180).
- Remove redundant doc Requires on rubygems (#526180).

* Sun Oct 4 2009 Matthew Kent <mkent@magoazul.com> - 1.0.12-1
- Remove redundant path in doc package (#526180).
- Use global over define (#526180).
- New upstream version (#526180).

* Mon Sep 28 2009 Matthew Kent <mkent@magoazul.com> - 1.0.9-1
- Initial package
