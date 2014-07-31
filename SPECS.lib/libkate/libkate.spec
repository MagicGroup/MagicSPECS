%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           libkate
Version: 0.4.1
Release:        1%{?dist}
Summary:        Libraries to handle the Kate bitstream format
Summary(zh_CN.UTF-8): 处理 Kate 位流格式的库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        BSD
URL:            http://code.google.com/p/libkate/
Source0:        http://libkate.googlecode.com/files/libkate-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  libogg-devel
BuildRequires:  liboggz
BuildRequires:  libpng-devel
BuildRequires:  bison
BuildRequires:  flex
%ifnarch s390 s390x %{sparc} %{arm} mips64el
BuildRequires:  valgrind
%endif
BuildRequires:  doxygen
 

%description
This is libkate, the reference implementation of a codec for the Kate bitstream
format.
Kate is a karaoke and text codec meant for encapsulation in an Ogg container.
It can carry text, images, and animate them.

Kate is meant to be used for karaoke alongside audio/video streams (typically
Vorbis and Theora), movie subtitles, song lyrics, and anything that needs text
data at arbitrary time intervals.

%description -l zh_CN.UTF-8
处理 Kate 位流格式的库，Kate 是一种 Ogg 容器格式，包括文本、图像和动画等。
是卡拉 OK 使用的格式。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       libogg-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package utils
Summary:        Encoder/Decoder utilities for %{name}
Summary(zh_CN.UTF-8): %{name} 的编码、解码工具
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:       %{name} = %{version}-%{release}
Requires:       liboggz

%description utils
The %{name}-utils package contains the katedec/kateenc binaries for %{name}.

%description utils -l zh_CN.UTF-8
%{name} 的编码、解码工具。

%package docs
Summary:        Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档

BuildArch:      noarch

%description docs
The %{name}-docs package contains the docs for %{name}.

%description docs -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q

# We regenerate theses files at built step
rm tools/kate_parser.{c,h}
rm tools/kate_lexer.c


%build
%configure --disable-static \
  --docdir=%{_docdir}/%{name}-%{version}

# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Fix for header timestramps
touch -r $RPM_BUILD_ROOT%{_includedir}/kate/kate_config.h \
 $RPM_BUILD_ROOT%{_includedir}/kate/kate.h


%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%exclude %{_docdir}/libkate-%{version}/html
%doc %{_docdir}/libkate-%{version}
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc examples/
%{_includedir}/kate/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files utils
%defattr(-,root,root,-)
%{python_sitelib}/kdj/
%{_bindir}/KateDJ
%{_bindir}/katalyzer
%{_bindir}/katedec
%{_bindir}/kateenc
%{_mandir}/man1/KateDJ.*
%{_mandir}/man1/katalyzer.*
%{_mandir}/man1/katedec.*
%{_mandir}/man1/kateenc.*

%files docs
%defattr(-,root,root,-)
%doc %{_docdir}/libkate-%{version}/html


%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.4.1-1
- 更新到 0.4.1

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.3.8-5
- 为 Magic 3.0 重建

* Mon Jan 09 2012 Liu Di <liudidi@gmail.com> - 0.3.8-4
- 为 Magic 3.0 重建

* Tue Mar 08 2011 Dennis Gilmore <dennis@ausil.us> - 0.3.8-3
- no valgrind on sparc or arm arches

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.3.8-1
- Update to 0.3.8

* Sat Aug 28 2010 Dan Horák <dan[at]danny.cz> - 0.3.7-3
- no valgrind on s390(x)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Nov 25 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.7-1
- Update to 0.3.7

* Fri Oct 16 2009 kwizart < kwizart at gmail.com > - 0.3.6-1
- Update to 0.3.6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009 kwizart < kwizart at gmail.com > - 0.3.4-1
- Update to 0.3.4

* Mon Jun 29 2009 kwizart < kwizart at gmail.com > - 0.3.3-2
- Split -docs - Fix #508589

* Mon May 11 2009 kwizart < kwizart at gmail.com > - 0.3.3-1
- Update to 0.3.3

* Fri Apr 10 2009 kwizart < kwizart at gmail.com > - 0.3.1-3
- Use Fedora compliant (using version) _docdir directory.
- Remove shebangs when not needed.
- Bundle examples within -devel
- Use global instead of define

* Sat Apr  4 2009 kwizart < kwizart at gmail.com > - 0.3.1-2
- Prevent conflict with GNU getline() in recent rawhide

* Tue Mar 17 2009 kwizart < kwizart at gmail.com > - 0.3.1-1
- Update to 0.3.1

* Tue Jan 13 2009 kwizart < kwizart at gmail.com > - 0.3.0-1
- Update to 0.3.0
- Add KateDJ and katalyzer in -utils
- Add BR liboggz and -utils Requires liboggz

* Wed Nov 27 2008 kwizart < kwizart at gmail.com > - 0.2.7-1
- Update to 0.2.7

* Mon Oct 20 2008 kwizart < kwizart at gmail.com > - 0.2.5-1
- Update to 0.2.5

* Mon Sep 29 2008 kwizart < kwizart at gmail.com > - 0.2.1-1
- Update to 0.2.1

* Thu Sep 11 2008 kwizart < kwizart at gmail.com > - 0.1.12-1
- Update to 0.1.12

* Thu Sep  4 2008 kwizart < kwizart at gmail.com > - 0.1.11-1
- Update to 0.1.11

* Wed Sep  3 2008 kwizart < kwizart at gmail.com > - 0.1.10-1
- Update to 0.1.10

* Tue Sep  2 2008 kwizart < kwizart at gmail.com > - 0.1.9-1
- Update to 0.1.9

* Fri Aug 29 2008 kwizart < kwizart at gmail.com > - 0.1.8-1
- Update to 0.1.8

* Mon Aug 11 2008 kwizart < kwizart at gmail.com > - 0.1.7-1
- Initial spec file

