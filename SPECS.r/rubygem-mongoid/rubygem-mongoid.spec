%global gem_name mongoid

Summary:       Elegant Persistance in Ruby for MongoDB
Name:          rubygem-%{gem_name}
Version:       4.0.0
Release:       4%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://mongoid.org
Source0:       https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fedora} >= 19 || 0%{?rhel} > 6
Requires:      ruby(release)
Requires:      rubygems
Requires:      rubygem(activemodel) >= 3.2
Requires:      rubygem(tzinfo) >= 0.3.22
Requires:      rubygem(moped) >= 1.4.2
Requires:      rubygem(origin) >= 1.0
BuildRequires: ruby(release)
%endif
BuildRequires: rubygems-devel
BuildArch:     noarch
Provides:      rubygem(%{gem_name}) = %{version}

%description
Mongoid is an ODM (Object Document Mapper) Framework for MongoDB, written in
Ruby.


%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

sed -i 's/<moped>, \[\"\~> 2.0.0\"\]/<moped>, \[\"> 1.4\"\]/' %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

# Remove build leftovers.
rm -rf %{buildroot}%{gem_instdir}/.yard*

%files
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.0.0-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jul 07 2014 Troy Dawson <tdawson@redhat.com> - 4.0.0-2
- Tweek dependencies

* Mon Jul 07 2014 Troy Dawson <tdawson@redhat.com> - 4.0.0-1
- Updated to version 4.0.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 04 2014 Troy Dawson <tdawson@redhat.com> - 3.1.6-1
- Updated to version 3.1.6

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 10 2013 Troy Dawson <tdawson@redhat.com> - 3.1.4-1
- Updated to 3.1.4
- Fixed moped version dependancy problem (#980526)

* Fri May 10 2013 Troy Dawson <tdawson@redhat.com> - 3.1.3-1
- Initial package
