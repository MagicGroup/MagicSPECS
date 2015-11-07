#Generated from fake_ftp-0.1.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fake_ftp

Name: rubygem-%{gem_name}
Version: 0.1.1
Release: 5%{?dist}
Summary: Creates a fake FTP server for use in testing
Group: Development/Languages
License: MIT
URL: http://rubygems.org/gems/fake_ftp
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) >= 1.3.6
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.6
BuildRequires: ruby
BuildRequires: rubygem-coderay
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Testing FTP? Use this!


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

#remove .files
rm -f .%{gem_instdir}/.gitignore
rm -f .%{gem_instdir}/.rspec
rm -f .%{gem_instdir}/.travis.yml

%install
mkdir -p %{buildroot}%{gem_dir}

cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/




# Run the test suite
%check
pushd .%{gem_instdir}
#tests require networking capabilities, disabling for now
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%exclude %{gem_cache}
%doc %{gem_instdir}/README.md


%files doc
%doc %{gem_docdir}
%{gem_instdir}/spec
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/Gemfile.lock
%{gem_instdir}/Guardfile
%{gem_instdir}/fake_ftp.gemspec
%doc %{gem_instdir}/CONTRIBUTORS.md

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.1.1-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.1.1-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 17 2015 Tomas Hrcka <thrcka@redhat.com> - 0.1.1-2
- Move CONTRIBUTORS.md to doc subpackage
- Fixed description
- Removed trailing whitespace

* Thu Feb 12 2015 Tomas Hrcka <thrcka@redhat.com> - 0.1.1-1
- Initial package

