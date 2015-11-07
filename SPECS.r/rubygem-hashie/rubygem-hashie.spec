# Generated from hashie-2.0.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name hashie

Name: rubygem-%{gem_name}
Version: 2.0.5
Release: 7%{?dist}
Summary: Your friendly neighborhood hash toolkit
Group: Development/Languages
License: MIT
URL: https://github.com/intridea/hashie
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby
BuildRequires: rubygem(rspec) < 3.0
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Hashie is a small collection of tools that make hashes more powerful.
Currently includes Mash (Mocking Hash) and Dash (Discrete Hash).

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

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
rspec2 spec/
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/LICENSE
%exclude %{gem_cache}
%exclude %{gem_instdir}/.*
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.markdown
%{gem_instdir}/Gemfile
%{gem_instdir}/Guardfile
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/spec/

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.0.5-7
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.5-6
- 为 Magic 3.0 重建

* Mon Jun 29 2015 Josef Stribny <jstribny@redhat.com> - 2.0.5-5
- Fix FTBFS: use RSpec 2.x

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 08 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 2.0.5-1
- Initial package
