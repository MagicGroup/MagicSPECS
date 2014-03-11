%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           pygtkglext
Version:        1.1.0
Release:        8%{?dist}
Summary:        Python bindings for GtkGLExt
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://www.k-3d.org/gtkglext/Main_Page
Source:         http://downloads.sourceforge.net/gtkglext/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gtkglext-devel pygtk2-devel python-devel
Requires:       pygtk2 PyOpenGL

%description
Python bindings for GtkGTLExt


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig pygtk2-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
iconv -f EUC-JP -t UTF8 AUTHORS > tmp
mv tmp AUTHORS
iconv -f EUC-JP -t UTF8 README > tmp
mv tmp README


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
if [ %{python_sitelib} != %{python_sitearch} ]; then
  mv $RPM_BUILD_ROOT%{python_sitelib}/gtk-2.0/gtk/gdkgl/* \
     $RPM_BUILD_ROOT%{python_sitearch}/gtk-2.0/gtk/gdkgl
  mv $RPM_BUILD_ROOT%{python_sitelib}/gtk-2.0/gtk/gtkgl/* \
     $RPM_BUILD_ROOT%{python_sitearch}/gtk-2.0/gtk/gtkgl
fi
rm $RPM_BUILD_ROOT%{python_sitearch}/gtk-2.0/gtk/gdkgl/_gdkgl.la
rm $RPM_BUILD_ROOT%{python_sitearch}/gtk-2.0/gtk/gtkgl/_gtkgl.la

# this can be executed to run some basic tests (it has a main and shebang)
chmod +x $RPM_BUILD_ROOT%{python_sitearch}/gtk-2.0/gtk/gtkgl/apputils.py

# for %%doc
rm examples/Makefile*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING COPYING.LIB README examples
%{python_sitearch}/gtk-2.0/gtk/gdkgl
%{python_sitearch}/gtk-2.0/gtk/gtkgl

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_datadir}/pygtk/2.0/defs/*


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.1.0-8
- 为 Magic 3.0 重建

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.1.0-5
- Rebuild for Python 2.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.0-4
- Autorebuild for GCC 4.3

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.0-3
- Update License tag for new Licensing Guidelines compliance

* Thu Mar 29 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.0-2
- Various specfile improvements (bz 234122)

* Sat Mar 24 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.0-1
- Initial Fedora Extras package
