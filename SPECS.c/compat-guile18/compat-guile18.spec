%bcond_without emacs
%global mver 1.8

Summary: A GNU implementation of Scheme for application extensibility
Summary(zh_CN.UTF-8): Guile 的 1.8 版本
Name: compat-guile18
Version: %{mver}.8
Release: 10%{?dist}
Source: ftp://ftp.gnu.org/pub/gnu/guile/guile-%{version}.tar.gz
URL: http://www.gnu.org/software/guile/
Patch1: guile-1.8.7-multilib.patch
Patch2: guile-1.8.7-testsuite.patch
Patch3: guile-1.8.8-deplibs.patch
License: LGPLv2+
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
BuildRequires: libtool libtool-ltdl-devel gmp-devel readline-devel
BuildRequires: gettext-devel
%{?with_emacs:BuildRequires: emacs}
Provides: guile = 5:%{version}-7
Provides: guile%{?_isa} = 5:%{version}-7
Obsoletes: guile < 5:%{version}-7
Obsoletes: guile%{?_isa} < 5:%{version}-7

%description
GUILE (GNU's Ubiquitous Intelligent Language for Extension) is a library
implementation of the Scheme programming language, written in C.  GUILE
provides a machine-independent execution platform that can be linked in
as a library during the building of extensible programs.

Install the compat-guile18 package if you'd like to add extensibility to
programs that you are developing.

%description -l zh_CN.UTF-8
Guile 的 1.8 版本，仅为兼容目的使用。

%package devel
Summary: Libraries and header files for the GUILE extensibility library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release} gmp-devel
Requires: pkgconfig
Provides: guile-devel = 5:%{version}-7
Provides: guile-devel%{?_isa} = 5:%{version}-7
Obsoletes: guile-devel < 5:%{version}-7
Obsoletes: guile-devel%{?_isa} < 5:%{version}-7

%description devel
The compat-guile18-devel package includes the libraries, header files, etc.,
that you'll need to develop applications that are linked with the
GUILE extensibility library.

You need to install the compat-guile18-devel package if you want to develop
applications that will be linked to GUILE.  You'll also need to install the
compat-guile18 package.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n guile-%{version}

%patch1 -p1 -b .multilib
%patch2 -p1 -b .testsuite
%patch3 -p1 -b .deplibs

%build

export LDFLAGS="-Wl,--as-needed"
%configure --disable-static --disable-error-on-warning

# Remove RPATH
sed -i 's|" $sys_lib_dlsearch_path "|" $sys_lib_dlsearch_path %{_libdir} "|' \
    {,guile-readline/}libtool

make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/guile/site

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libguile*.la

# Necessary renaming and removing
rm -rf ${RPM_BUILD_ROOT}%{_infodir}
mv ${RPM_BUILD_ROOT}%{_bindir}/guile{,%{mver}}
mv ${RPM_BUILD_ROOT}%{_bindir}/guile{,%{mver}}-tools
mv ${RPM_BUILD_ROOT}%{_mandir}/man1/guile{,%{mver}}.1
mv ${RPM_BUILD_ROOT}%{_bindir}/guile{,%{mver}}-config
mv ${RPM_BUILD_ROOT}%{_bindir}/guile{,%{mver}}-snarf
mv ${RPM_BUILD_ROOT}%{_datadir}/aclocal/guile{,%{mver}}.m4
sed -i -e 's|/usr/bin/guile|/usr/bin/guile%{mver}|' \
    ${RPM_BUILD_ROOT}%{_bindir}/guile%{mver}-config
sed -i -e 's|guile-tools|guile%{mver}-tools|g' \
    ${RPM_BUILD_ROOT}%{_bindir}/guile%{mver}-tools
sed -i -e 's|guile-snarf|guile%{mver}-snarf|g' \
    ${RPM_BUILD_ROOT}%{_bindir}/guile%{mver}-snarf

ac=${RPM_BUILD_ROOT}%{_datadir}/aclocal/guile%{mver}.m4
sed -i -e 's|,guile|,guile%{mver}|g' $ac
sed -i -e 's|guile-tools|guile%{mver}-tools|g' $ac
sed -i -e 's|guile-config|guile%{mver}-config|g' $ac
sed -i -e 's|GUILE_PROGS|GUILE1_8_PROGS|g' $ac
sed -i -e 's|GUILE_FLAGS|GUILE1_8_FLAGS|g' $ac
sed -i -e 's|GUILE_SITE_DIR|GUILE1_8_SITE_DIR|g' $ac
sed -i -e 's|GUILE_CHECK|GUILE1_8_CHECK|g' $ac
sed -i -e 's|GUILE_MODULE_CHECK|GUILE1_8_MODULE_CHECK|g' $ac
sed -i -e 's|GUILE_MODULE_AVAILABLE|GUILE1_8_MODULE_AVAILABLE|g' $ac
sed -i -e 's|GUILE_MODULE_REQUIRED|GUILE1_8_MODULE_REQUIRED|g' $ac
sed -i -e 's|GUILE_MODULE_EXPORTS|GUILE1_8_MODULE_EXPORTS|g' $ac
sed -i -e 's|GUILE_MODULE_REQUIRED_EXPORT|GUILE1_8_MODULE_REQUIRED_EXPORT|g' $ac

