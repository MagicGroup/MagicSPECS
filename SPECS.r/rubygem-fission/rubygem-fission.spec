# Generated from fission-0.5.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fission

Name: rubygem-%{gem_name}
Version: 0.5.0
Release: 4%{?dist}
Summary: Command line tool to manage VMware Fusion VMs
Group: Development/Languages
License: MIT
URL: https://github.com/thbishop/fission
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(CFPropertyList)
BuildRequires: rubygem(fakefs)
BuildRequires: rubygem(rspec)
BuildArch: noarch

%description
A simple utility to manage VMware Fusion VMs from the command line.


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


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# Fix RSpec 3.x compatibility.
sed -i 's/be_false/be_falsey/' spec/fission/action/execute_shell_command_spec.rb

rspec spec
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%exclude %{gem_instdir}/fission.gemspec
%{_bindir}/fission
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.5.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.5.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 13 2015 Vít Ondruch <vondruch@redhat.com> - 0.5.0-1
- Initial package
