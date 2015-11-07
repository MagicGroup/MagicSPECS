# Generated from hitimes-1.2.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name hitimes

Name: rubygem-%{gem_name}
Version: 1.2.2
Release: 3%{?dist}
Summary: A fast, high resolution timer library for recording performance metrics
Group: Development/Languages
License: ISC
URL: http://github.com/copiousfreetime/hitimes
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: rubygem(minitest)
Provides: rubygem(%{gem_name}) = %{version}

%description
Hitimes is a fast, high resolution timer library for recording performance
metrics.  It uses the appropriate low method calls for each system to get the
highest granularity time increments possible.

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
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}/%{gem_name}

cp -a .%{gem_extdir_mri}/%{gem_name}/2.2/%{gem_name}.so %{buildroot}%{gem_extdir_mri}/%{gem_name}/%{gem_name}.so
cp -a .%{gem_extdir_mri}/gem.build_complete %{buildroot}%{gem_extdir_mri}/

rm -rf %{buildroot}/%{gem_instdir}/{ext/,Rakefile}

%check
pushd ./%{gem_instdir}
# Remove simplecov uneeded dependency
sed -i '1,5d' spec/spec_helper.rb
ruby -I$(dirs +1)%{gem_extdir_mri}:lib:spec -e 'Dir.glob "./spec/*spec.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%license %{gem_instdir}/LICENSE
%{gem_extdir_mri}
%{gem_spec}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.travis.yml

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/HISTORY.md
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.md
%{gem_instdir}/spec/
%{gem_instdir}/tasks/
%{gem_instdir}/examples/

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.2.2-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.2-2
- 为 Magic 3.0 重建

* Wed Feb 18 2015 Josef Stribny <jstribny@redhat.com> - 1.2.2-1
- Update to 1.2.2
- Fix the packaging for Ruby 2.2

* Mon Jan 20 2014 Achilleas Pipinellis <axilleaspi@ymail.com> - 1.2.1-1
- Initial package
