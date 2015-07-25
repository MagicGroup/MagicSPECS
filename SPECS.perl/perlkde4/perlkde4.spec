#
# spec file for package perl-kde4
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           perlkde4
Version: 4.14.3
Release:        1%{?dist}
Summary:        Kdebindings Perl-KDE library
License:        LGPL-2.1+
Group:          Development/Libraries/KDE
Url:            https://projects.kde.org/projects/kde/kdebindings/perl/perlkde
Source0:        http://download.kde.org/stable/%{version}/src/perlkde-%{version}.tar.xz
BuildRequires:  kde4-kate-devel
BuildRequires:  jasper-devel
BuildRequires:  kdepimlibs4-devel
BuildRequires:  qimageblitz-devel
BuildRequires:  smokegen-devel
BuildRequires:  kde4-smokekde-devel
BuildRequires:  smokeqt-devel
BuildRequires:  kde4-okular-devel
BuildRequires:  perl
BuildRequires:  perlqt-devel
BuildRequires:  sqlite-devel
BuildRequires:  xz
Requires:       perlqt = %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       perl

%description
Perl bindings for libraries created by the KDE community.

%prep
%setup -q -n perlkde-%{version}

%build
mkdir build
cd build
EXTRA_FLAGS="-DCUSTOM_PERL_SITE_ARCH_DIR=`perl -MConfig -e 'print $Config{vendorarch}'`"
%cmake_kde4 $EXTRA_FLAGS ..
%__make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{kde4_plugindir}/kperlpluginfactory.so
%{perl_vendorarch}/*.pm
%{perl_vendorarch}/auto/

%changelog
* Wed Dec 31 2014 Liu Di <liudidi@gmail.com> - 4.14.3-1
- 更新到 4.14.3

* Fri Oct 31 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Sun Apr 27 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建


