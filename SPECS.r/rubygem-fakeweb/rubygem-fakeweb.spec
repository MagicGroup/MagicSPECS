# Generated from fakeweb-1.3.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fakeweb

Summary: A tool for faking responses to HTTP requests
Name: rubygem-%{gem_name}
Version: 1.3.0
Release: 15%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/chrisk/fakeweb
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0: patch_out_samuel.patch
# Needed for Ruby >= 2 (already in upstream)
#   Ruby 2.0: https://github.com/chrisk/fakeweb/pull/37
#   Ruby 2.1: See upstream commit e30d22030136a8c841a4fa63a1978144c11582a7
Patch1: ruby2-tests-fix.patch
# Use Minitest 5
# https://github.com/chrisk/fakeweb/pull/48
Patch2: rubygem-fakeweb-1.3.0-Minitest-5.patch
# Ruby 2.2 tests compatibility
# https://github.com/chrisk/fakeweb/pull/53
Patch3: rubygem-fakeweb-1.3.0-Ruby-2.2-tests-fix.patch
# Keeping so this spec can be used in EPEL5
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: rubygems-devel
# The following BR are there for %%check
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(minitest) > 5.0.0
BuildRequires: rubygem(http_connection)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
FakeWeb is a helper for faking web requests in Ruby. It works at a global
level, without modifying code or writing extensive stubs.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.


%prep
%gem_install -n %{SOURCE0}

pushd ./%{gem_instdir}/test
%patch0 -p0
%patch1 -p2
%patch2 -p2
%patch3 -p2

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Don't vendor all your gems...srsly
rm -rf %{buildroot}%{gem_instdir}/test/vendor/right_http*
rm -rf %{buildroot}%{gem_instdir}/test/vendor/samuel*

# rpmlint cleanup
rm -f %{buildroot}%{gem_instdir}/test/vendor/samuel-0.2.1/.gitignore
rm -f %{buildroot}%{gem_instdir}/.autotest
rm -f %{buildroot}%{gem_instdir}/.gitignore
# This file is also in specifications
rm -f %{buildroot}%{gem_instdir}/*.gemspec


%clean
rm -rf %{buildroot}

%check
pushd %{buildroot}%{gem_instdir}

# For newer versions of mocha
sed -i -e "s|require 'mocha'|require 'mocha/setup'|" test/test_helper.rb

ruby  -Ilib:test -e "Dir.glob './test/test_*.rb', &method(:require)"
popd

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/CHANGELOG
%{gem_libdir}
%{gem_cache}
%{gem_spec}

%files doc
%defattr(-, root, root, -)
%{gem_docdir}
%{gem_instdir}/test
%{gem_instdir}/Rakefile

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 19 2015 Josef Stribny <jstribny@redhat.com> - 1.3.0-14
- Fix FTBFS sue to Ruby 2.2

* Tue Aug 19 2014 Josef Stribny <jstribny@redhat.com> - 1.3.0-13
- Fix FTBFS: change mocha requirement

* Tue Jun 10 2014 Josef Stribny <jstribny@redhat.com> - 1.3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Fix tests for Ruby 2.1
- Use Minitest 5 in tests

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Josef Stribny <jstribny@redhat.com> - 1.3.0-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Change rubygem(right_http_connection) is now packed as rubygem(http_connection)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.0-6
- Rebuilt for Ruby 1.9.3.

* Sun Jan 08 2012 Michael Stahnke <mastahnke@gmail.com> - 1.3.0-5
- Bug bz#715907 FTBFS on rawhide

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 17 2010 Michael Stahnke <stahnma@fedoraproject.org> - 1.3.0-3
- A few minor fixes in spec per review

* Mon Sep 13 2010 Michael Stahnke <stahnma@fedoraproject.org> - 1.3.0-2
- Removing 'vendored' items

* Sun Sep 12 2010 Michael Stahnke <stahnma@fedoraproject.org> - 1.3.0-1
- Initial package
