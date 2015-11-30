Name:           mokutil
Version:        0.2.0
Release:        3%{?dist}
Epoch:          1
Summary:        Tool to manage UEFI Secure Boot MoK Keys
License:        GPLv3+
URL:            https://github.com/lcp/mokutil
ExclusiveArch:  %{ix86} x86_64 aarch64
BuildRequires:  autoconf automake gnu-efi git openssl-devel openssl
Source0:        https://github.com/lcp/mokutil/archive/%{version}.tar.gz
Conflicts:      shim < 0.8-1%{?dist}
Obsoletes:      mokutil < 0.2.0

%description
mokutil provides a tool to manage keys for Secure Boot through the MoK
("Machine's Own Keys") mechanism.

%prep
%setup -q -n %{name}-%{version}
git init
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make PREFIX=%{_prefix} LIBDIR=%{_libdir} DESTDIR=%{buildroot} install

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%{_bindir}/mokutil
%{_mandir}/man1/*

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1:0.2.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Oct 06 2014 Peter Jones <pjones@redhat.com> - 0.2.0-1
- First independent package.
