%global gem_name qpid_messaging
%global qpid_version 0.34

Summary:       Ruby bindings for the Qpid messaging framework
Name:          rubygem-%{gem_name}
Version:       %{qpid_version}.1
Release:       3%{?dist}
License:       ASL 2.0

URL:           http://qpid.apache.org
Source0:       http://rubygems.org/gems/%{gem_name}-%{version}.gem


BuildRequires: gcc-c++
BuildRequires: ruby(release)
BuildRequires: ruby-devel
BuildRequires: rubygems-devel
BuildRequires: qpid(cpp-client-devel)%{?_isa} = %{qpid_version}
BuildRequires: swig


%description
Qpid is an enterprise messaging framework. This package provides Ruby
language bindings based on that framework.



%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch


%description doc
%{Summary}.


%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/ChangeLog
%{gem_instdir}/examples
%doc %{gem_instdir}/TODO



%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# apply patches here


%build
gem build %{gem_name}.gemspec

export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

%if 0%{?fedora} > 20
mkdir -p %{buildroot}%{gem_extdir_mri}/
cp -a .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/
%endif

%if 0%{?rhel} > 6
mkdir -p %{buildroot}%{gem_extdir_mri}/lib
mv %{buildroot}%{gem_instdir}/lib/cqpid.so \
   %{buildroot}%{gem_extdir_mri}/lib
%endif

rm -rf %{buildroot}%{gem_instdir}/ext


%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.34.1-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.34.1-2
- 为 Magic 3.0 重建

* Thu Sep 10 2015 Irina Boverman <iboverma@redhat.com> - 0.34.1-1
- Rebased to qpid_messaging 0.34

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.32.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Tue Apr  7 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.32.0-1
- Rebased on qpid_messaging 0.32.0.

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Tue Oct  7 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.30.0-1
- Rebased on Qpid 0.30.

* Mon Aug 18 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28.0-3
- Updated Qpid requirements to use virtual provides.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28.0-2
- Removed all intra-package comments.

* Thu Jun  5 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28.0-1
- Rebased on qpid_messaging 0.28.0
- Added BR for gcc-c++.

* Tue Apr 15 2014 Vít Ondruch <vondruch@redhat.com> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Fri Feb 21 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26.0-1
- Rebased on qpid_messaging 0.26.0.

* Fri Oct 25 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24.2-1
- Rebased on qpid_messaging 0.24.2.
- Fixed ordering of caught exceptions from C++.

* Fri Oct 25 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24.1-2
- Removed the ARM exclusion.

* Fri Oct 25 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24.1-1
- Rebased on qpid_messaging 0.24.1.

* Tue Sep 24 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24.0-1
- Rebased on qpid_messaging 0.24.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.22-2
- Updated build to fix dependency issues on qpid-cpp.

* Tue Jun 18 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.22-1
- Rebased on qpid_messaging 0.22.

* Fri Mar  8 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.20.2-1
- Rebased on qpid_messaging 0.20.2.
- Updated to use the newer rubygems-devel macros.

* Thu Feb  7 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.0-2
- bump qpid_version to 0.20 to match release

* Mon Jan 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.20.0-1
- Rebased on qpid_messaging 0.20.0.

* Mon Jan  7 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.18.1-1.2
- Now installs the repackaged gem.

* Wed Dec 26 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18.1-1.1
- Removed Group field from the doc subpackage.
- Updated the specfile to match current Ruby packaging guidelines.

* Mon Sep 24 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18.1-1
- Rebased on qpid_messaging 0.18.1.
- Added the ChangeLog to the files in the -doc package.

* Mon Aug 13 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16.0-1.2
- Moved the gem install statement to the install section.

* Wed Aug  1 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16.0-1.1
- Added BR for ruby-devel.

* Thu Jul 19 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16.0-1
- Initial repackaging.
