Summary: GNU's bc (a numeric processing language) and dc (a calculator)
Summary(zh_CN.UTF-8): GNU 的 bc (一种数字处理语言) 和 dc (一个计算器)
Name: bc
Version: 1.06.95
Release: 7%{?dist}
License: GPLv2+
URL: http://www.gnu.org/software/bc/
Group: Applications/Engineering
Group(zh_CN.UTF-8): 应用程序/工程
Source: ftp://alpha.gnu.org/pub/gnu/bc/bc-%{version}.tar.bz2
Patch1: bc-1.06-dc_ibase.patch
Patch2: bc-1.06.95-memleak.patch
Patch3: bc-1.06.95-matlib.patch
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: readline-devel, flex, bison, texinfo

%description
The bc package includes bc and dc. Bc is an arbitrary precision
numeric processing arithmetic language. Dc is an interactive
arbitrary precision stack based calculator, which can be used as a
text mode calculator.

Install the bc package if you need its number handling capabilities or
if you would like to use its text mode calculator.

%description -l zh_CN.UTF-8
GNU 的 bc (一种数字处理语言) 和 dc (一个计算器)。

%prep
%setup -q
%patch1 -p1 -b .dc_ibase
%patch2 -p1 -b .memleak
%patch3 -p1 -b .matlib

%build
%configure --with-readline
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -e %{_infodir}/bc.info.gz -a -e %{_infodir}/dc.info.gz ]; then
  /sbin/install-info %{_infodir}/bc.info.gz %{_infodir}/dir \
  --entry="* bc: (bc).                      The GNU calculator language." || :
  /sbin/install-info %{_infodir}/dc.info.gz %{_infodir}/dir \
  --entry="* dc: (dc).                      The GNU RPN calculator." || :
fi

%preun
if [ $1 = 0 -a -e %{_infodir}/bc.info.gz -a -e %{_infodir}/dc.info.gz ]; then
  /sbin/install-info --delete %{_infodir}/bc.info.gz %{_infodir}/dir \
  --entry="* bc: (bc).                      The GNU calculator language." || :
  /sbin/install-info --delete %{_infodir}/dc.info.gz %{_infodir}/dir \
  --entry="* dc: (dc).                      The GNU RPN calculator." || :
fi

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB FAQ AUTHORS NEWS README Examples/
%{_bindir}/dc
%{_bindir}/bc
%{_mandir}/*/*
%{_infodir}/*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.06.95-7
- 为 Magic 3.0 重建

* Fri Sep 18 2015 Liu Di <liudidi@gmail.com> - 1.06.95-6
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.06.95-5
- 为 Magic 3.0 重建

* Wed Nov 02 2011 Liu Di <liudidi@gmail.com> - 1.06.95-4
- 为 Magic 3.0 重建 

