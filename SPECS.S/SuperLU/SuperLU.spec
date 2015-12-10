Name:			SuperLU
Version:		4.3
Release:		10%{?dist}
Summary:		Subroutines to solve sparse linear systems
%{?el5:Group:		System/Libraries}

License:		BSD
URL:			http://crd-legacy.lbl.gov/~xiaoye/SuperLU/
Source0:		http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_%{version}.tar.gz
# Build with -fPIC
Patch0:			%{name}-add-fpic.patch
# Build shared library
Patch1:			%{name}-build-shared-lib3.patch
# Fixes FTBFS if "-Werror=format-security" flag is used (#1037343)
Patch2:			%{name}-fix-format-security.patch
# Fixes testsuite
Patch3:			SuperLU-fix-testsuite.patch

%{?el5:BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)}
BuildRequires:		atlas-devel
BuildRequires:		csh

%description
SuperLU contains a set of subroutines to solve a sparse linear system 
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP). 
The columns of A may be preordered before factorization; the 
preordering for sparsity is completely separate from the factorization.

%package devel
Summary:		Header files and libraries for SuperLU development
%{?el5:Group:		Development/Libraries}
Requires:		%{name}%{?_isa}		=  %{version}-%{release}
%{?el5:Requires:	pkgconfig}

%description devel 
The %{name}-devel package contains the header files
and libraries for use with CUnit package.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
find . -type f | sed -e "/TESTING/d" | xargs chmod a-x
# Remove the shippped executables from EXAMPLE
find EXAMPLE -type f | while read file
do
   [ "$(file $file | awk '{print $2}')" = ELF ] && rm $file || :
done
cp -p MAKE_INC/make.linux make.inc
sed -i	-e "s|-O3|$RPM_OPT_FLAGS|"							\
	-e "s|\$(SUPERLULIB) ||"							\
	-e "s|\$(HOME)/Codes/%{name}_%{version}|%{_builddir}/%{name}_%{version}|"	\
	-e 's!lib/libsuperlu_4.3.a$!SRC/libsuperlu.so!'					\
	-e 's!-shared!& %{__global_ldflags}!'						\
%if 0%{?fedora} >= 21
	-e "s|-L/usr/lib -lblas|-L%{_libdir}/atlas -lsatlas|"				\
%else
	-e "s|-L/usr/lib -lblas|-L%{_libdir}/atlas -lf77blas|"				\
%endif
	make.inc

%build
make %{?_smp_mflags} superlulib
make -C TESTING

%install
%{?el5:rm -rf %{buildroot}}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/%{name}
install -p SRC/libsuperlu.so.%{version} %{buildroot}%{_libdir}
install -p SRC/*.h %{buildroot}%{_includedir}/%{name}
chmod -x %{buildroot}%{_includedir}/%{name}/*.h
cp -Pp SRC/libsuperlu.so %{buildroot}%{_libdir}

%check
pushd TESTING
for _test in c d s z
do
  chmod +x ${_test}test.csh
  ./${_test}test.csh
done
popd

%{?el5:%clean}
%{?el5:rm -rf %{buildroot}}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README
%{_libdir}/libsuperlu.so.*

%files devel
%doc DOC EXAMPLE FORTRAN
%{_includedir}/%{name}/
%{_libdir}/libsuperlu.so

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 4.3-10
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 4.3-9
- 为 Magic 3.0 重建

* Mon Jan 06 2014 Björn Esser <bjoern.esser@gmail.com> - 4.3-8
- fixed FTBFS if "-Werror=format-security" flag is used (#1037343)
- devel-pkg must Requires: %%{name}%%{?_isa}
- apply proper LDFLAGS
- added needed bits for el5
- reenable testsuite using Patch3

* Fri Oct 4 2013 Orion Poplawski <orion@cora.nwra.com> - 4.3-7
- Rebuild for atlas 3.10
- Handle UnversionedDocDirs change

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 4.3-5
- Ship SuperLU examples

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 4.3-3
- Use README in main package and DOC in devel package
- chmod a-x on SRC/qselect.c
- Remove -latlas linking in prep section
- Added Patch comments
- Use name RPM macro in patch name

* Wed Feb 01 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 4.3-2
- Use atlas library instead of blas.
- Use RPM_OPT_FLAGS and LIBS when building sources.
- Use macros as required for name and version.

* Fri Jan 06 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 4.3-1
- First release.
