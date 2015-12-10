# Generated from ipaddress-0.8.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ipaddress

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

Summary: IPv4/IPv6 addresses manipulation library
Name: rubygem-%{gem_name}
Version: 0.8.0
Release: 12%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/bluemonk/ipaddress
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0: rubygem-ipaddress-0.8.0-minitest.patch
Patch1: rubygem-ipaddress-0.8.0-ruby2-conversion.patch
%if 0%{?fedora} >= 19
Requires: ruby(release)
BuildRequires: ruby(release)
%else
Requires: ruby(abi) >= %{rubyabi}
BuildRequires: ruby(abi) >= %{rubyabi}
%endif
Requires: ruby(rubygems)
%{!?el6:BuildRequires: rubygems-devel}
BuildRequires: rubygem(minitest)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
IPAddress is a Ruby library designed to make manipulation
of IPv4 and IPv6 addresses both powerful and simple. It maintains
a layer of compatibility with Ruby's own IPAddr, while 
addressing many of its issues.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
mkdir -p .%{gem_dir}
gem install --local --install-dir .%{gem_dir} \
            --force %{SOURCE0}

# Remove un-needed file
# See https://github.com/bluemonk/ipaddress/issues/23
rm .%{gem_instdir}/.document

pushd .%{gem_instdir}
%patch0 -p1
%patch1 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)' 
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/README.rdoc
%{gem_instdir}/VERSION
%{gem_instdir}/CHANGELOG.rdoc
%{gem_instdir}/Rakefile

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.8.0-12
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.8.0-11
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.8.0-10
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 12 2014 Julian C. Dunn <jdunn@aquezada.com> - 0.8.0-8
- Patch tests for Minitest5 and Ruby 2.x (bz#1107145)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Julian C. Dunn <jdunn@aquezada.com> - 0.8.0-5
- Fix build breakage on >= F19 with new Ruby guidelines

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 29 2012 Julian C. Dunn <jdunn@aquezada.com> - 0.8.0-3
- Correct duplicate LICENSE file

* Thu Dec 27 2012 Julian C. Dunn <jdunn@aquezada.com> - 0.8.0-2
- Revised per review in bz#823340

* Mon Apr 30 2012 Jonas Courteau <rpms@courteau.org> - 0.8.0-1
- Initial package
- Submitted https://github.com/bluemonk/ipaddress/issues/23 upstream to remove extra file from gem
