%define with_kde3 0
Name:		gambas
Summary: 	IDE based on a basic interpreter with object extensions
Summary(zh_CN.UTF-8): 基于对象的 Basic 语言扩展的 IDE
Version: 	1.0.19
Release: 	12%{?dist}
License: 	GPL+
Group: 		Development/Tools
Group(zh_CN.UTF-8):	开发/工具
URL: 		http://gambas.sourceforge.net/
Source0: 	http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if 0%{?with_kde3}
BuildRequires:	kdelibs-devel
%endif
BuildRequires:  automake, autoconf, SDL-devel, SDL_mixer-devel
BuildRequires:	mysql-devel, postgresql-devel, sqlite-devel, libX11-devel
BuildRequires:	desktop-file-utils, gettext-devel, curl-devel, libXext-devel
BuildRequires:	qt-devel, bzip2-devel, libxslt-devel, libxml2-devel
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
# Code is not 64 bit clean.
# http://sourceforge.net/mailarchive/message.php?msg_id=15024630
ExcludeArch:	x86_64 ppc64
# Code is now endian clean.
# ExcludeArch:	ppc
Patch0:		gambas-1.0.9-gcc4.patch
Patch1:		gambas-1.0.6-dont-make-links.patch
Patch2:		gambas-1.0.6-noopt.patch
Patch3:		gambas-1.0.11-desktopfix.patch
Patch4:		gambas-1.0.13-gettextfix.patch
Patch5:		gambas-1.0.16-64bit.patch
%define tde 1
%if %{tde}
Patch6:		gambas-1.0.19-tde.patch
%endif

%description
Gambas is a free development environment based on a Basic interpreter
with object extensions, like Visual Basic (but it is NOT a clone !).
With Gambas, you can quickly design your program GUI, access MySQL or
PostgreSQL databases, pilot KDE applications with DCOP, translate your
program into many languages, create network applications easily, and so
on...

%description -l zh_CN.UTF-8
Gambas 是一个面向对象的 BASIC 语言分支和一个附带的IDE，能在Linux 以及
其他 Unix-like 计算机操作系统中运行。它提供一个与Visual Basic相似的用
户体验。Gambas 被设计成为一个针对迁移到 Linux 平台上Visual Basic 开发
者的 Visual Basic替代产品。

'Gambas' 是 Gambas Almost Means Basic 的递归缩写。Gambas 在西班牙语中
是表示虾，这也是 Gambas 标志的由来。

Gambas 在1999年由 Beno?t Minisini 在巴黎开始开发，Gambas 是自由软件，在
GNU 通用公共许可证下发布。

%package runtime
Summary:        Runtime environment for gambas
Summary(zh_CN.UTF-8): gambas 的运行环境
Group:          Development/Tools
Group(zh_CN.UTF-8):	开发/工具
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name}

%description runtime
Gambas is a free development environment based on a Basic interpreter
with object extensions, like Visual Basic. This package contains the 
runtime components necessary to run programs designed in gambas. 

%description runtime -l zh_CN.UTF-8
这个包包含了运行使用 gambas 设计的程序所必须的运行环境组件。

%package ide
Summary:	Development environment for gambas
Summary(zh_CN.UTF-8):	gambas 的开发环境
Group:		Development/Tools
Group(zh_CN.UTF-8):	开发/工具
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-compress = %{version}-%{release}
Requires:	%{name}-gb-db = %{version}-%{release}
Requires:	%{name}-gb-debug = %{version}-%{release}
Requires:	%{name}-gb-eval = %{version}-%{release}
Requires:	%{name}-gb-net-curl = %{version}-%{release}
Requires:       %{name}-gb-net = %{version}-%{release}
Requires:       %{name}-gb-qt = %{version}-%{release}
Requires:       %{name}-gb-qt-editor = %{version}-%{release}
Requires:       %{name}-gb-qt-ext = %{version}-%{release}
%if 0%{?with_kde3}
Requires:       %{name}-gb-qt-kde = %{version}-%{release}
Requires:       %{name}-gb-qt-kde-html = %{version}-%{release}
%endif
Requires:       %{name}-gb-sdl = %{version}-%{release}
Requires:       %{name}-gb-vb = %{version}-%{release}
Requires:       %{name}-gb-xml-libxml = %{version}-%{release}
Requires:       %{name}-gb-xml-libxml-rpc = %{version}-%{release}
Requires:       %{name}-gb-xml-libxml-xslt = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel, %{name}-help, %{name}-examples
Provides:	%{name}-help = %{version}-%{release}
Provides:	%{name}-examples = %{version}-%{release}

%description ide
The gambas-ide package contains the complete Gambas Development 
Environment, with the database manager, the help files, and all 
components. This is what you want to install if you want to 
create new programs with Gambas.

%description ide -l zh_CN.UTF-8
Gambas 的集成开发环境。

