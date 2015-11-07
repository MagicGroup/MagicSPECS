#
# spec file for package libtqt-perl (version R14)
#
# Copyright (c) 2014 Trinity Desktop Environment
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg libtqt-perl
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeincludedir %{tde_includedir}/tde


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	3.008
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.2
Summary:	Perl bindings for the TQt library
Summary(zh_CN.UTF-8): TQt 库的 Perl 绑定
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}

BuildRequires:	automake autoconf libtool
BuildRequires:	gcc-c++
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig

BuildRequires:	trinity-libsmoketqt-devel >= %{tde_version}

BuildRequires:	perl(ExtUtils::MakeMaker)

Requires:		perl-TQt = %{?epoch:%{epoch}:}%{version}-%{release}


%description
This module lets you use the TQt library from Perl.
It provides an object-oriented interface and is easy to use.

%description -l zh_CN.UTF-8
TQt 的 Perl 绑定。

%files
%defattr(-,root,root,-)
%{tde_bindir}/puic
%{tde_mandir}/man1/puic.1*
%{_bindir}/pqtapi
%{_bindir}/pqtsh
%if 0%{?rhel} == 5
%{_datadir}/doc/libqt-perl/
%endif

##########

%package -n perl-TQt
Summary:	Perl bindings for the TQt library
Summary(zh_CN.UTF-8): TQt 库的 Perl 绑定
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库

Provides:		perl(TQtShell)
Provides:		perl(TQtShellControl)

%description -n perl-TQt
This module lets you use the TQt library from Perl.
It provides an object-oriented interface and is easy to use.

%description -n perl-TQt -l zh_CN.UTF-8
TQt 库的 Perl 绑定。

%files -n perl-TQt
%defattr(-,root,root,-)
%{perl_vendorarch}/TQt.pm
%{perl_vendorarch}/TQt.pod
%dir %{perl_vendorarch}/TQt
%{perl_vendorarch}/TQt/GlobalSpace.pm
%{perl_vendorarch}/TQt/attributes.pm
%{perl_vendorarch}/TQt/constants.pm
%{perl_vendorarch}/TQt/debug.pm
%{perl_vendorarch}/TQt/enumerations.pm
%{perl_vendorarch}/TQt/isa.pm
%{perl_vendorarch}/TQt/properties.pm
%{perl_vendorarch}/TQt/signals.pm
%{perl_vendorarch}/TQt/slots.pm
%{perl_vendorarch}/auto/TQt/
%{_mandir}/man3/TQt.3pm.*

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export TDEDIR=%{tde_prefix}
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility \
  \
  --disable-smoke

# Fix invalid path in RHEL 5
%if 0%{?rhel} == 5
%__sed -i "PerlTQt/Makefile" -e "s|\$(PREFIX)/|\$(DESTDIR)\$(PREFIX)/|"
%endif

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Unwanted files
%__rm -f %{buildroot}%{perl_archlib}/perllocal.pod
%__rm -f %{buildroot}%{perl_vendorarch}/auto/TQt/.packlist
magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%Changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:3.008-1.2
- 为 Magic 3.0 重建

* Wed Oct 14 2015 Liu Di <liudidi@gmail.com> - 2:3.008-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 3.008-1
- Initial release for TDE 14.0.0
