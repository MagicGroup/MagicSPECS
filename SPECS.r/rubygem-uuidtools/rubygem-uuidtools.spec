# Generated from uuidtools-2.1.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name uuidtools


Summary: A simple universally unique ID generation library
Name: rubygem-%{gem_name}
Version: 2.1.5
Release: 4%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: https://github.com/sporkmonger/uuidtools
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
BuildRequires: ruby(release)
BuildRequires: %{_sbindir}/ip
BuildRequires: rubygem(rspec-core)
BuildRequires: rubygem(rspec-mocks)
BuildRequires: rubygem(rspec-expectations)
BuildArch: noarch

%description
UUIDTools was designed to be a simple library for generating any of the various
types of UUIDs.  It conforms to RFC 4122 whenever possible.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

%gem_install -n %{SOURCE0}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

%clean
rm -rf %{buildroot}

%check
pushd .%{gem_instdir}
rspec spec
popd

%files
%doc %{gem_instdir}/[A-Z]*
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/Rakefile
%{gem_instdir}/tasks
%{gem_instdir}/website
%{gem_instdir}/spec
%{gem_docdir}

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.1.5-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.1.5-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 16 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.5-1
- Update to UUIDTools 2.1.5.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 2.1.3-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Mo Morsi <mmorsi@redhat.com> - 2.1.3-1
- Updated to uuidtools 2.1.3.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 2.1.2-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Vít Ondruch <vondruch@redhat.com> - 2.1.2-1
- Updated to uuidtools 2.1.2.

* Thu Dec 15 2011 Vít Ondruch <vondruch@redhat.com> - 2.1.1-4
- Use RSpec 2.x instead of RSpec 1.x.

* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 2.1.1-3
- Initial package

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Mar 16 2010 Matthew Kent <mkent@magoazul.com> - 2.1.1-1
- Initial package
