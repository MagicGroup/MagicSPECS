#
# spec file for package python-trinity (version R14)
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

%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg python-trinity
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	3.16.3
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Summary:	Trinity bindings for Python
Group:		Development/Libraries/Python
URL:		http://www.trinitydesktop.org/
#URL:		http://www.simonzone.com/software/pykdeextensions

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}

BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++

# PYTHON support
BuildRequires:	python
BuildRequires:	python-tqt-devel
Requires:		python-tqt

# SIP
BuildRequires:	sip4-tqt-devel >= 4.10.5
Requires:		sip4-tqt >= 4.10.5

Obsoletes:	python-trinity < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python-trinity = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Python binding module that provides wide access to the Trinity API,
also known as PyTDE. Using this, you'll get (for example) classes
from tdeio, tdejs, tdehtml and tdeprint.

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{python_sitearch}/*.so
%{python_sitearch}/dcop*.py*
%{python_sitearch}/pytde*.py*

##########

%package devel
Summary:	Trinity bindings for Python - Development files and scripts
Group:		Development/Libraries/Python
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:	python-trinity-devel < %{version}-%{release}
Provides:	python-trinity-devel = %{version}-%{release}

%description devel
Development .sip files with definitions of PyTDE classes. They
are needed to build PyTDE, but also as building blocks of other
packages based on them. 
The package also contains kdepyuic, a wrapper script around PyQt's 
user interface compiler.

%files devel
%defattr(-,root,root,-)
%{tde_bindir}/tdepyuic
# The SIP files are outside TDE's prefix
%{_datadir}/sip/trinity/

##########

%package doc
Summary:	Documentation and examples for PyTDE
Group:		Development/Libraries/Python

Obsoletes:	python-trinity-doc < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python-trinity-doc = %{?epoch:%{epoch}:}%{version}-%{release}

%description doc
General documentation and examples for PyTDE providing programming
tips and working code you can use to learn from.

%files doc
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/en/python-trinity/

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export LD_RUN_PATH="%{tde_libdir}"

export DH_OPTIONS

%__python configure.py \
	-k %{tde_prefix} \
	-L %{_lib} \
	-v %{_datadir}/sip/trinity

%__make %{_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Install documentation
%__mkdir_p %{buildroot}%{tde_tdedocdir}/HTML/en/
%__cp -rf doc %{buildroot}%{tde_tdedocdir}/HTML/en/python-trinity/


%clean
%__rm -rf %{buildroot}


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:3.16.3-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:3.16.3-1
- Initial release for TDE 14.0.0
