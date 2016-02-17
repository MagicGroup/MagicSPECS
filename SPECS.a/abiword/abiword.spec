%define majorversion 3
%define minorversion 0
%define microversion 1

Summary: The AbiWord word processor
Summary(zh_CN): AbiWord 字处理程序
Name: abiword
Version: %{majorversion}.%{minorversion}.%{microversion}
Release: 12%{?dist}
Epoch: 1
Group: Applications/Editors
Group(zh_CN): 应用程序/编辑器
License: GPLv2+
Source0: http://abisource.com/downloads/abiword/%{version}/source/abiword-%{version}.tar.gz
Source1: http://abisource.com/downloads/abiword/%{version}/source/abiword-docs-%{version}.tar.gz
Source11: abiword.mime
Source12: abiword.keys
Source13: abiword.xml
Source50: TelepathyBuddy.h
URL: http://www.abisource.com/
Requires: libabiword = %{epoch}:%{version}-%{release}

%description
AbiWord is a cross-platform Open Source word processor. It is full-featured,
while still remaining lean.

%description -l zh_CN
AbiWord 是一个跨平台的开源字处理程序。它功能很全，不过仍有需要完善的地方。

%package -n libabiword
Summary: Library for developing applications based on AbiWord's core
Summary(zh_CN): 基于 AbiWord 的核心开发程序需要的库
Group: System Environment/Libraries
Group(zh_CN): 系统环境/库
Patch0: abiword-2.6.0-windowshelppaths.patch
Patch1: abiword-2.8.3-desktop.patch
Patch2: abiword-2.6.0-boolean.patch

BuildRequires: autoconf, libtool
BuildRequires: desktop-file-utils
BuildRequires: fribidi-devel, enchant-devel, wv-devel
BuildRequires: zlib-devel, popt-devel, libpng-devel
BuildRequires: gtk2-devel, libgsf-devel
BuildRequires: boost-devel, t1lib-devel
BuildRequires: dbus-glib-devel >= 0.70
BuildRequires: readline-devel
BuildRequires: bzip2-devel
BuildRequires: poppler-devel >= 0.4.0
BuildRequires: ots-devel >= 0.4.2
BuildRequires: libwpd-devel >= 0.9.0
BuildRequires: libwpg-devel
BuildRequires: librsvg2-devel
BuildRequires: libwmf-devel
BuildRequires: aiksaurus-devel, aiksaurus-gtk-devel
BuildRequires: link-grammar-devel >= 4.2.2
BuildRequires: gtkmathview-devel >= 0.7.5, flex, bison
BuildRequires: loudmouth-devel
BuildRequires: asio-devel
BuildRequires: libsoup-devel

%description -n libabiword
Library for developing applications based on AbiWord's core.

%description -n libabiword -l zh_CN
基于 AbiWord 的核心开发程序需要的库。

%package -n libabiword-devel
Summary: Files for developing with libabiword
Summary(zh_CN): 使用 libabiword 编译需要的开发文件
Group: Development/Libraries
Group(zh_CN): 开发/库
Requires: libabiword = %{epoch}:%{version}-%{release}

%description -n libabiword-devel
Includes and definitions for developing with libabiword.

%description -n libabiword-devel -l zh_CN
使用 libabiword 编译程序需要的开发文件。

%prep
# setup abiword
%setup -q
#临时性措施
# cp %{SOURCE50} plugins/collab/backends/telepathy/unix/

# patch abiword
%patch1 -p1 -b .desktop
%patch2 -p1 -b .boolean

# setup abiword documentation
%setup -q -T -b 1 -n abiword-docs-%{version}
%patch0 -p1 -b .windowshelppaths

%build
# build libabiword and abiword
cd $RPM_BUILD_DIR/abiword-%{version}
# we need to update the generated configuration files because of patch104
autoreconf --force --install
%configure --disable-static --enable-dynamic --enable-plugins --enable-clipart --enable-templates
make %{?_smp_mflags} V=1

# build the documentation
cd $RPM_BUILD_DIR/abiword-docs-%{version}
ABI_DOC_PROG=$(pwd)/../%{name}-%{version}/src/abiword ./make-html.sh

%install

# install abiword
cd $RPM_BUILD_DIR/abiword-%{version}
%{__make} install DESTDIR=$RPM_BUILD_ROOT

