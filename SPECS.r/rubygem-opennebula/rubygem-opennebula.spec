%global gem_name opennebula

Name:           rubygem-%{gem_name}
Version:        4.12.1
Release:        5%{?dist}
Summary:        OpenNebula Client API

Group:          Development/Languages
License:        ASL 2.0
URL:            http://opennebula.org
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildArch:      noarch
BuildRequires:  rubygems-devel
%if 0%{?fedora} && 0%{?fedora} <= 20 || 0%{?rhel} && 0%{?rhel} <= 7
Requires:       ruby(release)
Requires:       ruby(rubygems)
Requires:       rubygem(nokogiri)
Requires:       rubygem(json)
Requires:       rubygem(rbvmomi)
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
Libraries needed to talk to OpenNebula.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

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


# no testsuite
#%%check


%files
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/NOTICE
%dir %{gem_instdir}/
%{gem_libdir}/
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}/


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 4.12.1-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 4.12.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.12.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 09 2015 František Dvořák <valtri@civ.zcu.cz> - 4.12.1-1
- Update to 4.12.1 (#1209626)

* Sat Jan 24 2015 František Dvořák <valtri@civ.zcu.cz> - 4.10.2-1
- Update to 4.10.2

* Thu Nov 27 2014 František Dvořák <valtri@civ.zcu.cz> - 4.10.1-1
- Update to 4.10.1

* Tue Sep 16 2014 František Dvořák <valtri@civ.zcu.cz> - 4.8.0-1
- Initial package
