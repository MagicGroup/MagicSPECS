Name:           compat-lua
Version:        5.1.4
Release:        8%{?dist}
Summary:        Powerful light-weight programming language (compat version)
Summary(zh_CN.UTF-8): 强力的轻量级程序语言（兼容版本）
Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        MIT
URL:            http://www.lua.org/
Source0:        http://www.lua.org/ftp/lua-%{version}.tar.gz
Patch0:         lua-5.1.4-autotoolize.patch
Patch1:         lua-5.1.4-lunatic.patch
Patch2:         lua-5.1.4-idsize.patch
Patch3:         lua-5.1.4-2.patch
Patch4:         lua-5.1.4-pc-compat.patch
BuildRequires:  readline-devel ncurses-devel libtool
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       lua = 5.1

%description
This package contains a compatibility version of the lua-5.1 binaries.

%description -l zh_CN.UTF-8
这个包包含了 lua-5.1 版本的二进制文件。

%package libs
Summary:        Powerful light-weight programming language (compat version)
Summary(zh_CN.UTF-8): %{name} 的运行库
Provides:       lua(abi) = 5.1

%description libs
This package contains a compatibility version of the lua-5.1 libraries.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for compat-lua-libs.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n lua-%{version}
%patch0 -p1 -E -z .autoxxx
%patch1 -p0 -z .lunatic
%patch2 -p1 -z .idsize
%patch3 -p0 -d src -z .bugfix2
%patch4 -p1
# fix perms on auto files
chmod u+x autogen.sh config.guess config.sub configure depcomp install-sh missing
# Avoid make doing auto-reconf itself, killing our rpath removel in the process
autoreconf -i -f


%build
%configure --with-readline
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# hack so that only /usr/bin/lua gets linked with readline as it is the
# only one which needs this and otherwise we get License troubles
make %{?_smp_mflags} LIBS="-lm -ldl" luac_LDADD="liblua.la -lm -ldl"
# also remove readline from lua.pc
sed -i 's/-lreadline -lncurses //g' etc/lua.pc


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/liblua.{a,la}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/lua/5.1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lua/5.1
# Rename some files to avoid conflicts with 5.2
mv $RPM_BUILD_ROOT%{_bindir}/lua $RPM_BUILD_ROOT%{_bindir}/lua-5.1
mv $RPM_BUILD_ROOT%{_bindir}/luac $RPM_BUILD_ROOT%{_bindir}/luac-5.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/lua.1 \
  $RPM_BUILD_ROOT%{_mandir}/man1/lua-5.1.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/luac.1 \
  $RPM_BUILD_ROOT%{_mandir}/man1/luac-5.1.1
mkdir -p $RPM_BUILD_ROOT%{_includedir}/lua-5.1
mv $RPM_BUILD_ROOT%{_includedir}/l*h* $RPM_BUILD_ROOT%{_includedir}/lua-5.1
rm $RPM_BUILD_ROOT%{_libdir}/liblua.so
mv $RPM_BUILD_ROOT%{_libdir}/pkgconfig/lua.pc \
  $RPM_BUILD_ROOT%{_libdir}/pkgconfig/lua-5.1.pc
magic_rpm_clean.sh

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%{_bindir}/lua-5.1
%{_bindir}/luac-5.1
%{_mandir}/man1/lua*5.1.1*

%files libs
%doc COPYRIGHT HISTORY README doc/*.html doc/*.css doc/*.gif doc/*.png
%{_libdir}/liblua-5.1.so
%dir %{_libdir}/lua
%dir %{_libdir}/lua/5.1
%dir %{_datadir}/lua
%dir %{_datadir}/lua/5.1

%files devel
%{_includedir}/lua-5.1/
%{_libdir}/pkgconfig/lua-5.1.pc


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 5.1.4-8
- 为 Magic 3.0 重建

* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 5.1.4-7
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Liu Di <liudidi@gmail.com> - 5.1.4-6
- 为 Magic 3.0 重建

* Sat Aug  3 2013 Hans de Goede <hdegoede@redhat.com> - 5.1.4-5
- New Fedora package with full lua-5.1 for use with applications not yet
  ported to 5.2
- Release fields start at 5 to be newer the compat-lua-libs from the
  non-compat lua package
