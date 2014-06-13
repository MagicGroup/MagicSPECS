%define git 1
%define gitdate 20111215
%define real_name      kchmviewer
%define version    3.1
%if %{git}
%define release	   0.git%{gitdate}%{?dist}
%else
%define release    1%{?dist}
%endif

%define prefix     /usr
%define sysconfdir /etc

Summary:	A CHM viewer program for KDE.
Summary(zh_CN.UTF-8):	KDE下的一个CHM查看程序
Name:	%{real_name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Applications/File
Group(zh_CN.UTF-8):	应用程序/文件
Url:		http://kchmviewer.soureforge.net/
%if %{git}
Source0:	%{name}-git%{gitdate}.tar.xz
%else
Source0:	http://downloads.sourceforge.net/project/kchmviewer/kchmviewer/%{version}/%{real_name}-%{version}.tar.gz
%endif
Source1:	kchmviewer_zh_CN.po
Source2:	kchmviewer.desktop
Source3:	make_kchmviewer_git_package.sh
Patch1:		kchmviewer-libtool.patch
Packager:	sejishikong <sejishikong@263.net>
BuildRoot:	%{_tmppath}/%{name}--buildroot

%description
KchmViewer is a chm (MS HTML help file format) viewer, written in C++. Unlike most existing CHM viewers for Unix, it uses Trolltech Qt widget library, and does not depend on KDE or Gnome. However, it may be compiled with full KDE support, including KDE widgets and KIO/KHTML. 

%description -l zh_CN.UTF-8
Kchmviewer是一个chm（微软HTML帮助文件格式）查看器，用C++写成。和许多在Unix
下已有的CHM查看器不一样，它使用了Trolltech Qt组件库，不依赖KDE或Gnome，不过，
它可以编译成完全的KDE支持，包括KDE组件和KIO/KHTML。

%prep
rm -rf %{buildroot}
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q -n %{real_name}-%{version}
%endif
%patch1 -p1

%build
. /etc/profile.d/qt.sh
make -f admin/Makefile.common 
LDFLAGS=$LDFLAGS:-L%{_libdir}/qt-3.3/lib
%configure --with-kde --with-qt-dir=%{_libdir}/qt-3.3 --with-qt-libraries=%{_libdir}/qt-3.3/lib
# 临时措施
sed -i 's/\-lqt\-mt/\-L\/usr\/lib\/qt\-3.3\/lib \-lqt\-mt/g' lib/kio-msits/Makefile
make

rm -rf $RPM_BUILD_ROOT
%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/locale/
rm -rf %{buildroot}%{_datadir}/applnk
mkdir -p %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES
msgfmt -o %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/%{name}.mo %{SOURCE1}
mkdir -p %{buildroot}%{_datadir}/applications/
cp %{SOURCE2} %{buildroot}%{_datadir}/applications/
rm -f %{buildroot}%{_libdir}/*.a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/kchmviewer
%{_libdir}/trinity/kio_msits.*
%{_datadir}/applications/kchmviewer.desktop
%{_datadir}/icons/crystalsvg/*/apps/kchmviewer.png
%{_datadir}/locale/zh_CN/LC_MESSAGES/kchmviewer.mo
%{_datadir}/services/msits.protocol

%changelog
