#define fz_rc   rc2
Name:           filezilla
Version:        3.5.2
Release:        1%{?fz_rc:_%{?fz_rc}}%{?dist}.1
Summary:        FileZilla FTP, FTPS and SFTP client
Summary(zh_CN.UTF-8): FTP, FTPS 和 SFTP 客户端

Group:          Applications/Internet
Group(zh_CN.UTF-8):	应用程序/互联网
License:        GPLv2+
URL:            http://filezilla-project.org/
Source0:        http://downloads.sourceforge.net/project/filezilla/FileZilla_Client/%{version}/FileZilla_%{version}%{?fz_rc:-%{?fz_rc}}_src.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## Needed if autogen.sh is invoked
#BuildRequires:  automake, autoconf, libtool
## 
## Needed if test program is build
BuildRequires:  cppunit-devel >= 1.10.2
##
BuildRequires:  desktop-file-utils

BuildRequires:  dbus-devel
BuildRequires:  gettext
BuildRequires:  gnutls-devel >= 2.8.4
BuildRequires:  libidn-devel
BuildRequires:  wx-gtk2-unicode-devel >= 2.8.9

#暂时使用内部的
#BuildRequires:	tinyxml-devel


%description
FileZilla is a FTP, FTPS and SFTP client for Linux with a lot of features.
- Supports FTP, FTP over SSL/TLS (FTPS) and SSH File Transfer Protocol (SFTP)
- Cross-platform
- Available in many languages
- Supports resume and transfer of large files >4GB
- Easy to use Site Manager and transfer queue
- Drag & drop support
- Speed limits
- Filename filters
- Network configuration wizard 

%description -l zh_CN.UTF-8
一个快速可靠的 ftp 客户端。

%prep
%setup -q -n %{name}-%{version}%{?fz_rc:-%{?fz_rc}}

# Run autotools if needed
# sh autoconf


%build
%configure \
  --disable-static \
  --enable-locales \
  --with-tinyxml=builtin \
  --disable-manualupdatecheck \
  --disable-autoupdatecheck 

## Do not use --enable-buildtype=official 
## that option enables the "check for updates" dialog to download
## new binaries from the official website.

# Remove the timyxml internal static lib to configure will not fails
#rm -rf src/tinyxml/

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p -c"

for i in 16x16 32x32 48x48 ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}/apps
  ln -sf ../../../../%{name}/resources/${i}/%{name}.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}/apps/%{name}.png
done

rm -rf $RPM_BUILD_ROOT%{_datadir}/pixmaps

desktop-file-install --vendor "fedora" \
  --delete-original \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop


magic_rpm_clean.sh
%find_lang %{name}

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi || :

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS
%doc %{_datadir}/%{name}/docs/*
%{_bindir}/*
%{_datadir}/filezilla/
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man1/*
%{_mandir}/man5/*


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.5.2-1.1
- 为 Magic 3.0 重建


