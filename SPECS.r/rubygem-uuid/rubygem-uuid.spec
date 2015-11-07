%global gem_name uuid

Name:           rubygem-%{gem_name}
Version:        2.3.7
Release:        4%{?dist}
Summary:        UUID generator based on RFC 4122

Group:          Development/Languages
License:        MIT or CC-BY-SA
URL:            http://github.com/assaf/uuid
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://github.com/assaf/uuid/pull/39
Patch0:         %{name}-tool.patch

BuildArch:      noarch
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(macaddr)
BuildRequires:  rubygem(mocha)
BuildRequires:  rubygem(test-unit)
%if 0%{?fedora} && 0%{?fedora} <= 20 || 0%{?rhel} && 0%{?rhel} <= 7
Requires:       ruby(release)
Requires:       ruby(rubygems)
Requires:       rubygem(macaddr) >= 1.0
Requires:       rubygem(macaddr) < 2
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
UUID generator for producing universally unique identifiers based on RFC 4122
(http://www.ietf.org/rfc/rfc4122.txt).


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
%patch0 -p1
sed -i -e '1s,.*,#!/usr/bin/ruby,' bin/uuid

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
# rename to fix conflict with uuid package
mv .%{_bindir}/uuid \
        %{buildroot}%{_bindir}/uuid.rb

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x


%check
pushd .%{gem_instdir}
# https://github.com/assaf/uuid/issues/43
sed -i -e "s,'mocha','mocha/setup'," test/*.rb
ruby -Ilib:test -e 'Dir.glob "./test/*.rb", &method(:require)'
popd


%files
%dir %{gem_instdir}/
%dir %{gem_instdir}/bin/
%license %{gem_instdir}/MIT-LICENSE
%{_bindir}/uuid.rb
%{gem_instdir}/bin/uuid
%{gem_libdir}/
%{gem_spec}
%{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_instdir}/bin/rake
%exclude %{gem_instdir}/bin/yard
%exclude %{gem_instdir}/bin/yardoc
%exclude %{gem_instdir}/bin/yri
%exclude %{gem_instdir}/test/
%exclude %{gem_cache}
%exclude %{gem_instdir}/Rakefile

%files doc
%doc %{gem_docdir}/
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/README.rdoc


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.3.7-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.3.7-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Feb 08 2015 František Dvořák <valtri@civ.zcu.cz> - 2.3.7-1
- Initial package
