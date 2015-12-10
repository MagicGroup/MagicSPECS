Name:           libpgf
Version: 6.14.12
Release:        2%{?dist}
Summary:        PGF (Progressive Graphics File) library
Summary(zh_CN.UTF-8): PGF (渐进式图形文件) 库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.libpgf.org
#Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.zip
Source0:	http://downloads.sourceforge.net/project/libpgf/libpgf/%{version}-latest/libpgf-src-%{version}.tar.gz

BuildRequires:  doxygen
BuildRequires:  libtool

%description
libPGF contains an implementation of the Progressive Graphics File (PGF)
which is a new image file format, that is based on a discrete, fast
wavelet transform with progressive coding features. PGF can be used
for lossless and lossy compression.

%description -l zh_CN.UTF-8
PGF (渐进式图形文件) 库，PGF 是一种新的图形格式。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}

for i in `find . -name "*"`;do dos2unix $i;done
sed -i 's|$(DESTDIR)$(datadir)/doc/$(DOC_MODULE)|$(RPM_BUILD_DIR)/libpgf|g' doc/Makefile.am


%build
sh autogen.sh

%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING README
<<<<<<< HEAD
%{_libdir}/libpgf.so.*
=======
%{_libdir}/libpgf.so.6*
>>>>>>> 89271a087f1c72d56263855d2bc4eecf69c5daef

%files devel
%doc html
%{_includedir}/%{name}
%{_libdir}/libpgf.so
%{_libdir}/pkgconfig/libpgf.pc
%{_mandir}/man3/*


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 6.14.12-2
- 为 Magic 3.0 重建

* Mon Jul 28 2014 Liu Di <liudidi@gmail.com> - 6.14.12-1
- 更新到 6.14.12

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 6.11.42-2
- 为 Magic 3.0 重建

* Fri Oct 28 2010 Alexey Kurov <nucleo@fedoraproject.org> - 6.11.42-1
- libpgf-6.11.42

* Fri Sep 23 2010 Alexey Kurov <nucleo@fedoraproject.org> - 6.11.24-1
- Initial RPM release
- added svn r46-48 fixes (6.11.32)
- install docs in -devel
