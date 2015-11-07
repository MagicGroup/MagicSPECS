%define         rc_subver     rc5

Summary:        ASCII art library
Summary(zh_CN.UTF-8): ASCII 艺术库
Name:           aalib
Version:        1.4.0
Release:        18%{dist}
License:        LGPL
Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
URL:            http://aa-project.sourceforge.net/aalib/
Source0:        http://download.sourceforge.net/aa-project/%{name}-1.4%{rc_subver}.tar.gz
Patch0:         aalib-aclocal.patch
Patch1:         aalib-config-rpath.patch
Patch2:         aalib-1.4rc5-bug149361.patch
Patch3:         aalib-1.4rc5-rpath.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  slang-devel libXt-devel gpm-devel

%description
AA-lib is a low level gfx library just as many other libraries are. The
main difference is that AA-lib does not require graphics device. In
fact, there is no graphical output possible. AA-lib replaces those
old-fashioned output methods with a powerful ASCII art renderer. The API
is designed to be similar to other graphics libraries.

%description -l zh_CN.UTF-8
AA-lib是一和个和许多其它库类似的一个低级别GFX库。
主要不一样的地方在于AA-lib不需要图形设备。事实上，
它也不允许图形输出。AA-lib用一个强力的ASCII艺术渲染器
替换了老旧的输出方式。API设计的其它图形库是一样的。


%package devel
Summary:        Development files for aalib
Summary(zh_CN.UTF-8): aalib的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8):   开发/库
Requires:       %{name} = %{version}-%{release}
Requires(post):  /sbin/install-info
Requires(postun): /sbin/install-info

%description devel
This package contains header files and other files needed to develop
with aalib.

%description devel -l zh_CN.UTF-8
这个包包含了使用aalib开发所需的头文件和其它文件


%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1 -b .bug149361
%patch3 -p1 -b .rpath
sed -i -e 's/^\(.*SHARED.*\)@AALIB_LIBS@/\1 -laa/' aalib-config.in
# sigh stop autoxxx from rerunning because of our patches above.
touch aclocal.m4
touch configure
touch src/stamp-h.in
touch src/config.h.in
touch `find -name Makefile.in`


%build
%configure --disable-static
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT{%{_libdir}/libaa.la,%{_infodir}/dir}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/libaa.info %{_infodir}/dir 2>/dev/null || :

%preun devel
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/libaa.info %{_infodir}/dir \
    2>/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc README COPYING ChangeLog NEWS
%{_bindir}/aafire
%{_bindir}/aainfo
%{_bindir}/aasavefont
%{_bindir}/aatest
%{_libdir}/libaa.so.*
%{_mandir}/man1/aafire.1*

%files devel
%defattr(-,root,root,-)
%{_bindir}/aalib-config
%{_mandir}/man3/*
%{_libdir}/libaa.so
%{_includedir}/aalib.h
%{_infodir}/aalib.info*
%{_datadir}/aclocal/aalib.m4

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.4.0-18
- 为 Magic 3.0 重建

* Sun Sep 27 2015 Liu Di <liudidi@gmail.com> - 1.4.0-17
- 为 Magic 3.0 重建

* Tue May 14 2013 Liu Di <liudidi@gmail.com> - 1.4.0-16
- 重新编译

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.4.0-15
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.4.0-14
- 为 Magic 3.0 重建

* Tue Dec 04 2012 Liu Di <liudidi@gmail.com> - 1.4.0-13
- 为 Magic 3.0 重建

* Mon Oct 24 2011 Liu Di <liudidi@gmail.com> 1.4.0-12
- 重建

* Fri Sep 15 2006 Liu Di <liudidi@gmail.com> 1.4.0-9.1mgc
- Rebuild for Magic
