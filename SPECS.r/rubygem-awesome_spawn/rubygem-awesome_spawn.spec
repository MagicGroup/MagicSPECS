# Generated from awesome_spawn-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name awesome_spawn

Name: rubygem-%{gem_name}
Version: 1.3.0
Release: 4%{?dist}
Summary: A module that provides some useful features over Ruby's Kernel.spawn
Group: Development/Languages
License: MIT
URL: https://github.com/ManageIQ/awesome_spawn
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: rubygems
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(rspec-core)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
AwesomeSpawn is a module that provides some useful features over Ruby's
Kernel.spawn.

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

%build

# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install

mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Remove developer-only files.
pushd %{buildroot}%{gem_instdir}
rm {.rspec,.yardopts}
popd

%check
pushd .%{gem_instdir}
sed -i '/[Cc]overalls/d' spec/spec_helper.rb
rspec spec/
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.md
%exclude %{gem_cache}
%exclude %{gem_instdir}/.rspec
%exclude %{gem_instdir}/.yardopts
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/spec/

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.3.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.3.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Josef Stribny <jstribny@redhat.com> - 1.3.0-1
- Update to 1.3.0

* Fri Aug 08 2014 Achilleas Pipinellis <axilleas@fedoraproject.org> - 1.2.1-1
- Bump version

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Achilleas Pipinellis <axilleas@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Tue Jan 21 2014 Achilleas Pipinellis <axilleaspi@ymail.com> - 1.0.0-2
- Remove unecessary comments
- Fix Requires/BuildRequires typos

* Sun Jan 19 2014 Achilleas Pipinellis <axilleaspi@ymail.com> - 1.0.0-1
- Initial package
