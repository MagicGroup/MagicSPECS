
%global enable_checks 1

# Generated from deep_merge-1.0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name deep_merge

Name: rubygem-%{gem_name}
Version: 1.0.1
Release: 8%{?dist}
Summary: Merge Deeply Nested Hashes
Group: Development/Languages
License: MIT
URL: https://github.com/danielsdeleo/deep_merge
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://github.com/danielsdeleo/deep_merge/pull/13
Patch0: deep_merge-minitest5.patch
# LICENSE file is in git repository but not in package.
# https://github.com/danielsdeleo/deep_merge/pull/14
Source1: https://raw.githubusercontent.com/danielsdeleo/deep_merge/master/LICENSE
%if 0%{?el6}
Requires:      ruby(abi) = 1.8
%endif
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires:      ruby(release)
%endif
Requires: ruby(rubygems) 
BuildRequires: rubygems-devel 
BuildRequires: ruby 
%if 0%{?enable_checks}
%if 0%{?fc19} || 0%{?fc20} || 0%{?el6} || 0%{?el7}
BuildRequires: rubygem(minitest) < 5
%else
BuildRequires: rubygem(minitest) >= 5
%endif
%endif

BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el6} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Recursively merge hashes. 

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%if 0%{?fc19} || 0%{?fc20} ||  0%{?el6} || 0%{?el7}
%else
%patch0 -p1
%endif
cp -p %{SOURCE1} LICENSE


%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
%if 0%{?enable_checks}
ruby -Ilib test/test_deep_merge.rb
%endif

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache} 
%exclude %{gem_instdir}/CHANGELOG
%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/Rakefile
%{gem_spec}
%doc LICENSE
%doc

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md 


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.0.1-8
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.1-7
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 19 2014 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-5
- Ensure rubygem(minitest) is > 5 version on fc21.

* Tue Jun 3 2014 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-4
- Include LICENSE file in main package.

* Mon Jun 2 2014 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-3
- Drop usage of testrb and use ruby instead for checks.

* Fri May 30 2014 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-2
- latest ruby guidelines and minitest5 patch

* Wed Feb 12 2014 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-1
- Initial package
