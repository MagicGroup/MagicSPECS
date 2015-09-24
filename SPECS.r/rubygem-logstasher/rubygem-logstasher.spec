%global gem_name logstasher

# tests require rspec >= 3
%if 0%{?fedora} && 0%{?fedora} <= 21 || 0%{?rhel} && 0%{?rhel} <= 7
%global with_tests 0
%else
%global with_tests 1
%endif

Name:           rubygem-%{gem_name}
Version:        0.6.5
Release:        2%{?dist}
Summary:        Awesome rails logs

Group:          Development/Languages
License:        MIT
URL:            https://github.com/shadabahmed/logstasher
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/shadabahmed/logstasher.git && cd logstasher
# git checkout v0.6.5
# tar -czf rubygem-logstasher-0.6.5-repo.tgz sample_logstash_configurations/ spec/ LICENSE README.md
Source1: %{name}-%{version}-repo.tgz
# bundler killer patch
# (not intended for upstream)
Patch0:         logstasher-tests-unbundle.diff
# https://github.com/shadabahmed/logstasher/commit/422dc5781126f91f6dacffdc0642dbf8c903426e
Patch1:         logstasher-tests-time.diff

BuildArch:      noarch
BuildRequires:  rubygems-devel
%if 0%{?with_tests}
BuildRequires:  rubygem(logstash-event) => 1.2
BuildRequires:  rubygem(rails) >= 3.0
BuildRequires:  rubygem(redis)
BuildRequires:  rubygem(request_store)
BuildRequires:  rubygem(rspec) >= 3
%endif
# explicit runtime dependency on activesupport
# https://github.com/shadabahmed/logstasher/pull/55
Requires:       rubygem(activesupport) >= 3.0
%if 0%{?fedora} && 0%{?fedora} <= 20 || 0%{?rhel} && 0%{?rhel} <= 7
Requires:       ruby(release)
Requires:       ruby(rubygems)
Requires:       rubygem(logstash-event) => 1.1.0
Requires:       rubygem(request_store)
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
Logstasher gem generates logstash compatible logs in JSON format. It can also
easily log events from Rails.


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
tar xzf %{SOURCE1}
%patch0 -p1
%patch1 -p1

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

cp -a sample_logstash_configurations/ LICENSE README.md \
        %{buildroot}%{gem_instdir}/


%check
%if 0%{?with_tests}
cp -pr spec/ ./%{gem_instdir}
pushd .%{gem_instdir}
rspec -Ilib -Ispec spec
popd
rm -rf spec/
%endif


%files
%license %{gem_instdir}/LICENSE
%dir %{gem_instdir}/
%{gem_libdir}//
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/README.md
%doc %{gem_docdir}/
%{gem_instdir}/sample_logstash_configurations/


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 15 2015 František Dvořák <valtri@civ.zcu.cz> - 0.6.5-1
- Update to 0.6.5
- Patches for tests addressed by upstream

* Fri Jan 09 2015 František Dvořák <valtri@civ.zcu.cz> - 0.6.2-1
- Update to 0.6.2
- Enable tests for Rawhide (Fedora >= 22)
- Use %%license macro
- Don't package the tests

* Tue Sep 16 2014 František Dvořák <valtri@civ.zcu.cz> - 0.6.1-1
- Update to 0.6.1

* Wed Sep 10 2014 František Dvořák <valtri@civ.zcu.cz> - 0.6.0-2
- Explicit runtime dependency on activesupport

* Thu Aug 28 2014 František Dvořák <valtri@civ.zcu.cz> - 0.6.0-1
- Initial package
