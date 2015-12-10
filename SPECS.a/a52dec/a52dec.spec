Summary: Library for decoding ATSC A/52 (aka AC-3) audio streams
Summary(zh_CN.UTF-8): 解码 ATSC A/52(aka AC-3) 声音流的开发库
Name: a52dec
Version: 0.7.4
Release: 9%{?dist}
License: GPL
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL: http://liba52.sourceforge.net/
Source: http://liba52.sourceforge.net/files/a52dec-%{version}.tar.gz
Patch: a52dec-0.7.4-PIC.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc-c++
BuildRequires: autoconf, automake, libtool

%description
liba52 is a free library for decoding ATSC A/52 streams. It is released
under the terms of the GPL license. The A/52 standard is used in a
variety of applications, including digital television and DVD. It is
also known as AC-3.

%description -l zh_CN.UTF-8
liba52是一个自由的解码 ATSC A/52 流的库。它在 GPL 授权下分发。
A/52一般是用在数字电视和DVD的应用程序上。它也被称做 AC-3


%package devel
Summary: Development header files and static library for liba52
Summary(zh_CN.UTF-8): liba52的开发头文件和静态链接库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}

%description devel
liba52 is a free library for decoding ATSC A/52 streams. It is released
under the terms of the GPL license. The A/52 standard is used in a
variety of applications, including digital television and DVD. It is
also known as AC-3.

These are the header files and static libraries from liba52 that are needed
to build programs that use it.

%description devel -l zh_CN.UTF-8
这是liba52的头文件和静态库文件，编译程序可以需要使用它。


%prep
%setup
%patch -p1 -b .PIC


%build
%{__libtoolize} --force
%{__aclocal}
%{__automake} -a
%{__autoconf}
%configure --enable-shared
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%makeinstall
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}
%{__rm} -rf %{builddir}/%{name}-%{version}

%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null


%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING HISTORY NEWS README TODO doc/liba52.txt
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*


%files devel
%defattr(-, root, root, 0755)
%{_includedir}/*
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/*.so


%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 0.7.4-9
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.7.4-8
- 为 Magic 3.0 重建

* Tue May 14 2013 Liu Di <liudidi@gmail.com> - 0.7.4-6
- 重新编译

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.7.4-5
- 为 Magic 3.0 重建

* Mon Oct 24 2011 Liu Di <liudidi@gmail.com> - 0.7.4-4
- Rebuild

* Tue Oct 11 2008 Liu Di <liudidi@gmail.com> - 0.7.4-2mgc25
- 在 Magic 2.5 上重建

