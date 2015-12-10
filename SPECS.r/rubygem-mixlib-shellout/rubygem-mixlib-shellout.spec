# Generated from mixlib-shellout-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name mixlib-shellout
# EPEL6 lacks rubygems-devel package that provides these macros
%if %{?el6}0
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_libdir %{gem_instdir}/lib
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%endif

%if %{?el6}0 || %{?fc16}0
%global rubyabi 1.8
%else
%global rubyabi 1.9.1
%endif

Summary: Run external commands on Unix or Windows
Name: rubygem-%{gem_name}
Version: 2.0.1
Release: 5%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: https://github.com/chef/mixlib-shellout
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Tests for this package are not in the gem. To update:
# git clone https://github.com/chef/mixlib-shellout.git && cd mixlib-shellout
# git checkout 2.0.1
# tar czvf rubygem-mixlib-shellout-2.0.1-specs.tgz spec/
Source1: rubygem-%{gem_name}-%{version}-specs.tgz

%if 0%{?fedora} >= 19
Requires: ruby(release)
BuildRequires: ruby(release)
%else
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(abi) = %{rubyabi}
%endif

Requires: ruby(rubygems)
BuildRequires: ruby(rubygems)
%{!?el6:BuildRequires: rubygem(rspec)}
%{!?el6:BuildRequires: rubygems-devel}
BuildRequires: procps
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Run external commands on Unix or Windows

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T

%if 0%{?fedora} >= 19
%gem_install -n %{SOURCE0}
%else
mkdir -p .%{gem_dir}
gem install --local --install-dir .%{gem_dir} \
            --force %{SOURCE0}
%endif

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
tar zxvf %{SOURCE1}
# One of the tests involves a fork && sleep 10 that may not finish before mock
rspec && sleep 10
popd

%files
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.0.1-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.0.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 23 2015 Julian C. Dunn <jdunn@aquezada.com> - 2.0.1-1
- Upgrade to 2.0.1 (bz#1150550)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 08 2014 Julian C. Dunn <jdunn@aquezada.com> - 1.4.0-1
- Upgrade to 1.4.0 (bz#1087380)

* Wed Dec 04 2013 Julian C. Dunn <jdunn@aquezada.com> - 1.3.0-1
- Upgrade to 1.3.0 (bz#1038148)

* Sun Sep 01 2013 Julian C. Dunn <jdunn@aquezada.com> - 1.2.0-1
- Upgrade to 1.2.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Josef Stribny <jstribny@redhat.com> - 1.1.0-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Julian C. Dunn <jdunn@aquezada.com> - 1.1.0-4
- make sure to BuildRequires ruby(rubygems) as well

* Thu Dec 20 2012 Julian C. Dunn <jdunn@aquezada.com> - 1.1.0-3
- fix incorrect ruby(abi) requires

* Tue Dec 18 2012 Julian C. Dunn <jdunn@aquezada.com> - 1.1.0-2
- add patches for rspec test issues on Fedora

* Sun Oct 21 2012 Julian C. Dunn <jdunn@aquezada.com> - 1.1.0-1
- rebuild with 1.1.0

* Sun Jun 17 2012 Jonas Courteau <rpms@courteau.org> - 1.0.0-3
- move all test-related operations into check
- excluding gem_cache

* Sun Jun 3 2012 Jonas Courteau <rpms@courteau.org> - 1.0.0-2
- exclude specs from final package
- link to upstream bug reports for missing specs, broken test

* Sat May 12 2012  Jonas Courteau <rpms@courteau.org> - 1.0.0-1
- Initial package
