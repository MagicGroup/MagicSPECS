Name:           stoken
Version:	0.90
Release:	3%{?dist}
Summary:        Token code generator compatible with RSA SecurID 128-bit (AES) token
Summary(zh_CN.UTF-8): 使用 RSA SecurID 128 位 (AES) 算法的令牌码生成器

License:        LGPLv2+
URL:            http://%{name}.sf.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

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

%description -l zh_CN.UTF-8
使用 RSA SecurID 128 位 (AES) 算法的令牌码生成器。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}-libs%{_isa} = %{version}-%{release}

%description devel
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

This package provides the development files for %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package libs
Summary:        Libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的运行库
Requires(post): ldconfig

%description libs
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

This package contains %{name} libraries.
%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package cli
Summary:        Command line tool for %{name}
Summary(zh_CN.UTF-8): %{name} 的命令行工具
Requires:       %{name}-libs%{_isa} = %{version}-%{release}

%description cli
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

This package contains the command line tool for %{name}.

%description cli -l zh_CN.UTF-8
%{name} 的命令行工具。

%package gui
Summary:        Graphical interface program for %{name}
Summary(zh_CN.UTF-8): %{name} 的图形界面程序
Requires:       %{name}-libs%{_isa} = %{version}-%{release}

%description gui
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

This package contains the graphical interface program for %{name}.
%description gui -l zh_CN.UTF-8
%{name} 的图形界面程序。

%prep
%setup -q

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
%{_libdir}/*.so.*

%files cli
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%files gui
%{_bindir}/%{name}-gui
%{_datadir}/applications/%{name}-gui.desktop
%{_datadir}/pixmaps/%{name}-gui.png
%{_mandir}/man1/%{name}-gui.1.gz
%{_datadir}/applications/stoken-gui-small.desktop
%{_datadir}/stoken/*.ui

%files devel
%{_includedir}/%{name}.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_docdir}/stoken/*


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.90-3
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.90-2
- 为 Magic 3.0 重建

* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 0.90-1
- 更新到 0.90

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
