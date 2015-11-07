%define perl_vendorarch %(eval "`perl -V:installvendorarch`"; echo $installvendorarch)
%define perl_archlib %(eval "`perl -V:archlib`"; echo $archlib)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')
%define git 1
%define vcsdate 20151101

Name: openbabel
Version: 2.3.90
%if 0%{?git}
Release: 0.git%{vcsdate}%{?dist}.7
%else
Release: 11%{?dist}
%endif
Summary: Chemistry software file format converter
Summary(zh_CN.UTF-8): 化学软件文件格式转换器
License: GPLv2
Group: Applications/File
Group(zh_CN.UTF-8): 应用程序/文件
URL: http://openbabel.org/
%if 0%{?git}
Source0: %{name}-git%{vcsdate}.tar.xz
%else
Source0: http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz
%endif
Source1: obgui.desktop
Source2: make_openbabel_git_package.sh

# fix perl modules install path
Patch1: %{name}-perl.patch
# fix plugin directory location (#680292, patch by lg)
Patch4: openbabel-plugindir.patch
# fix SWIG_init even when not using swig (#772149)
Patch6: openbabel-noswig-rubymethod.patch
# On F-17, directory for C ruby files changed to use vendorarch directory
Patch7: openbabel-ruby19-vendorarch.patch
# temporarily disable some tests on:
# - ppc64 and s390(x) to unblock other builds (#1108103)
# - ARM (#1094491)
# - aarch64 (#1094513)
# Upstream bugs: https://sourceforge.net/p/openbabel/bugs/927/ https://sourceforge.net/p/openbabel/bugs/945/
Patch8: openbabel-disable-tests-some-arches.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: inchi-devel >= 1.0.3
BuildRequires: libtool
BuildRequires: libxml2-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: python
BuildRequires: python-devel
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: swig
BuildRequires: wx-gtk2-unicode-devel
BuildRequires: zlib-devel

%description
Open Babel is a free, open-source version of the Babel chemistry file
translation program. Open Babel is a project designed to pick up where
Babel left off, as a cross-platform program and library designed to
interconvert between many file formats used in molecular modeling,
computational chemistry, and many related areas.

Open Babel includes two components, a command-line utility and a C++
library. The command-line utility is intended to be used as a replacement
for the original babel program, to translate between various chemical file
formats. The C++ library includes all of the file-translation code as well
as a wide variety of utilities to foster development of other open source
scientific software. 

%description -l zh_CN.UTF-8
Open Babel 是一款 Babel 化学文件翻译程序的免费自由，开源版本。
Open Babel 是个旨在重新整理 Babel 遗留的项目，并作为跨平台的程序和库，
能够双向转换许多种用于分子模型，计算化学和很多相关领域的文件格式。

Open Babel 包括两个组件，一个命令行工具和一个 C++ 库。命令行工具意在
作为原 babel 程序的替代物，用于在多种化学文件格式之间翻译转换。C++ 库
包含所有的文件翻译代码以及纷繁的工具以促进其他开源科学软件的开发。

%package devel
Summary: Development tools for programs which will use the Open Babel library
Summary(zh_CN.UTF-8): 使用 Open Babel 库开发程序所需的工具
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package includes the header files and libraries
necessary for developing programs using the Open Babel library.

If you are going to develop programs which will use this library
you should install %{name}-devel.  You'll also need to have the
%{name} package installed.

%description devel -l zh_CN.UTF-8
%{name}-devel 软件包包含了使用 Open Babel 库开发程序所必需的头文件
和库。

如果您想要使用这个库开发程序，那么您应该安装 %{name}-devel。您也需要
安装 %{name} 软件包。

%package doc
Summary: Additional documentation for the Open Babel library
Summary(zh_CN.UTF-8): %{name} 的附加文档
Group: Documentation
Group(zh_CN.UTF-8): 文档
BuildArch: noarch

%description doc
This package contains additional documentation for Open Babel.

%description doc -l zh_CN.UTF-8
%{name} 的附加文档。

