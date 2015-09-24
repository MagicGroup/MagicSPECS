# Generated from hashicorp-checkpoint-0.1.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name hashicorp-checkpoint

Name: rubygem-%{gem_name}
Version: 0.1.4
Release: 2%{?dist}
Summary: Internal HashiCorp service to check version information
Group: Development/Languages
License: MPLv2.0
URL: http://www.hashicorp.com
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel 
# BuildRequires: rubygem(rspec) => 3.0.0
# BuildRequires: rubygem(rspec) < 3.1
# BuildRequires: rubygem(rspec-its) => 1.0.0
# BuildRequires: rubygem(rspec-its) < 1.1
BuildArch: noarch

%description
Internal HashiCorp service to check version information.

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

# We need RSpec3
# Run the test suite
#%%check
#pushd .%%{gem_instdir}
#rspec spec
#popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/ruby-checkpoint.gemspec
%exclude %{gem_instdir}/.gitignore
%{gem_spec}
%license %{gem_instdir}/LICENSE.txt

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/spec

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 09 2014 Josef Stribny <jstribny@redhat.com> - 0.1.4-1
- Initial package
