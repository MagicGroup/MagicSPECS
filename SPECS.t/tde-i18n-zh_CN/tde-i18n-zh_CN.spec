%define git 1
%define gitdate	20111225

Name: 	 tde-i18n-zh_CN
Summary: Chinese-Simplified(zh_CN) language support for KDE
Summary(zh_CN.UTF-8): KDE 的简体中文(zh_CN)语言支持
Group:	 User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Version: 3.5.14
%if %{git}
Release: 0.git%{gitdate}%{?dist}
%else
Release: 4%{?dist}
%endif
%if %git
Source0:	%{name}-git%{?gitdate}.tar.xz
%else
Source0:	 kde-i18n-zh_CN-%{version}.tar.bz2
%endif
Source1:	make_tde-i18n-zh_CN_git_package.sh
Patch1: kde-i18n-zh_CN-extra_option.patch
Patch2: tde-i18n-zh_CN-libtool.patch
Patch3:	tde-i18n-zh_CN-htmldir.patch
License: GPL
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildArch: noarch

# We manually specifiy dependancies. 
AutoReq: no 

%if "%{is_release}" != "1"
BuildRequires: autoconf > 2.53
BuildRequires: automake >= 1.6
%endif
# BuildRequires: kdelibs-devel >= %{kdelibs_ver}
BuildRequires: findutils

Requires: tdelibs

%description
Chinese-Simplified language support for KDE

%description -l zh_CN.UTF-8
KDE 的简体中文语言支持。

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate} 
%else
%setup -q
%endif

%patch2 -p1
%patch3 -p1

%build
unset QTDIR || : ; . /etc/profile.d/qt.sh

export OLD_PO_FILE_INPUT=yes

make -f admin/Makefile.common
# This breaks configure...(??), what's up with @ anyway? -- Rex
export DO_NOT_COMPILE="sr@Latn"

%configure 

make %{_smp_mflags}


%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install


# Remove zero length files
for i in $(find %{buildroot}%{_docdir}/HTML -size 0) ; do
   rm -f "$i"
done

# conflict with other packages
rm -f %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/{amarok.mo,gwenview.mo,kaffeine.mo,ktorrent.mo,kftpgrabber.mo,smb4k.mo}

%files
%defattr(-,root,root)
%lang(zh_CN) %{_datadir}/locale/zh_CN/*
%lang(zh_CN) %doc %{_docdir}/kde/HTML/zh_CN

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}


%changelog
* Fri Dec 23 2011 Liu Di <liudidi@gmail.com> - 3.5.10-4
- 为 Magic 3.0 重建

* Fri Dec 23 2011 Liu Di <liudidi@gmail.com> - 3.5.10-3
- 为 Magic 3.0 重建

* Mon Sep 01 2008 Liu Di <liudidi@gmail.com> - 3.5.10-1mgc
- 更新到 3.5.10

* Wed Feb 19 2008 Liu Di <liudidi@gmail.com> - 3.5.9-1mgc
- update to 3.5.9

* Fri Oct 19 2007 Liu Di <liudidi@gmail.com> - 3.5.8-1mgc
- update to 3.5.8

* Tue May 29 2007 kde <athena_star {at} 163 {dot} com> - 3.5.7-1mgc
- update to 3.5.7

* Sat Jan 27 2007 Liu Di <liudidi@gmail.com> - 3.5.6-1mgc
- update to 3.5.6

* Wed Nov 08 2006 Liu Di <liudidi@gmail.coM> - 3.5.5-1mgc
- update to 3.5.5

* Fri Aug 25 2006 Liu Di <liudidi@gmail.com> - 3.5.4-1mgc
- update to 3.5.4

* Thu Jul  1 2006 Liu Di <liudidi@gmail.com> - 3.5.3-1mgc
- update to 3.5.3

* Sun Apr 16 2006 KanKer <kanker@163.com>
-3.5.2

* Fri Feb 10 2006 KanKer <kanker@163.com>
- update kdevelop's po

* Sun Jan 15 2006 KanKer <kanker@163.com>
- add extra option translations in kdebase

* Thu Oct 18 2005 KanKer <kanker@163.com>
- 3.4.3

* Wed Jun 1 2005 KanKer <kanker@163.com>
- 3.4.1

* Sat Mar 19 2005 KanKer <kanker@163.com>
- 3.4.0

* Fri Dec 17 2004 KanKer <kanker@163.com>
- updateto 3.3.2

* Fri Oct 15 2004 KanKer <kanker@163.com>
- update to 3.3.1 for ML.

* Sat Aug 21 2004 KanKer <kanker@163.com>
- 3.3

* Sun Jul 11 2004 KanKer <kanker@163.com>
-3.2beta1

* Thu Jun 10 2004 KanKer <kanker@163.com>
- 3.2.3
* Mon Apr 05 2004 Rex Dieter <rexdieter at sf.net> 1:3.2.2-0.fdr.0
- 3.2.2
