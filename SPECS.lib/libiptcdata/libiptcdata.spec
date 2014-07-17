%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name: libiptcdata
Version: 1.0.4
Release: 6%{?dist}
Summary: IPTC tag library
Summary(zh_CN.UTF-8): IPTC 标签库

Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License: LGPLv2+
URL: http://libiptcdata.sourceforge.net/
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: libtool
BuildRequires: gtk-doc

%description
libiptcdata is a library for parsing, editing, and saving IPTC data
stored inside images.  IPTC is a standard for encoding metadata such
as captions, titles, locations, etc. in the headers of an image file.
libiptcdata also includes a command-line utility for modifying the
metadata.

%description -l zh_CN.UTF-8
IPTC 标签库。

%package devel
Summary: Headers and libraries for libiptcdata application development
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk-doc

%description devel
The libiptcdata-devel package contains the libraries and include files
that you can use to develop libiptcdata applications.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package python
Summary: Python bindings for libiptcdata
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
BuildRequires: python-devel

%description python
The libiptcdata-python package contains a Python module that allows Python
applications to use the libiptcdata API for reading and writing IPTC
metadata in images.

%description python -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%prep
%setup -q

%build
%configure --enable-gtk-doc --enable-python --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} INSTALL="%{__install} -c -p" install
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.la
rm -f $RPM_BUILD_ROOT%{python_sitearch}/iptcdata.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libiptcdata
%{_datadir}/gtk-doc/html/libiptcdata

%files python
%defattr(-,root,root)
%doc python/README
%doc python/examples/*
%{python_sitearch}/*.so

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.4-6
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 1.0.4-5
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 05 2009 David Moore <dcm@acm.org> 1.0.4-1
- New upstream version

* Sun Apr 12 2009 David Moore <dcm@acm.org> 1.0.3-3
- Added 'BuildRequires: gtk-doc'

* Sun Apr 12 2009 David Moore <dcm@acm.org> 1.0.3-2
- Added 'Requires: gtk-doc' and 'BuildRequires: libtool' and gettext

* Sun Apr 12 2009 David Moore <dcm@acm.org> 1.0.3-1
- New upstream version
- Added translation to file list

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.2-4
- Rebuild for Python 2.6

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.2-3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-2
- Autorebuild for GCC 4.3

* Tue May 15 2007 David Moore <dcm@acm.org> 1.0.2-1
- New upstream version

* Fri Mar 23 2007 David Moore <dcm@acm.org> 1.0.1-1
- New upstream version

* Thu Mar 22 2007 David Moore <dcm@acm.org> 1.0.0-2
- Fixed URL, removed INSTALL file, fixed python path and timestamps

* Wed Mar 21 2007 David Moore <dcm@acm.org> 1.0.0-1
- Updated spec file to better match Fedora guidelines

* Sun Jan 28 2007 David Moore <dcm@acm.org>
- Added libiptcdata-python package

* Wed Apr 12 2006 David Moore <dcm@acm.org>
- Removed *.mo from spec file since there are no translations yet

* Mon Feb 28 2005 David Moore <dcm@acm.org>
- Initial version
