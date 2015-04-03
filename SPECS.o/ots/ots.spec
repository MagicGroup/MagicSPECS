Name:		ots
Summary:	A text summarizer
Summary(zh_CN.UTF-8): 一个文本统计器
Version:	0.5.0
Release:	7%{?dist}

License:	GPLv2+
URL:		http://libots.sourceforge.net/
Group:		System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库

Source0:	http://prdownloads.sourceforge.net/libots/ots-%{version}.tar.gz
Patch0:  ots-0.5.0-remove_double_en.xml.patch


BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libxml2-devel >= 2.4.23
BuildRequires:	popt-devel >= 1.5
BuildRequires:	libtool

Requires:	%{name}-libs = %{version}-%{release}

%description
The open text summarizer is an open source tool for summarizing texts.
The program reads a text and decides which sentences are important and
which are not.

%description -l zh_CN.UTF-8
这是一个开源的文本统计器，它读取文本并决定那些句子是重要的，那些不是。
 
%package	devel
Summary: 	Libraries and include files for developing with libots
Summary(zh_CN.UTF-8): %name 的开发包
Group: 		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:	%{name}-libs = %{version}-%{release}
Requires: 	glib2-devel >= 2.0
Requires:	libxml2-devel >= 2.4.23
Requires:	popt-devel >= 1.5
Requires:	pkgconfig

%description	devel
This package provides the necessary development libraries and include
files to allow you to develop with libots.

%description devel -l zh_CN.UTF-8
%name 的开发包

%package	libs
Summary:	Shared libraries for %{name}
Summary(zh_CN.UTF-8): %name 的共享库
Group:		Development/Libraries
Group(zh_CN.UTF-8):   开发/库

%description	libs
The %{name}-libs package contains shared libraries used by %{name}.

%description libs -l zh_CN.UTF-8
%name 的共享库。

%prep
%setup -q 
#%patch0 -p1


%build
touch ./gtk-doc.make
autoreconf -fisv
%configure --with-html-dir=%{_datadir}/gtk-doc/html/ots
%{__make} LIBTOOL=%{_bindir}/libtool


%install
rm -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%post	libs -p /sbin/ldconfig


%postun	libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/ots

%files	libs
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libots-1.so.*
%{_datadir}/ots/

%files	devel
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libots-1.so
%{_includedir}/libots-1/
%{_libdir}/pkgconfig/libots-1.pc


%changelog
* Fri Apr 03 2015 Liu Di <liudidi@gmail.com> - 0.5.0-7
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.5.0-6
- 为 Magic 3.0 重建

* Sun Oct 28 2012 Liu Di <liudidi@gmail.com> - 0.5.0-5
- 为 Magic 3.0 重建

* Fri Jan 20 2012 Liu Di <liudidi@gmail.com> - 0.5.0-4
- 为 Magic 3.0 重建

* Tue Oct 25 2011 Liu Di <liudidi@gmail.com> - 0.5.0-3
- 为 Magic 3.0 重建
