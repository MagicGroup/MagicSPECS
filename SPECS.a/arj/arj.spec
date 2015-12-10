Summary:	Archiver for .arj files
Summary(zh_CN):	.arj 文件的归档
Name:		arj
Version:	3.10.22
Release:	13%{?dist}
License:	GPL+
Group:		Applications/Archiving
Group(zh_CN):	应用程序/归档
URL:		http://arj.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# unarj.* from Debian
Source1:	unarj.sh
Source2:	unarj.1
Patch0:		arj-3.10.22-arches_align.patch
Patch1:		arj-3.10.22-no_remove_static_const.patch
Patch2:		arj-3.10.22-64_bit_clean.patch
Patch3:		arj-3.10.22-parallel_build.patch
Patch4:		arj-3.10.22-use_safe_strcpy.patch
Patch5:		arj-3.10.22-doc_refer_robert_k_jung.patch
Patch6:		arj-3.10.22-security_format.patch
Patch7:		arj-3.10.22-missing-protos.patch
Patch8:		arj-3.10.22-custom-printf.patch
# Filed into upstream bugtracker as https://sourceforge.net/tracker/?func=detail&aid=2853421&group_id=49820&atid=457566
Patch9:		arj-3.10.22-quotes.patch
Patch10:        arj-3.10.22-security-afl.patch
Patch11:        arj-3.10.22-security-traversal-dir.patch
Patch12:        arj-3.10.22-security-traversal-symlink.patch
BuildRequires:	autoconf
Provides:	unarj = %{version}-%{release}
Obsoletes:	unarj < 3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This package is an open source version of the arj archiver. It has
been created with the intent to preserve maximum compatibility and
retain the feature set of original ARJ archiver as provided by ARJ
Software, Inc.

%description -l zh_CN
这是压缩和解压 arj 文件命令的开放源码版本。

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

pushd gnu
  autoconf
popd

%build
pushd gnu
  %configure
popd

# Disable binary strippings
make %{?_smp_mflags} ADD_LDFLAGS=""

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

install -Dpm 644 resource/rearj.cfg.example $RPM_BUILD_ROOT%{_sysconfdir}/rearj.cfg
install -pm 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/unarj
install -pm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man1/unarj.1

# remove the register remainders of arj's sharewares time
rm -f $RPM_BUILD_ROOT%{_bindir}/arj-register
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/arj-register.1*

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog* doc/COPYING doc/rev_hist.txt
%config(noreplace) %{_sysconfdir}/rearj.cfg
%{_bindir}/*arj*
%{_libdir}/arj/
%{_mandir}/man1/*arj*1.*

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 3.10.22-13
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 3.10.22-12
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 3.10.22-10
- 为 Magic 3.0 重建

* Sun Oct 30 2011 Liu Di <liudidi@gmail.com> - 3.10.22-9
- 为 Maigc 3.0 重建
