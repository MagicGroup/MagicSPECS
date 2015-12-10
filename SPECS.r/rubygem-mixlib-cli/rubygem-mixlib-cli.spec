# Generated from mixlib-cli-1.0.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name mixlib-cli

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

Summary: Simple Ruby mix-in for CLI interfaces
Name: rubygem-%{gem_name}
Version: 1.5.0
Release: 6%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: https://github.com/opscode/mixlib-cli
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Patch to silence mixlib-cli tests;
# see http://tickets.opscode.com/browse/MIXLIB-8
Patch0: mixlib-cli-silence-tests.patch
Requires: ruby(rubygems)

%if 0%{?fedora} >= 19
Requires: ruby(release)
BuildRequires: ruby(release)
%else
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(abi) = %{rubyabi}
%endif

%{!?el6:BuildRequires: rubygems-devel}
%{!?el6:BuildRequires: rubygem(rspec)}
BuildRequires: rubygem(rake)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A simple mix-in for CLI interfaces, including option parsing.

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

pushd .%{gem_instdir}
%patch0 -p1
popd

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
%{gem_docdir}
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/NOTICE
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/spec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.5.0-6
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.5.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.5.0-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 27 2014 Julian C. Dunn <jdunn@aquezada.com> - 1.5.0-1
- Update to 1.5.0 (bz#1091745)

* Fri Dec 20 2013 Julian C. Dunn <jdunn@aquezada.com> - 1.4.0-1
- Update to 1.4.0 (bz#1038983)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Josef Stribny <jstribny@redhat.com> - 1.3.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Julian C. Dunn <jdunn@aquezada.com> - 1.3.0-1
- Update to 1.3.0

* Sun Jan 13 2013 Julian C. Dunn <jdunn@aquezada.com> - 1.2.2-3
- Suppress %check on F16; RSpec too old

* Thu Dec 13 2012 Julian C. Dunn <jdunn@aquezada.com> - 1.2.2-2
- Unify build on EPEL6 and Fedora

* Mon Apr 30 2012 Jonas Courteau <rpm@courteau.org> - 1.2.2-1
- Repackaged for fc17
- Changed check to avoid need for patch
- New upstream version

* Wed Jun 9 2010 Matthew Kent <mkent@magoazul.com> - 1.1.0-3
- New patch to enable check again.

* Tue Jun 8 2010 Matthew Kent <mkent@magoazul.com> - 1.1.0-2
- Disable check for now.

* Tue Mar 23 2010 Matthew Kent <mkent@magoazul.com> - 1.1.0-1
- New upstream version - moves to jeweler for gem creation.

* Mon Oct 5 2009 Matthew Kent <mkent@magoazul.com> - 1.0.4-3
- Remove unused ruby_sitelib macro (#526179).
- Remove redundant doc Requires on rubygems (#526179).

* Sun Oct 4 2009 Matthew Kent <mkent@magoazul.com> - 1.0.4-2
- Remove redundant path in doc package (#526179).
- Use global over define (#526179).

* Mon Sep 28 2009 Matthew Kent <mkent@magoazul.com> - 1.0.4-1
- Initial package
