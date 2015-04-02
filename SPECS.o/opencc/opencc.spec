Name:       opencc
Version:	1.0.2
Release:	1%{?dist}
Summary:    Libraries for Simplified-Traditional Chinese Conversion
Summary(zh_CN.UTF-8): 简繁体中文转换的库
License:    ASL 2.0
Group:      System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:        https://github.com/BYVoid/OpenCC
Source0:    https://github.com/BYVoid/OpenCC/archive/ver.%{version}.tar.gz
Patch1:	    opencc-fixes-cmake.patch

BuildRequires:  gettext
BuildRequires:  cmake

%description
OpenCC is a library for converting characters and phrases between
Traditional Chinese and Simplified Chinese.

%description -l zh_CN.UTF-8
中文简繁转换开源项目，支持词汇级别的转换、异体字转换和地区习惯用词转换（中国大陆、台湾、香港）。

特点：

严格区分「一简对多繁」和「一简对多异」。
完全兼容异体字，可以实现动态替换。
严格审校一简对多繁词条，原则为「能分则不合」。
支持中国大陆、台湾、香港异体字和地区习惯用词转换，如「里」「里」、「鼠标」「鼠标」。
词库和函数库完全分离，可以自由修改、导入、扩展。
支持C、C++、Python、PHP、Java、Ruby、Node.js。
兼容Windows、Linux、Mac平台。

%package doc
Summary:    Documentation for OpenCC
Summary(zh_CN.UTF-8): %{name} 的文档
Group:      Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
Requires:   %{name} = %{version}-%{release}

%description doc
Doxygen generated documentation for OpenCC.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%package tools
Summary:    Command line tools for OpenCC
Summary(zh_CN.UTF-8): OpenCC 的命令行工具
Group:      Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
Requires:   %{name} = %{version}-%{release}

%description tools
Command line tools for OpenCC, including tools for conversion via CLI and
for building dictionaries.

%description tools -l zh_CN.UTF-8
OpenCC 的命令行工具，包括 CLI 下的转换工具和词典构建。

%package devel
Summary:    Development files for OpenCC
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:      Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:   %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n OpenCC-ver.%{version}
%patch1 -p1 -b .cmake

%build
%cmake . -DENABLE_GETTEXT:BOOL=ON -DBUILD_DOCUMENTATION:BOOL=ON
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
magic_rpm_clean.sh

%check
ctest

#%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS LICENSE README.md
%{_libdir}/lib*.so.*
%{_datadir}/opencc/
%exclude %{_datadir}/opencc/doc

%files doc
%{_datadir}/opencc/doc

%files tools
%{_bindir}/*
#%{_datadir}/man/man1/*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Mar 27 2015 Liu Di <liudidi@gmail.com> - 1.0.2-1
- 更新到 1.0.2

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.2.0-4
- 为 Magic 3.0 重建

* Thu Jan 19 2012 Liu Di <liudidi@gmail.com> - 0.2.0-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 25 2010 BYVoid <byvoid.kcp@gmail.com> - 0.2.0-1
- Upstream release.
- Use CMake instead of autotools.

* Wed Sep 29 2010 jkeating - 0.1.2-2
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 BYVoid <byvoid.kcp@gmail.com> - 0.1.2-1
- Upstream release.

* Thu Aug 12 2010 BYVoid <byvoid.kcp@gmail.com> - 0.1.1-1
- Upstream release.

* Thu Jul 29 2010 BYVoid <byvoid.kcp@gmail.com> - 0.1.0-1
- Upstream release.

* Fri Jul 16 2010 BYVoid <byvoid.kcp@gmail.com> - 0.0.4-1
- Initial release of RPM.