%package gb-compress
Summary:        Gambas component package for compress
Summary(zh_CN.UTF-8):	Gambas 的压缩组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-compress
%{summary}

%description gb-compress -l zh_CN.UTF-8
Gambas 的压缩组件。

%package gb-db
Summary:        Gambas component package for db
Summary(zh_CN.UTF-8): Gambas 的数据库组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-db
%{summary}

%description gb-db -l zh_CN.UTF-8
Gambas 的数据库组件。

%package gb-debug
Summary:        Gambas component package for debug
Summary(zh_CN.UTF-8): Gambas 的调试组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-debug
%{summary}

%description gb-debug -l zh_CN.UTF-8
Gambas 的调试组件。

%package gb-eval
Summary:        Gambas component package for eval
Summary(zh_CN.UTF-8): Gambas 的计算组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-eval
%{summary}

%description gb-eval -l zh_CN.UTF-8
Gambas 的计算组件。

%package gb-net
Summary:        Gambas component package for net
Summary(zh_CN.UTF-8): Gambas 的网络组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-net
%{summary}

%description gb-net -l zh_CN.UTF-8
Gambas 的网络组件。

%package gb-net-curl
Summary:        Gambas component package for net.curl
Summary(zh_CN.UTF-8): Gambas 的网络 curl 组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-net-curl
%{summary}

%description gb-net-curl -l zh_CN.UTF-8
Gambas 的网络 curl 组件。

%package gb-qt
Summary:        Gambas component package for qt
Summary(zh_CN.UTF-8): Gambas 的 qt 组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-qt
%{summary}

%description gb-qt -l zh_CN.UTF-8
Gambas 的 qt 组件。

%package gb-qt-editor
Summary:        Gambas component package for qt.editor
Summary(zh_CN.UTF-8): Gambas 的 qt 编辑器组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-qt-editor
%{summary}

%description gb-qt-editor -l zh_CN.UTF-8
Gambas 的 qt 编辑器组件。

%package gb-qt-ext
Summary:        Gambas component package for qt.ext
Summary(zh_CN.UTF-8):	Gambas 的 qt 扩展组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-qt-ext
%{summary}

%description gb-qt-ext -l zh_CN.UTF-8
Gambas 的 qt 扩展组件。

%if 0%{?with_kde3}
%package gb-qt-kde
Summary:        Gambas component package for qt.kde
Summary(zh_CN.UTF-8): Gambas 的 KDE 组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-qt-kde
%{summary}

%description gb-qt-kde -l zh_CN.UTF-8
Gambas 的 KDE 组件。

%package gb-qt-kde-html
Summary:        Gambas component package for qt.kde.html
Summary(zh_CN.UTF-8): Gambas 的 KDE html 组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-qt-kde-html
%{summary}

%description gb-qt-kde-html -l zh_CN.UTF-8
Gambas 的 KDE html 组件。
%endif

%package gb-sdl
Summary:        Gambas component package for sdl
Summary(zh_CN.UTF-8):	Gambas 的 SDL 组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-sdl
%{summary}

%description gb-sdl -l zh_CN.UTF-8
Gambas 的 SDL 组件。

%package gb-vb
Summary:        Gambas component package for vb
Summary(zh_CN.UTF-8):	Gambas 的 vb 组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-vb
%{summary}

%description gb-vb -l zh_CN.UTF-8
Gambas 的 vb 组件。

%package gb-xml-libxml
Summary:        Gambas component package for xml.libxml
Summary(zh_CN.UTF-8):	Gambas 的 XML 组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-xml-libxml
%{summary}

%description gb-xml-libxml -l zh_CN.UTF-8
Gambas 的 XML 组件。

%package gb-xml-libxml-rpc
Summary:        Gambas component package for xml.libxml.rpc
Summary(zh_CN.UTF-8): Gambase 的 XML RPC 组件
Group:          Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:       %{name}-runtime = %{version}-%{release}

%description gb-xml-libxml-rpc
%{summary}

%description gb-xml-libxml-rpc -l zh_CN.UTF-8
Gambase 的 XML RPC 组件。

%package gb-xml-libxml-xslt
Summary:	Gambas component package for xml.libxml.xslt
Summary(zh_CN.UTF-8): Gambas 的 XML XSLT 组件
Group:		Development/Tools
Group(zh_CN.UTF-8):   开发/工具
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-xml-libxml-xslt
%{summary}

%description gb-xml-libxml-xslt -l zh_CN.UTF-8
Gambas 的 XML XSLT 组件。

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%if %{tde}
%patch6 -p1
%endif

%build
# Gambas can't deal with -Wp,-D_FORTIFY_SOURCE=2
CFLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g'`

