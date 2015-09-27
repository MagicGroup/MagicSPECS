Name:           sgabios
Version:        0
Release:        0.20110625SVN%{?dist}
Summary:        Open-source serial graphics BIOS option rom
Summary(zh_CN.UTF-8): 开源的串口图形 BIOS 

Group:          Applications/Emulators
Group(zh_CN.UTF-8): 应用程序/模拟器
License:        ASL 2.0
URL:            http://code.google.com/p/sgabios/
# Tarball created from SVN archive using the following commands:
# svn export -r 8 http://sgabios.googlecode.com/svn/trunk sgabios-0
# tar -czvf sgabios-0-svnr8.tar.gz sgabios-0
Source0:        sgabios-0-svnr8.tar.gz

BuildRoot:      %{_tmppath}/%{name}-root-%(%{__id_u} -n)

ExclusiveArch: %{ix86} x86_64

Requires: %{name}-bin = %{version}-%{release}

# Sgabios is noarch, but required on architectures which cannot build it.
# Disable debuginfo because it is of no use to us.
%global debug_package %{nil}

%description
SGABIOS is designed to be inserted into a BIOS as an option rom to provide over
a serial port the display and input capabilities normally handled by a VGA
adapter and a keyboard, and additionally provide hooks for logging displayed
characters for later collection after an operating system boots.

%description -l zh_CN.UTF-8
开源的串口图形 BIOS。

%ifarch %{ix86} x86_64 
%package bin
Summary: Sgabios for x86
Summary(zh_CN.UTF-8): x86 的 Sgabios
Buildarch: noarch

%description bin
SGABIOS is designed to be inserted into a BIOS as an option rom to provide over 
a serial port the display and input capabilities normally handled by a VGA
adapter and a keyboard, and additionally provide hooks for logging displayed
characters for later collection after an operating system boots.
%description bin -l zh_CN.UTF-8
x86 的 Sgabios。
%endif

%prep
%setup -q

%build
%ifarch %{ix86} x86_64 
export CFLAGS="$RPM_OPT_FLAGS"
make
%endif


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sgabios
%ifarch %{ix86} x86_64 
install -m 0644 sgabios.bin $RPM_BUILD_ROOT%{_datadir}/sgabios
%endif
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING design.txt

%ifarch %{ix86} x86_64 
%files bin
%defattr(-,root,root,-)
%dir %{_datadir}/sgabios/
%{_datadir}/sgabios/sgabios.bin
%endif


%changelog
* Sat Sep 26 2015 Liu Di <liudidi@gmail.com> - 0-0.20110625SVN
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0-0.20110624SVN
- 为 Magic 3.0 重建

* Mon Feb 06 2012 Liu Di <liudidi@gmail.com> - 0-0.20110623SVN
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.20110622SVN
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Justin M. Forbes <jforbes@redhat.com> 0.0-0.20110621SVN
- Updates per review.

* Tue Jun 21 2011 Justin M. Forbes <jforbes@redhat.com> 0.1-0.20110621SVN
- Created initial package