# install the documentation
cd $RPM_BUILD_DIR/abiword-docs-%{version}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{majorversion}.%{minorversion}/AbiWord/help
cp -rp help/* $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{majorversion}.%{minorversion}/AbiWord/help/
# some of the help dirs have bad perms (#109261)
find $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{majorversion}.%{minorversion}/AbiWord/help/ -type d -exec chmod -c o+rx {} \;

# finish up
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps/
cp $RPM_BUILD_DIR/abiword-%{version}/abiword.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/abiword.png

cd $RPM_BUILD_DIR/abiword-%{version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor magic --add-category X-Magic \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category X-Red-Hat-Extra --remove-category X-Red-Hat-Base \
  --add-category Applications --add-category Office \
  ./abiword.desktop
# remove the original one (which has X-Red-Hat-Base)  (#107023)
%{__rm} -f $RPM_BUILD_ROOT/%{_datadir}/applications/abiword.desktop

%{__install} -p -m 0644 -D %{SOURCE11} $RPM_BUILD_ROOT%{_datadir}/mime-info/abiword.mime
%{__install} -p -m 0644 -D %{SOURCE12} $RPM_BUILD_ROOT%{_datadir}/mime-info/abiword.keys
%{__install} -p -m 0644 -D %{SOURCE13} $RPM_BUILD_ROOT%{_datadir}/mime/packages/abiword.xml

# nuke .la files
%{__rm} -f $RPM_BUILD_ROOT/%{_libdir}/libabiword-%{majorversion}.%{minorversion}.la
%{__rm} -f $RPM_BUILD_ROOT/%{_libdir}/%{name}-%{majorversion}.%{minorversion}/plugins/*.la

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :

%postun
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :

%files
%defattr(-,root,root)
%{_bindir}/abiword
%{_datadir}/applications/*
%{_datadir}/mime-info/abiword.mime
%{_datadir}/mime-info/abiword.keys
%{_datadir}/mime/packages/abiword.xml
%{_datadir}/pixmaps/*.png
%{_datadir}/icons/hicolor/*x*/apps/*.png
# Abiword help
%{_datadir}/%{name}-%{majorversion}.%{minorversion}/AbiWord
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.AbiCollab.service
%{_datadir}/telepathy/clients/AbiCollab.client
%{_mandir}/man1/abiword.1.gz
%{_datadir}/icons/hicolor/scalable/apps/abiword.svg

%files -n libabiword
%doc $RPM_BUILD_DIR/%{name}-%{version}/COPYING $RPM_BUILD_DIR/%{name}-%{version}/COPYRIGHT.TXT
%{_libdir}/libabiword-%{majorversion}.%{minorversion}.so
%{_libdir}/libAiksaurusGtk3*
%{_libdir}/%{name}-%{majorversion}.%{minorversion}
%{_datadir}/%{name}-%{majorversion}.%{minorversion}
# Abiword help - included in GUI app
%exclude %{_datadir}/%{name}-%{majorversion}.%{minorversion}/AbiWord

%files -n libabiword-devel
%{_includedir}/%{name}-%{majorversion}.%{minorversion}
%{_libdir}/pkgconfig/%{name}-%{majorversion}.%{minorversion}.pc

%changelog
* Sun Feb 14 2016 Liu Di <liudidi@gmail.com> - 1:3.0.1-12
- 为 Magic 3.0 重建

* Tue Dec 01 2015 Liu Di <liudidi@gmail.com> - 1:3.0.1-11
- 为 Magic 3.0 重建

* Tue Dec 01 2015 Liu Di <liudidi@gmail.com> - 1:3.0.1-10
- 为 Magic 3.0 重建

* Mon Nov 16 2015 Liu Di <liudidi@gmail.com> - 1:3.0.1-9
- 为 Magic 3.0 重建

* Mon Nov 16 2015 Liu Di <liudidi@gmail.com> - 1:3.0.1-8
- 为 Magic 3.0 重建

* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1:3.0.1-7
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1:3.0.1-6
- 更新到 3.0.1

* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 1:3.0.0-5
- 为 Magic 3.0 重建

* Thu Jul 17 2014 Liu Di <liudidi@gmail.com> - 1:3.0.0-4
- 为 Magic 3.0 重建

* Sun Jul 13 2014 Liu Di <liudidi@gmail.com> - 1:3.0.0-3
- 更新到 3.0.0

* Sun Jul 13 2014 Liu Di <liudidi@gmail.com> - 1:2.9.4-3
- 更新到 2.9.4

* Tue Dec 04 2012 Liu Di <liudidi@gmail.com> - 1:2.9.3-3
- 为 Magic 3.0 重建

* Fri Nov 23 2012 Liu Di <liudidi@gmail.com> - 1:2.9.3-2
- 为 Magic 3.0 重建

* Wed Oct 26 2011 Liu Di <liudidi@gmail.com> - 2.9.1-1
- 升级到 2.9.1
