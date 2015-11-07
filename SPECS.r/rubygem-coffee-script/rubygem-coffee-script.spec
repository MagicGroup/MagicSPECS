# Generated from coffee-script-2.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name coffee-script

Summary: Ruby CoffeeScript Compiler
Name: rubygem-%{gem_name}
Version: 2.3.0
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/josh/ruby-coffee-script
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# To get the tests:
# git clone https://github.com/josh/ruby-coffee-script && cd ruby-coffee-script
# git checkout v2.3.0 && tar czf coffee-script-tests-2.3.0.tgz test/
Source1: coffee-script-tests-%{version}.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(coffee-script-source)
BuildRequires: rubygem(execjs)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(therubyracer)
BuildArch: noarch

%description
Ruby CoffeeScript is a bridge to the JS CoffeeScript compiler.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

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
# unpack and patch the tests
tar xzf %{SOURCE1}

ruby -Ilib -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.3.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.3.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 27 2015 Vít Ondruch <vondruch@redhat.com> - 2.3.0-1
- Update to Ruby CoffeeScript 2.3.0.

* Wed Jun 25 2014 Vít Ondruch <vondruch@redhat.com> - 2.2.0-6
- Fix FTBFS in Rawhide (rhbz#1107086).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Vít Ondruch <vondruch@redhat.com> - 2.2.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 17 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.2.0-1
- Initial package
