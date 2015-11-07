#Note: %{nil} stand for none.
%define subver %{nil}
%define _date 20111229
%define _release %(if [ "X%{_date}" != "X" ]; then echo "0.cvs.%{_date}."; fi)2%{?dist}

%define git 0
%define gitdate 20111229

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg eva
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

Summary: Eva is the client end of QQ for KDE.
Summary(zh_CN.UTF-8): KDE 下的 QQ 客户端
Name: trinity-%{tde_pkg}
Version: 0.4.92
%if %{git}
Release: 0.git%{gitdate}%{?dist}.3
%else
Release: %{_release}.3
%endif
License: GPL
URL: http://www.sourceforge.net/projects/evaq
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
%if %{git}
Source0: %{name}-git%{gitdate}.tar.xz
%else
Source0: %{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.bz2
%endif
Source1: make_eva_git_package.sh
Patch1: eva-gcc44.patch
Prefix: %{_prefix}
Requires: libtqt3-mt, trinity-tdelibs, trinity-tdebase
Packager: Bamfox<bamfox@163.com>, kde <jack@linux.net.cn>

%description
Eva is the client end of QQ for KDE.

%description -l zh_CN.UTF-8
Eva 是 KDE 下的一个 QQ (腾讯)客户端。

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
#%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}


%files
%defattr(-,root,root)
%{tde_bindir}
%{tde_datadir}

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.4.92-0.cvs.20111229.2.3
- 为 Magic 3.0 重建

* Thu Oct 08 2015 Liu Di <liudidi@gmail.com> - 0.4.92-0.cvs.20111229.2.2
- 为 Magic 3.0 重建

* Thu Oct 08 2015 Liu Di <liudidi@gmail.com> - 0.4.92-0.cvs.20111229.2.1
- 为 Magic 3.0 重建

* Mon Jan 21 2008 KanKer <kanker@163.com> - 0.4.91-0.cvs.20080120.1mgc
- update to 20080120

* Mon Jun 25 2007 kde <athena_star {at} 163 {dot} com> -0.4.2-0.cvs.20070623.1mgc
- update to 20070623

* Fri Apr 6 2007 kde <athena_star {at} 163 {dot} com> -0.4.2-0.cvs.20070403.1mgc
- update to 20070403

* Wed  Sep 06 2006 bamfox <bamfox@163.com> 0.4.1-4mgc
- update to last version of eva-0.4.1-20060906

* Wed Aug  16 2006 bamfox <bamfox@163.com> 0.4.1-3mgc
- update to last version of eve-0.4.1

* Thu Feb 9 2006 kde <jack@linux.net.cn> 0.4.1-2mgc
- update to 0.4.1

* Tue Jan 24 2006 kde <jack@linux.net.cn> 0.4.1-1mgc
- update to 0.4.1

* Tue Jan 24 2006 kde <jack@linux.net.cn> 0.4.0-2mgc
- update to 0.4.0
- fix the QQ version

* Sun Oct 2 2005 kde <jack@linux.net.cn> 0.3.2-1mgc
- update to 0.3.2-1

* Mon Mar 14 2005 bamfox<bamfox@163.com> 0.2.0-1mgc
- update to 0.2.0

* Sun Mar 13 2005 bamfox<bamfox@163.com> 0.2.0.20050312-2mgc
- fix a bug about smile face

* Sat Mar 12 2005 bamfox<bamfox@163.com> 0.2.0.20050312-1mgc
- update to 0.2.0.20050312

* Fri Mar 4 2005 kde <jack@linux.net.cn> 0.2.0.20050301-4mgc
- patch the systemtray

* Thu Mar 3 2005 kde <jack@linux.net.cn> 0.2.0.20050301-3mgc
- modify the spec file and rebuild

* Thu Mar 01 2005 Bamfox<bamfox@163.com> 0.2.0.20050301-2mgc
- correct the zh_CN translation

* Mon Feb 28 2005 Bamfox<bamfox@163.com> 0.2.0.20050301-1mgc
- built for MagicLinux-1.2
