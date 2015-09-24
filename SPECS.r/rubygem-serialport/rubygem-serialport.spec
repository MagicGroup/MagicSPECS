%global gem_name serialport

Summary: Ruby library that provides a class for using RS-232 serial ports
Name: rubygem-%{gem_name}
Version: 1.3.1
Release: 5%{?dist}
Group: Development/Languages
License: GPLv2
URL: http://github.com/hparra/ruby-serialport/ 
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires: ruby-devel
BuildRequires: rubygems-devel

%description
Ruby SerialPort is a class for using RS232 serial ports. It also contains 
low-level function to check current state of signals on the line. 

%package doc
BuildArch: noarch
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.


%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
#mkdir -p ./%{gem_dir}
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

# Prevent dangling symlink in -debuginfo.
rm -rf %{buildroot}%{gem_instdir}/ext

chmod a-x %{buildroot}%{gem_libdir}/serialport.rb


%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_extdir_mri}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/LICENSE
%exclude %{gem_cache}
%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_instdir}/CHANGELOG
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/CHECKLIST
%exclude %{gem_instdir}/MANIFEST
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/Gemfile
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/CHANGELOG

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2


* Thu Aug 21 2014 Alejandro Pérez <aeperezt@fedoraproject.org> - 1.3.1-3
--fixed lib path
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 8 2014 Alejandro Pérez <aeperezt@fedoraproject.org> - 1.3.1-1
- Initial package
