Name:        SDL_console
Version:     2.1
Release:     5%{?dist}
Summary:     Text console for SDL
Summary(zh_CN.UTF-8): SDL的文本控制台
License:   LGPL
Group:       System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
URL:         http://sdlconsole.sourceforge.net
Source:      sdlconsole-%{version}.tar.gz
Buildroot:   %{_tmppath}/%{name}-root
BuildPreReq: SDL-devel SDL_image-devel
Requires:    SDL SDL_image

%description
This is a console that can be added to any SDL application. It is similar to
Quake and other game consoles but with lots of added features. A console is
meant to be a very simple way of interacting with a program and executing
commands. Commands are linked to the console with callback functions so that
when a command is typed in, a specific function is executed automatically.

Authors:
-------
    Clemens Wacha <reflex-2000@gmx.net>
    Garrett Banuk <mongoose@mongeese.org>
    Boris Lesner <talanthyr@tuxfamily.org>

%description -l zh_CN.UTF-8
这是一个可以添加了任何SDL程序的控制台。它像Quake或其它游戏的控制台，但是添加了
许多特性。控制台的意思是一个非常简单的方式来同程序交互和执行命令。命令是连接到
控制台的回叫函数，所以当输入一个命令，一个特定的函数会自动执行。

%package devel
Summary:     Development files for SDL_console
Summary(zh_CN.UTF-8): SDL_console的开发文件
Group:       Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description devel
Development files for SDL_console

Authors:
-------
    Clemens Wacha <reflex-2000@gmx.net>
    Garrett Banuk <mongoose@mongeese.org>
    Boris Lesner <talanthyr@tuxfamily.org>

%description devel -l zh_CN.UTF-8
SDL_console的开发文件。

%prep
%setup -q -n sdlconsole-%{version}

%build
CFLAGS=$RPM_OPT_FLAGS ./configure \
        --prefix=/usr
make %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/sdlconsole-%{version}

%files
%defattr (-, root, root)
%doc COPYING README
/usr/lib/libSDL_console-%{version}.so.*

%files devel
%defattr (-, root, root)
%doc docs example
/usr/lib/libSDL_console.a
/usr/lib/libSDL_console.la
/usr/lib/libSDL_console.so
/usr/include/SDL_console/DT_drawtext.h
/usr/include/SDL_console/SDL_console.h
/usr/include/SDL_console/internal.h

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.1-5
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 2.1-4
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.1-3
- 为 Magic 3.0 重建

* Mon Jan 30 2006 kde <jack@linux.net.cn> 2.1-1mgc
- port to Magic Linux 2.0

* Thu Oct 30 2003 - James Oakley <jfunk@funktronics.ca> - 2.1-1
- Update
- Build for SUSE 9.0

* Sun May 25 2003 - James Oakley <jfunk@funktronics.ca> - 2.0-1
- Update
- Build for SuSE 8.2

* Wed Feb 26 2003 - James Oakley <jfunk@funktronics.ca> - 1.3-1
- Initial Package
