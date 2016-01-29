%global commit 4346c30bae8b1a64acba564f6775cb0bacd026e4
%global commitdate 20150918
%global checkout %{commitdate}git%{shortcommit}
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global shortname clc

# this stop us generating an empty debuginfo
%global debug_package %{nil}

Name:           libclc
Version:        0.0.1
Release:        12.%{checkout}%{?dist}
Summary:        An open source implementation of the OpenCL 1.1 library requirements
Summary(zh_CN.UTF-8): OpenCL 1.1 库需求的开源实现

License:        BSD
URL:            http://libclc.llvm.org/
# created using:
# $ export PKG=libclc-$(date +%Y%m%d)git$(git describe --always)
# $ git archive --prefix $PKG/ --format tar HEAD | xz > $PKG.tar.xz
Source0:        https://github.com/llvm-mirror/%{name}/archive/%{commit}/%{name}-%{checkout}.tar.gz

# Only builds on x86
ExclusiveArch:	%{ix86} x86_64

BuildRequires:  clang-devel
BuildRequires:  libedit-devel
BuildRequires:  llvm-devel
BuildRequires:  llvm-static
BuildRequires:  python
BuildRequires:  zlib-devel

%description
libclc is an open source, BSD licensed implementation of the library
requirements of the OpenCL C programming language, as specified by the
OpenCL 1.1 Specification. The following sections of the specification
impose library requirements:

  * 6.1: Supported Data Types
  * 6.2.3: Explicit Conversions
  * 6.2.4.2: Reinterpreting Types Using as_type() and as_typen()
  * 6.9: Preprocessor Directives and Macros
  * 6.11: Built-in Functions
  * 9.3: Double Precision Floating-Point
  * 9.4: 64-bit Atomics
  * 9.5: Writing to 3D image memory objects
  * 9.6: Half Precision Floating-Point

libclc is intended to be used with the Clang compiler's OpenCL frontend.

libclc is designed to be portable and extensible. To this end, it provides
generic implementations of most library requirements, allowing the target
to override the generic implementation at the granularity of individual
functions.

libclc currently only supports the PTX target, but support for more
targets is welcome.

%description -l zh_CN.UTF-8
OpenCL 1.1 库需求的开源实现。

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
%setup -q -n "%{name}-%{commit}"

%build
CFLAGS="%{optflags} -D__extern_always_inline=inline"
./configure.py --prefix=%{_prefix} --libexecdir=%{_libdir}/%{shortname}/ --pkgconfigdir=%{_libdir}/pkgconfig/

# fstack-protector-strong is currently not supported by clang++
sed -i "s/fstack-protector-strong/fstack-protector/" Makefile

make %{?_smp_mflags}


%install
%make_install
magic_rpm_clean.sh

%files
%doc LICENSE.TXT README.TXT CREDITS.TXT
%{_libdir}/%{shortname}/*.bc
%{_includedir}/%{shortname}

%files devel
%doc
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.0.1-12.20140901gite822ae3
- 为 Magic 3.0 重建

* Mon Sep 07 2015 Liu Di <liudidi@gmail.com> - 0.0.1-11.20140901gite822ae3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-10.20140901gite822ae3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 08 2015 Adel Gadllah <adel.gadllah@gmail.com> - 0.0.1-9.20140901gite822ae3
- Rebuilt with newer llvm

* Tue Oct 28 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 0.0.1-8.20140901gite822ae3
- Update to a newer snapshot

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-7.20140705git61127c5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 25 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.0.1-6
- Rebuild now llvm bits are fixed for gcc-4.9
- Minor cleanups

* Sat Jul 05 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-5
- Update to latest snapshot to support AMD Kaveri APUs
- Move bitcode files to an arch dependent dir, as they are arch dependent

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-4.20140429git4341094
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-2.20140429git4341094
- Update to latest snapshot
- Support for AMD Kabini

* Mon Jan 13 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-2.20140108gitc002f62
- Move headers to main package, needed by clover at runtime

* Wed Jan 08 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-1.20140108gitc002f62
- Could not use latest master because it doesn't build
- Update to a fresher snapshot
- Limit to x86

* Sun Jul 14 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-0.20130714git5217211
- Initial package
