Name:		libpari23
Version:	2.3.5
Release:	10%{?dist}
Summary:	Number Theory-oriented Computer Algebra Library
Summary(zh_CN.UTF-8): 用于数论的计算机代数库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
# No version is specified
License:	GPL+
URL:		http://pari.math.u-bordeaux.fr/
Source0:	http://pari.math.u-bordeaux.fr/pub/pari/unix/OLD/pari-%{version}.tar.gz
Patch1:		libpari23-optflags.patch
Patch2:		libpari23-fsf-address.patch
Patch3:		Math-Pari-2.01080604-extra-stack-for-test.patch
BuildRequires:	readline-devel
BuildRequires:	gmp-devel
BuildRequires:	tex(tex)
BuildRequires:	tex(dvips)
BuildRequires:	desktop-file-utils
BuildRequires:	libX11-devel
BuildRequires:	xmkmf

# Avoid doc-file dependencies and provides
%global __provides_exclude_from ^%{_datadir}/pari/PARI/
%global __requires_exclude_from ^%{_datadir}/pari/PARI/

%description
PARI is a widely used computer algebra system designed for fast computations in
number theory (factorizations, algebraic number theory, elliptic curves...),
but also contains a large number of other useful functions to compute with
mathematical entities such as matrices, polynomials, power series, algebraic
numbers, etc., and a lot of transcendental functions.

This is an old version of the library, for compatibility with applications and
library bindings that have not been migrated to the current stable release.

%description -l zh_CN.UTF-8
PARI/GP 是一种针对数论中的快速计算(大数分解，代数数论，椭圆曲线...) 而设计的广泛
应用的计算机代数系统，同样具备大量实用的函数来对于数学实体的计算， 诸如矩阵，多
项式，幂级数，代数数，以及相当多的超越方程等等。 PARI也可以作为快速计算的C语言库。

这个系统最初是由Henri Cohen和他的合作者们（来自法国的波尔多第一大学）发展起来的。 
PARI现在在公共授权条款(GPL)之下并在许多志愿者的帮助下由Karim Belabas进行维护。

%package devel
Summary:	Header files and libraries for PARI development
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
Header files and libraries for PARI development with the old version 2.3.x
API.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。


%prep
%setup -q -n pari-%{version}

# Use our optflags, not upstream's
%patch1
sed -i -e 's|@OPTFLAGS@|%{optflags} -fPIC|' config/get_cc

# Update FSF address in copyright notices
%patch2 -p1

# perl-Math-Pari uses libpari23's test suite but needs more stack on some architectures
%patch3 -p2

# Avoid unwanted rpaths
sed -i "s|runpathprefix='.*'|runpathprefix=''|" config/get_ld

# Create a pkg-config file
cat > libpari23.pc << __EOF__
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
libdir=%{_libdir}
includedir=%{_includedir}
datadir=%{_datadir}
paridir=%{_datadir}/%{name}

Name: Libpari23
Description: Number Theory-oriented Computer Algebra Library.
URL: http://pari.math.u-bordeaux.fr/
Version: %{version}
Libs: -lpari23
Cflags: -I\${includedir}/%{name}
__EOF__

%build
./Configure \
    --prefix=%{_prefix} \
    --share-prefix=%{_datadir} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir}/man1 \
    --datadir=%{_datadir}/pari \
    --with-gmp
make %{?_smp_mflags} all

%install
make install \
	DESTDIR=%{buildroot} \
	INSTALL="install -p" \
	STRIP=/bin/true

# we move pari.cfg to the docdir
rm -rf %{buildroot}%{_prefix}/lib/pari

# We'll link to this library as libpari23 rather than libpari
mv %{buildroot}%{_libdir}/libpari{.so,23.so}

# Move header files to avoid conflicting with pari-devel
mkdir %{buildroot}%{_includedir}/%{name}
mv %{buildroot}%{_includedir}/{pari,%{name}/pari}

# Install tests and documentation, needed e.g. by perl-Math-Pari
mkdir -p %{buildroot}%{_datadir}/%{name}/src/
cp -a src/test/ %{buildroot}%{_datadir}/%{name}/src/
cp -a doc %{buildroot}%{_datadir}/%{name}/

# Additional headers needed e.g. by perl-Math-Pari
mkdir -p %{buildroot}%{_datadir}/%{name}/src/{graph,gp,headers,language}/
cp -a src/graph/*.h %{buildroot}%{_datadir}/%{name}/src/graph/
cp -a src/gp/*.h %{buildroot}%{_datadir}/%{name}/src/gp/
cp -a src/headers/*.h %{buildroot}%{_datadir}/%{name}/src/headers/
cp -a src/language/*.h %{buildroot}%{_datadir}/%{name}/src/language/

# Install our pkg-config file so the library can be found
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
cp -p libpari23.pc %{buildroot}%{_libdir}/pkgconfig/

# Remove emacs support files if built on a system with emacs
rm -rf %{buildroot}%{_datadir}/emacs/site-lisp/pari/

# Placate rpmlint regarding binary and library permissions
%{_fixperms} %{buildroot}{%{_bindir},%{_libdir}}
magic_rpm_clean.sh

%check
make dobench
make dotest-compat
make dotest-intnum
make dotest-qfbsolve
make dotest-rfrac
make dotest-round4

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS CHANGES* COPYING COMPAT NEW README
%doc Olinux-*/pari.cfg
%{_libdir}/libpari-gmp.so.%{version}
%{_libdir}/libpari-gmp.so.2

# Files for the pari-gp calculator, which we don't ship
%exclude %{_bindir}/gp
%exclude %{_bindir}/gp-2.3
%exclude %{_bindir}/gphelp
%exclude %{_bindir}/tex2mail
%exclude %doc %{_datadir}/pari/PARI/
%exclude %doc %{_datadir}/pari/doc/
%exclude %doc %{_datadir}/pari/examples/
%exclude %{_datadir}/pari/misc/
%exclude %{_datadir}/pari/pari.desc
%exclude %{_mandir}/man1/gp-2.3.1*
%exclude %{_mandir}/man1/gp.1*
%exclude %{_mandir}/man1/gphelp.1*
%exclude %{_mandir}/man1/pari.1*
%exclude %{_mandir}/man1/tex2mail.1*

%files devel
%{_includedir}/%{name}/pari/
%{_libdir}/libpari23.so
%{_libdir}/pkgconfig/libpari23.pc
%{_datadir}/%{name}/

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 2.3.5-10
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.3.5-9
- 为 Magic 3.0 重建

* Fri Jul 25 2014 Liu Di <liudidi@gmail.com> - 2.3.5-8
- 为 Magic 3.0 重建

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 2.3.5-7
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Paul Howarth <paul@city-fan.org> - 2.3.5-2
- Incorporate changes from package review (#837004)
  - Remove %%clean section and cleaning of buildroot in %%install
  - Build with -fPIC
  - Update FSF address in copyright notices
  - Remove emacs support files if built on a system with emacs

* Wed Jun 13 2012 Paul Howarth <paul@city-fan.org> - 2.3.5-1
- Initial RPM version
