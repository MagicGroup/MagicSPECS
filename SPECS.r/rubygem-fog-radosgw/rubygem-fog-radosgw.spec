# Generated from fog-radosgw-0.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fog-radosgw

Name: rubygem-%{gem_name}
Version: 0.0.3
Release: 5%{?dist}
Summary: Fog backend for provisioning Ceph Radosgw
Group: Development/Languages
License: MIT
URL: https://github.com/fog/fog-radosgw
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(fog-xml)
BuildRequires: rubygem(fog-json)
BuildRequires: rubygem(shindo)
BuildArch: noarch

%description
Fog backend for provisioning users on Ceph Radosgw - the Swift and S3
compatible REST API for Ceph.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/



%check
pushd .%{gem_instdir}
FOG_MOCK=true shindo
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.md
%exclude %{gem_instdir}/fog-radosgw.gemspec
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%exclude %{gem_instdir}/.gitignore
%doc %{gem_instdir}/CONTRIBUTORS.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/tests

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.0.3-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.0.3-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.0.3-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 11 2015 Vít Ondruch <vondruch@redhat.com> - 0.0.3-1
- Initial package
