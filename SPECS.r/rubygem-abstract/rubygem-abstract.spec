# Generated from abstract-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name abstract


Summary: Allows you to define an abstract method in Ruby
Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 12%{?dist}
Group: Development/Languages
License: GPLv2 or Ruby
URL: http://rubyforge.org/projects/abstract
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem

Patch0: update-minitest.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby(release)
BuildRequires: rubygem(minitest)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Small library that allows you to define an abstract method in Ruby.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%patch0

%build
gem build %{gem_name}.gemspec

%gem_install

%check
pushd .%{gem_instdir}
ruby -Ilib test/test.rb
popd

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# We have this in specifications/
rm -f %{buildroot}%{gem_instdir}/abstract.gemspec

# And we install via gem
rm -f %{buildroot}%{gem_instdir}/setup.rb

%files
%defattr(-,root,root,-)
%doc %{gem_instdir}/README.txt
%doc %{gem_instdir}/ChangeLog
%dir %{gem_instdir}
%{gem_libdir}
%{gem_cache}
%{gem_spec}

%files doc
%defattr(-,root,root,-)
%{gem_instdir}/test
%{gem_docdir}

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 16 2014 Mo Morsi <mmorsi@redhat.com>- 1.0.0-11
- Incorporate patch updating test suite to minitest 5
- Update spec to comply w/ latest guidelines

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.0-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 30 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.0-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 24 2009 Matthew Kent <mkent@magoazul.com> - 1.0.0-2
- Fix license

* Mon Oct 19 2009 Matthew Kent <mkent@magoazul.com> - 1.0.0-1
- Initial package
