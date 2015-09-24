%global gem_name charlock_holmes

Name: rubygem-%{gem_name}
Version: 0.7.3
Release: 7%{?dist}
Summary: Character encoding detection, brought to you by ICU
Group: Development/Languages
License: MIT
URL: https://github.com/brianmario/charlock_holmes
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: libicu-devel
BuildRequires: zlib-devel
BuildRequires: rubygem(minitest)

# The Python code in the tests subdirectory references /usr/bin/env.
# Filter this from RPM's autorequires.
%global __requires_exclude ^/usr/bin/env$

%description
Character encoding detecting library for Ruby using ICU

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

# Remove unecessary bundler dependency
sed -i '/bundler/d' test/helper.rb

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

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -pa .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

# Remove the binary extension sources and build leftovers.
rm -rf %{buildroot}/%{gem_instdir}/ext/

# Fix permission
chmod +x %{buildroot}/%{gem_instdir}/test/fixtures/laholator.py

%check
pushd .%{gem_instdir}
# Set locale to UTF due to failing tests in mock
# https://github.com/brianmario/charlock_holmes/issues/39
LANG=en_US.utf8
ruby -I"lib:%{buildroot}%{gem_extdir_mri}" test/*.rb
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_extdir_mri}
%{gem_spec}
%doc %{gem_instdir}/MIT-LICENSE
%exclude %{gem_cache}
%exclude %{gem_instdir}/.*

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/benchmark/
%{gem_instdir}/test/
%exclude %{gem_instdir}/%{gem_name}.gemspec


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.7.3-6
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 0.7.3-5
- rebuild for ICU 54.1

* Thu Jan 15 2015 Vít Ondruch <vondruch@redhat.com> - 0.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 0.7.3-3
- rebuild for ICU 53.1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.7.3-1
- Update to charlock_holmes 0.7.3 (RHBZ #1105821)
- Use HTTPS URL

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.7.1-1
- Update to charlock_holmes 0.7.1 (RHBZ #1100754)

* Mon May 12 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.7.0-1
- Update to charlock_holmes 0.7.0 (supports Minitest 5)
- rm gem2rpm auto-generated comment
- exclude extra gemspec

* Wed Apr 09 2014 Achilleas Pipinellis <axilleas@fedoraproject.org> - 0.6.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Use minitest4

* Fri Feb 14 2014 David Tardon <dtardon@redhat.com> - 0.6.9.4-4
- rebuild for new ICU

* Wed Aug 07 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 0.6.9.4-3
- Filter /usr/bin/env from RPM's autorequires
- Removed extra newline from description

* Sun Aug 04 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 0.6.9.4-2
- Move bundler removal to %prep
- Include github issue of failing tests

* Mon Jul 22 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 0.6.9.4-1
- Initial package
