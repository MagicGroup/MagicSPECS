Name:           stoken
Version:        0.2
Release:        5%{?dist}
Summary:        Token code generator compatible with RSA SecurID 128-bit (AES) token

License:        LGPLv2+
URL:            http://%{name}.sf.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         %{name}-0.2-no-static-cflags.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  libtool
BuildRequires:  pkgconfig(libtomcrypt)

%description
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}

%description devel
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

This package provides the development files for %{name}.

%package libs
Summary:        Libraries for %{name}
Requires(post): ldconfig

%description libs
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

This package contains %{name} libraries.

%package cli
Summary:        Command line tool for %{name}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}

%description cli
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

This package contains the command line tool for %{name}.

%package gui
Summary:        Graphical interface program for %{name}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}

%description gui
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

This package contains the graphical interface program for %{name}.

%prep
%setup -q
%patch0 -p1 -b .no-static-cflags

%build
autoreconf -v -f --install
%configure --with-gtk
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-gui.desktop
find %{buildroot} -type f -name "*.la" -delete
find %{buildroot} -type f -name "*.a" -delete

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%doc COPYING.LIB README
%{_libdir}/*.so.*

%files cli
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%files gui
%{_bindir}/%{name}-gui
%{_datadir}/applications/%{name}-gui.desktop
%{_datadir}/pixmaps/%{name}-gui.png
%{_mandir}/man1/%{name}-gui.1.gz

%files devel
%{_includedir}/%{name}.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 05 2013 Simone Caronni <negativo17@gmail.com> - 0.2-4
- Change gtk and libtomcrypt build requirements.
- Remove useless "--with-libtomcrypt" parameter from %%configure.

* Tue Jun 04 2013 Simone Caronni <negativo17@gmail.com> - 0.2-3
- Add patch to avoid static CFLAGS.
- Require proper libtomcrypt version.

* Mon Jun 03 2013 Simone Caronni <negativo17@gmail.com> - 0.2-2
- Remove CFLAGS override and rpath commands.

* Mon Jun 03 2013 Simone Caronni <negativo17@gmail.com> - 0.2-1
- First build.
