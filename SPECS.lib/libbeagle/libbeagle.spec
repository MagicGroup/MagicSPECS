%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name: 		libbeagle
Version: 	0.3.9
Release: 	8%{?dist}
Summary:	Beagle C interface
Summary(zh_CN): Beagle C 接口
Group: 		Development/Libraries
Group(zh_CN):	开发/库
License:	MIT
URL:		http://beagle-project.org/
Source0: 	http://download.gnome.org/sources/libbeagle/0.3/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libxml2-devel
BuildRequires:	glib2-devel
BuildRequires:  pygtk2-devel
BuildRequires:  python-devel
BuildRequires:	pygobject2-devel
# http://bugzilla.gnome.org/show_bug.cgi?id=570521
Patch0:		libbeagle-pyexec.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=588994
Patch1:		fix-install.patch
Patch2:		libbeagle-0.3.9-fixcompile.patch

BuildRequires: 	automake, autoconf, libtool

%description
Library to talk to the beagle server in C.

%description -l zh_CN
Beagle C 接口.

%package -n libbeagle-devel
Summary:	Beagle C interface
Summary(zh_CN): %name 的开发包
Group:		Development/Libraries
Group(zh_CN):	开发/库
Requires:	libbeagle = %{version}-%{release} 
Requires:	libxml2-devel 
Requires:	glib2-devel
Requires:	pkgconfig
Requires:	gtk-doc

%description -n libbeagle-devel
Library to talk to the beagle server in C.

%description -n libbeagle-devel -l zh_CN
%name 的开发包。

%package -n libbeagle-python
Summary:	Beagle python interface
Summary(zh_CN): Beagle 的 Python 接口
Group:		Development/Libraries
Group(zh_CN):   开发/库
Requires:	libbeagle = %{version}-%{release}
Requires:	python

%description -n libbeagle-python
Python wrappers for libbeagle

%description -n libbeagle-python -l zh_CN
Beagle 的 Python 接口.

%prep
%setup -q
%patch0 -p1 -b .pyexec
%patch1 -p1 -b .fix-install
%patch2 -p1

# patch 0 touches .am
autoreconf -i -f

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libbeagle.{a,la}
rm -f $RPM_BUILD_ROOT%{python_sitearch}/beagle/beagle.{a,la}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-, root, root)
%doc COPYING AUTHORS README
%{_libdir}/libbeagle.so.*


%files -n libbeagle-devel
%defattr(-, root, root)
%{_includedir}/libbeagle
%{_libdir}/libbeagle.so
%{_libdir}/pkgconfig/libbeagle*.pc
%{_datadir}/gtk-doc/html/beagle


%files -n libbeagle-python
%dir %{python_sitearch}/beagle
%{python_sitearch}/beagle/beagle.so
%{python_sitearch}/beagle/*.py
%{python_sitearch}/beagle/*.pyc
%{python_sitearch}/beagle/*.pyo


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.3.9-8
- 为 Magic 3.0 重建

* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 0.3.9-7
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.3.9-6
- 为 Magic 3.0 重建


