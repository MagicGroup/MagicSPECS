Name:	 	cce
Version:	0.51
Release:	9%{?dist}
Summary:	A CJK console with many input method.
Summary(zh_CN.UTF-8): 带有多种输入法的CJK控制台
Group:		System Environment/Shells
Group(zh_CN.UTF-8):   系统环境/外壳
License:	GPL
URL:		http://sourceforge.net/projects/cce2k/
Source0:	cce-0.51.tar.bz2
#新版 glibc 下编译出来的运行会出错，临时用一个老版本的替换掉
Source1:	cin2tab
#Source: cce-0.51-02132004-dist.tgz
Patch1: cce-gcc4.patch       
Patch2: cce-0.51-newkernel.patch
Patch3:	cce-fb-vga.diff
Patch4: cce-0.51-fixwarnings.patch
Patch5: cce-0.51-sdlfirst.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:	SDL
##Requires:	xorg-x11
BuildRequires:SDL-devel
##BuildRequires:xorg-x11-devel

%description
CCE let you display and input Chinese/Japanese/Korean/UTF8 in many OS: Linux *BSD Solaris LynxOS QNX SCOUnix Minix Hurd BeOS Windows Darwin MacOSX. It supports console(framebuffer/VGA) & X11(through GGI/SDL), bitmap/TrueType fonts and many input methods.

%description -l zh_CN.UTF-8
CCE 使您能在多种操作系统里显示和输入中文/日文/韩文/UTF-8：Linux *BSD Solaris LynxOS QNX SCOUnix Minix Hurd BeOS Windows Darwin MacOSX。它支持控制台(祯缓冲/VGA)以及 X11(通过 GGI/SDL)，bitmap/TrueType 字体和众多输入法。

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%configure --disable-lrmi
#临时的处理措施
make || cp %{SOURCE1} inputs/utils -f
make DESTDIR=%{buildroot}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall
rm -rf $RPM_BUILD_ROOT%{_bindir}/cceb5
rm -rf $RPM_BUILD_ROOT%{_bindir}/cceconv
rm -rf $RPM_BUILD_ROOT%{_bindir}/ccegbk
rm -rf $RPM_BUILD_ROOT%{_bindir}/ccejis
rm -rf $RPM_BUILD_ROOT%{_bindir}/cceksc

%post
cd %{_bindir}
ln -sf ./cce ./cceb5
ln -sf ./cce ./cceconv
ln -sf ./cce ./ccegbk
ln -sf ./cce ./ccejis
ln -sf ./cce ./cceksc

%postun
cd %{_bindir}
rm -rf ./cceb5
rm -rf ./cceconv
rm -rf ./ccegbk
rm -rf ./ccejis
rm -rf ./cceksc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README README.Linux
%{_bindir}/*
%{_datadir}/cce/*
%{_mandir}/man1/*1*


%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 0.51-9
- 为 Magic 3.0 重建

* Thu Jan 10 2013 Liu Di <liudidi@gmail.com> - 0.51-8
- 为 Magic 3.0 重建

* Mon Feb 02 2009 Liu Di <liudidi@gmail.com> - 0.51-5
- 在 gcc 4 上编译
- 添加 gcc 4 编译补丁
- 添加在新内核上编译的补丁

* Tue Jul 26 2005 kde <jack@linux.net.cn> 0.51-2mgc
- rebuild based on xorg-x11 6.8.2
- fix the spec file

* Sun Sep 19 2004 kde <jack@linux.net.cn>
- 0.51 release
- initialize the first spec file
