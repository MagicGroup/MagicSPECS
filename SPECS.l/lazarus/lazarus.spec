Name:           lazarus
Version:	1.2.2
Release:        0
Summary:        Lazarus Component Library and IDE
Summary(zh_CN.UTF-8): Lazarus 组件库和 IDE

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        GPL and modified LGPL
URL:            http://www.lazarus.freepascal.org/
Source0:        http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}-%{release}.tar.gz
patch0:         Makefile_patch.diff
patch1:         Desktop_patch.diff

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  fpc, gtk2-devel, glibc-devel
Requires:       fpc-src, fpc, gtk2-devel, glibc-devel, binutils, gdb

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%define _source_filedigest_algorithm 0
%define _binary_filedigest_algorithm 0

%description
Lazarus is a free and open source Rapid Application Development tool for
the FreePascal compiler using the Lazarus component library - LCL. The LCL
is included in this package.

%description -l zh_CN.UTF-8
这是一个自由开源的快速开发工具，使用 FreePascal 编译器并使用 Lazarus 组件库(LCL)。
LCL 包含在此包中。

%prep
%setup -c
%patch0 -p0
%patch1 -p0

%build
cd lazarus
# Remove the files for building other packages
rm -rf debian
cd tools
find install -depth -type d ! \( -path "install/linux/*" -o -path "install/linux" -o -path "install" \) -exec rm -rf '{}' \;
cd ..
# Remove patch-backup files
rm Makefile.fpc.orig
rm install/lazarus.desktop.orig

export FPCDIR=%{_datadir}/fpcsrc/
fpcmake -Tall
make bigide OPT='-gl -gw'
make tools OPT='-gl -gw'
# make lazbuilder OPT='-gl -gw'

%install
[ %{buildroot} != "/" ] && ( rm -rf %{buildroot} )

make -C lazarus install INSTALL_PREFIX=%{buildroot}%{_prefix} _LIB=%{_lib}

install -D -p -m 0644 lazarus/install/lazarus-mime.xml $LazBuildDir%{buildroot}%{_datadir}/mime/packages/lazarus.xml
install -D -p -m 0644 lazarus/images/ide_icon48x48.png %{buildroot}%{_datadir}/pixmaps/lazarus.png
desktop-file-install \
        --dir %{buildroot}%{_datadir}/applications \
        lazarus/install/%{name}.desktop

ln -sf ../%{_lib}/%{name}/lazarus %{buildroot}%{_bindir}/lazarus-ide
ln -sf ../%{_lib}/%{name}/startlazarus %{buildroot}%{_bindir}/startlazarus
ln -sf ../%{_lib}/%{name}/lazbuild %{buildroot}%{_bindir}/lazbuild

install -d %{buildroot}%{_sysconfdir}/lazarus
sed 's#__LAZARUSDIR__#%{_libdir}/%{name}#;s#__FPCSRCDIR__#%{_datadir}/fpcsrc#' \
        lazarus/tools/install/linux/environmentoptions.xml \
        > %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml

chmod 755 %{buildroot}%{_libdir}/%{name}/components/lazreport/tools/localize.sh


%clean
[ %{buildroot} != "/" ] && ( rm -rf %{buildroot} )

%post
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
update-mime-database %{_datadir}/mime &> /dev/null || :

%files
%defattr(-,root,root,-)
%{_libdir}/%{name}
%{_bindir}/%{name}-ide
%{_bindir}/startlazarus
%{_bindir}/lazbuild
%{_datadir}/pixmaps/lazarus.png
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/mime/packages/lazarus.xml
%doc lazarus/COPYING*
%doc lazarus/README.txt
%dir %{_sysconfdir}/lazarus
%config(noreplace) %{_sysconfdir}/lazarus/environmentoptions.xml
%{_mandir}/*/*

%changelog
* Sat Jun 07 2014 Liu Di <liudidi@gmail.com> - 1.2.2-0
- 更新到 1.2.2

* Mon Jun 21 2012 Mattias Gaertner <mattias@freepascal.org> 1.0-0
- 128x128 icon, chmhelp
* Sat Sep 9 2006 Mattias Gaertner <mattias@freepascal.org> 0.9.18-0
- Initial build.
* Wed Jul 20 2005 Joost van der Sluis <joost@cnoc.nl> 0.9.8-0.1
- Initial build.

