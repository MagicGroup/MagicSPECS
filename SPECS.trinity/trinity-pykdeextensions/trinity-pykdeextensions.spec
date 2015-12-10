%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif
%define tdeversion 3.5.13.2

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}



Name:		trinity-pytdeextensions
Summary:	Python packages to support TDE applications (scripts) [Trinity]
Version:	0.4.0
Release:	6%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.simonzone.com/software/pykdeextensions

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	pykdeextensions-trinity-%{tdeversion}.tar.xz




# [pykdeextensions] Fix hardcoded path to Guidance python libraries [Bug #999]
Patch2:		pykdeextensions-3.5.13.1-fix_extra_module_dir.patch
# [pykdeextensions] Fix include directory search location
Patch5:		pykdeextensions-3.5.13-fix_include_dir.patch
# [pykdeextensions] Fix 'libgcc' search location
Patch6:		pykdeextensions-3.5.13.1-fix_libgcc_detection.patch

BuildRequires: trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires: trinity-arts-devel >= 3.5.13.1
BuildRequires: trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	python-trinity-devel

%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	python-qt
%else
%if 0%{?rhel} == 5 || 0%{?suse_version}
BuildRequires:	trinity-PyQt-devel
%else
BuildRequires:	PyQt-devel
%endif
%endif

Requires:		trinity-libpythonize0 = %{version}-%{release}

Obsoletes:		trinity-pykdeextensions < %{version}-%{release}
Provides:		trinity-pykdeextensions = %{version}-%{release}


%description
PyKDE Extensions is a collection of software and Python packages
to support the creation and installation of KDE applications.


%package -n trinity-libpythonize0
Summary:		Python packages to support KDE applications (library) [Trinity]	
Group:			Environment/Libraries

%description -n trinity-libpythonize0
PyKDE Extensions is a collection of software and Python packages
to support the creation and installation of KDE applications.

This package contains the libpythonize library files.


%package -n trinity-libpythonize0-devel
Summary:		Python packages to support KDE applications (development) [Trinity]
Group:			Development/Libraries
Requires:		trinity-libpythonize0 = %{version}-%{release}

%description -n trinity-libpythonize0-devel
PyKDE Extensions is a collection of software and Python packages
to support the creation and installation of KDE applications.

This package contains the libpythonize development files.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n pykdeextensions-trinity-%{tdeversion}
%patch2 -p1 -b .extramodule
%patch5 -p1 -b .incdir

# Changes library directory to 'lib64'
for f in src/*.py; do
  %__sed -i "${f}" \
    -e "s|%{tde_prefix}/lib/|%{tde_libdir}/|g" \
    -e "s|/usr/lib/pyshared/python\*|%{python_sitearch}|g" \
    -e "s|'pykde-dir=',None,|'pykde-dir=','%{python_sitearch}',|g" \
    -e "s|self.pykde_dir = None|self.pykde_dir = \"%{python_sitearch}\"|g" \
    -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g"
done

%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"
export PYTHONPATH=%{python_sitearch}/trinity-sip:%{python_sitearch}/trinity-PyQt

%__mkdir_p build
./setup.py build_libpythonize

%install
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export PYTHONPATH=%{python_sitearch}/trinity-sip:%{python_sitearch}/trinity-PyQt

# Avoids 'error: byte-compiling is disabled.' on Mandriva/Mageia
export PYTHONDONTWRITEBYTECODE=

%__rm -rf %{buildroot}

./setup.py install \
	--root=%{buildroot} \
	--prefix=%{tde_prefix} \
	--install-clib=%{tde_libdir} \
	--install-cheaders=%{tde_tdeincludedir}

# Removes BUILDROOT directory reference in installed files
for f in \
	%{buildroot}%{tde_libdir}/libpythonize.la \
	%{buildroot}%{tde_datadir}/apps/pykdeextensions/app_templates/kcontrol_module/src/KcontrolModuleWidgetUI.py \
	%{buildroot}%{tde_datadir}/apps/pykdeextensions/app_templates/kdeutility/src/KDEUtilityDialogUI.py \
; do
	%__sed -i "${f}" -e "s|%{buildroot}||g"
:
done

# Moves PYTHON libraries to distribution directory
%__mkdir_p %{buildroot}%{python_sitearch}
%__mv -f %{buildroot}%{tde_prefix}/lib/python*/site-packages/* %{buildroot}%{python_sitearch}
%__rm -rf %{buildroot}%{tde_prefix}/lib/python*/site-packages

# Removes useless files
%__rm -rf %{?buildroot}%{tde_libdir}/*.a

# Fix permissions on include files
%__chmod 644 %{?buildroot}%{tde_tdeincludedir}/*.h

%clean
%__rm -rf %{buildroot}


%post -n trinity-libpythonize0
/sbin/ldconfig

%postun -n trinity-libpythonize0
/sbin/ldconfig

%post -n trinity-libpythonize0-devel
/sbin/ldconfig

%postun -n trinity-libpythonize0-devel
/sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{tde_datadir}/apps/pykdeextensions
%{tde_tdedocdir}/HTML/en/pykdeextensions
%{python_sitearch}/*

%files -n trinity-libpythonize0
%defattr(-,root,root,-)
%{tde_libdir}/libpythonize.so.*

%files -n trinity-libpythonize0-devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/*.h
%{tde_libdir}/libpythonize.la
%{tde_libdir}/libpythonize.so


%Changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.4.0-6.opt
- 为 Magic 3.0 重建

* Tue Oct 02 2012 Francois Andriot <francois.andriot@free.fr> - 0.4.0-3
- Initial release for TDE 3.5.13.1
