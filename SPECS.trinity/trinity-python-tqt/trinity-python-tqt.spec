#
# spec file for package python-tqt (version R14)
#
# Copyright (c) 2014 Trinity Desktop Environment
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg python-tqt
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	3.18.1
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.2
Summary:	TQt bindings for Python
Summary(zh_CN.UTF-8): TQt 的 Python 绑定
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Project
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Obsoletes:		trinity-PyQt
Obsoletes:		trinity-python-qt3

BuildRequires:	tqt3-apps-devel >= 3.5.0
BuildRequires:	libtqt4-devel >= %{?epoch:%{epoch}:}4.2.0
BuildRequires:	trinity-filesystem >= %{tde_version}
BuildRequires:	sip4-tqt-devel >= %{?epoch:%{epoch}:}4.10.5
BuildRequires:	libtqscintilla-devel >= %{?epoch:%{epoch}:}1.7.1

BuildRequires:	gcc-c++
BuildRequires:	python
BuildRequires:	python-devel

# MESA support
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libGLU-devel

# XMU support
BuildRequires: libXmu-devel

%description
Python binding module that allows use of TQt X Window toolkit v3.
You can use it to create portable graphics-capable scripts.

At this moment python-tqt offers a vast subset of TQt API. There are
some minor issues related to the differences between C++ and Python
(types, etc), but usually you'll be able to write code pretty much the
same way in both languages (with syntax differences, of course)

%description -l zh_CN.UTF-8
TQt 的 Python 绑定。

##########

%package -n python-tqt
Summary:	TQt bindings for Python
Summary(zh_CN.UTF-8): TQt 的 Python 绑定
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	trinity-filesystem >= %{tde_version}
Requires:	sip4-tqt >= %{?epoch:%{epoch}:}4.10.5
Requires:	libtqt4 >= %{?epoch:%{epoch}:}4.2.0

%description -n python-tqt
Python binding module that allows use of TQt X Window toolkit v3.
You can use it to create portable graphics-capable scripts.

At this moment python-tqt offers a vast subset of TQt API. There are
some minor issues related to the differences between C++ and Python
(types, etc), but usually you'll be able to write code pretty much the
same way in both languages (with syntax differences, of course)

%description -n python-tqt -l zh_CN.UTF-8
TQt 的 Python 绑定。

%files -n python-tqt
%defattr(-,root,root,-)
%doc NEWS README
%dir %{python_sitearch}/python_tqt
%{python_sitearch}/python_tqt/__init__.py*
%{python_sitearch}/python_tqt/qt.so
%{python_sitearch}/python_tqt/qtcanvas.so
%{python_sitearch}/python_tqt/qtnetwork.so
%{python_sitearch}/python_tqt/qtsql.so
%{python_sitearch}/python_tqt/qttable.so
%{python_sitearch}/python_tqt/qtui.so
%{python_sitearch}/python_tqt/qtxml.so

##########

%package -n python-tqt-gl
Summary:	TQt OpenGL bindings for Python
Summary(zh_CN.UTF-8): TQt OpenGL 的 Python 绑定
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	python-tqt = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python-tqt-gl
Python binding module that allows use of the OpenGL facilities
offered by the TQt X Window toolkit v3. You can use it to create
portable graphics-capable scripts.

%description -n python-tqt-gl -l zh_CN.UTF-8
TQt OpenGL 的 Python 绑定。

%files -n python-tqt-gl
%defattr(-,root,root,-)
%{python_sitearch}/python_tqt/qtgl.so

##########

%package -n python-tqt-tqtext
Summary:	TQtext extensions for python-tqt
Group:		Development/Libraries/Python
Requires:	python-tqt = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python-tqt-tqtext
python-tqt Extensions. Contains:

* TQScintilla: a featureful TQt source code editing component based
              on Scintilla.

%files -n python-tqt-tqtext
%defattr(-,root,root,-)
%{python_sitearch}/python_tqt/qtext.so

##########

%package -n trinity-pytqt-tools
Summary:	Pyuic and pylupdate for TQt
Group:		Development/Libraries/Python
Requires:	python-tqt = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n trinity-pytqt-tools
pyuic is the PyQt counterpart for TQt's uic. It takes an XML
user interface file and generates Python code.

pylupdate is the counterpart for TQt's lupdate. It updates TQt
Linguist translation files from Python code.

%files -n trinity-pytqt-tools
%defattr(-,root,root,-)
%{tde_bindir}/pylupdate
%{tde_bindir}/pyuic

##########

%package -n python-tqt-devel
Summary:	TQt bindings for Python - Development files
Group:		Development/Libraries/Python
Requires:	python-tqt = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	trinity-pytqt-tools = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	libtqt4-devel >= %{?epoch:%{epoch}:}4.2.0

%description -n python-tqt-devel
Development .sip files with definitions of PyQt classes. They
are needed to build PyQt, but also as building blocks of other
packages based on them, like PyTDE.

%files -n python-tqt-devel
%defattr(-,root,root,-)
%{python_sitearch}/python_tqt/pyqtconfig.py*
%dir %{_datadir}/sip
%{_datadir}/sip/tqt/

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

mkdir build
cd build

# WTF ? CentOS 6 !
cp -rf ../pyuic3 ../pylupdate3 

echo yes | %__python ../configure.py \
	-c -n %{_includedir}/tqscintilla \
	-q %{_datadir}/tqt3 \
	-y tqt-mt \
	-o %{_libdir} -u -j 10 \
	-d %{python_sitearch}/python_tqt \
	-v %{_datadir}/sip/tqt \
	-b %{tde_bindir} \
	-w \
	CXXFLAGS_RELEASE="" CXXFLAGS="${RPM_OPT_FLAGS} -I%{_includedir}/tqt" STRIP=""

%__make


%install
%__rm -rf %{?buildroot}
%__make install DESTDIR=%{?buildroot} -C build

%__install -d %{?buildroot}%{_datadir}/sip/
%__cp -rf sip/* %{?buildroot}%{_datadir}/sip/tqt/


%clean
%__rm -rf %{?buildroot}%{python_sitearch}/python_tqt/__init__.py


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:3.18.1-1.opt.2
- 为 Magic 3.0 重建

* Tue Oct 06 2015 Liu Di <liudidi@gmail.com> - 2:3.18.1-1.opt.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 3.18.1-1
- Initial release for TDE R14.0.0
