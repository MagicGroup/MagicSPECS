%define real_name Xdialog

Name: xdialog
Summary: X11 drop in replacement for cdialog
Summary(zh_CN.UTF-8): cdialog 的 X11 替代程序
Version: 2.3.1
Release: 7%{?dist}
License: GPL+
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://xdialog.free.fr

Source0: http://xdialog.free.fr/%{real_name}-%{version}.tar.bz2
Patch0: xdialog-2.3.1-nostrip.patch
Patch1: xdialog-2.3.1-secure-fprintf.diff
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gtk+-devel >= 1.2.0
BuildRequires: gtk2-devel >= 2.2.0
BuildRequires: gettext

Provides: %{real_name} = %{version}-%{release}
Obsoletes: %{real_name} < %{version}-%{release}

# there is no need for .desktop file since there is a mandatory argument

%description
Xdialog is designed to be a drop in replacement for the cdialog program.
It converts any terminal based program into a program with an X-windows
interface. The dialogs are easier to see and use and Xdialog adds even
more functionalities (help button+box, treeview, editbox, file selector,
range box, and much more).

%description -l zh_CN.UTF-8
cdialog 的 X11 替代程序，它可以转换终端程序为 X 窗口程序。

%prep
%setup -q -n %{real_name}-%{version}
iconv -f latin1 -t utf8 ChangeLog > ChangeLog.utf8
touch -c -r ChangeLog ChangeLog.utf8
mv ChangeLog.utf8 ChangeLog
%patch0 -p1 -b .nostrip
%patch1 -p0
touch -c -r configure.nostrip configure
touch -c -r configure.in.nostrip configure.in

%build
# build both the gtk1 and gtk2 versions. Upstream advises not to use 
# the gtk2 version, however the issues with gtk2 version is with non UTF-8 
# locales which should be rare on fedora, and gtk2 has more features.
%configure
make %{?_smp_mflags}
mv src/Xdialog src/Xdialog-gtk1
make clean
%configure --with-gtk2
make %{?_smp_mflags}
sed -i -e 's:%{_datadir}/doc/Xdialog:%{_datadir}/doc/%{name}:g' doc/Xdialog.1

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL='install -p'
install -m0755 src/Xdialog-gtk1 %{buildroot}%{_bindir}

rm -rf __dist_html
mkdir -p __dist_html/html
cp -p doc/*.html doc/*.png __dist_html/html
# there are references to the samples in the documentation.
ln -s ../samples __dist_html/html/samples
magic_rpm_clean.sh
#%find_lang %{real_name}

%clean
rm -rf %{buildroot}

#%files -f %{real_name}.lang
%files
%defattr(-, root, root, -)
%doc AUTHORS BUGS COPYING ChangeLog README
%doc __dist_html/html/ samples/
%{_mandir}/man1/Xdialog.1*
%{_bindir}/Xdialog
%{_bindir}/Xdialog-gtk1
%exclude %{_docdir}/%{real_name}-%{version}

%changelog
* Thu Oct 22 2015 Liu Di <liudidi@gmail.com> - 2.3.1-7
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.3.1-6
- 为 Magic 3.0 重建

* Fri Feb 24 2012 Liu Di <liudidi@gmail.com> - 2.3.1-5
- 为 Magic 3.0 重建


