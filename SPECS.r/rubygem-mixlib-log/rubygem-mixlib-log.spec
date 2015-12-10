# Generated from mixlib-log-1.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name mixlib-log

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

Summary: Ruby mix-in for log functionality
Name: rubygem-%{gem_name}
Version: 1.6.0
Release: 6%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://github.com/opscode/mixlib-log
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem

%if 0%{?fedora} >= 19
Requires: ruby(release)
BuildRequires: ruby(release)
%else
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(abi) = %{rubyabi}
%endif
Requires: ruby(rubygems)
BuildRequires: ruby(rubygems)
%{!?el6:BuildRequires: rubygem(rspec)}
%{!?el6:BuildRequires: rubygems-devel}
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A gem that provides a simple mix-in for log functionality.

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
pushd ./%{gem_instdir}
rspec
popd
%endif

%files
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%exclude %{gem_instdir}/.gemtest
%exclude %{gem_instdir}/%{gem_name}.gemspec

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/NOTICE
%{gem_instdir}/spec
%{gem_instdir}/Rakefile

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.6.0-6
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.6.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.6.0-4
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 15 2013 Julian C. Dunn <jdunn@aquezada.com> - 1.6.0-1
- Update to 1.6.0

* Fri Mar 08 2013 Josef Stribny <jstribny@redhat.com> - 1.4.1-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 Julian C. Dunn <jdunn@aquezada.com> - 1.4.1-3
- Exclude %check from running on F16 since RSpec is too old

* Wed Jan 02 2013 Julian C. Dunn <jdunn@aquezada.com> - 1.4.1-2
- Move extra files into -doc subpackage per review (#823332)

* Fri Dec 21 2012 Julian C. Dunn <jdunn@aquezada.com> - 1.4.1-1
- Rebuilt with 1.4.1, specs are bundled

* Sun Apr 29 2012 Jonas Courteau <rpms@courteau.org> - 1.3.0-1
- Repackaged for fc17
- New upstream version
- Removed check patch
- Modified check - pull tests manually as they've been removed from gem

* Wed Jun 9 2010 Matthew Kent <mkent@magoazul.com> - 1.1.0-3
- New patch to enable check again.

* Tue Jun 8 2010 Matthew Kent <mkent@magoazul.com> - 1.1.0-2
- Disable check for now.

* Tue Mar 23 2010 Matthew Kent <mkent@magoazul.com> - 1.1.0-1
- New upstream version - moves to jeweler for gem creation.

* Mon Oct 5 2009 Matthew Kent <mkent@magoazul.com> - 1.0.3-3
- Missing complete source url (#526181).
- Remove unused ruby_sitelib macro (#526181).
- Remove redundant doc Requires on rubygems (#526181).

* Sun Oct 4 2009 Matthew Kent <mkent@magoazul.com> - 1.0.3-2
- Remove redundant path in doc package (#526181).
- Use global over define (#526181).

* Mon Sep 28 2009 Matthew Kent <mkent@magoazul.com> - 1.0.3-1
- Initial package
