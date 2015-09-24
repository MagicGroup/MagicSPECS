# Generated from origin-1.1.0.gem by gem2rpm -*- f19.spec -*-
%global gem_name origin

Summary:       Simple DSL for MongoDB query generation
Name:          rubygem-%{gem_name}
Version:       2.1.1
Release:       2%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://mongoid.org
Source0:       https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/mongoid/origin.git && cd origin
# git checkout v2.1.1
# tar -czf rubygem-origin-2.1.1-specs.tgz spec/
Source1: %{name}-%{version}-specs.tgz
Requires:      ruby(release)
Requires:      rubygems
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
# For testing
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(i18n)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(tzinfo)
BuildArch:     noarch
Provides:      rubygem(%{gem_name}) = %{version}

%description
Origin is a simple DSL for generating MongoDB selectors and options

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

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
# Remove build leftovers.
rm -rf %{buildroot}%{gem_instdir}/.yard*

%check
pushd ./%{gem_instdir}
tar -xzf %{SOURCE1}
rspec -Ilib spec
rm -rf spec
popd

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

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 03 2014 Troy Dawson <tdawson@redhat.com> - 2.1.1-1
- Updated to version 2.1.1

* Tue Feb 04 2014 Troy Dawson <tdawson@redhat.com> - 2.1.0-1
- Updated to version 2.1.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 05 2013 Troy Dawson <tdawson@redhat.com> - 1.1.0-3
- Moved test unpacking to check section
- Fixed dependancies

* Tue May 28 2013 Troy Dawson <tdawson@redhat.com> - 1.1.0-2
- Fixed what goes in doc
- Added spec from upstream and run check

* Fri May 10 2013 Troy Dawson <tdawson@redhat.com> - 1.1.0-1
- Initial package
