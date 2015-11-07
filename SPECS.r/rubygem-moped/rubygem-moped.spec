# Generated from moped-1.4.5.gem by gem2rpm -*- f19.spec -*-
%global gem_name moped

Summary:       A MongoDB driver for Ruby
Name:          rubygem-%{gem_name}
Epoch:         1
Version:       1.5.3
Release:       3%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://mongoid.org/en/moped
Source0:       https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires:      ruby(release)
Requires:      rubygems 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildArch:     noarch
Provides:      rubygem(%{gem_name}) = %{version}

%description
Moped is a MongoDB driver for Ruby, which exposes a simple, elegant,
and fast API. Moped is the supported driver for Mongoid 
from version 3 and higher.

Moped is composed of three parts: an implementation of the 
BSON specification, an implementation of the Mongo Wire 
Protocol, and the driver itself.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{epoch}:%{version}-%{release}
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

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1:1.5.3-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1:1.5.3-2
- 为 Magic 3.0 重建

* Wed Jul 01 2015 Troy Dawson <tdawson@redhat.com> - 1.5.3-1
- Updated to version 1.5.3
- Security fix for CVE-2015-4411 (#1229708)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 26 2015 Kalev Lember <kalevlember@gmail.com> - 1:1.5.2-5
- Bump epoch for the version downgrade

* Wed Nov 05 2014 Troy Dawson <tdawson@redhat.com> - 1.5.2-4
- Reverting back again.

* Wed Jul 09 2014 Troy Dawson <tdawson@redhat.com> - 1.5.2-3
- Rebuild to revert

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 04 2014 Troy Dawson <tdawson@redhat.com> - 1.5.2-1
- Updated to version 1.5.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Troy Dawson <tdawson@redhat.com> - 1.5.0-1
- Updated to 1.5.0
- Fixed what goes in doc

* Fri May 10 2013 Troy Dawson <tdawson@redhat.com> - 1.4.5-1
- Initial package
