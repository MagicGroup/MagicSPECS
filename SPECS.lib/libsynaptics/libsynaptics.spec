Name:           libsynaptics
Version:        0.14.6c
Release:        3%{?dist}
Summary:        Synaptics touchpad driver library
Summary(zh_CN.UTF-8):	Synaptics触摸板驱动库

Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
License:        GPL
URL:            http://qsynaptics.sourceforge.net/
Source0:        http://qsynaptics.sourceforge.net/libsynaptics-%{version}.tar.bz2
Patch0:		%{name}-%{version}-xinclude.patch
Patch1:		libsynaptics-0.14.6c-gcc44.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  xorg-x11-proto-devel


%description
A small C++ library usable by the synaptics driver.
The version numbering will follow any driver releases, the appended letter
marks releases due to bug fixing.

%description -l zh_CN.UTF-8
一个由synaptics驱动使用的小C++库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8):	%{name}的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%name-devel包包含了使用%name开发所需要的静态库和头文件。


%prep
%setup -q
%patch1 -p1

%build
%configure --disable-static CPPFLAGS="-I/usr/X11/include" LDFLAGS="-L/usr/X11/lib"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.14.6c-3
- 为 Magic 3.0 重建

* Wed Feb 28 2007 Liu Di <liudidi@gmail.com> - 0.14.6c-1mgc
- update to 0.14.6c

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 0.14.6b-1mgc
- reubild for Magic

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.14.6b-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Aug 29 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.14.6b-3
- Rebuild for FC6

* Mon Jul 31 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.14.6b-2
- Add BR xorg-x11-proto-devel

* Fri Jul 28 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.14.6b-1
- Initial Fedora Extras version
