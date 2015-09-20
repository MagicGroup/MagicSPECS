# $Id: lame.spec 4387 2006-05-20 08:44:31Z dag $
# Authority: matthias
# Upstream: <mp3encoder$minnie,tuhs,org>
%define realver 3.99.3
Summary: LAME Ain't an MP3 Encoder... but it's the best of all
Summary(zh_CN.UTF-8): LAME 不是一个 MP3编码器...它是所有中最好的
Name: lame
Version: 3.99.3
Release: 3%{?dist}
License: LGPL
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL: http://lame.sourceforge.net/
Source: http://dl.sf.net/lame/lame-%{realver}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: ncurses-devel, gcc-c++
BuildRequires: prelink
%ifarch %{ix86} x86_64
BuildRequires: nasm
%endif
Provides: mp3encoder

%description
LAME is an educational tool to be used for learning about MP3 encoding.
The goal of the LAME project is to use the open source model to improve
the psycho acoustics, noise shaping and speed of MP3. Another goal of
the LAME project is to use these improvements for the basis of a patent
free audio compression codec for the GNU project.

%description -l zh_CN.UTF-8
LAME是一个教育性的工具来学习关于MP3编码。LAME项目的目标是使用开源模式来
增强MP3的心理声音，修整噪声及速度。另外一个目标是为GNU项目提供自由使用
专利的这些增强。


%package devel
Summary: Shared and static libraries for LAME
Summary(zh_CN.UTF-8): LAME的静态和共享库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}

%description devel
LAME is an educational tool to be used for learning about MP3 encoding.
This package contains both the shared and the static libraries from the
LAME project.

You will also need to install the main lame package in order to install
these libraries.

%description devel -l zh_CN.UTF-8
LAME是一个教育性的工具，用来学习MP3的编码。
这个包同时包含了LAME项目的共享库和静态库。

要安装这个包，你还需要安装lame包。


%prep
%setup -q -n %{name}-%{realver}


%build
%configure \
    --program-prefix=%{?_program_prefix} \
    --disable-static \
%ifarch %{ix86} x86_64
    --enable-nasm \
%endif
    --enable-decoder \
    --with-vorbis \
    --enable-analyser="no" \
    --enable-brhist
%{__make} test CFLAGS="%{optflags}"


%install
%{__rm} -rf %{buildroot}
%makeinstall

### Some apps still expect to find <lame.h>
%{__ln_s} -f lame/lame.h %{buildroot}%{_includedir}/lame.h

### Clean up documentation to be included
find doc/html -name "Makefile*" | xargs rm -f
%{__rm} -rf %{buildroot}%{_docdir}/lame/

### Clear not needed executable stack flag bit
execstack -c %{buildroot}%{_libdir}/*.so.*.*.* || :


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING doc/html/ README TODO USAGE
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-, root, root, 0755)
%doc API HACKING STYLEGUIDE
%{_includedir}/*
%exclude %{_libdir}/*.la
%{_libdir}/*.so


%changelog
* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 3.99.3-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.99.3-2
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Liu Di <liudidi@gmail.com> - 3.98.4-3
- 为 Magic 3.0 重建

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 3.97-1mgc
- update to 3.97


