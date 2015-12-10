Summary:        The GNU Portable Threads library
Summary(zh_CN.UTF-8):	GNU 可移植线程库
Name:           pth
Version:        2.0.7
Release:        13%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
URL:            http://www.gnu.org/software/pth/
Source:         ftp://ftp.gnu.org/gnu/pth/pth-%{version}.tar.gz
Source1:        ftp://ftp.gnu.org/gnu/pth/pth-%{version}.tar.gz.sig
Patch1:         pth-2.0.7-dont-remove-gcc-g.patch
Patch2:         pth-2.0.7-config-script.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Pth is a very portable POSIX/ANSI-C based library for Unix platforms
which provides non-preemptive priority-based scheduling for multiple
threads of execution ("multithreading") inside server applications.
All threads run in the same address space of the server application,
but each thread has it's own individual program-counter, run-time
stack, signal mask and errno variable.

%description -l zh_CN.UTF-8
GNU 可移植线程库。

%package devel
Summary:        Development headers and libraries for GNU Pth
Summary(zh_CN.UTF-8):	%{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers and libraries for GNU Pth.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch1 -p1 -b .dont-remove-gcc-g
%patch2 -p1 -b .config-script


%build
%configure --disable-static ac_cv_func_sigstack='no'

# Work around multiarch conflicts in the pth-config script in order
# to complete patch2. Make the script choose between /usr/lib and
# /usr/lib64 at run-time.
if [ "%_libdir" == "/usr/lib64" ] ; then
    if grep -e '^pth_libdir="/usr/lib64"' pth-config ; then
        sed -i -e 's!^pth_libdir="/usr/lib64"!pth_libdir="/usr/lib"!' pth-config
    else
        echo "ERROR: Revisit the multiarch pth_libdir fixes for pth-config!"
        exit 1
    fi
fi
if grep -e "$RPM_OPT_FLAGS" pth-config ; then
    # Remove our extra CFLAGS from the pth-config script, since they
    # don't belong in there.
    sed -i -e "s!$RPM_OPT_FLAGS!!g" pth-config
else
    echo "ERROR: Revisit the multiarch CFLAGS fix for pth-config!"
    exit 1
fi

# this is necessary; without it make -j fails
make pth_p.h
make %{?_smp_mflags}


%check
make test
l=$($(pwd)/pth-config --libdir)
%ifarch x86_64 ppc64
    [ "$l" == "/usr/lib64" ]
%endif


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ANNOUNCE AUTHORS COPYING ChangeLog HISTORY NEWS PORTING README
%doc SUPPORT TESTS THANKS USERS
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc HACKING
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/*/*
%{_datadir}/aclocal/*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.0.7-13
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.0.7-12
- 为 Magic 3.0 重建

* Fri Aug 07 2015 Liu Di <liudidi@gmail.com> - 2.0.7-11
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.0.7-10
- 为 Magic 3.0 重建

* Wed Oct 10 2012 Liu Di <liudidi@gmail.com> - 2.0.7-9
- 为 Magic 3.0 重建

* Wed Jan 25 2012 Liu Di <liudidi@gmail.com> - 2.0.7-8
- 为 Magic 3.0 重建


