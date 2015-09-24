%global gem_name unicode

Name:           rubygem-%{gem_name}
Version:        0.4.4.1
Release:        5%{?dist}
Summary:        Unicode normalization library for Ruby
License:        Ruby
URL:            http://www.yoshidam.net/Ruby.html#unicode
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://github.com/blackwinter/unicode/issues/7
Source1:        https://www.ruby-lang.org/en/about/license.txt
# This is a C extension linked against MRI, it's not compatible with other 
# interpreters. So we require MRI specifically instead of ruby(release).
Requires:       ruby
BuildRequires:  ruby-devel
BuildRequires:  rubygems-devel
# rubygem Requires/Provides are automatically generated in F21+
%if ! (0%{?fedora} >= 21 || 0%{?rhel} >= 8)
Requires:       rubygems
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
Unicode normalization library for Ruby.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
cp -p %{SOURCE1} .

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/specifications %{buildroot}%{gem_dir}/
mkdir -p %{buildroot}%{gem_instdir}
cp -pa .%{gem_instdir}/lib %{buildroot}%{gem_instdir}/
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 8
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -pa .%{gem_extdir_mri}/%{gem_name} .%{gem_extdir_mri}/gem.build_complete %{buildroot}%{gem_extdir_mri}/
%else
mkdir -p %{buildroot}%{gem_extdir_mri}/lib
mv %{buildroot}%{gem_instdir}/lib/unicode %{buildroot}%{gem_extdir_mri}/lib/
%endif

%check
%if 0%{?rhel}
ruby -I.%{gem_instdir}/lib:.%{gem_extdir_mri} test/test.rb
%else
ruby-mri -I.%{gem_instdir}/lib:.%{gem_extdir_mri} test/test.rb
%endif

%files
%doc README license.txt
%{gem_instdir}
%{gem_extdir_mri}
%{gem_spec}

%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.4.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Fri Jan 09 2015 Dan Callaghan <dcallagh@redhat.com> - 0.4.4.1-3
- RHBZ#1179543 include gem.build_complete file so that rubygems doesn't attempt 
  to rebuild the gem

* Mon Jul 14 2014 Dan Callaghan <dcallagh@redhat.com> - 0.4.4.1-2
- run test program in %%check
- use HTTPS for Ruby license source URL

* Thu Jun 05 2014 Dan Callaghan <dcallagh@redhat.com> - 0.4.4.1-1
- updated to upstream release 0.4.4.1
- fixed spec for rubygem changes in F21+

* Tue Jan 28 2014 Dan Callaghan <dcallagh@redhat.com> - 0.4.4-1
- Initial package
