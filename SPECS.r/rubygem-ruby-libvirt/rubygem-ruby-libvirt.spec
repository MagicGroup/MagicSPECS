# Generated from ruby-libvirt-0.4.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ruby-libvirt

Summary: Ruby bindings for LIBVIRT
Name: rubygem-%{gem_name}
Version: 0.5.2
Release: 7%{?dist}
Group: Development/Languages
License: LGPLv2+
URL: http://libvirt.org/ruby/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: libvirt-daemon-kvm
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: libvirt-devel
Provides: ruby-libvirt%{?_isa} = %{version}-%{release}
Obsoletes: ruby-libvirt <= %{version}-7
Obsoletes: ruby-libvirt%{?_isa} <= %{version}-7
Obsoletes: ruby(libvirt) <= %{version}

%description
Ruby bindings for libvirt.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# remove shebangs from test files
pushd %{buildroot}%{gem_instdir}/tests
find -type f -name '*.rb' -print | xargs sed -i '/#!\/usr\/bin\/ruby/d'
popd

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Remove the binary extension sources and build leftovers.
rm -rf %{buildroot}%{gem_instdir}/ext

%check
pushd .%{gem_instdir}
# I disabled the tests because they modify system in possibly
# dangerous way and need to be run with root privileges
# testrb tests
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/COPYING
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/NEWS
%doc %{gem_instdir}/README
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/tests

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.5.2-7
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.5.2-6
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.5.2-5
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Josef Stribny <jstribny@redhat.com> - 0.5.2-4
- Add requirement on libvirt-daemon-kvm

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Josef Stribny <jstribny@redhat.com> - 0.5.2-2
- Fix obsoletes for ruby-libvirt

* Tue Jun 09 2015 Josef Stribny <jstribny@redhat.com> - 0.5.2-1
- Update to 0.5.2

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Vít Ondruch <vondruch@redhat.com> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.0-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.0-1
- Initial package
