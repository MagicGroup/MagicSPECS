Name:           libgxps
Version:        0.2.2
Release:        7%{?dist}
Summary:        GObject based library for handling and rendering XPS documents
Summary(zh_CN.UTF-8): 基于 GObject 的处理和渲染 XPS 文档的库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

License:        LGPLv2+
URL:            http://live.gnome.org/libgxps
Source0:        http://ftp.gnome.org/pub/gnome/sources/%{name}/0.2/%{name}-%{version}.tar.xz

BuildRequires:  gtk3-devel
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  cairo-devel
BuildRequires:  libarchive-devel
BuildRequires:  freetype-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  lcms2-devel
BuildRequires:  chrpath

%description
libgxps is a GObject based library for handling and rendering XPS
documents.

%description -l zh_CN.UTF-8
基于 GObject 的处理和渲染 XPS 文档的库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        tools
Summary:        Command-line utility programs for manipulating XPS files
Summary(zh_CN.UTF-8): 处理 XPS 文件的命令行工具程序
Group:          Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
The %{name}-tools contains command-line programs for manipulating XPS format
documents using the %{name} library.

%description tools -l zh_CN.UTF-8
处理 XPS 文件的命令行工具程序。

%prep
%setup -q


%build
%configure --disable-static --enable-man
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/xpsto*
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/gtk-doc/html/libgxps

%files tools
%{_bindir}/xpsto*
%{_mandir}/man1/xpsto*.1.gz


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.2.2-7
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.2.2-6
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 0.2.2-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.2.2-4
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May  6 2012 Tom Hughes <tom@compton.nu> - 0.2.2-2
- Rebuilt for new libtiff.

* Mon Mar 19 2012 Tom Hughes <tom@compton.nu> - 0.2.2-1
- Update to 0.2.2 upstream release.

* Thu Jan 26 2012 Tomas Bzatek <tbzatek@redhat.com> - 0.2.1-4
- Rebuilt for new libarchive

* Thu Jan 26 2012 Tom Hughes <tom@compton.nu> - 0.2.1-3
- Correct summary and description for tools package.

* Thu Jan 26 2012 Tom Hughes <tom@compton.nu> - 0.2.1-2
- Rebuild for libarchive soname bump.

* Sat Jan 21 2012 Tom Hughes <tom@compton.nu> - 0.2.1-1
- Update to 0.2.1 upstream release.

* Wed Jan  4 2012 Tom Hughes <tom@compton.nu> - 0.2.0-2
- Rebuilt for gcc 4.7 mass rebuild.
- Run autoreconf to update libtool.

* Thu Dec  1 2011 Tom Hughes <tom@compton.nu> - 0.2.0-1
- Update to 0.2.0 upstream release.

* Sat Nov  5 2011 Tom Hughes <tom@compton.nu> - 0.1.0-2
- Fix base package dependency in devel package.

* Fri Nov  4 2011 Tom Hughes <tom@compton.nu> - 0.1.0-1
- Initial build.
