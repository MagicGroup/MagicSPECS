#
# spec file for package k3b-i18n (version R14)
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
%define tde_version 14.0.0
%endif
%define tde_pkg k3b-i18n
%define tde_prefix /opt/trinity
%define tde_appdir %{tde_datadir}/applications
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		1.0.5
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:		Internationalization support for TDE [Trinity]
Group:			Applications/Archiving
URL:			http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

# Speed build options
%define debug_package %{nil}
%define __spec_install_post %{nil}
AutoReq: no

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

Requires(post): coreutils
Requires(postun): coreutils

Requires:		trinity-k3b


%description
K3b provides a comfortable user interface to perform most CD/DVD
burning tasks. While the experienced user can take influence in all
steps of the burning process the beginner may find comfort in the
automatic settings and the reasonable k3b defaults which allow a quick
start.

##########

%package Danish
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		Danish (da) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-da < %{version}-%{release}
Provides:		trinity-k3b-i18n-da = %{version}-%{release}

%description Danish
This package contains the Danish translations for K3B.

%files Danish
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/da/k3b
%{tde_datadir}/locale/da/LC_MESSAGES/*.mo

##########

%package German
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		German (de) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-de < %{version}-%{release}
Provides:		trinity-k3b-i18n-de = %{version}-%{release}

%description German
This package contains the German translations for K3B.

%files German
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/de/k3b
%{tde_datadir}/locale/de/LC_MESSAGES/*.mo

##########

%package Greek
Group:			Applications/Archiving
Requires:		trinity-k3b >= %{version}
Summary:		Greek (el) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-el < %{version}-%{release}
Provides:		trinity-k3b-i18n-el = %{version}-%{release}

%description Greek
This package contains the greek translations for K3B.

%files Greek
%defattr(-,root,root,-)
#%{tde_tdedocdir}/HTML/el/k3b
%{tde_datadir}/locale/el/LC_MESSAGES/*.mo

##########

%package Spanish
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		Spanish (es) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-es < %{version}-%{release}
Provides:		trinity-k3b-i18n-es = %{version}-%{release}

%description Spanish
This package contains the Spanish translations for K3B.

%files Spanish
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/es/k3b
%{tde_datadir}/locale/es/LC_MESSAGES/*.mo

##########

%package Estonian
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		Estonian (et) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-et < %{version}-%{release}
Provides:		trinity-k3b-i18n-et = %{version}-%{release}

%description Estonian
This package contains the Estonian translations for K3B.

%files Estonian
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/et/k3b
%{tde_datadir}/locale/et/LC_MESSAGES/*.mo

##########

%package French
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		French (fr) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-fr < %{version}-%{release}
Provides:		trinity-k3b-i18n-fr = %{version}-%{release}

%description French
This package contains the French translations for K3B.

%files French
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/fr/k3b
%{tde_datadir}/locale/fr/LC_MESSAGES/*.mo

##########

%package Italian
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		Italian (it) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-it < %{version}-%{release}
Provides:		trinity-k3b-i18n-it = %{version}-%{release}

%description Italian
This package contains the Italian translations for K3B.

%files Italian
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/it/k3b
%{tde_datadir}/locale/it/LC_MESSAGES/*.mo

##########

%package Dutch
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		Dutch (nl) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-nl < %{version}-%{release}
Provides:		trinity-k3b-i18n-nl = %{version}-%{release}

%description Dutch
This package contains the Dutch translations for K3B.

%files Dutch
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/nl/k3b
%{tde_datadir}/locale/nl/LC_MESSAGES/*.mo

##########

%package Polish
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		Polish (pl) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-pl < %{version}-%{release}
Provides:		trinity-k3b-i18n-pl = %{version}-%{release}

%description Polish
This package contains the Polish translations for K3B.

%files Polish
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/pl/k3b
%{tde_datadir}/locale/pl/LC_MESSAGES/*.mo

##########

%package Portuguese
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		Portuguese (pt) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-pt < %{version}-%{release}
Provides:		trinity-k3b-i18n-pt = %{version}-%{release}

%description Portuguese
This package contains the Portuguese translations for K3B.

%files Portuguese
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/pt/k3b
%{tde_datadir}/locale/pt/LC_MESSAGES/*.mo

##########

%package Brazil
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		Brazilian Portuguese (pt_BR) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-pt_BR < %{version}-%{release}
Provides:		trinity-k3b-i18n-pt_BR = %{version}-%{release}
Obsoletes:		trinity-k3b-i18n-ptbr < %{version}-%{release}
Provides:		trinity-k3b-i18n-ptbr = %{version}-%{release}

%description Brazil
This package contains the Brazilian Portuguese translations for K3B.

%files Brazil
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/pt_BR/k3b
%{tde_datadir}/locale/pt_BR/LC_MESSAGES/*.mo

##########

%package Russian
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		Russian (ru) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-ru < %{version}-%{release}
Provides:		trinity-k3b-i18n-ru = %{version}-%{release}

%description Russian
This package contains the Russian translations for K3B.

%files Russian
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/ru/k3b
%{tde_datadir}/locale/ru/LC_MESSAGES/*.mo

##########

%package Swedish
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		Swedish (sv) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-sv < %{version}-%{release}
Provides:		trinity-k3b-i18n-sv = %{version}-%{release}

%description Swedish
This package contains the Swedish translations for K3B.

%files Swedish
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/sv/k3b
%{tde_datadir}/locale/sv/LC_MESSAGES/*.mo

##########

%package Ukrainian
Group:			Applications/Archiving
Requires:		trinity-k3b
Summary:		Ukrainian (uk) translations for K3B [Trinity]

Obsoletes:		trinity-k3b-i18n-uk < %{version}-%{release}
Provides:		trinity-k3b-i18n-uk = %{version}-%{release}

%description Ukrainian
This package contains the Ukrainian translations for K3B.

%files Ukrainian
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/uk/k3b
%{tde_datadir}/locale/uk/LC_MESSAGES/*.mo

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

./configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --docdir=%{tde_tdedocdir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%__rm -rf %{buildroot}%{tde_datadir}/locale/af
%__rm -rf %{buildroot}%{tde_datadir}/locale/ar
%__rm -rf %{buildroot}%{tde_datadir}/locale/bg
%__rm -rf %{buildroot}%{tde_datadir}/locale/br
%__rm -rf %{buildroot}%{tde_datadir}/locale/bs
%__rm -rf %{buildroot}%{tde_datadir}/locale/ca
%__rm -rf %{buildroot}%{tde_datadir}/locale/cs
%__rm -rf %{buildroot}%{tde_datadir}/locale/cy
%__rm -rf %{buildroot}%{tde_datadir}/locale/en_GB
%__rm -rf %{buildroot}%{tde_datadir}/locale/eu
%__rm -rf %{buildroot}%{tde_datadir}/locale/fa
%__rm -rf %{buildroot}%{tde_datadir}/locale/fi
%__rm -rf %{buildroot}%{tde_datadir}/locale/ga
%__rm -rf %{buildroot}%{tde_datadir}/locale/gl
%__rm -rf %{buildroot}%{tde_datadir}/locale/he
%__rm -rf %{buildroot}%{tde_datadir}/locale/hi
%__rm -rf %{buildroot}%{tde_datadir}/locale/hu
%__rm -rf %{buildroot}%{tde_datadir}/locale/is
%__rm -rf %{buildroot}%{tde_datadir}/locale/ja
%__rm -rf %{buildroot}%{tde_datadir}/locale/ka
%__rm -rf %{buildroot}%{tde_datadir}/locale/km
%__rm -rf %{buildroot}%{tde_datadir}/locale/lt
%__rm -rf %{buildroot}%{tde_datadir}/locale/mk
%__rm -rf %{buildroot}%{tde_datadir}/locale/ms
%__rm -rf %{buildroot}%{tde_datadir}/locale/nb
%__rm -rf %{buildroot}%{tde_datadir}/locale/nds
%__rm -rf %{buildroot}%{tde_datadir}/locale/ne
%__rm -rf %{buildroot}%{tde_datadir}/locale/nn
%__rm -rf %{buildroot}%{tde_datadir}/locale/pa
%__rm -rf %{buildroot}%{tde_datadir}/locale/rw
%__rm -rf %{buildroot}%{tde_datadir}/locale/se
%__rm -rf %{buildroot}%{tde_datadir}/locale/sk
%__rm -rf %{buildroot}%{tde_datadir}/locale/sr
%__rm -rf %{buildroot}%{tde_datadir}/locale/sr@Latn
%__rm -rf %{buildroot}%{tde_datadir}/locale/ta
%__rm -rf %{buildroot}%{tde_datadir}/locale/tr
%__rm -rf %{buildroot}%{tde_datadir}/locale/uz
%__rm -rf %{buildroot}%{tde_datadir}/locale/uz@cyrillic
%__rm -rf %{buildroot}%{tde_datadir}/locale/zh_CN
%__rm -rf %{buildroot}%{tde_datadir}/locale/zh_TW


%clean
%__rm -rf %{buildroot}


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.0.5-1
- Initial release for TDE 14.0.0