%package gui
Summary: Chemistry software file format converter - GUI version
Summary(zh_CN.UTF-8): %{name} 的图形界面
Group: Applications/File
Group(zh_CN.UTF-8): 应用程序/文件

%description gui
Open Babel is a free, open-source version of the Babel chemistry file
translation program. Open Babel is a project designed to pick up where
Babel left off, as a cross-platform program and library designed to
interconvert between many file formats used in molecular modeling,
computational chemistry, and many related areas.

This package contains the graphical interface.

%description gui -l zh_CN.UTF-8
%{name} 的图形界面。

%package libs
Summary: Chemistry software file format converter - libraries
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
Open Babel is a free, open-source version of the Babel chemistry file
translation program. Open Babel is a project designed to pick up where
Babel left off, as a cross-platform program and library designed to
interconvert between many file formats used in molecular modeling,
computational chemistry, and many related areas.

This package contains the C++ library, which includes all of the
file-translation code.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package -n perl-%{name}
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Summary: Perl wrapper for the Open Babel library
Summary(zh_CN.UTF-8): Open Babel 库的 perl 包装
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Obsoletes: %{name}-perl < 2.2.0
Provides: %{name}-perl = %{version}-%{release}

%description -n perl-%{name}
Perl wrapper for the Open Babel library.

%description -n perl-%{name} -l zh_CN.UTF-8
Open Babel 库的 perl 包装。

%package -n python-%{name}
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Summary: Python wrapper for the Open Babel library
Summary(zh_CN.UTF-8): Open Babel 库的 python 包装
Obsoletes: %{name}-python < 2.2.0
Provides: %{name}-python = %{version}-%{release}

%description -n python-%{name}
Python wrapper for the Open Babel library.

%description -n python-%{name} -l zh_CN.UTF-8
Open Babel 库的 python 包装。

%package -n ruby-%{name}
Summary: Ruby wrapper for the Open Babel library
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: ruby
Requires: %{name} = %{version}-%{release}
Obsoletes: %{name}-ruby < 2.2.0
Provides: %{name}-ruby = %{version}-%{release}

%description -n ruby-%{name}
Ruby wrapper for the Open Babel library.

%description -n ruby-%{name} -l zh_CN.UTF-8
Open Babel 库的 ruby 包装。

%prep
%if 0%{?git}
%setup -q -n %{name}-git%{vcsdate}
%else
%setup -q -n %{name}-%{version}
%endif
%patch1 -p1 -b .perl_path
%patch4 -p1 -b .plugindir
%patch6 -p1 -b .noswig_ruby
%patch7 -p1 -b .ruby_vendor
%ifarch %{power64} s390 s390x armv7hl aarch64
%patch8 -p1 -b .some_arches
%endif
convert src/GUI/babel.xpm -transparent white babel.png

# Remove duplicate html files
pushd doc
for man in *.1; do
 html=`basename $man .1`.html
 if [ -f $html ]; then
   rm $html
 fi
done

%build
%cmake \
 -DCMAKE_SKIP_RPATH:BOOL=ON \
 -DBUILD_GUI:BOOL=ON \
 -DPYTHON_BINDINGS:BOOL=ON \
 -DPERL_BINDINGS:BOOL=ON \
 -DRUBY_BINDINGS:BOOL=ON \
 -DOPENBABEL_USE_SYSTEM_INCHI=true \
 -DENABLE_VERSIONED_FORMATS=false \
 -DRUN_SWIG=true \
 -DENABLE_TESTS:BOOL=ON \
 .
make VERBOSE=1 
#%{?_smp_mflags}

%install
make VERBOSE=1 DESTDIR=%{buildroot} install

