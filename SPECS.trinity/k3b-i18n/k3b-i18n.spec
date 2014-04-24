%define version 1.0.5
%define release 3%{?dist}


Summary:        Internationalization package for k3b.
Summary(zh_CN.UTF-8):	K3b 的国际化包
Name:           k3b-i18n
Version:        %{version}
Release:        %{release}
License:        GPL
URL:            http://www.k3b.org
Packager:       KanKer <kanker@163.com>
Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
Source:		%{name}-%{version}.tar.bz2
Patch:		k3b-i18n-tde.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Prefix:         %(kde-config --prefix)
Requires:       k3b >= 1.0.1
#BuildRequires:  XFree86-devel
BuildRequires:  kdelibs-devel >= 3.1, arts-devel
BuildRequires:  zlib-devel
BuildRequires:  gettext
BuildArch:	noarch


%description
This package adds support for multiple languages to k3b.

%description -l zh_CN.UTF-8
这个包为 k3b 添加多语言支持。

%prep
%setup -q
%patch -p1

%build
[ -z "$QTDIR" ] && . %{_sysconfdir}/profile.d/qt.sh
./configure --prefix=$(kde-config --prefix) --with-extra-includes=%{_includedir}/tqt
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

#The scripts should be removed on other computer to compile
magic_rpm_clean.sh


%find_lang k3b


%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}


%files -f k3b.lang
%defattr(644,root,root,755)
%{_datadir}/*

%changelog
* Thu Dec 15 2011 Liu Di <liudidi@gmail.com> - 1.0.5-3
- 为 Magic 3.0 重建

* Fri Nov 09 2007 Liu Di <liudidi@gmail.com> - 1.0.4-1mgc
- update to 1.0.4

* Tue May 29 2007 kde <athena_star {at} 163 {dot} com> - 1.0.1-1mgc
- update to 1.0.1

* Mon Mar 19 2007 Liu Di <liudidi@gmail.com> - 1.0-1mgc
- update to 1.0

* Sat Aug 26 2006 Liu Di <liudidi@gmail.com> - 0.12.17-1mgc
- update to 0.12.17

* Fri Dec 16 2005 KanKer <kanker@163.com>
- 0.12.9
* Sat Nov 26 2005 KanKer <kanker@163.com>
- 0.12.8
* Fri Nov 4 2005 KanKer <kanker@163.com>
- 0.12.7
* Mon Oct 31 2005 KanKer <kanker@163.com>
- 0.12.6
* Wed Oct 19 2005 KanKer <kanker@163.com>
- 0.12.5
* Wed Sep 21 2005 KanKer <kanker@163.com>
- 0.12.4a
* Sat Jul 30 2005 KanKer <kanker@163.com>
- 0.12.3
* Sun Jul 3 2005 KanKer <kanker@163.com>
- 0.12.2
* Sat Jun 18 2005 KanKer <kanker@163.com>
- 0.12.1
* Thu Jun 14 2005 KanKer <kanker@163.com>
- 0.12
* Sat Jun 12 2004 KanKer <kanker@163.com>
- rebuild 
* Fri Mar 23 2004 Mihai Maties <mihai@xcyb.org> - k3b-0.11-2.xcyb.*
- Convert the spec for the upcoming merge with fedora.us
