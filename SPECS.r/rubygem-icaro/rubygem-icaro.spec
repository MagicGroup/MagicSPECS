%global gem_name icaro

Summary: Icaro API for Ruby
Name: rubygem-%{gem_name}
Version: 1.0.6
Release: 7%{?dist}
Group: Development/Languages
License: GPLv3
URL: http://github.com/aeperezt/ruby-icaro 
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby-devel
BuildRequires: rubygems-devel
Requires: rubygem-serialport
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Icaro Robot project Ruby API

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.


%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
mkdir -p ./%{gem_dir}
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

%clean
rm -rf %{buildroot}

%files
%dir %{gem_instdir}
%{gem_instdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.0.6-7
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.6-6
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Alejandro Pérez <aeperez@fedoraproject.org> - 1.0.6-2
- change rubygem-icaro.spec permits
* Sun Apr 07 2013 Alejandro Pérez <aeperezt@fedoraproject.org> - 1.0.6-1
- Initial package