rm -f  $(find . -type f | egrep "Makefile$") $(find . -type f | egrep "Makefile.in$")
./reconf || echo reconf gives a warning but lets continue anyway
%configure \
	--datadir="%{_datadir}" \
	--enable-intl \
	--enable-conv \
	--enable-qt \
%if 0%{?with_kde3}
	--enable-kde \
%endif
	--enable-net \
	--enable-curl \
	--enable-postgresql \
	--enable-mysql \
	--enable-sqlite \
	--enable-sdl \
	--enable-vb \
	CPPFLAGS="$CPPFLAGS -I/usr/include/tqt"
%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export PATH=$RPM_BUILD_ROOT/usr/bin:$PATH
mkdir -p %{buildroot}%{_includedir}
make DESTDIR=$RPM_BUILD_ROOT install
# Yes, I know. Normally we'd nuke the .la files, but Gambas is retar^Wspecial.
# rm -rf $RPM_BUILD_ROOT%{_libdir}/gambas/*.la
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
install -m0644 ./app/gambas/.icon/32.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/gambas.png
install src/share/gambas.h $RPM_BUILD_ROOT/%{_includedir}

desktop-file-install --vendor fedora			\
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications	\
  debian/gambas.desktop

# Pull buildroot out of the examples files
for i in `grep -lr "$RPM_BUILD_ROOT" $RPM_BUILD_ROOT%{_datadir}/%{name}/examples/`; 
do
  sed -i "s|$RPM_BUILD_ROOT||g" $i; 
done

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig
update-desktop-database %{_datadir}/applications &> /dev/null

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
  update-desktop-database %{_datadir}/applications &> /dev/null
fi

%files runtime
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING INSTALL README README.REDHAT TODO
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.component
%{_bindir}/gambas
%{_bindir}/gbi
%{_bindir}/gbx
%{_datadir}/pixmaps/gambas.png
%{_datadir}/applications/*.desktop
%dir %{_datadir}/gambas/
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.info
%{_datadir}/gambas/info/gb.list

%files ide
%defattr(-, root, root, 0755)
%{_bindir}/gbc
%{_bindir}/gba
%{_bindir}/gambas-database-manager
%{_includedir}/gambas.h
%{_datadir}/gambas/
%exclude %{_datadir}/gambas/info/

# For what its worth, I think this packaging layout is horrific.
# But, I'm going to play nice with upstream and let the user suffer.
# ~spot

%files gb-compress
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.compress.*
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.compress.*

%files gb-db
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.db.*
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.db.*

%files gb-debug
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.debug.*
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.debug.*

%files gb-eval
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.eval.*
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.eval.*

%files gb-net
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.net.component
%{_libdir}/gambas/lib.gb.net.so*
%{_libdir}/gambas/lib.gb.net.la
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.net.info
%{_datadir}/gambas/info/gb.net.list

%files gb-net-curl
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.net.curl.*
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.net.curl.*

%files gb-qt 
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas 
%{_libdir}/gambas/lib.gb.qt.component 
%{_libdir}/gambas/lib.gb.qt.so* 
%{_libdir}/gambas/lib.gb.qt.la 
%dir %{_datadir}/gambas/info 
%{_datadir}/gambas/info/gb.qt.info 
%{_datadir}/gambas/info/gb.qt.list

%files gb-qt-editor 
%defattr(-, root, root, 0755) 
%dir %{_libdir}/gambas 
%{_libdir}/gambas/lib.gb.qt.editor.*
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.qt.editor.*

%files gb-qt-ext
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.qt.ext.*
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.qt.ext.*

%if 0%{?with_kde3}
%files gb-qt-kde
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.qt.kde.component
%{_libdir}/gambas/lib.gb.qt.kde.so*
%{_libdir}/gambas/lib.gb.qt.kde.la
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.qt.kde.info
%{_datadir}/gambas/info/gb.qt.kde.list

%files gb-qt-kde-html
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.qt.kde.html.*
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.qt.kde.html.*
%endif

%files gb-sdl
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.sdl.*
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.sdl.*

%files gb-vb
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.vb.*
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.vb.*

%files gb-xml-libxml
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.xml.libxml.component
%{_libdir}/gambas/lib.gb.xml.libxml.so*
%{_libdir}/gambas/lib.gb.xml.libxml.la
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.xml.libxml.info
%{_datadir}/gambas/info/gb.xml.libxml.list

%files gb-xml-libxml-rpc
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.xml.libxml.rpc.*
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.xml.libxml.rpc.*

%files gb-xml-libxml-xslt
%defattr(-, root, root, 0755)
%dir %{_libdir}/gambas
%{_libdir}/gambas/lib.gb.xml.libxml.xslt.*
%dir %{_datadir}/gambas/info
%{_datadir}/gambas/info/gb.xml.libxml.xslt.*

%changelog
* Fri Nov 25 2011 Liu Di <liudidi@gmail.com> - 1.0.19-11
- 为 Magic 3.0 重建


