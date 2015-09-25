# Generated from ansi-1.4.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ansi

# Disable checks since dependencies not
# available and some of them depend on this.
%global enable_checks 0

Name: rubygem-%{gem_name}
Version: 1.5.0
Release: 3%{?dist}
Summary: ANSI at your fingertips!
Group: Development/Languages
License: BSD
URL: http://rubyworks.github.com/ansi
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?el6}
Requires:      ruby(abi) = 1.8
Requires:      rubygems
%endif
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires:      ruby(release)
Requires:      rubygems
%endif
BuildRequires: rubygems-devel 
BuildRequires: ruby 

%if 0%{?enable_checks}
BuildRequires: rubygem(detroit) 
BuildRequires: rubygem(qed) 
BuildRequires: rubygem(lemon) 
%endif
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el6} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
The ANSI project is a superlative collection of ANSI escape code related
libraries enabling ANSI colorization and styling of 
console output. Byte for byte ANSI is the best ANSI code 
library available for the Ruby programming
language.

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
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/




# Run the test suite
%check
%if 0%{?enable_checks}
pushd .%{gem_instdir}
testrb -Ilib test
popd
%endif

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.yardopts
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE.txt
%exclude %{gem_instdir}/.index

%files doc
%doc %{gem_docdir}
%{gem_instdir}/.index
%doc %{gem_instdir}/HISTORY.md
%doc %{gem_instdir}/DEMO.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/NOTICE.md
%doc %{gem_instdir}/demo
%doc %{gem_instdir}/test


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.5.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Steve Traylen <steve.traylen@cern.ch> - 1.5.0-1
- New release 1.5.0

* Mon Jul 28 2014 Steve Traylen <steve.traylen@cern.ch> - 1.4.3-2
- Add rubygems BR.

* Thu Jul 03 2014 Steve Traylen <steve.traylen@cern.ch> - 1.4.3-1
- Initial package
