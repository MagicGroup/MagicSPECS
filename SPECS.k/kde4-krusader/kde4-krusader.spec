%define real_name krusader
%define beta beta3
Name:		kde4-krusader
Version:	2.4.0
Release:	0.2%{?dist}
Summary:	An advanced twin-panel (commander-style) file-manager for KDE
Summary(zh_CN):	KDE 下的一个高级双面板文件管理器

Group:		Applications/File
Group(zh_CN): 应用程序/文件
License:	GPLv2+
URL:		http://krusader.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{real_name}/%{real_name}-%{version}%{?beta:-%{beta}}.tar.bz2
Patch0:		krusader-2.0.0-gcc-4.4.patch
Patch1:		krusader-2.4.0-beta3-remove-unused-doc.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	cmake
BuildRequires:	kdelibs4-devel >= 4.1.0 phonon-devel
BuildRequires:	libjpeg-devel libpng-devel giflib-devel
BuildRequires:	zlib-devel bzip2-devel
BuildRequires:	pcre-devel gamin-devel libacl-devel
BuildRequires:	xdg-utils gettext

%description
Krusader is an advanced twin panel (commander style) file manager for KDE and
other desktops in the *nix world, similar to Midnight or Total Commander.
It provides all the file management features you could possibly want.
Plus: extensive archive handling, mounted filesystem support, FTP, advanced
search module, an internal viewer/editor, directory synchronisation,
file content comparisons, powerful batch renaming and much much more.
It supports a wide variety of archive formats and can handle other KIO slaves
such as smb or fish. It is (almost) completely customizable, very user
friendly, fast and looks great on your desktop! You should give it a try.

%description -l zh_CN
KDE 下类似 Total Commander 的双面板高级文件管理器。

%package -n kde4-kio_iso
Summary: KIO slave to access ISO images
Summary(zh_CN): 访问 ISO 文件的 KIO 
Group: Applications/File
Group(zh_CN): 应用程序/文件

%description -n kde4-kio_iso
KIO slave to access ISO images

%description -n kde4-kio_iso -l zh_CN
访问 ISO 文件的 KIO

%prep
%setup -q -n %{real_name}-%{version}%{?beta:-%{beta}}
%patch1 -p1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}

# Make symlink relative and remove wrong EOL
pushd $RPM_BUILD_ROOT%{_kde4_docdir}/HTML/
for i in *
do
	pushd $RPM_BUILD_ROOT%{_kde4_docdir}/HTML/$i/krusader/
	for j in *.docbook
	do
		tr -d '\r' < $j > ${j}.tmp
		mv -f ${j}.tmp $j
	done
	ln -sf ../common
	popd
done
popd
magic_rpm_clean.sh
#%find_lang %{name}

%post
xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :
xdg-icon-resource forceupdate --theme locolor 2> /dev/null || :
xdg-desktop-menu forceupdate 2> /dev/null || :

%postun
xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :
xdg-icon-resource forceupdate --theme locolor 2> /dev/null || :
xdg-desktop-menu forceupdate 2> /dev/null || :

%clean
rm -rf %{buildroot}

#%files -f %{name}.lang
%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ README SVNNEWS TODO
%{_kde4_bindir}/*
%{_kde4_libdir}/kde4/*.so
%{_kde4_datadir}/applications/kde4/krusader*.desktop
%{_kde4_datadir}/config/kio_isorc
%{_kde4_docdir}/HTML/en/krusader/
%{_kde4_iconsdir}/hicolor/*/apps/*.png
%{_kde4_iconsdir}/locolor/*/apps/*.png
%{_kde4_datadir}/apps/krusader/
%{_kde4_datadir}/kde4/services/*.protocol
%{kde4_localedir}/zh_CN/LC_MESSAGES/krusader.mo
%{kde4_localedir}/zh_TW/LC_MESSAGES/krusader.mo
#%{kde4_mandir}/man1/krusader.1*
%exclude %{_kde4_libdir}/kde4/kio_iso.so
%exclude %{_kde4_datadir}/config/kio_isorc
%exclude %{_kde4_datadir}/kde4/services/iso.protocol

%files -n kde4-kio_iso
%defattr(-,root,root,-)
%{_kde4_libdir}/kde4/kio_iso.so
%{_kde4_datadir}/config/kio_isorc
%{_kde4_datadir}/kde4/services/iso.protocol


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.4.0-0.2
- 为 Magic 3.0 重建


