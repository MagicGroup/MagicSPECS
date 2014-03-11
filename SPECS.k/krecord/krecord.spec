Summary:	Sound recorder for KDE
Summary(zh_CN.UTF-8): KDE 下的录音机
Name:		krecord
Version:	1.16
Release:	1%{?dist}
License:	GPL
Group:		Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
Source0:	http://dl.bytesex.org/releases/krecord/%{name}-%{version}.tar.gz
# Source0-md5:	d0b4b0d981bf1c4a3872423b8d4b4b1d
Source1:	%{name}.desktop
patch0:		%{name}-doc-path.patch
Patch1:		krecord-1.16-tde.patch
URL:		http://bytesex.org/krecord.html
BuildRequires:	gettext-devel
BuildRequires:	tdelibs-devel >= 3.0.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_htmldir	/usr/share/doc/kde/HTML

%description
A simple KDE interface to record sounds.

%description -l zh_CN.UTF-8
KDE 下的一个简单的录音机。

%define _desktopdir %{_datadir}/applications/kde

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
. /etc/profile.d/qt.sh
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
magic_rpm_clean.sh
%find_lang %{name} --with-kde --all-name || :
rm -f $RPM_BUILD_ROOT%{_datadir}/applnk/Multimedia/krecord.desktop
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/kde/HTML/en/krecord/index.html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%attr(755,root,root) %{_bindir}/krecord
%{_desktopdir}/%{name}.desktop
%{_datadir}/apps/krecord

%changelog

