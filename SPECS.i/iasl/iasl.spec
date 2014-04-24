Name:           iasl
Version:        20100528
Release:        6%{?dist}
Summary:        Intel ASL compiler/decompiler
Summary(zh_CN.UTF-8): Intel ASL 编译器/反编译器

Group:          Development/Languages
Group(zh_CN.UTF-8):     开发/语言
License:        Intel ACPI
URL:            http://developer.intel.com/technology/iapc/acpi/ 
Source0:        http://www.acpica.org/download/acpica-unix-%{version}.tar.gz
Source1:        iasl-README.Fedora
Source2:	iasl.1
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  bison patchutils flex


%description
iasl compiles ASL (ACPI Source Language) into AML (ACPI Machine Language),
which is suitable for inclusion as a DSDT in system firmware. It also can
disassemble AML, for debugging purposes.

%description -l zh_CN.UTF-8
iasl 编译 ASL (ACPI 源语言) 到 AML (ACPI 机器语言)，用来在系统固件中包括 DSDT。
他也可以反编译 AML，用来调试。

%prep
%setup -q -n acpica-unix-%{version}
cp -p %{SOURCE1} README.Fedora
cp -p %{SOURCE2} iasl.1

%build
export CC=gcc
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$CFLAGS"
cd compiler
# does not compile with %{?_smp_mflags}
make


%install
rm -rf $RPM_BUILD_ROOT
install -p -D compiler/iasl $RPM_BUILD_ROOT%{_bindir}/iasl
install -m 0644 -p -D iasl.1 $RPM_BUILD_ROOT%{_mandir}/man1/iasl.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc changes.txt README README.Fedora
%{_bindir}/iasl
%{_mandir}/man1/iasl.1.gz


%changelog
* Thu Apr 17 2014 Liu Di <liudidi@gmail.com> - 20100528-6
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 20100528-5
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 20100528-4
- 为 Magic 3.0 重建

* Thu Nov 03 2011 Liu Di <liudidi@gmail.com> - 20100528-3
- 更新到 20100528