rm %{buildroot}%{_libdir}/cmake/openbabel2/*.cmake

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
install -Dpm644 babel.png %{buildroot}%{_datadir}/pixmaps/babel.png
magic_rpm_clean.sh

%check
# rm the built ruby bindings for testsuite to succeed (bug #1191173)
rm %{_lib}/openbabel.so
export CTEST_OUTPUT_ON_FAILURE=1
make test

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/babel
%{_bindir}/ob*
%{_bindir}/roundtrip
%{_mandir}/man1/*.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}-2.0
%{_libdir}/libopenbabel.so
%{_libdir}/pkgconfig/*.pc

%files doc
%defattr(-,root,root,-)
%doc doc/*.html doc/README* doc/dioxin.*

%files gui
%defattr(-,root,root,-)
%{_bindir}/obgui
%{_datadir}/applications/obgui.desktop
%{_datadir}/pixmaps/babel.png

%files libs
%defattr(-,root,root,-)
%{_datadir}/%{name}/
%{_libdir}/%{name}/
%{_libdir}/libopenbabel.so.*

%files -n perl-%{name}
%defattr(-,root,root,-)
%{perl_vendorarch}/Chemistry/OpenBabel.pm
%dir %{perl_vendorarch}/*/Chemistry/OpenBabel
%{perl_vendorarch}/*/Chemistry/OpenBabel/OpenBabel.so

%files -n python-%{name}
%defattr(-,root,root,-)
%{python2_sitearch}/_openbabel.so
%{python2_sitearch}/openbabel.py*
%{python2_sitearch}/pybel.py*
# Egg-info is not generated in 2.3.2, see upstream bug 837
#%{python_sitearch}/openbabel*.egg-info

%files -n ruby-%{name}
%defattr(-,root,root,-)
%{ruby_vendorarchdir}/openbabel.so


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.3.90-0.git20151101.7
- 更新到 20151101 日期的仓库源码

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.3.90-0.git20150922.6
- 为 Magic 3.0 重建

* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 2.3.90-0.git20150922.5
- 更新到 20150922 日期的仓库源码

* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 2.3.90-0.git20150917.4
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 2.3.90-0.git20150917.3
- 更新到 20150917 日期的仓库源码

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 2.3.90-0.git20150325.2
- 为 Magic 3.0 重建

* Wed Mar 25 2015 Liu Di <liudidi@gmail.com> - 2.3.90-0.git20150325.1
- 更新到 20150325 日期的仓库源码

* Wed Mar 25 2015 Liu Di <liudidi@gmail.com> - 2.3.90-0.git20150301.1
- 为 Magic 3.0 重建

* Wed Mar 25 2015 Liu Di <liudidi@gmail.com> - 2.3.1-4
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.3.1-3
- 为 Magic 3.0 重建

* Tue Oct 30 2012 Liu Di <liudidi@gmail.com> - 2.3.1-2
- 为 Magic 3.0 重建

* Tue Sep 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 2.2.0-1mgc
- 更新至 2.2.0 正式版
- 戊子  九月初二

* Fri May 23 2008 Ni Hui <shuizhuyuanluo@126.com> - 2.2.0-0.svn2481.1mgc
- 更新至 svn2481
- #autoreconf --force --install
- ./autogen.sh
- 戊子  四月十九

* Sat Apr 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 2.2.0-0.beta4.1mgc
- 更新至 2.2.0-beta4
- 未编译 ruby 绑定
- 戊子  三月十四

* Sat Dec 22 2007 Ni Hui <shuizhuyuanluo@126.com> - 2.1.1-0.1mgc
- rebuild for MagicLinux-2.1

* Wed Nov 28 2007 Dominik Mierzejewski <rpm@greysector.net> 2.1.1-2
- build against external inchi

* Fri Aug 17 2007 Dominik Mierzejewski <rpm@greysector.net> 2.1.1-1
- updated to 2.1.1
- better work around for testsuite crash
- updated the License tag according to the new guidelines

* Tue Apr 17 2007 Dominik Mierzejewski <rpm@greysector.net> 2.1.0-2
- work around testsuite crash

* Mon Apr 16 2007 Dominik Mierzejewski <rpm@greysector.net> 2.1.0-1
- updated to 2.1.0 final
