Summary: An extended version of DVIPDFMx with support for XeTeX output
Summary(zh_CN.UTF-8): 支持 XeTeX 输出的 DVIPDFMx 的扩展版本
Name: xdvipdfmx
Version: 0.4
Release: 6%{?dist}
License: GPLv2+
Group: Applications/Publishing
Group(zh_CN.UTF-8): 应用程序/出版
Source: http://scripts.sil.org/svn-view/xdvipdfmx/TAGS/xdvipdfmx-%{version}.tar.gz
URL: http://scripts.sil.org/xetex_linux

Requires: tex(tex), dvipdfmx
# dvipdfmx is required because some data files are shared
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# to build, we need various -devel packages...
BuildRequires: fontconfig-devel, freetype-devel, libpng-devel, zlib-devel, kpathsea-devel, libpaper-devel

%description
xdvipdfmx is an output driver for the XeTeX typesetting system.
It is an extended version of DVIPDFMx by Jin-Hwan Cho and Shunsaku Hirata,
which is itself an extended version of dvipdfm by Mark A. Wicks.
This driver converts XDV (extended DVI) output from the xetex program
into standard PDF that can be viewed or printed.

%description -l zh_CN.UTF-8
支持 XeTeX 输出的 DVIPDFMx 的扩展版本。

# # # # # # # # # #
# PREP
# # # # # # # # # #

%prep

# setup macro does standard clean-and-unpack
%setup -q

# # # # # # # # # #
# BUILD
# # # # # # # # # #

%build
chmod +x configure
%{configure} --with-freetype2=`freetype-config --prefix` 
make %{?_smp_mflags}

# # # # # # # # # #
# INSTALL
# # # # # # # # # #

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh
# # # # # # # # # #
# FILE LIST
# # # # # # # # # #

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/xdvipdfmx
%doc README AUTHORS BUGS COPYING TODO doc/tug2003.pdf index.html *.css

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.4-6
- 为 Magic 3.0 重建

* Fri Feb 24 2012 Liu Di <liudidi@gmail.com> - 0.4-5
- 为 Magic 3.0 重建


