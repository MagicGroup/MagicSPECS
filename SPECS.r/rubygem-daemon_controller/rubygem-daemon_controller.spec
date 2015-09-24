# Generated from daemon_controller-0.2.5.gem by gem2rpm -*- rpm-spec -*-
%define gem_name daemon_controller

Summary: A library for implementing daemon management capabilities
Name: rubygem-%{gem_name}
Version: 1.2.0
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/FooBarWidget/daemon_controller/tree/master
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires: ruby
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec) < 3
BuildArch: noarch

%description
A library for robust daemon management.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}

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

rm -rf %{buildroot}%{gem_instdir}/debian.template
rm -rf %{buildroot}%{gem_instdir}/rpm
rm -rf %{buildroot}%{gem_instdir}/Rakefile

%check
pushd .%{gem_instdir}
# be explicit so localhost doesn't resolve to an ipv6 address.
sed -i 's/localhost/127.0.0.1/g' spec/daemon_controller_spec.rb

rspec2 spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%license %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.markdown
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/*.gemspec
%{gem_docdir}
%{gem_instdir}/spec

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 10 2014 Brett Lentz <blentz@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Thu Jan 23 2014 Brett Lentz <blentz@redhat.com> - 1.1.8-1
- Update to 1.1.8

* Wed Jul 31 2013 Brett Lentz <blentz@redhat.com> - 1.1.5-1
- Update to 1.1.5

* Fri May 03 2013 Brett Lentz <blentz@redhat.com> - 1.1.4-1
- Update to 1.1.4

* Mon Mar 18 2013 Brett Lentz <blentz@redhat.com> - 1.1.2-2
- use %%gem_install macro

* Fri Mar 15 2013 Brett Lentz <blentz@redhat.com> - 1.1.2-1
- Update to 1.1.2

* Wed Mar 13 2013 Brett Lentz <blentz@redhat.com> - 1.1.1-2
- Update to new packaging guidelines.

* Fri Feb 22 2013 Brett Lentz <blentz@redhat.com> - 1.1.1-1
- Update to 1.1.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 13 2012 Brett Lentz <blentz@redhat.com> - 1.0.0-1
- Update to 1.0.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Vít Ondruch <vondruch@redhat.com> - 0.2.6-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Apr 25 2011  Peng Wu <pwu@redhat.com> - 0.2.6-1
- Update to version 0.2.6

* Thu Apr 21 2011  Peng Wu <pwu@redhat.com> - 0.2.5-3
- Run test suite

* Wed Apr 20 2011  Peng Wu <pwu@redhat.com> - 0.2.5-2
- Fixes the spec

* Wed Apr 20 2011 Peng Wu <pwu@redhat.com> - 0.2.5-1
- Initial package
