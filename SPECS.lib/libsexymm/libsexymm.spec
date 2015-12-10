Name:           libsexymm
Version:        0.1.9
Release:        11%{?dist}

Summary:        C++ wrapper for libsexy
Summary(zh_CN.UTF-8):	libsexy 的 C++ 绑定

Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License:        LGPLv2+
URL:            http://www.chipx86.com/wiki/Libsexy
Source0:        http://releases.chipx86.com/libsexy/libsexymm/libsexymm-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  gtkmm24-devel >= 2.4.0
BuildRequires:  libsexy-devel >= 0.1.10
BuildRequires: libxml2-devel

%description
libsexymm is a set of C++ bindings around libsexy, 
compatible with programs using gtkmm.

%description -l zh_CN.UTF-8
libsexymm 是 libsexy 的 C++ 绑定，和 gtkmm 程序兼容。

%package devel
Summary:        Headers for developing programs that will use libsexymm
Summary(zh_CN.UTF-8): %name 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       gtkmm24-devel >= 2.4.0
Requires:       libsexy-devel >= 0.1.10

%description devel
This package contains the headers that programmers will need to
develop applications which will use libsexymm.

%description devel -l zh_CN.UTF-8
%name 的开发包。


%prep
%setup -q -n libsexymm-%{version}


%build
%configure --disable-static --enable-docs

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
mkdir -p $RPM_BUILD_ROOT%{_datadir}/libsexymm/
mv $RPM_BUILD_ROOT%{_libdir}/libsexymm/include/libsexymmconfig.h \
 $RPM_BUILD_ROOT%{_includedir}/libsexymm/libsexymmconfig.h
mv $RPM_BUILD_ROOT%{_libdir}/libsexymm/proc/ \
 $RPM_BUILD_ROOT%{_datadir}/libsexymm/

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, -)
%doc COPYING ChangeLog INSTALL NEWS
%{_libdir}/*.so.*


%files devel
%defattr(-, root, root, -)
%{_includedir}/libsexymm/
%dir %{_datadir}/libsexymm
%{_datadir}/libsexymm/proc
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.1.9-11
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.1.9-10
- 为 Magic 3.0 重建

* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 0.1.9-9
- 为 Magic 3.0 重建

