#
# spec file for package perl-qt4
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


Name:           perlqt
Version: 4.3
Release:        4%{?dist}
Summary:        PerlQt kdebindings library
Summary(zh_CN.UTF-8): Perl 的 Qt 绑定
License:        GPL-2.0+
Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Url:            https://projects.kde.org/projects/kde/kdebindings/perl/perlqt
Source0:        http://download.kde.org/stable/%{version}/src/perlqt-%{version}.tar.xz
BuildRequires:  cmake
BuildRequires:  kde4-filesystem
BuildRequires:  smokegen
BuildRequires:  qtwebkit-devel
BuildRequires:  qimageblitz-devel
BuildRequires:  qscintilla-devel
BuildRequires:  smokegen-devel
BuildRequires:  smokeqt-devel
BuildRequires:  perl
BuildRequires:  phonon-devel
BuildRequires:  qwt-devel
BuildRequires:  sqlite-devel
BuildRequires:  xz
Requires:       perl
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Perl bindings for the Qt4 libraries from the kdebindings project.

%description -l zh_CN.UTF-8
Perl 的 Qt 绑定。

%package devel
Summary:        Development libraries for Perl-Qt4
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}

%description devel
This package contains development files for the Perl bindings for the Qt4 libraries.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n perlqt-%{version}

%build
  mkdir build
  cd build
  EXTRA_FLAGS="-DCUSTOM_PERL_SITE_ARCH_DIR=`perl -MConfig -e 'print $Config{vendorarch}'`"
  %cmake_kde4 $EXTRA_FLAGS ..
  %__make %{?_smp_mflags}

%install
  cd build
  make DESTDIR=%{buildroot} install
magic_rpm_clean.sh

%files
%defattr(-,root,root)
%dir %{_datadir}/perlqt
%{_datadir}/perlqt/doxsubpp.pl
%{_kde4_bindir}/prcc4_bin
%{_kde4_bindir}/puic4
%{_kde4_bindir}/qdbusxml2perl
%{perl_vendorarch}/*.pm
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/QtCore4/

%files devel
%defattr(-,root,root)
%{_datadir}/perlqt/cmake/
%{_kde4_includedir}/perlqt/

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 4.3-4
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 4.3-3
- 更新到 4.3

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 4.14.3-2
- 为 Magic 3.0 重建

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


