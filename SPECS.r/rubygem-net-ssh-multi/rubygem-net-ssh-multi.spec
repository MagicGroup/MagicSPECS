# Generated from net-ssh-multi-1.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name net-ssh-multi

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

Summary: Control multiple Net::SSH connections via a single interface
Name: rubygem-%{gem_name}
Version: 1.2.0
Release: 5%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/net-ssh/net-ssh-multi
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0: rubygem-net-ssh-multi-1.2.0-minitest.patch
%if 0%{?fedora} >= 19
Requires: ruby(release)
BuildRequires: ruby(release)
%else
Requires: ruby(abi) >= %{rubyabi}
BuildRequires: ruby(abi) >= %{rubyabi}
%endif
Requires: ruby(rubygems)
Requires: rubygem(net-ssh) >= 2.6.5
Requires: rubygem(net-ssh-gateway) >= 1.2.0
%{!?el6:BuildRequires: rubygems-devel}
BuildRequires: rubygem(net-ssh)
BuildRequires: rubygem(net-ssh-gateway)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Control multiple Net::SSH connections via a single interface.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}

%prep
%setup -q -c -T
mkdir -p .%{gem_dir}
gem install --local \
  --install-dir $(pwd)%{gem_dir} \
  --force --rdoc \
   %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd %{buildroot}%{gem_instdir}
ruby -Ilib:test test/test_all.rb
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%exclude %{gem_cache}
%exclude %{gem_instdir}/net-ssh-multi.gemspec

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/CHANGES.txt
%doc %{gem_instdir}/LICENSE.txt
%{gem_instdir}/gem-public_cert.pem
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.0-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 13 2014 Julian C. Dunn <jdunn@aquezada.com> - 1.2.0-3
- Convert to Minitest (bz#1107179)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 21 2013 Julian C. Dunn <jdunn@aquezada.com> - 1.2.0-1
- Update to 1.2.0 (bz#1015287)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 16 2013 Julian C. Dunn <jdunn@aquezada.com> - 1.1-4
- Unbreak build on >= F19

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 27 2012 Julian C. Dunn <jdunn@aquezada.com> - 1.1-2
- Unified EPEL and Fedora builds

* Sat Apr 14 2012  <rpms@courteau.org> - 1.1-1
- Initial package
