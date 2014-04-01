Summary: DWARF optimization and duplicate removal tool
Summary(zh_CN.UTF-8): DWARF 优化和重复移除工具
Name: dwz
Version: 0.11
Release: 1%{?dist}
License: GPLv2+ and GPLv3+
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
# git archive --format=tar --remote=git://sourceware.org/git/dwz.git \
#   --prefix=%{name}-%{version}/ %{name}-%{version} \
#   | bzip2 -9 > %{name}-%{version}.tar.bz2
Source: %{name}-%{version}.tar.bz2
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: elfutils-libelf-devel%{?_isa}

%description
The dwz package contains a program that attempts to optimize DWARF
debugging information contained in ELF shared libraries and ELF executables
for size, by replacing DWARF information representation with equivalent
smaller representation where possible and by reducing the amount of
duplication using techniques from DWARF standard appendix E - creating
DW_TAG_partial_unit compilation units (CUs) for duplicated information
and using DW_TAG_imported_unit to import it into each CU that needs it.

%description -l zh_CN.UTF-8
这个包包含了一个优化 ELF 共享库和 ELF 可执行程序中的 DWARF 调试信息的工具。

%prep
%setup -q

%build
make %{?_smp_mflags} CFLAGS='%{optflags}' prefix=%{_prefix} \
  mandir=%{_mandir} bindir=%{_bindir}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} prefix=%{_prefix} mandir=%{_mandir} bindir=%{_bindir} \
  install
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING COPYING3 COPYING.RUNTIME
%{_bindir}/dwz
%{_mandir}/man1/dwz.1*

%changelog
* Thu Nov 29 2012 Jakub Jelinek <jakub@redhat.com> 0.8-1
- fix recompute_abbrevs (#880634)
- optimize DW_FORM_data[48] DW_AT_high_pc that GCC 4.8 produces

* Fri Aug 10 2012 Jakub Jelinek <jakub@redhat.com> 0.7-1
- fix iterative hasing on big-endian targets (#846685)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Jakub Jelinek <jakub@redhat.com> 0.6-1
- add --version/-v option support (Matt Newsome)
- fix building on RHEL 5

* Wed Jul  4 2012 Jakub Jelinek <jakub@redhat.com> 0.5-1
- handle .gdb_index version 7

* Fri Jun 22 2012 Jakub Jelinek <jakub@redhat.com> 0.4-1
- fix up DIE counting in low-mem mode for testing the -L limit

* Fri Jun 15 2012 Jakub Jelinek <jakub@redhat.com> 0.3-1
- update to dwz-0.3 (#830863)

* Mon Jun 11 2012 Jakub Jelinek <jakub@redhat.com> 0.2-1
- new package
