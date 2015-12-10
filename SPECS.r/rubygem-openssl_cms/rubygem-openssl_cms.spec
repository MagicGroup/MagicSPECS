%global gem_basename openssl_cms
%global gem_rubyver 2_2
%global gem_name %{gem_basename}_%{gem_rubyver}

Name:           rubygem-%{gem_basename}
Version:        0.0.3
Release:        5%{?dist}
Summary:        OpenSSL with CMS functions
Group:          Development/Languages

License:        Ruby or BSD
URL:            https://github.com/arax/openssl-cms
# gem_basename="openssl_cms"
# gem_rubyver="2_2"
# gem_name="${gem_basename}_${gem_rubyver}"
# version="0.0.3"
#
# git clone --branch ruby_${gem_rubyver} https://github.com/arax/openssl-cms && cd openssl-cms
# gem build ${gem_basename}.gemspec
Source0:        %{gem_name}-%{version}.gem

BuildRequires:  openssl-devel
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby-devel => 2.2

%description
OpenSSL with Cryptographic Message Syntax functions for Ruby.


%package -n rubygem-%{gem_name}
Summary:        OpenSSL with CMS functions for Ruby 2.2
Group:          Development/Languages
Requires:       ruby(release) >= 2.2

%description -n rubygem-%{gem_name}
OpenSSL with Cryptographic Message Syntax functions for Ruby 2.2.


%package -n rubygem-%{gem_name}-doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       rubygem-%{gem_name} = %{version}-%{release}
BuildArch:      noarch

%description -n rubygem-%{gem_name}-doc
Documentation for %{name}.


%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/


# No testsuite
#%%check


%files -n rubygem-%{gem_name}
%license %{gem_instdir}/BSDL
%license %{gem_instdir}/LICENSE
%dir %{gem_instdir}/
%{gem_libdir}/
%{gem_extdir_mri}/
%exclude %{gem_cache}
%{gem_spec}
%exclude %{gem_instdir}/.gitignore

%files -n rubygem-%{gem_name}-doc
%doc %{gem_docdir}/
%{gem_instdir}/README.md
%exclude %{gem_instdir}/%{gem_basename}.gemspec


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.0.3-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.0.3-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.0.3-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 11 2015 František Dvořák <valtri@civ.zcu.cz> - 0.0.3-1
- Update to 0.0.3

* Wed Jan 28 2015 František Dvořák <valtri@civ.zcu.cz> - 0.0.2-3.20140212gitb789b69
- Add support for ruby 2.2

* Sun Jan 18 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.2-3.20140212git7fea071
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Wed Oct 08 2014 František Dvořák <valtri@civ.zcu.cz> - 0.0.2-2.20140212git7fea071
- Bump the version for proper update

* Wed Oct 08 2014 František Dvořák <valtri@civ.zcu.cz> - 0.0.2-1.20140212git7fea071
- Initial package