# Compress large documentation
bzip2 NEWS

touch $RPM_BUILD_ROOT%{_datadir}/guile/%{mver}/slibcat
ln -s ../../slib $RPM_BUILD_ROOT%{_datadir}/guile/%{mver}/slib

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%triggerin -- slib
# Remove files created in guile < 1.8.3-2
rm -f %{_datadir}/guile/site/slib{,cat}

ln -sfT ../../slib %{_datadir}/guile/%{mver}/slib
rm -f %{_datadir}/guile/%{mver}/slibcat
export SCHEME_LIBRARY_PATH=%{_datadir}/slib/

# Build SLIB catalog
for pre in \
    "(use-modules (ice-9 slib))" \
    "(load \"%{_datadir}/slib/guile.init\")"
do
    %{_bindir}/guile%{mver} -c "$pre
        (set! implementation-vicinity (lambda ()
        \"%{_datadir}/guile/%{mver}/\"))
        (require 'new-catalog)" &> /dev/null && break
    rm -f %{_datadir}/guile/%{mver}/slibcat
done
:

%triggerun -- slib
if [ "$2" = 0 ]; then
    rm -f %{_datadir}/guile/%{mver}/slib{,cat}
fi

%files
%doc AUTHORS COPYING* ChangeLog HACKING NEWS.bz2 README THANKS
%{_bindir}/guile%{mver}
%{_bindir}/guile%{mver}-tools
%{_libdir}/libguile*.so.*
# The following unversioned libraries are needed in runtime
%{_libdir}/libguilereadline-*.so
%{_libdir}/libguile-srfi-srfi-*.so
%dir %{_datadir}/guile
%dir %{_datadir}/guile/%{mver}
%{_datadir}/guile/%{mver}/ice-9
%{_datadir}/guile/%{mver}/lang
%{_datadir}/guile/%{mver}/oop
%{_datadir}/guile/%{mver}/scripts
%{_datadir}/guile/%{mver}/srfi
%{_datadir}/guile/%{mver}/guile-procedures.txt
%ghost %{_datadir}/guile/%{mver}/slibcat
%ghost %{_datadir}/guile/%{mver}/slib
%dir %{_datadir}/guile/site
%if %{with emacs}
%dir %{_datadir}/emacs/site-lisp
%{_datadir}/emacs/site-lisp/*.el
%endif
%{_mandir}/man1/guile%{mver}.1*

%files devel
%{_bindir}/guile%{mver}-config
%{_bindir}/guile%{mver}-snarf
%{_datadir}/aclocal/*
%{_libdir}/libguile.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/guile
%{_includedir}/libguile
%{_includedir}/libguile.h

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.8.8-10
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.8.8-9
- 为 Magic 3.0 重建

* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 1.8.8-8
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Jan Synáček <jsynacek@redhat.com> - 1.8.8-5
- Add additional Provides and Obsoletes with %%{?_isa} to fix upgrade path

* Fri Jan 18 2013 Jan Synáček <jsynacek@redhat.com> - 1.8.8-4
- Bump Provides/Obsoletes by a release
- Add Provides/Obsoletes to -devel package as well
- Add a comment about unversion libraries
- Fix mixed tabs/spaces (remove tabs)

* Thu Jan 17 2013 Jan Synáček <jsynacek@redhat.com> - 5:1.8.8-3
- Move .so files back to the main package (needed in runtime)

* Thu Jan 17 2013 Jan Synáček <jsynacek@redhat.com> - 5:1.8.8-2
- Move unversioned .so files to -devel package
- Remove unnecessary %%clear
- Use %%global instead of %%define
- Remove unnecessary (compatible) licenses
- Fix %%post onliner
- Compile with --as-needed
- Add _isa flag where appropriate
- Correctly specify Provides and Obsoletes
- Rename to guile-compat18

* Fri Oct 19 2012 Jan Synáček <jsynacek@redhat.com> - 5:1.8.8-1
- Make compat-package
