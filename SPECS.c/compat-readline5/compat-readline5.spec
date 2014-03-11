Summary: A library for editing typed command lines
Name: compat-readline5
Version: 5.2
Release: 21%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
Source: ftp://ftp.gnu.org/gnu/readline/readline-%{version}.tar.gz
Patch1: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-001
Patch2: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-002
Patch3: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-003
Patch4: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-004
Patch5: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-005
Patch6: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-006
Patch7: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-007
Patch8: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-008
Patch9: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-009
Patch10: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-010
Patch11: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-011
Patch12: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-013
Patch13: ftp://ftp.gnu.org/gnu/readline/readline-5.2-patches/readline52-014
# fix file permissions, remove RPATH, use CFLAGS
Patch20: readline-5.2-shlib.patch
# fixed in readline-6.0
Patch21: readline-5.2-redisplay-sigint.patch
BuildRequires: ncurses-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Readline library provides a set of functions that allow users to
edit command lines. Both Emacs and vi editing modes are available. The
Readline library includes additional functions for maintaining a list
of previously-entered command lines for recalling or editing those
lines, and for performing csh-like history expansion on previous
commands.

%package devel
Summary: Files needed to develop programs which use the readline library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: ncurses-devel

%description devel
The Readline library provides a set of functions that allow users to
edit typed command lines. If you want to develop programs that will
use the readline library, you need to have the readline-devel package
installed. You also need to have the readline package installed.

%package static
Summary: Static libraries for the readline library
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The readline-static package contains the static version of the readline
library.

%prep
%setup -q -n readline-%{version}
%patch1 -p0 -b .001
%patch2 -p0 -b .002
%patch3 -p0 -b .003
%patch4 -p0 -b .004
%patch5 -p0 -b .005
%patch6 -p0 -b .006
%patch7 -p0 -b .007
%patch8 -p0 -b .008
%patch9 -p0 -b .009
%patch10 -p0 -b .010
%patch11 -p0 -b .011
%patch12 -p0 -b .013
%patch13 -p0 -b .014
%patch20 -p1 -b .shlib
%patch21 -p1 -b .redisplay-sigint

%build
export CPPFLAGS="-I%{_includedir}/ncurses"
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT{/%{_lib},%{_libdir}/readline5}
mv $RPM_BUILD_ROOT%{_libdir}/lib*.a $RPM_BUILD_ROOT%{_libdir}/readline5

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.so
ln -sf ../libreadline.so.5 $RPM_BUILD_ROOT%{_libdir}/readline5/libreadline.so
ln -sf ../libhistory.so.5 $RPM_BUILD_ROOT%{_libdir}/readline5/libhistory.so

mkdir $RPM_BUILD_ROOT%{_includedir}/readline5
mv $RPM_BUILD_ROOT%{_includedir}/readline{,5}

rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -rf $RPM_BUILD_ROOT%{_mandir}

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES COPYING NEWS README USAGE
%{_libdir}/libreadline*.so.*
%{_libdir}/libhistory*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/readline5
%dir %{_libdir}/readline5
%{_libdir}/readline5/lib*.so

%files static
%defattr(-,root,root,-)
%{_libdir}/readline5/lib*.a

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 5.2-21
- 为 Magic 3.0 重建

* Sun Apr 15 2012 Liu Di <liudidi@gmail.com> - 5.2-20
- 为 Magic 3.0 重建

