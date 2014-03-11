Name:           libglademm24
Version:        2.6.7
Release:        3%{?dist}

Summary:        C++ wrapper for libglade
Summary(zh_CN.GB18030):	libglade µƒ C++ ∞Û∂®

Group:          System Environment/Libraries
Group(zh_CN.GB18030):	œµÕ≥ª∑æ≥/ø‚
License:        LGPLv2+
URL:            http://gtkmm.sourceforge.net/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/libglademm/2.6/libglademm-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  gtkmm24-devel >= 2.6.0
BuildRequires:  libglade2-devel >= 2.6.1

%description
This package provides a C++ interface for libglademm. It is a
subpackage of the GTKmm project.  The interface provides a convenient
interface for C++ programmers to create Gnome GUIs with GTK+'s
flexible object-oriented framework.

%description -l zh_CN.GB18030
libglade µƒ C++ ∞Û∂®°£

%package devel
Summary:        Headers for developing programs that will use libglademm.
Summary(zh_CN.GB18030):	%{name} µƒø™∑¢∞¸
Group:          Development/Libraries
Group(zh_CN.GB18030):	ø™∑¢/ø‚
Requires:       %{name} = %{version}-%{release}
Requires:       gtkmm24-devel
Requires:       libglade2-devel

%description devel
This package contains the headers that programmers will need to
develop applications which will use libglademm, part of GTKmm, the C++
interface to the GTK+.

%description devel -l zh_CN.GB18030
%name µƒø™∑¢∞¸°£

%prep
%setup -q -n libglademm-%{version}


%build
%configure --disable-static --enable-docs
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT docs-to-include
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
%{__mkdir} docs-to-include
%{__mv} ${RPM_BUILD_ROOT}%{_docdir}/gnomemm-2.6/libglademm-2.4/* docs-to-include/
rm -f ${RPM_BUILD_ROOT}%{_datadir}/devhelp/books/libglademm-2.4/*


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig


%postun
/sbin/ldconfig


%files
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, -)
%doc docs-to-include/*
%{_includedir}/libglademm-2.4
%{_libdir}/*.so
%{_libdir}/libglademm-2.4
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 2.6.7-3
- ‰∏∫ Magic 3.0 ÈáçÂª∫


