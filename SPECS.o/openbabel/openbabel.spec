%define perl_vendorarch %(eval "`perl -V:installvendorarch`"; echo $installvendorarch)
%define perl_archlib %(eval "`perl -V:archlib`"; echo $archlib)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')

Name: openbabel
Version: 2.3.1
Release: 3%{?dist}
Summary: Chemistry software file format converter
Summary(zh_CN.UTF-8): 化学软件文件格式转换器
License: GPLv2
Group: Applications/File
Group(zh_CN.UTF-8): 应用程序/文件
URL: http://openbabel.org/
Source: http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch1: openbabel-2.3.1-rpm.patch
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
%setup -q -n %{name}-%{version}
%patch1 -p1

%build
#这里应该加个开关
%cmake -DOPENBABEL_USE_SYSTEM_INCHI=ON .
%{__make} %{?_smp_mflags}

%if 0
pushd scripts/perl
perl Makefile.PL INSTALLDIRS="vendor"
%{__make} %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"
popd

pushd scripts/python
python setup.py build
popd

pushd scripts/ruby
ruby extconf.rb --with-openbabel-include=../../include --with-openbabel-lib=../../src/.libs
%{__make} %{?_smp_mflags}
popd
%endif

%install
%{__rm} -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

#%{__rm} %{buildroot}%{_libdir}{,/%{name}/%{version}}/*.la

%if 0
# perl 部分安装
pushd scripts/perl
%{__make} install DESTDIR=%{buildroot}
popd
%{__rm} -f %{buildroot}%{perl_archlib}/perllocal.pod
%{__rm} -f %{buildroot}%{perl_vendorarch}/*/Chemistry/OpenBabel/{.packlist,OpenBabel.bs}
chmod 755 %{buildroot}%{perl_vendorarch}/*/Chemistry/OpenBabel/OpenBabel.so

# python 部分安装
pushd scripts/python
%{__python} setup.py install --skip-build --root %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd
chmod 755 $RPM_BUILD_ROOT%{python_sitearch}/_openbabel.so

# ruby 部分安装
pushd scripts/ruby
%{__make} install DESTDIR=%{buildroot}
popd
%endif

magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%check
%{__make} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README THANKS
%doc doc/*.html
%doc doc/README* doc/dioxin.*
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{name}
%{_libdir}/libopenbabel.so.*
%{_libdir}/%{name}

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}-2.0
%{_libdir}/libopenbabel.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/*

%if 0
%files -n perl-%{name}
%defattr(-,root,root,-)
%{perl_vendorarch}/Chemistry/OpenBabel.pm
%dir %{perl_vendorarch}/*/Chemistry/OpenBabel
%{perl_vendorarch}/*/Chemistry/OpenBabel/OpenBabel.so

%files -n python-%{name}
%defattr(-,root,root,-)
%{python_sitearch}/_openbabel.so
%{python_sitearch}/openbabel.py*
%{python_sitearch}/pybel.py*
%{python_sitearch}/openbabel*.egg-info

%files -n ruby-%{name}
%defattr(-,root,root,-)
%{ruby_sitearch}/openbabel.so
%endif

%changelog
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
