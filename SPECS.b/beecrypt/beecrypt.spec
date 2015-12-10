%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:	An open source cryptography library
Summary(zh_CN.UTF-8): 一个开源的加密算法库
Name:		beecrypt
Version:	4.2.1
Release:	8%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://beecrypt.sourceforge.net/
Source:		http://downloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Patch0:		beecrypt-4.1.2-biarch.patch
Patch1:		beecrypt-4.2.1-no-c++.patch
BuildRequires:	autoconf, automake, libtool
BuildRequires:	tetex-dvips, tetex-latex, graphviz
BuildRequires:	doxygen, m4, python-devel
BuildRequires:	texlive-doublestroke
Obsoletes:	beecrypt-java <= 4.1.2-3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
BeeCrypt is an ongoing project to provide a strong and fast cryptography
toolkit. Includes entropy sources, random generators, block ciphers, hash
functions, message authentication codes, multiprecision integer routines
and public key primitives.

%description -l zh_CN.UTF-8
一个开源的加密算法库。

%package devel
Summary:	Development files for the beecrypt toolkit and library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}

%description devel
The beecrypt-devel package includes header files and libraries necessary
for developing programs which use the beecrypt C toolkit and library. And
beecrypt is a general-purpose cryptography library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package apidocs
Summary:	API documentation for beecrypt toolkit and library
Summary(zh_CN.UTF-8): %{name} 的 API 文档
Group:		Documentation
Group(zh_CN.UTF-8): 文档

%description apidocs
Beecrypt is a general-purpose cryptography library. This package contains
API documentation for developing applications with beecrypt.

%description apidocs -l zh_CN.UTF-8
%{name} 的 API 文档。

%package python
Summary:	Files needed for python applications using beecrypt
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}

%description python
Beecrypt is a general-purpose cryptography library. This package contains
files needed for using python with beecrypt.

%description python -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%prep
%setup -q
%patch0 -p1 -b .biarch
%patch1 -p1 -b .no-c++
libtoolize
autoreconf -i

%build
%configure --with-cplusplus=no --with-java=no
make %{?_smp_mflags} pythondir=%{python_sitelib}

cd include/beecrypt
doxygen
cd ../..

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT pythondir=%{python_sitelib} install
rm -f $RPM_BUILD_ROOT{%{_libdir},%{python_sitelib}}/*.{a,la}

iconv -f ISO-8859-1 -t UTF-8 CONTRIBUTORS -o CONTRIBUTORS.utf8
mv -f CONTRIBUTORS.utf8 CONTRIBUTORS

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS BENCHMARKS CONTRIBUTORS
%doc COPYING COPYING.LIB NEWS README
%{_libdir}/libbeecrypt.so.*

%files devel
%defattr(-,root,root,-)
%doc BUGS 
%{_includedir}/%{name}
%{_libdir}/libbeecrypt.so

%files apidocs
%defattr(-,root,root,-)
%doc docs/html

%files python
%defattr(-,root,root,-)
%{python_sitelib}/_bc.so

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 4.2.1-8
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 4.2.1-7
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 4.2.1-5
- 为 Magic 3.0 重建

