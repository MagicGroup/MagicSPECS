%global gem_name macaddr

Name:           rubygem-%{gem_name}
Version:        1.7.1
Release:        4%{?dist}
Summary:        MAC Address Determination for Ruby

Group:          Development/Languages
License:        Ruby or BSD
URL:            https://github.com/ahoward/macaddr
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
# full license text not in the sources
# https://github.com/ahoward/macaddr/issues/27
Source1:        https://raw.githubusercontent.com/ruby/ruby/trunk/COPYING
Source2:        https://raw.githubusercontent.com/ruby/ruby/trunk/BSDL

BuildArch:      noarch
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(systemu) >= 2.6.2
BuildRequires:  rubygem(systemu) < 2.7
BuildRequires:  rubygem(test-unit)
%if 0%{?fedora} && 0%{?fedora} <= 20 || 0%{?rhel} && 0%{?rhel} <= 7
Requires:       ruby(release)
Requires:       ruby(rubygems)
Requires:       rubygem(systemu) >= 2.6.2
Requires:       rubygem(systemu) < 2.7
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
Cross platform mac address determination for Ruby.


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

cp -p %{SOURCE1} %{SOURCE2} %{buildroot}%{gem_instdir}/


%check
pushd .%{gem_instdir}
ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd


%files
%dir %{gem_instdir}/
%doc %{gem_instdir}/LICENSE
%license %{gem_instdir}/COPYING
%license %{gem_instdir}/BSDL
%{gem_libdir}/
%exclude %{gem_cache}
%{gem_spec}
%exclude %{gem_instdir}/test/
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/rvmrc.example
%exclude %{gem_instdir}/%{gem_name}.gemspec

%files doc
%doc %{gem_docdir}/
%doc %{gem_instdir}/README


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.7.1-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Feb 08 2015 František Dvořák <valtri@civ.zcu.cz> - 1.7.1-2
- Update for F22, proper BR for test/unit

* Mon Dec 29 2014 František Dvořák <valtri@civ.zcu.cz> - 1.7.1-1
- Initial package
