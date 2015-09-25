# Generated from qpid_proton-0.0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name qpid_proton
%global proton_version 0.10

%{!?gem_extdir_mri: %global gem_extdir_mri %{_libdir}/gems/ruby/%{gem_name}-%{version}}

Summary:       Ruby language bindings for the Qpid Proton messaging framework
Name:          rubygem-%{gem_name}
Version:       0.10.1
Release:       2%{?dist}
License:       ASL 2.0

URL:           http://qpid.apache.org/proton
# rubygems.org is currently read-only and the newer gem cannot be pushed ATM.
Source0:       http://rubygems.org/gems/%{gem_name}-%{version}.gem

%if 0%{?fedora} > 0
BuildRequires: ruby(release)
%endif

BuildRequires: ruby-devel
BuildRequires: rubygems-devel
BuildRequires: qpid-proton-c-devel >= %{proton_version}
BuildRequires: libuuid-devel
BuildRequires: swig

Requires:      qpid-proton-c = %{proton_version}
Requires:      rubygem(json)



%description
Proton is a high performance, lightweight messaging library. It can be used in
the widest range of messaging applications including brokers, client libraries,
routers, bridges, proxies, and more. Proton is based on the AMQP 1.0 messaging
standard.



%package doc
Summary:   Documentation for %{name}

# RHEL6 rdoc doesn't seem to work well with noarch doc packages
%if 0%{?rhel} != 6
BuildArch: noarch
%endif

%description doc
%{summary}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# apply any patches here

%build
gem build %{gem_name}.gemspec

export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}

%if 0%{?fedora} > 20
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/
%endif

rm -rf %{buildroot}%{gem_instdir}/ext


%check


%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE


%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/ChangeLog
%doc %{gem_instdir}/TODO

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.10.1-2
- 为 Magic 3.0 重建

* Thu Sep 10 2015 Irina Boverman <iboverma@redhat.com> - 0.10.1-1
- Rebased to 0.10.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr  7 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.9-1
- Rebased on qpid_proton 0.9.0.
- Added dependency on rubygem(json).

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Wed Nov 19 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.8-1
- Rebased on Proton 0.8.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.7-4
- Removed intra-package comments.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May  1 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.7-2
- Made the -doc package arch-specific for EL6 due to rdoc issues.

* Wed Apr 30 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.7-1
- Rebased on Proton 0.7.

* Tue Apr 15 2014 Vít Ondruch <vondruch@redhat.com> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Mon Feb 10 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.6-2
- Removed requirement on the main package by the doc subpackage.
- Removed Group declarations.

* Fri Jan 17 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.6-1
- Rebased on Proton 0.6.

* Thu Aug 29 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.5-1
- Rebased on Proton 0.5.

* Mon Apr  1 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-2.2
- Fixed the dependencies to be qpid-proton-c and qpid-proton-c-devel.

* Wed Mar  6 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-2.1
- Changed ruby(release) to ruby(abi) for Fedora < 19.
- Resolves: BZ#906843

* Wed Mar  6 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-2
- First official build for Fedora.
- Resolves: BZ#906843

* Sat Mar  2 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-1.1
- Changed the BR for Ruby to match F19 packaging guidelines.
- Changed install to use the gem_install macro.
- Fixed the installation of the native library.

* Fri Mar  1 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-1
- Rebased on Proton 0.4.

* Mon Feb 25 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-1.1
- Updated to meet the new Fedora 19 packaging guidelines.

* Fri Feb  1 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-1
- Initial package
